from __future__ import annotations

from typing import TYPE_CHECKING

from vectice.models.resource.metadata.db_metadata import TableType

if TYPE_CHECKING:
    from pandas import DataFrame


class AutologPandasService:
    def __init__(self, key: str, asset: DataFrame):
        self._asset = asset
        self._key = key

    def get_asset(self):
        return {
            "variable": self._key,
            "dataframe": self._asset,
            "type": TableType.PANDAS,
        }
