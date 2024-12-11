from typing import List, TypeVar, Union, Iterator, Sequence, Protocol, Optional
import pandas as pd
from unacatlib.unacast.catalog.v3 import ListDataReferencesResponse, DataReference
from unacatlib.query.text_utils import extract_plain_text_from_portable_text
from unacatlib.query.field_definition_list_plugin import FieldDefinitionList

from unacatlib.query.text_utils import to_snake_case


class DataReferenceListProtocol(Protocol):
    """Protocol defining the interface for DataReferenceList"""

    def to_df(self) -> pd.DataFrame: ...


class DataReferenceList(list, DataReferenceListProtocol):
    """A list subclass specifically for DataReference objects that adds DataFrame conversion capabilities."""

    def __init__(self, items: Union[List[DataReference], None] = None):
        super().__init__(items or [])
        # Ensure fields are wrapped in FieldDefinitionList for each DataReference
        for item in self:
            wrap_data_reference_fields(item)

    def to_df(self) -> pd.DataFrame:
        """
        Convert the list of DataReferences to a pandas DataFrame.

        Returns:
            pd.DataFrame: A DataFrame containing the data references with columns:
                - name: Data reference name
                - data_product_display_name: Display name of the data product
                - data_product_description: Description of the data product
                - data_listing_display_name: Display name of the data listing
                - data_listing_description: Description of the data listing in portable text format
                - data_listing_description_plain: Plain text description of the data listing inferred from the portable text format

        Example:
            >>> list_data_references_response.data_references.to_df()
            # Returns DataFrame with data references
        """
        if not self:
            return pd.DataFrame()

        references_data = [
            {
                **ref.to_pydict(),
                "data_listing_description_plain": extract_plain_text_from_portable_text(
                    ref.data_listing_description
                ),
            }
            for ref in self
        ]

        df = pd.DataFrame(references_data)
        df.rename(columns={col: to_snake_case(col) for col in df.columns}, inplace=True)
        return df

    def __getitem__(self, i):
        result = super().__getitem__(i)
        if isinstance(i, slice):
            return DataReferenceList(result)
        return result

    def __iter__(self) -> Iterator[DataReference]:
        return super().__iter__()

    def append(self, item: DataReference) -> None:
        wrap_data_reference_fields(item)
        super().append(item)

    def extend(self, items: Sequence[DataReference]) -> None:
        for item in items:
            wrap_data_reference_fields(item)
        super().extend(items)


# Monkey patch DataReference to wrap fields in FieldDefinitionList
def wrap_data_reference_fields(data_reference: DataReference) -> None:
    """Wrap fields in a FieldDefinitionList"""
    if hasattr(data_reference, "fields") and not isinstance(
        data_reference.fields, FieldDefinitionList
    ):
        data_reference.fields = FieldDefinitionList(data_reference.fields)


original_data_reference_init = DataReference.__init__


def new_data_reference_init(self, *args, **kwargs):
    original_data_reference_init(self, *args, **kwargs)
    wrap_data_reference_fields(self)


DataReference.__init__ = new_data_reference_init

# Add type hints to DataReference
DataReference.fields: FieldDefinitionList


# Monkey patch ListDataReferencesResponse to wrap data_references in DataReferenceList
def wrap_data_references(response: ListDataReferencesResponse) -> None:
    """Wrap data_references in a DataReferenceList"""
    if hasattr(response, "data_references"):
        response.data_references = DataReferenceList(response.data_references)


original_init = ListDataReferencesResponse.__init__


def new_init(self, *args, **kwargs):
    original_init(self, *args, **kwargs)
    wrap_data_references(self)


ListDataReferencesResponse.__init__ = new_init

# Add type hints to ListDataReferencesResponse
ListDataReferencesResponse.data_references: DataReferenceList
