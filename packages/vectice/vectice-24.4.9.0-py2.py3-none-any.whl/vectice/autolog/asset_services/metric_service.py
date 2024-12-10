from __future__ import annotations

import ast
import math
from functools import reduce
from typing import TYPE_CHECKING, Any

from vectice.utils.code_parser import VariableVisitor, preprocess_code

if TYPE_CHECKING:
    from keras.models import Model as KerasModel  # type: ignore[reportMissingImports]
    from numpy import float_
    from statsmodels.base.wrapper import ResultsWrapper


# basic metrics
_autolog_metric_allowlist = [
    "aic",
    "bic",
    "centered_tss",
    "condition_number",
    "df_model",
    "df_resid",
    "ess",
    "f_pvalue",
    "fvalue",
    "llf",
    "mse_model",
    "mse_resid",
    "mse_total",
    "rsquared",
    "rsquared_adj",
    "scale",
    "ssr",
    "uncentered_tss",
]


class MetricService:
    def __init__(self, cell_data: dict, custom_metrics: set[str | None] = set()):
        self._cell_data = cell_data
        self._model_cell = None
        self._custom_metrics = custom_metrics

    def _get_model_metrics(self, data: dict) -> dict[str, Any]:
        # TODO mix of models ?
        cell_content = data["cell"]
        variables = data["variables"]

        if not cell_content:
            return {}
        # Get model cell content for metrics
        self._model_cell = preprocess_code(cell_content)

        tree = ast.parse(self._model_cell)
        visitor = VariableVisitor(True, self._custom_metrics)
        visitor.visit(tree)

        metrics = list(visitor.metric_variables)

        return reduce(
            lambda identified_metrics, key: (
                {**identified_metrics, key: variables[key]}
                if key in metrics and isinstance(variables[key], (int, float))
                else identified_metrics
            ),
            variables.keys(),
            {},
        )

    def _get_keras_training_metrics(self, model: KerasModel) -> dict[str, float]:
        try:
            return {
                str(key)
                + "_train": float(model.get_metrics_result()[key].numpy())  # pyright: ignore[reportGeneralTypeIssues]
                for key in model.get_metrics_result().keys()  # pyright: ignore[reportGeneralTypeIssues]
            }
        except Exception:
            return {}

    def _get_statsmodels_metrics(self, model: ResultsWrapper):
        try:
            # statsmodels can function without numpy
            import numpy

            has_numpy = True
        except ImportError:
            has_numpy = False

        def _convert_metric(metric_value: float | float_) -> float | None:
            if metric_value is numpy.float_:  # pyright: ignore[reportPossiblyUnboundVariable]
                metric_value = metric_value.item()

            if math.isnan(float(metric_value)):
                return None
            return round(float(metric_value), 4)

        result_metrics = {}
        for metric in _autolog_metric_allowlist:
            try:
                if hasattr(model, metric):
                    metric_value = getattr(model, metric)
                    if has_numpy:
                        # handle numpy floats
                        converted_metric = _convert_metric(metric_value)
                    else:
                        # simple conversion
                        converted_metric = None if math.isnan(float(metric_value)) else round(float(metric_value), 4)

                    if converted_metric:
                        result_metrics[metric] = _convert_metric(metric_value)
            except Exception:
                pass
        return result_metrics
