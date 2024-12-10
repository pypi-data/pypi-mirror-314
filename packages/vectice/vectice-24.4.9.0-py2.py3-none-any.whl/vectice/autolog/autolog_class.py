from __future__ import annotations

import ast
import logging
import re
import tempfile
from collections import OrderedDict
from importlib.util import find_spec
from typing import TYPE_CHECKING, Any, Callable, TypeVar

import matplotlib.pyplot as plt
from typing_extensions import TypedDict

from vectice.api.http_error_handlers import VecticeException
from vectice.autolog.autolog_asset_factory import AssetFactory
from vectice.autolog.model_library import ModelLibrary
from vectice.models.dataset import Dataset
from vectice.models.model import Model
from vectice.models.representation.dataset_representation import DatasetRepresentation
from vectice.models.representation.dataset_version_representation import DatasetVersionRepresentation
from vectice.models.representation.model_representation import ModelRepresentation
from vectice.models.representation.model_version_representation import ModelVersionRepresentation
from vectice.models.table import Table
from vectice.models.validation import ValidationModel
from vectice.utils.code_parser import FilePathVisitor, VariableVisitor, parse_comments, preprocess_code
from vectice.utils.common_utils import ensure_correct_project_id_from_representation_objs
from vectice.utils.last_assets import _get_asset_parent_name  # pyright: ignore [reportPrivateUsage]

if TYPE_CHECKING:
    from tempfile import TemporaryDirectory

    from pandas import DataFrame
    from pyspark.sql import DataFrame as SparkDF
    from sklearn.pipeline import Pipeline

    # Vectice Object types
    from vectice.autolog.asset_services import TVecticeObjects
    from vectice.autolog.model_types import ModelTypes
    from vectice.models import Phase
    from vectice.models.resource.metadata.db_metadata import TableType

    TModel = TypedDict(
        "TModel",
        {
            "variable": str,
            "model": ModelTypes,
            "library": ModelLibrary,
            "technique": str,
            "metrics": dict,
            "properties": dict,
        },
    )

    DataframeTypes = TypeVar("DataframeTypes", SparkDF, DataFrame)
    TDataset = TypedDict(
        "TDataset",
        {"variable": str, "dataframe": DataframeTypes, "type": TableType},
    )

try:
    from IPython.core.getipython import get_ipython
    from IPython.core.interactiveshell import InteractiveShell
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "To use autolog, please install extra dependencies from vectice package using '%pip install vectice[autolog]'"
    ) from None

is_plotly = False
is_matplotlib = False
if find_spec("plotly") is not None:
    is_plotly = True

if find_spec("matplotlib") is not None:
    is_matplotlib = True

_logger = logging.getLogger(__name__)

NOTEBOOK_CELLS = {}
GRAPHS = {}


def _get_cell_id(ipython: Any) -> str:
    cell_metadata = ipython.get_parent()["metadata"]  # type: ignore
    if cell_metadata.get("colab") and "cell_id" in cell_metadata.get("colab"):  # type: ignore
        cell_id = cell_metadata["colab"]["cell_id"]
    elif cell_metadata.get("commandId"):  # type: ignore
        cell_id = cell_metadata["commandId"]
    else:
        cell_id = cell_metadata["cellId"]
    return cell_id


