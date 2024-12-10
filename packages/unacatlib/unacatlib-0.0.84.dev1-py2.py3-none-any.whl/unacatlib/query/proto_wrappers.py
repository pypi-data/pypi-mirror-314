from typing import List
from unacatlib.unacast.catalog.v3 import (
    DataReference as DataReferenceProto,
    GetDataReferenceResponse as GetDataReferenceResponseProto,
    ListDataReferencesResponse as ListDataReferencesResponseProto,
    ListRecordsResponse,
    FieldDefinition,
    Record,
    SearchFieldValuesResponse,
)
from unacatlib.unacast.catalog.v3alpha import (
    ListRecordsStatisticsResponse as ListRecordsStatisticsResponseProto,
)

from unacatlib.query.record_list_plugin import RecordList
from unacatlib.query.field_definition_list_plugin import FieldDefinitionList
from unacatlib.query.record_statistics_list_plugin import (
    RecordStatisticsList,
    wrap_statistics,
)
from unacatlib.query.data_reference_list_plugin import (
    DataReferenceList,
    wrap_data_references,
    wrap_data_reference_fields,
)
from unacatlib.query.values_list_plugin import wrap_values_list


class ListDataReferencesResponse(ListDataReferencesResponseProto):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        wrap_data_references(self)

    # Type hints for IDE support
    data_references: DataReferenceList


class DataReference(DataReferenceProto):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        wrap_data_reference_fields(self)

    # Type hints for IDE support
    fields: FieldDefinitionList


class GetDataReferenceResponse(GetDataReferenceResponseProto):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        wrap_data_reference_fields(self.data_reference)

    # Type hints for IDE support
    data_reference: DataReference


class ListRecordsStatisticsResponse(ListRecordsStatisticsResponseProto):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        wrap_statistics(self)

    # Type hints for IDE support
    statistics: RecordStatisticsList


class PaginatedListRecordsResponse:
    """
    A wrapper around ListRecordsResponse that only exposes the desired attributes
    and methods while hiding pagination details.
    """

    __slots__ = ("_response", "records", "field_definitions", "total_size")

    def __init__(
        self,
        records: List[Record],
        field_definitions: List[FieldDefinition],
        total_size: int,
    ):
        # Create the wrapped response
        self._response = ListRecordsResponse(
            records=records, field_definitions=field_definitions, next_page_token=""
        )
        # Wrap collections in their respective list types
        self.field_definitions = FieldDefinitionList(self._response.field_definitions)
        self.total_size = total_size
        self.records = RecordList(self._response.records, self.field_definitions)

    def to_dict(self) -> dict:
        """Convert to dictionary representation"""
        d = self._response.to_dict()
        if "next_page_token" in d:
            del d["next_page_token"]
        return d

    def __dir__(self) -> List[str]:
        """Control which attributes are visible"""
        return ["records", "field_definitions", "to_dict", "total_size"]

    # Type hints for IDE support
    records: RecordList
    field_definitions: FieldDefinitionList


class PaginatedSearchFieldValuesResponse:
    """
    A wrapper around SearchFieldValuesResponse that only exposes the desired attributes
    and methods while hiding pagination details.
    """

    __slots__ = ("_response", "values", "field_definition", "total_size")

    def __init__(
        self,
        values: List[str],
        field_definition: FieldDefinition,
        total_size: int,
    ):
        self._response = SearchFieldValuesResponse(
            values=values, field_definition=field_definition, next_page_token=""
        )
        self.field_definition = FieldDefinitionList([field_definition])
        self.total_size = total_size
        self.values = wrap_values_list(values)

    def to_dict(self) -> dict:
        """Convert to dictionary representation"""
        d = self._response.to_dict()
        if "next_page_token" in d:
            del d["next_page_token"]
        return d

    def __dir__(self) -> List[str]:
        """Control which attributes are visible"""
        return ["values", "field_definition", "to_dict", "total_size"]

    # Type hints for IDE support
    field_definition: FieldDefinitionList
