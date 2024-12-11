from typing import List, Union, Iterator, Sequence, Protocol, Optional
import pandas as pd
from unacatlib.unacast.catalog.v3 import ListRecordsResponse, Record, FieldDefinition


class RecordListProtocol(Protocol):
    """Protocol defining the interface for RecordList"""

    def to_df(self) -> pd.DataFrame: ...


class RecordList(list, RecordListProtocol):
    """A list subclass specifically for Record objects that adds DataFrame conversion capabilities."""

    def __init__(
        self,
        items: Union[List[Record], None] = None,
        field_definitions: Optional[List[FieldDefinition]] = None,
    ):
        super().__init__(items or [])
        self._field_definitions = field_definitions

    def to_df(self) -> pd.DataFrame:
        """
        Convert the list of Records to a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing all records with their fields as columns,
                         ordered according to the field definitions if available.

        Example:
            >>> list_records_response.records.to_df()
            # Returns DataFrame with all records
        """
        if not self:
            return pd.DataFrame()

        # Convert records to list of dictionaries
        records_data = [record.fields for record in self]
        df = pd.DataFrame(records_data)

        # Apply type conversions based on field definitions
        if self._field_definitions:
            for field_def in self._field_definitions:
                if field_def.name in df.columns:
                    field_type = field_def.type
                    if field_type == "COLUMN_TYPE_STRING":
                        df[field_def.name] = df[field_def.name].astype(str)
                    elif field_type == "COLUMN_TYPE_INTEGER":
                        df[field_def.name] = pd.to_numeric(
                            df[field_def.name], errors="coerce"
                        ).astype("Int64")
                    elif field_type == "COLUMN_TYPE_FLOAT":
                        df[field_def.name] = pd.to_numeric(
                            df[field_def.name], errors="coerce"
                        )
                    elif field_type == "COLUMN_TYPE_BOOLEAN":
                        df[field_def.name] = (
                            df[field_def.name]
                            .astype(str)
                            .str.lower()
                            .map({"true": True, "false": False})
                        )
                    elif field_type == "COLUMN_TYPE_DATE":
                        df[field_def.name] = pd.to_datetime(
                            df[field_def.name], errors="coerce"
                        )
                    else:
                        df[field_def.name] = df[field_def.name].astype(str)

            # Reorder columns based on field definitions
            current_cols = df.columns.tolist()
            ordered_fields = [f.name for f in self._field_definitions]
            ordered_cols = [col for col in ordered_fields if col in current_cols]
            extra_cols = [col for col in current_cols if col not in ordered_fields]
            df = df[ordered_cols + extra_cols]

        return df

    def __getitem__(self, i):
        result = super().__getitem__(i)
        if isinstance(i, slice):
            return RecordList(result, field_definitions=self._field_definitions)
        return result

    def __iter__(self) -> Iterator[Record]:
        return super().__iter__()

    def append(self, item: Record) -> None:
        super().append(item)

    def extend(self, items: Sequence[Record]) -> None:
        super().extend(items)

    def __dir__(self) -> List[str]:
        """Hide field_definitions from dir() and tab completion"""
        attrs = super().__dir__()
        return [attr for attr in attrs if not attr.endswith("field_definitions")]


# Monkey patch ListRecordsResponse to wrap records in RecordList
def wrap_records(response: ListRecordsResponse) -> None:
    """Wrap records in a RecordList"""
    if hasattr(response, "records"):
        response.records = RecordList(
            response.records, field_definitions=response.field_definitions
        )


original_init = ListRecordsResponse.__init__


def new_init(self, *args, **kwargs):
    original_init(self, *args, **kwargs)
    wrap_records(self)


ListRecordsResponse.__init__ = new_init

# Add type hints to ListRecordsResponse
ListRecordsResponse.records: RecordList
