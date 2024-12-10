from typing import List

import pandas as pd

VALID_COMPARISONS = ("lt", "lte", "gt", "gte", "eq", "neq")


def split_dict(items: List[str], tokensep: str, keysep: str = ":"):
    """Splits the items in a list of strings to generate a set of (key, value) pairs."""
    return (
        tuple(token.split(keysep, maxsplit=1))
        for item in items
        for token in item.split(tokensep)
    )


def series_compare(series: pd.Series, operator: str, value: float):
    """Applies the comparison operator against a scalar value over a pandas Series."""
    if operator == "lt":
        return series.lt(value)
    if operator == "lte":
        return series.le(value)
    if operator == "gt":
        return series.gt(value)
    if operator == "gte":
        return series.ge(value)
    if operator == "eq":
        return series.eq(value)
    if operator == "neq":
        return series.ne(value)

    raise ValueError(f"Invalid comparison operator '{operator}'")


def df_pivot(df: pd.DataFrame, *, index: str, column: str, value: str):
    """Pivots a DataFrame."""
    return (
        pd.pivot_table(df, index=[index], columns=[column], values=value)
        .reset_index()
        .set_index(index)
        .dropna(axis=1, how="all")
        .fillna(0)
        .astype(float)
    )


def df_melt(df: pd.DataFrame, *, index: str, value: str):
    """Unpivots a DataFrame. Adds category labels for the drilldown IDs."""
    df = (
        df.reset_index()
        .set_index(index)
        .dropna(axis=1, how="all")
        .fillna(0)
        .reset_index()
    )
    return pd.melt(df, id_vars=[index], value_name=value)
