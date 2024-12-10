import pandas as pd
from typing import List


class ValuesList(list):
    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame(self)


def wrap_values_list(values_list: List[str]) -> ValuesList:
    """Wrap values in a ValuesList"""
    if not isinstance(values_list, ValuesList):
        values_list = ValuesList(values_list)
    return values_list
