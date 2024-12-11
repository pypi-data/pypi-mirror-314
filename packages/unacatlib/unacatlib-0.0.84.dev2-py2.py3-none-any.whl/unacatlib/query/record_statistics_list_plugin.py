from typing import List, Union, Protocol
import pandas as pd
from unacatlib.unacast.catalog.v3alpha import (
    ListRecordsStatistics,
    ListRecordsStatisticsResponse,
)
from unacatlib.query.text_utils import to_snake_case


class RecordStatisticsListProtocol(Protocol):
    """Protocol defining the interface for RecordStatisticsList"""

    def to_df(self) -> pd.DataFrame: ...


class RecordStatisticsList(list, RecordStatisticsListProtocol):
    """A list subclass specifically for Record objects that adds statistical analysis capabilities."""

    def __init__(
        self,
        items: Union[List[ListRecordsStatistics], None] = None,
    ):
        super().__init__(items or [])

    def __getitem__(self, index: int) -> ListRecordsStatistics:
        return super().__getitem__(index)

    def to_df(self) -> pd.DataFrame:
        """
        Convert the list of Records to a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing all records with their fields as columns,
                         ordered according to the field definitions if available.
        """
        if not self:
            return pd.DataFrame()

        records_data = [record.to_pydict() for record in self]
        df = pd.DataFrame(records_data)
        df.rename(columns={col: to_snake_case(col) for col in df.columns}, inplace=True)
        return df


# Monkey patch ListRecordsResponse to wrap records in RecordStatisticsList
def wrap_statistics(response: ListRecordsStatisticsResponse) -> None:
    """Wrap statistics in a RecordStatisticsList"""
    if hasattr(response, "statistics"):
        response.statistics = RecordStatisticsList(response.statistics)


original_init = ListRecordsStatisticsResponse.__init__


def new_init(self, *args, **kwargs):
    original_init(self, *args, **kwargs)
    wrap_statistics(self)


ListRecordsStatisticsResponse.__init__ = new_init

# Add type hints to ListRecordsStatisticsResponse
ListRecordsStatisticsResponse.statistics: RecordStatisticsList