def start_listen():
    ipython = get_ipython()  # type: ignore

    def _notebook_cell_content_update():
        global NOTEBOOK_CELLS

        cell_id = _get_cell_id(ipython)
        cell_content = ipython.get_parent()["content"]["code"]  # type: ignore
        NOTEBOOK_CELLS[cell_id] = cell_content

    def _setup_cell():
        # if a cell is run or re-run, clear the dictionary
        cell_id = _get_cell_id(ipython)
        GRAPHS[cell_id] = {
            "saved": [],
            "displayed": [],
        }

    def _load_ipython_extension():
        from matplotlib_inline.backend_inline import flush_figures

        from vectice.utils.plot_tracker import PlotTracker

        # Connect the plot tracker hook to IPython's display hook
        # NB we monkey patch plotly if package is found, see in plot_tracker.py
        plot_tracker = PlotTracker()
        # Apply the patch for savefig
        plt.savefig = plot_tracker.patched_savefig

        # unregister the matplotlib inline event
        # this is done so the graphs aren't flushed before we can capture them
        is_flush_figure_registered = get_event_callback(ipython, "post_execute", "flush_figures")
        if is_flush_figure_registered:
            ipython.events.unregister("post_execute", flush_figures)  # type: ignore

        """Load the extension in IPython."""
        ipython.events.register("pre_execute", _setup_cell)  # type: ignore
        ipython.events.register("post_execute", _notebook_cell_content_update)  # type: ignore
        ipython.events.register("post_execute", plot_tracker.get_all_figures)  # type: ignore
        # register the matplotlib event so we don't break the display output
        if is_flush_figure_registered:
            ipython.events.register("post_execute", flush_figures)  # type: ignore

    pre_execute_callback = get_event_callback(ipython, "pre_execute", "_setup_cell")
    post_execute_callback = get_event_callback(ipython, "post_execute", "_notebook_cell_content_update")
    post_run_cell_callback = get_event_callback(ipython, "post_execute", "_get_all_figures")
    if ipython and not (pre_execute_callback and post_execute_callback and post_run_cell_callback):  # type: ignore
        _load_ipython_extension()


def get_event_callback(ipython: InteractiveShell | None, event_name: str, callback_name: str) -> Callable | None:
    """Helper function to find a registered callback by name."""
    if ipython:
        event_callbacks = [ev for ev in ipython.events.callbacks[event_name] if callback_name in str(ev)]
        return event_callbacks[0] if event_callbacks else None
    return None


