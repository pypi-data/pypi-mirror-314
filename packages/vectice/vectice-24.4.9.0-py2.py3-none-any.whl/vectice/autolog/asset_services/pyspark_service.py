from __future__ import annotations

from typing import TYPE_CHECKING

from vectice.models.resource.metadata.db_metadata import TableType

if TYPE_CHECKING:
    from pyspark.sql import DataFrame as SparkDF
    from pyspark.sql.connect.dataframe import DataFrame as SparkConnectDF


class AutologPysparkService:
    def __init__(self, key: str, asset: SparkDF | SparkConnectDF):
        self._asset = asset
        self._key = key

    def get_asset(self):
        return {
            "variable": self._key,
            "dataframe": self._asset,
            "type": TableType.SPARK,
        }
