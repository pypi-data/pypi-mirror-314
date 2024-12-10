from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vectice.autolog.asset_services.metric_service import MetricService
from vectice.autolog.asset_services.technique_service import TechniqueService
from vectice.autolog.model_library import ModelLibrary

if TYPE_CHECKING:
    from keras import Model as KerasModel  # type: ignore[reportMissingImports]  # type: ignore[reportMissingImports]
    from keras.layers import InputLayer  # type: ignore[reportMissingImports]
    from keras.models import Model as KerasModel  # type: ignore[reportMissingImports]


class AutologKerasService(MetricService, TechniqueService):
    def __init__(self, key: str, asset: KerasModel, data: dict, custom_metrics_data: set[str | None]):
        self._asset = asset
        self._key = key

        super().__init__(cell_data=data, custom_metrics=custom_metrics_data)

    def get_asset(self):
        model_metrics = self._get_model_metrics(self._cell_data)
        training_metrics = self._get_keras_training_metrics(self._asset)
        _, params = self._get_keras_info(self._asset)
        return {
            "variable": self._key,
            "model": self._asset,
            "library": ModelLibrary.KERAS,
            "technique": self._get_model_technique(self._asset, ModelLibrary.KERAS),
            "metrics": {**model_metrics, **training_metrics},
            "properties": params,
        }

    def _format_keras_params(self, model: KerasModel) -> dict[str, Any]:
        params: dict[str, Any] = {}

        def _get_output_shape(layer: InputLayer) -> tuple:
            try:
                # Keras 2.15.1 & below
                return layer.output_shape
            except AttributeError:
                return layer.output.shape  # pyright: ignore[reportAttributeAccessIssue]

        for i, layer in enumerate(model.layers):
            output_shape = _get_output_shape(layer)
            params[f"Layer-{i}"] = {
                "name": layer.name,
                "param": layer.count_params(),
                "output shape": output_shape,
            }
        params["Total # of weights"] = model.count_params()

        return params

    def _get_keras_info(self, model: KerasModel) -> tuple[str, dict[str, Any]] | tuple[None, None]:
        try:
            return "keras", self._format_keras_params(model)
        except Exception:
            return None, None