####### Autolog logic
class Autolog:
    def __init__(
        self,
        phase: Phase | None,
        ipy: InteractiveShell,
        is_notebook: bool,
        create: bool = True,
        note: str | None = None,
        capture_schema_only: bool = True,
        capture_comments: bool = True,
        prefix: str | None = None,
    ):
        from vectice.services.phase_service import PhaseService

        if phase is None:
            raise ValueError("Login")

        if create is True:
            iteration = phase.create_iteration()
        else:
            iteration = PhaseService(
                phase._client  # pyright: ignore[reportPrivateUsage]
            ).get_active_iteration_or_create(phase)

        self._iteration = iteration
        self._iteration_service = iteration._service  # pyright: ignore[reportPrivateUsage]
        self._capture_schema_only = capture_schema_only
        self._ip = ipy
        self._local_vars = self._ip.user_global_ns
        self._metric_functions = self._get_metric_functions()
        self._capture_comments = capture_comments
        self._prefix = prefix
        self._is_notebook = is_notebook
        self._cell_content = self._get_notebook_cell_content() if is_notebook is True else self._get_cell_content()
        self._vectice_data = self._get_variable_matches(self._local_vars)
        self._failed_assets = []

        # Get back objects to log
        self._assets = self._get_assets()
        graphs = self._get_graphs(is_notebook)

        if note:
            self._iteration_service.log_comment(note)
            _logger.info(f"Note logged in iteration {self._iteration.name!r}.")

        # Log objects

        self._log_assets(self._assets)

        if graphs:
            for graph in graphs:
                try:
                    self._iteration_service.log_image_or_file(graph)
                    graph = graph if isinstance(graph, str) else graph.filename
                    _logger.info(f"Graph {graph!r} logged in iteration {self._iteration.name!r}.")
                except Exception as e:
                    self._failed_assets.append({"reason": e, "asset": graph, "type": "Graph"})

        if len(self._failed_assets):
            _logger.warning("The following assets failed to log:")
        for failed_asset in self._failed_assets:
            _logger.warning(f"{failed_asset['type']} {failed_asset['asset']!r}, reason: {failed_asset['reason']}")

    def _get_metric_functions(self) -> set[str | None]:
        return set(
            {
                name: func for name, func in self._local_vars.items() if getattr(func, "custom_metric_function", False)
            }.keys()
        )

    def _get_variable_matches(self, local_vars: dict[str, Any]) -> list[dict[Any, Any]]:
        vectice_data = []
        all_cell_vars = set()
        all_vectice_calls = set()

        for cell_not_processed in self._cell_content:
            cell = preprocess_code(cell_not_processed)
            variable_comments = parse_comments(cell_not_processed) if self._capture_comments else []
            vectice_match = {}
            all_vars: OrderedDict[str, Any] = OrderedDict()

            vectice_match["cell"] = cell
            vectice_match["comments"] = variable_comments

            # Parse the cell content using the VariableVisitor
            try:
                tree = ast.parse(cell)
            except SyntaxError as err:
                raise SyntaxError(
                    "Autolog is unable to parse the code. Make sure all non-Python syntax, such as bash commands, are properly indented and preceded by '%' or '!'. If the error persist, please contact your sales representative."
                ) from err

            visitor = VariableVisitor(custom_metrics=self._metric_functions)
            visitor.visit(tree)
            # Keep set of all vectice call vars
            all_vectice_calls = all_vectice_calls.union(visitor.vectice_call_vars)
            # Update all_vars with variable names and values in the order they appear
            for var in visitor.variables:
                if var in local_vars and var not in all_vars:
                    all_vars[var] = local_vars[var]
                # check if the var exists in a previous cell for autolog.notebook before the vectice object uses the var
                if self._is_notebook:
                    all_vectice_calls = {vect_var for vect_var in all_vectice_calls if vect_var not in all_cell_vars}
                # Keep track of all vars
                all_cell_vars.add(var)

            vectice_match["variables"] = all_vars
            vectice_data.append(vectice_match)
        clean_vectice_data = []
        for data in vectice_data:
            for var in all_vectice_calls:
                # the order of cells misses vars
                if var in data["variables"]:
                    del data["variables"][var]
            # check that there are vars for the cell and then append or if there are comments
            if len(data["variables"]) >= 1 or len(data["comments"]) >= 1:
                clean_vectice_data.append(data)
        return clean_vectice_data

    def _get_notebook_cell_content(self) -> list[Any]:
        cell_id = _get_cell_id(self._ip)
        cell_content = self._ip.get_parent()["content"]["code"]  # type: ignore
        NOTEBOOK_CELLS[cell_id] = cell_content
        return list(NOTEBOOK_CELLS.values())

    def _get_cell_content(self) -> list[Any]:
        """Used by autolog cell to get the content of the cell. This is used to parse for variables."""
        cell_content = self._ip.get_parent()["content"]["code"]  # pyright: ignore[reportAttributeAccessIssue]
        if cell_content is None:
            raise ValueError("Failed to get cell content.")
        return [cell_content]

    def _get_asset_comments(self, comments: dict, key: str) -> tuple[str | None, str | None]:
        try:
            comment_before = comments["comment_matches_before"][key]["comment"]
        except KeyError:
            comment_before = None
        try:
            comment_after = comments["comment_matches_after"][key]["comment"]
        except KeyError:
            comment_after = None
        return comment_before, comment_after

    def _get_assets(self) -> list[TModel | TDataset | TVecticeObjects]:
        assets = []

        for data in self._vectice_data:
            for key in data["variables"].keys():
                # skip cell inputs/outputs
                if key.startswith("_"):
                    continue
                asset = data["variables"][key]
                try:
                    asset_information = AssetFactory.get_asset_service(
                        key, asset, data, self._metric_functions
                    ).get_asset()
                    if asset_information is not None:
                        assets.append(asset_information)
                except VecticeException:
                    pass

        return self._deduplicate_assets(assets)

    def _deduplicate_assets(self, assets: list[dict[str, Any]]) -> list[TModel | TDataset | TVecticeObjects]:
        unique_dict = {}
        result = []

        for item in assets:
            variable = item["variable"]

            if variable not in unique_dict.keys():
                # If variable is not seen before, add it to the dictionary
                unique_dict[variable] = item
                result.append(item)
            else:
                existing_item = unique_dict[variable]
                if "vectice_object" in item:
                    existing_item["vectice_object"] = item["vectice_object"]
                elif "dataframe" in item:
                    existing_item["type"] = item["type"]
                else:
                    existing_item["library"] = item["library"]

                    # Merge dictionaries for the "metrics" attribute
                    existing_item_metrics = existing_item["metrics"]
                    item_metrics = item["metrics"]

                    for key, value in item_metrics.items():
                        existing_item_metrics[key] = value

        return result

    def _get_pipeline_steps(self, pipeline: Pipeline) -> dict:
        sklearn_pipeline = {}
        try:
            for step in pipeline.steps:
                step_name, step_obj = step
                if hasattr(step_obj, "named_transformers_"):
                    for k, v in step_obj.named_transformers_.items():
                        sklearn_pipeline[f"pipeline_{step_name}_{k}_steps"] = list(v.named_steps.keys())
            return sklearn_pipeline
        except Exception:
            return sklearn_pipeline

    def _get_pipeline_info(self, pipeline: Pipeline) -> tuple[str, dict[str, Any]] | tuple[None, None]:
        # if pipeline with classifier
        try:
            from sklearn.base import is_classifier, is_regressor

            model = pipeline.steps[-1][-1]
            model_name = pipeline.steps[-1][0]
            if is_regressor(model) or is_classifier(model):
                model_params = {
                    f"{model_name}_{key}": value
                    for key, value in model.get_params().items()
                    if value is not None and bool(str(value))
                }
                model_params.update(self._get_pipeline_steps(pipeline))
                return "sklearn-pipeline", model_params
        except Exception:
            pass

        try:
            pipeline_params = {
                str(key): value
                for key, value in pipeline.get_params().items()
                if value is not None and bool(str(value))
            }
            return "sklearn-pipeline", pipeline_params
        except Exception:
            return None, None

    def _get_all_cells_comments(self) -> list[dict]:
        # Get all comments from all cells
        all_comments_and_variables = []
        for data in self._vectice_data:
            if data["comments"]:
                for comments in data["comments"]:
                    all_comments_and_variables.append(comments)
        return all_comments_and_variables

    def _get_comments_before(
        self,
        all_comments_and_variables: list[dict],
        asset: TModel | TDataset | TVecticeObjects,
        comments_logged: list,
    ):
        comments_to_log = []
        for data in all_comments_and_variables:
            # If we find the variable we log all the comments found
            if data["variable"] == asset["variable"]:
                return comments_to_log
            # We only want comments remaining
            if data["comment"] not in comments_logged:
                comments_to_log.append(data["comment"])
        # return nothing if we don't see the asset
        return []

    def _log_comments_before_asset(
        self,
        all_comments_and_variables: list[dict],
        asset: TModel | TDataset | TVecticeObjects,
        comments_logged: list,
    ) -> list:
        # Get comments to log before each asset
        comments_before = self._get_comments_before(all_comments_and_variables, asset, comments_logged)
        # Log comments before each asset
        if comments_before:
            for comment in comments_before:
                if comment:
                    self._iteration_service.log_comment(comment)
            # Keep track of what's logged
            return comments_logged + comments_before
        return comments_logged

    def _log_remaining_comments(self, all_unique_comments: set, comments_logged: list) -> None:
        # Ensure last asset comments are filtered out
        all_comments_logged = set(comments_logged)
        still_comments_to_log = list(all_unique_comments - all_comments_logged)
        # Log remaining comments after last asset
        if still_comments_to_log:
            for comment in still_comments_to_log:
                if comment:
                    self._iteration_service.log_comment(comment)
        # Logging for comments captured
        all_comments_logged.discard(None)
        filtered_comments = list(filter(lambda comment: comment is not None, still_comments_to_log))
        if filtered_comments or all_comments_logged:
            _logger.info(f"Comments logged in iteration {self._iteration.name!r}.")

    def _log_assets(
        self,
        assets: list[TModel | TDataset | TVecticeObjects],
    ):
        from vectice.services import iteration_service

        # all comments and variables
        all_comments_and_variables = self._get_all_cells_comments()
        # Unique comment set
        all_unique_comments = set([data["comment"] for data in all_comments_and_variables])
        # Keep track of what is logged
        comments_logged = []
        for asset in assets:
            try:
                comments_logged = self._log_comments_before_asset(all_comments_and_variables, asset, comments_logged)
                if "vectice_object" in asset:
                    self._log_vectice_asset(asset)
                elif "model" in asset:
                    self._log_model(asset)
                elif "dataframe" in asset:
                    self._log_dataset(asset)
            except Exception as e:
                if "vectice_object" in asset:
                    asset_type = "Vectice object"
                elif "model" in asset:
                    asset_type = "Model"
                else:
                    asset_type = "Dataset"
                self._failed_assets.append({"reason": e, "asset": asset["variable"], "type": asset_type})
        # Log the remaining comments
        self._log_remaining_comments(all_unique_comments, comments_logged)
        # After logging, don't re-use code file
        iteration_service.lineage_file_id = None

    def _check_for_single_model(self):
        model_list = [asset for asset in self._assets if "model" in asset]
        if len(model_list) > 1:
            return False
        return True

    def _get_single_model_metrics(self) -> dict:
        from vectice.autolog.asset_services.metric_service import MetricService

        # get a single models metrics for notebook function
        metrics = {}
        if not self._check_for_single_model():
            return {}
        for data in self._vectice_data:
            cell_metrics = MetricService(data["cell"], self._metric_functions)._get_model_metrics(data)  # type: ignore[reportPrivateUsage]
            if cell_metrics:
                metrics.update(cell_metrics)
        return metrics

    def _log_model(self, model: TModel):
        temp_dir: TemporaryDirectory | None = None
        temp_file_path: str | None = None

        if model["library"] is ModelLibrary.KERAS:
            graph = None

            try:
                from keras.utils import plot_model  # type: ignore[reportMissingImports]

                temp_dir = tempfile.TemporaryDirectory()
                file_name = f"{model['variable']!s}_plot.png"
                temp_file_path = rf"{temp_dir.name}\{file_name}"
                graph = plot_model(model["model"], to_file=temp_file_path, show_shapes=True, show_layer_names=False)

                if graph is None:
                    temp_file_path = None
                    _logger.info(
                        "Unable to generate the model plot. Please check the 'plot_model' function from the Keras library is working correctly. Make sure that the graphviz and pydot packages are installed and configured properly."
                    )

            except Exception as e:
                _logger.info(
                    f"Unable to generate the model plot. Ensure that the Keras library is correctly installed and up-to-date. Error details: {e}"
                )

        model_object = model["model"]

        library, algorithm, params = model["library"], model["technique"], model["properties"]
        if library is ModelLibrary.STATSMODEL:
            model_summary = model_object.summary().as_text()  # type: ignore[reportAttributeAccessIssue]
        else:
            model_summary = None
        model_name = self._get_asset_name(model["variable"], self._prefix)
        # safety check, if no metrics and single model, get metrics
        model_metrics = model["metrics"] if model["metrics"] else self._get_single_model_metrics()
        temp_files = []
        if library is ModelLibrary.SKLEARN_PIPELINE:
            temp_dir, temp_json_file_path, temp_html_file_path = self._get_sklearn_pipeline(model_object, model_name)
            if temp_json_file_path:
                temp_files.append(temp_json_file_path)
            if temp_html_file_path:
                temp_files.append(temp_html_file_path)

        if library is ModelLibrary.SKLEARN_SEARCH:
            tables = self._get_sklearn_search_results_and_space_tables(model_object, model_name)
            temp_files.extend(tables)

        self._iteration_service.log_model(
            Model(
                library=library.value,
                technique=algorithm,
                metrics=model_metrics,
                properties=params,
                name=model_name,
                predictor=model_object,
                attachments=temp_file_path or temp_files,
            ),
        )
        _logger.info(f"Model {model_name!r} logged in iteration {self._iteration.name!r}.")

        if model_summary:
            # log statsmodel summary
            self._iteration_service.log_comment(model_summary)

        if temp_dir is not None:
            temp_dir.cleanup()

    def _get_sklearn_pipeline(
        self, pipeline: ModelTypes, model_name: str
    ) -> tuple[TemporaryDirectory[str], str, str] | tuple[None, None, None]:
        temp_dir = None
        try:
            from sklearn.utils import estimator_html_repr

            from vectice.utils.sklearn_pipe_utils import pipeline_to_json

            temp_dir = tempfile.TemporaryDirectory()
            json_file_name = f"{model_name!s}_pipeline.json"
            html_file_name = f"{model_name!s}_pipeline.html"
            temp_json_file_path = rf"{temp_dir.name}\{json_file_name}"
            temp_html_file_path = rf"{temp_dir.name}\{html_file_name}"

            pipeline_json = pipeline_to_json(pipeline)
            pipeline_html = estimator_html_repr(pipeline)
            if pipeline_json:
                with open(temp_json_file_path, "w") as json_file:
                    json_file.write(pipeline_json)

            if pipeline_html:
                with open(temp_html_file_path, "w", encoding="utf-8") as html_file:
                    html_file.write(pipeline_html)

            return temp_dir, temp_json_file_path, temp_html_file_path
        except Exception:
            return None, None, None

    def _get_sklearn_search_results_and_space_tables(self, model: ModelTypes, model_name: str) -> list:
        tables = []
        try:
            import pandas as pd

            results_df = pd.DataFrame(model.cv_results_)  # pyright: ignore[reportAttributeAccessIssue]
        except Exception:
            return tables
        try:
            tables.append(self._get_sklearn_search_space(model, model_name, results_df))
        except Exception:
            pass
        try:
            tables.append(self._get_sklearn_search_results(model, model_name, results_df))
        except Exception:
            pass
        return tables

    def _get_sklearn_search_results(self, model: ModelTypes, model_name: str, results_df: DataFrame) -> Table:
        sorted_df = results_df.sort_values(by="rank_test_score")
        top_scores_df = sorted_df.head(5)
        return Table(top_scores_df, name=f"{model_name}_search_results")

    def _get_sklearn_search_space(self, model: ModelTypes, model_name: str, results_df: DataFrame) -> Table:
        import pandas as pd

        param_columns = [col for col in results_df.columns if "param" in col and "params" not in col]
        data_dict = {}
        for param in param_columns:
            try:
                data_dict[f"{param} (min,max)"] = [[results_df[param].min(), results_df[param].max()]]
            except Exception:
                data_dict[f"{param} (uniques)"] = [results_df[param].unique()]

        params_df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data_dict.items()]))
        # Transpose the DataFrame
        df_transposed = params_df.transpose()
        # Reset the index to move row headers into a column
        df_transposed_reset = df_transposed.reset_index()
        # Rename the index column for clarity
        df_transposed_reset = df_transposed_reset.rename(columns={"index": "Parameters", 0: "Values"})
        return Table(df_transposed_reset, name=f"{model_name}_search_space")

    def _log_vectice_asset(self, asset: TVecticeObjects) -> None:

        asset_to_log = asset["vectice_object"]
        if isinstance(asset_to_log, ValidationModel):
            object_name = asset["variable"]
        else:
            object_name = asset_to_log.name

        ensure_correct_project_id_from_representation_objs(self._iteration.project.id, asset_to_log)

        if isinstance(asset_to_log, Dataset):
            self._iteration_service.log_dataset(asset_to_log)
            _logger.info(f"Dataset {object_name!r} logged in iteration {self._iteration.name!r}.")
        elif isinstance(asset_to_log, Table):
            self._iteration_service.log_table(asset_to_log)
            _logger.info(f"Table {object_name!r} logged in iteration {self._iteration.index!r}.")
        elif isinstance(asset_to_log, Model):
            if asset_to_log.predictor:
                self._iteration._assign_model_predictor_metadata(asset_to_log)  # pyright: ignore[reportPrivateUsage]
            self._iteration_service.log_model(asset_to_log)
            _logger.info(f"Model {object_name!r} logged in iteration {self._iteration.index!r}.")
        elif isinstance(
            asset_to_log,
            (ModelRepresentation, ModelVersionRepresentation, DatasetRepresentation, DatasetVersionRepresentation),
        ):
            asset_type, already_assigned = self._iteration_service.assign_version_representation(
                asset_to_log
            )  # pyright: ignore[reportPrivateUsage]
            link = "already linked" if already_assigned else "linked"
            asset_name_variable = asset["variable"]
            is_parent = isinstance(asset_to_log, (ModelRepresentation, DatasetRepresentation))
            asset_version = (
                asset_to_log._last_version.name  # pyright: ignore [reportPrivateUsage]
                if (is_parent and asset_to_log._last_version is not None)  # pyright: ignore [reportPrivateUsage]
                else asset_to_log.name
            )
            asset_name = (
                asset_to_log.name
                if is_parent
                else _get_asset_parent_name(asset_to_log)  # pyright: ignore [reportPrivateUsage]
            )
            _logger.info(
                f"{asset_type} {asset_name!r} {asset_version} named {asset_name_variable!r} as a variable {link} to iteration {self._iteration.index!r}."
            )
        else:
            self._iteration._log_validation_model(asset_to_log)  # pyright: ignore[reportPrivateUsage]

    def _log_dataset(self, dataset: TDataset) -> None:
        from vectice import Dataset, DatasetType, FileResource, NoResource

        resource = self._get_dataset_resource(dataset)
        dataset_name = self._get_asset_name(dataset["variable"], self._prefix)
        no_resource_dataset = Dataset(
            type=DatasetType.UNKNOWN,
            resource=NoResource(
                dataframes=dataset["dataframe"],
                origin="DATAFRAME",
                type=dataset["type"],
                capture_schema_only=self._capture_schema_only,
            ),
            name=dataset_name,
        )
        if resource:
            # TODO Dataset type ?
            vec_dataset = Dataset(
                type=DatasetType.UNKNOWN,
                resource=FileResource(
                    paths=resource,
                    dataframes=dataset["dataframe"],
                    capture_schema_only=self._capture_schema_only,
                ),
                name=dataset_name,
            )
        else:
            vec_dataset = no_resource_dataset
        try:
            self._iteration_service.log_dataset(vec_dataset)
        except FileNotFoundError:
            self._iteration_service.log_dataset(no_resource_dataset)
        _logger.info(f"Dataset {dataset_name!r} logged in iteration {self._iteration.name!r}.")

    def _get_dataset_resource(self, dataset: TDataset) -> str | None:

        if not self._cell_content:
            return None
        try:
            # Avoid getting stray dataset with autolog.notebook()

            match = []
            for cell in self._cell_content:
                cell = preprocess_code(cell)
                tree = ast.parse(cell)
                visitor = FilePathVisitor(is_dataset_path=True)
                visitor.visit(tree)
                for resource_info in visitor.dataset_file_paths:
                    path_var, file_path = resource_info["variable"], resource_info["path"]
                    dataset_variable = re.escape(dataset["variable"])
                    if path_var:
                        pattern = rf"{dataset_variable}\s*=\s*pd\.read_csv\(\s*{path_var}\s*\).*\n"
                    else:
                        regex_path = re.escape(file_path)
                        pattern = rf"{dataset_variable}\s*=\s*pd\.read_csv\(.*?{regex_path}.*?\).*\n"
                    match_dataset_path = re.search(pattern, cell)
                    if match_dataset_path:
                        match.append(file_path)

            if len(match) < 1:
                return None
            # TODO update regex
            # check if read csv has comma dominated arguments
            return match[0]
        except TypeError:
            return None

    def _get_graphs(self, is_notebook: bool) -> list[Any]:
        global GRAPHS

        graphs = []
        if is_notebook:
            displayed_graphs = [displayed_graph for cell in GRAPHS.values() for displayed_graph in cell["displayed"]]
            saved_graphs = [graph for cell in GRAPHS.values() for graph in cell["saved"]]
        else:
            cell_id = _get_cell_id(self._ip)
            cells_graphs = GRAPHS[cell_id]
            displayed_graphs = cells_graphs["displayed"]
            saved_graphs = cells_graphs["saved"]

        graphs += saved_graphs
        graphs += displayed_graphs
        return graphs

    def _get_asset_name(self, variable: str, prefix: str | None = None) -> str:
        if prefix is None:
            return f"{self._iteration.phase.id}-{variable}"
        elif prefix == "":
            return variable
        return f"{prefix}-{variable}"
