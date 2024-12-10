from __future__ import annotations

from typing import Any

from vectice.autolog.asset_services.metric_service import MetricService
from vectice.autolog.asset_services.property_service import PropertyService
from vectice.autolog.asset_services.technique_service import TechniqueService
from vectice.autolog.model_library import ModelLibrary


class AutologPysparkMLService(MetricService, PropertyService, TechniqueService):
    def __init__(self, key: str, asset: Any, data: dict):
        self._asset = asset
        self._key = key

        super().__init__(cell_data=data)

    def get_asset(self, asset: Any | None = None):
        # Pipeline isn't fitted and PipelineModel has a fit
        from pyspark.ml.pipeline import PipelineModel
        from pyspark.ml.tuning import CrossValidatorModel

        original_asset = self._asset
        if asset:
            self._asset = asset

        if isinstance(self._asset, PipelineModel):
            return self.get_pipeline()
        if isinstance(self._asset, CrossValidatorModel):
            return self.get_validator()

        # .extractParamMap() as hash / params as list
        parameters = {
            param.name: value
            for param, value in self._asset.extractParamMap().items()
            if value and isinstance(value, (str, int, float))
        }

        # only estimators will have a summary
        summary_metrics = {}
        if hasattr(self._asset, "hasSummary") and self._asset.hasSummary:
            summary_metrics = self.get_summary_metrics(self._asset.summary)
        metrics = self._get_model_metrics(self._cell_data)
        metrics.update({key: value for key, value in summary_metrics.items() if key not in metrics})

        library = ModelLibrary.PYSPARKML
        asset = {
            "variable": self._key,
            "model": self._asset,
            "library": library,
            "technique": self._get_model_technique(self._asset, library),
            "metrics": metrics,
            "properties": parameters,
        }
        if asset:
            self._asset = original_asset
        return asset

    def get_summary_metrics(self, summary: Any, prefix: str | None = None) -> dict:
        # metrics
        summary_metrics = {}
        for attr_name in dir(summary):
            # Skip special methods
            if not attr_name.startswith("__"):
                attr_value = getattr(summary, attr_name)
                # get simple values for now, there are pd.DF returns aswell
                if isinstance(attr_value, (float, int)):
                    if prefix:
                        summary_metrics[f"{prefix}_{attr_name}"] = attr_value
                    else:
                        summary_metrics[attr_name] = attr_value
        return summary_metrics

    def get_validator(self):
        # .extractParamMap() as hash / params as list
        validator_key = self._asset.uid
        # just get the tuning parameters
        validator_prefix = validator_key.split("_")[0]
        parameters = {
            f"{validator_prefix}_{param.name}": value
            for param, value in self._asset.extractParamMap().items()
            if value and isinstance(value, (str, int, float)) and not isinstance(param, (dict, set))
        }
        best_model = self._asset.bestModel
        best_model_key = best_model.uid
        best_model_prefix = best_model_key.split("_")[0]
        best_model_params = {
            f"{best_model_prefix}_{param.name}": value
            for param, value in best_model.extractParamMap().items()
            if value and isinstance(value, (str, int, float))
        }
        parameters.update(best_model_params)

        # only estimators will have a summary
        best_model_metrics = {}
        if hasattr(best_model, "hasSummary") and best_model.hasSummary:
            best_model_metrics = self.get_summary_metrics(best_model.summary, best_model_prefix)

        metrics = self._get_model_metrics(self._cell_data)
        metrics.update(best_model_metrics)

        library = ModelLibrary.PYSPARKML
        asset = {
            "variable": self._key,
            "model": self._asset,
            "library": library,
            "technique": self._get_model_technique(self._asset, library),
            "metrics": metrics,
            "properties": parameters,
        }
        return asset

    def get_pipeline(self):
        library = ModelLibrary.PYSPARKML
        # Pipeline has getStages & PipelineModel has stages
        stages = self._asset.stages
        parsed_assets_metrics = {}
        parsed_assets_parameters = {}
        for stage in stages:
            parsed_asset = self.get_asset(stage)
            prefix = parsed_asset["technique"]
            parsed_asset_metrics = {f"{prefix}_{key}": value for key, value in parsed_asset["metrics"].items()}  # type: ignore[reportAttributeAccessIssue]
            parsed_asset_parameters = {f"{prefix}_{key}": value for key, value in parsed_asset["properties"].items()}  # type: ignore[reportAttributeAccessIssue]
            parsed_assets_metrics.update(parsed_asset_metrics)
            parsed_assets_parameters.update(parsed_asset_parameters)

        # only estimators will have a summary
        summary_metrics = {}
        if hasattr(self._asset, "hasSummary") and self._asset.hasSummary:
            summary_metrics = self.get_summary_metrics(self._asset.summary)

        metrics = self._get_model_metrics(self._cell_data)
        metrics.update(parsed_assets_metrics)
        metrics.update(summary_metrics)

        # .extractParamMap() as hash
        parameters = {param.name: value for param, value in self._asset.extractParamMap().items()}
        parameters.update(parsed_assets_parameters)

        return {
            "variable": self._key,
            "model": self._asset,
            "library": library,
            "technique": self._get_model_technique(self._asset, library),
            "metrics": metrics,
            "properties": parameters,
        }
