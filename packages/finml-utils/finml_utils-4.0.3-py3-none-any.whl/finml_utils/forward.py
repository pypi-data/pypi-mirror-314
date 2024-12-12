from collections.abc import Callable

import pandas as pd
from pandas.core.indexers.objects import VariableOffsetWindowIndexer
from pandas.tseries.offsets import BaseOffset


def variable_rolling(
    df: pd.Series | pd.DataFrame,
    window: int,
    offset: type[BaseOffset],
    min_periods: int | None,
) -> pd.core.window.rolling.Rolling:
    indexer = VariableOffsetWindowIndexer(index=df.index, offset=offset(window))

    if isinstance(offset, pd.offsets.Day | pd.offsets.BDay) and min_periods is not None:
        min_periods *= 10

    return df.rolling(window=indexer, min_periods=min_periods)


def create_forward_rolling(
    transformation_func: Callable | None,
    agg_func: Callable,
    series: pd.Series,
    period: int,
    extra_shift_by: int | None,
    offset: type[BaseOffset] | None,
) -> pd.Series:
    assert period > 0
    extra_shift_by = abs(extra_shift_by) if extra_shift_by is not None else 0
    transformation_func = transformation_func if transformation_func else lambda x: x

    transformed = transformation_func(series)
    rolled = (
        variable_rolling(transformed, period, offset, min_periods=1)
        if offset is not None
        else transformed.rolling(window=period, min_periods=1)
    )

    return agg_func(rolled).shift(-period - extra_shift_by)
