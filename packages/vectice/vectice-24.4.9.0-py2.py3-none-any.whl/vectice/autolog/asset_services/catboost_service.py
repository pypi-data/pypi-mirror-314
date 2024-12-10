from __future__ import annotations

from typing import TYPE_CHECKING, Any

from vectice.autolog.asset_services.metric_service import MetricService
from vectice.autolog.asset_services.technique_service import TechniqueService
from vectice.autolog.model_library import ModelLibrary

if TYPE_CHECKING:
    from catboost.core import CatBoost


class AutologCatboostService(MetricService, TechniqueService):
    def __init__(self, key: str, asset: CatBoost, data: dict, custom_metrics_data: set[str | None]):
        self._asset = asset
        self._key = key

        super().__init__(cell_data=data, custom_metrics=custom_metrics_data)

    def get_asset(self):
        _, params = self._get_catboost_info(self._asset)
        return {
            "variable": self._key,
            "model": self._asset,
            "library": ModelLibrary.CATBOOST,
            "technique": self._get_model_technique(self._asset, ModelLibrary.CATBOOST),
            "metrics": self._get_model_metrics(self._cell_data),
            "properties": params,
        }

    def _get_catboost_info(self, model: CatBoost) -> tuple[str, dict[str, Any]] | tuple[None, None]:
        try:
            params = {str(key): value for key, value in model.get_all_params().items() if value is not None}
            return "catboost", params
        except AttributeError:
            return None, None
