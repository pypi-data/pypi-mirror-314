from collections.abc import Callable

import pandas as pd
from pandas.core.indexers.objects import VariableOffsetWindowIndexer
from pandas.tseries.offsets import BaseOffset


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
        transformed.rolling(
            VariableOffsetWindowIndexer(index=series.index, offset=offset(period)),
            min_periods=1,
        )
        if offset
        else transformed.rolling(window=period, min_periods=1)
    )

    return agg_func(rolled).shift(-period - extra_shift_by)
