from typing import (
    List,
    TypeVar,
    Callable,
    ClassVar,
    Sequence,
    Generic,
    overload,
    Union,
    Iterator,
    Protocol,
)
import pandas as pd
from unacatlib.unacast.catalog.v3 import FieldDefinition, ListRecordsResponse
from unacatlib.query.text_utils import to_snake_case


class FieldDefinitionListProtocol(Protocol):
    """Protocol defining the interface for FieldDefinitionList"""

    def to_df(self) -> pd.DataFrame: ...


class FieldDefinitionList(list, FieldDefinitionListProtocol):
    """A list subclass specifically for FieldDefinition objects that adds DataFrame conversion capabilities."""

    def __init__(self, items: Union[List[FieldDefinition], None] = None):
        super().__init__(items or [])

    def to_df(self) -> pd.DataFrame:
        """
        Convert the list of FieldDefinitions to a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the field definitions with columns:
                - name: Field name
                - type: Field type
                - description: Field description
                - filters: Available filters
                - example_value: Example value
                - included_by_default: Whether field is included by default

        Example:
            >>> list_records_response.field_definitions.to_df()
            # Returns DataFrame with field definitions
        """
        if not self:
            return pd.DataFrame()

        fields_data = [
            {
                **f.to_dict(),
                "filters_plain": f.filters.supported_operators,
            }
            for f in self
        ]

        df = pd.DataFrame(fields_data)
        df.rename(columns={col: to_snake_case(col) for col in df.columns}, inplace=True)
        return df

    # Add type hints for standard list methods to ensure they show up in IDE
    @overload
    def __getitem__(self, i: int) -> FieldDefinition: ...

    @overload
    def __getitem__(self, s: slice) -> "FieldDefinitionList": ...

    def __getitem__(self, i):
        result = super().__getitem__(i)
        if isinstance(i, slice):
            return FieldDefinitionList(result)
        return result

    def __iter__(self) -> Iterator[FieldDefinition]:
        return super().__iter__()

    def append(self, item: FieldDefinition) -> None:
        super().append(item)

    def extend(self, items: Sequence[FieldDefinition]) -> None:
        super().extend(items)


# Monkey patch ListRecordsResponse to wrap field_definitions in FieldDefinitionList
def wrap_field_definitions(response: ListRecordsResponse) -> None:
    """Wrap field_definitions in a FieldDefinitionList"""
    if hasattr(response, "field_definitions"):
        response.field_definitions = FieldDefinitionList(response.field_definitions)


original_init = ListRecordsResponse.__init__


def new_init(self, *args, **kwargs):
    original_init(self, *args, **kwargs)
    wrap_field_definitions(self)


ListRecordsResponse.__init__ = new_init

# Add type hints to ListRecordsResponse
ListRecordsResponse.field_definitions: FieldDefinitionList
