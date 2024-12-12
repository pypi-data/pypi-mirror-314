import datetime as dt
import typing
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd

from sklearn.base import TransformerMixin, BaseEstimator
from sklearn.utils import check_array
from sklearn.utils.validation import check_is_fitted

from tide.utils import (
    check_and_return_dt_index_df,
    timedelta_to_int,
    validate_odd_param,
    process_stl_odd_args,
    get_data_blocks,
)


class BaseProcessing(ABC, TransformerMixin, BaseEstimator):
    def get_feature_names_out(self, input_features=None):
        check_is_fitted(self, attributes=["features_"])
        return self.features_

    @abstractmethod
    def fit(self, X: pd.Series | pd.DataFrame, y=None):
        """Operations happening during fitting process"""
        pass

    @abstractmethod
    def transform(self, X):
        """Operations happening during transforming process"""
        pass


class BaseSTL(ABC, BaseEstimator):
    def __init__(
        self,
        period: int | str | dt.timedelta = "24h",
        trend: int | str | dt.timedelta = "15d",
        seasonal: int | str | dt.timedelta = None,
        stl_kwargs: dict[str, typing.Any] = None,
    ):
        self.stl_kwargs = stl_kwargs
        self.period = period
        self.trend = trend
        self.seasonal = seasonal

    def _pre_fit(self, X: pd.Series | pd.DataFrame):
        self.stl_kwargs = {} if self.stl_kwargs is None else self.stl_kwargs

        X = check_and_return_dt_index_df(X)
        check_array(X)

        self.stl_kwargs["period"] = timedelta_to_int(self.period, X)
        validate_odd_param("trend", self.trend)
        self.stl_kwargs["trend"] = self.trend
        process_stl_odd_args("trend", X, self.stl_kwargs)
        if self.seasonal is not None:
            self.stl_kwargs["seasonal"] = self.seasonal
            process_stl_odd_args("seasonal", X, self.stl_kwargs)


class BaseFiller:
    def __init__(
        self,
        gaps_lte: str | pd.Timedelta | dt.timedelta = None,
        gaps_gte: str | pd.Timedelta | dt.timedelta = None,
    ):
        self.gaps_lte = gaps_lte
        self.gaps_gte = gaps_gte

    def get_gaps_dict_to_fill(self, X: pd.Series | pd.DataFrame):
        X = check_and_return_dt_index_df(X)
        return get_data_blocks(
            X,
            is_null=True,
            select_inner=False,
            lower_td_threshold=self.gaps_lte,
            upper_td_threshold=self.gaps_gte,
            upper_threshold_inclusive=True,
            lower_threshold_inclusive=True,
            return_combination=False,
        )

    def get_gaps_mask(self, X: pd.Series | pd.DataFrame):
        gaps_dict = self.get_gaps_dict_to_fill(X)
        df_mask = pd.DataFrame(index=X.index)
        for col, idx_list in gaps_dict.items():
            if idx_list:
                combined_idx = pd.concat([idx.to_series() for idx in idx_list]).index
                df_mask[col] = X.index.isin(combined_idx)
            else:
                df_mask[col] = np.zeros_like(X.shape[0]).astype(bool)

        return df_mask
