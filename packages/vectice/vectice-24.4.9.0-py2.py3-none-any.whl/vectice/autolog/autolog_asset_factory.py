from __future__ import annotations

from abc import abstractmethod
from importlib.util import find_spec
from typing import Any, Protocol

from vectice.api.http_error_handlers import VecticeException
from vectice.autolog.asset_services import (
    AutologCatboostService,
    AutologKerasService,
    AutologLightgbmService,
    AutologPandasService,
    AutologPysparkMLService,
    AutologPysparkService,
    AutologPytorchService,
    AutologSklearnService,
    AutologStatsModelWrapperService,
    AutologVecticeAssetService,
    VecticeObjectClasses,
)


class IAutologService(Protocol):
    @abstractmethod
    def get_asset(self) -> dict[str, Any] | None: ...


class AssetFactory:
    @staticmethod
    def get_asset_service(key: str, asset: Any, data: dict, custom_metrics: set[str | None] = set()) -> IAutologService:
        is_pandas = find_spec("pandas") is not None
        is_pyspark = find_spec("pyspark") is not None
        is_lgbm = find_spec("lightgbm") is not None
        is_sklearn = find_spec("sklearn") is not None
        is_catboost = find_spec("catboost") is not None
        is_keras = find_spec("keras") is not None
        is_statsmodels = find_spec("statsmodels") is not None
        is_pytorch = find_spec("torch") is not None

        if is_pandas:
            from pandas import DataFrame

            if isinstance(asset, DataFrame):
                return AutologPandasService(key, asset)

        if is_pyspark:
            # base estimator class, Predictor is for a model with no fit
            from pyspark.ml.base import Model, PredictionModel
            from pyspark.ml.pipeline import PipelineModel
            from pyspark.ml.tuning import CrossValidatorModel

            # pyspark evaluators
            # Pipeline isn't fitted and PipelineModel has a fit
            # clustering models e.g kmeans
            # JavaParams is for pipeline components (might remove/move logic due to overlaps)
            from pyspark.ml.wrapper import JavaModel

            # , Evaluator, JavaParams, Pipeline
            pyspark_service_types = (CrossValidatorModel, PredictionModel, JavaModel, Model, PipelineModel)

            from pyspark.sql import DataFrame as SparkDF
            from pyspark.sql.connect.dataframe import DataFrame as SparkConnectDF

            if isinstance(asset, (SparkDF, SparkConnectDF)):
                return AutologPysparkService(key, asset)

            # # internal note: predictor = no fit & estimator = fit
            # if isinstance(asset, (Pipeline, PipelineModel)):
            #     return AutologPysparkMLService(key, asset, data)

            if isinstance(asset, pyspark_service_types):
                return AutologPysparkMLService(key, asset, data)

        if is_lgbm:
            from lightgbm.basic import Booster

            if isinstance(asset, Booster):
                return AutologLightgbmService(key, asset, data, custom_metrics)

        if is_catboost:
            from catboost.core import CatBoost

            if isinstance(asset, CatBoost):
                return AutologCatboostService(key, asset, data, custom_metrics)

        if is_keras:
            from keras.models import Model as KerasModel  # type: ignore[reportMissingImports]

            if isinstance(asset, KerasModel):
                return AutologKerasService(key, asset, data, custom_metrics)

        if is_pytorch:
            from torch.nn import Module

            if isinstance(asset, Module):
                return AutologPytorchService(key, asset, data, custom_metrics)

        if isinstance(asset, VecticeObjectClasses):
            return AutologVecticeAssetService(key, asset)  # type: ignore[reportArgumentType]

        if is_statsmodels:
            from statsmodels.base.wrapper import ResultsWrapper

            if isinstance(asset, ResultsWrapper):
                return AutologStatsModelWrapperService(key, asset, data, custom_metrics)

        if is_sklearn:
            return AutologSklearnService(key, asset, data, custom_metrics)

        raise VecticeException(f"Asset {asset} of type ({type(asset)!r}) not handled")
