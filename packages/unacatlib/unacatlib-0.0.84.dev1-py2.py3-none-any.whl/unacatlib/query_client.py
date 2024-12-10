from typing import List
from grpclib.client import Channel
from syncer import sync
from typing import Optional
from unacatlib.query.data_reference_list_plugin import wrap_data_references
from unacatlib.unacast.unatype import FilterClause
from unacatlib.unacast.catalog.v3 import (
    CatalogQueryStub,
    Options,
    GetDataReferenceRequest,
    ListDataReferencesRequest,
    ListRecordsRequest,
    ListRecordsResponse,
    OrderBy,
    OrderDirection,
    SearchFieldValuesRequest,
    SearchFieldValuesResponse,
    TrimToPeriodOfExistence,
    Field,
    BoundingBox,
)
from unacatlib.unacast.catalog.v3alpha import (
    CatalogQueryStub as CatalogQueryAlphaStub,
    FileDownloadRequest,
    FileDownloadResponse,
)

from unacatlib.query.proto_wrappers import (
    PaginatedListRecordsResponse,
    PaginatedSearchFieldValuesResponse,
    GetDataReferenceResponse,
    ListDataReferencesResponse,
    ListRecordsStatisticsResponse,
)


SERVER_ADDRESS = "catalog.unacastapis.com"
PORT = 443
REQUEST_TAGS = {"source": "unacat-py"}

LIST_RECORDS_PAGE_SIZE = 300
SEARCH_FIELD_VALUES_PAGE_SIZE = 1000
ABSOLUTE_MAX_NUMBER_OF_RECORDS = 100_000
OVER_ABSOLUTE_MAX_NUMBER_OF_RECORDS_MESSAGE = f"If you want to retrieve more than {ABSOLUTE_MAX_NUMBER_OF_RECORDS}, we suggest using the file export endpoint or setting up a file delivery. Please contact Unacast support if you need assistance at support@unacast.com."


__all__ = [
    "QueryClient",
    "FilterClause",
    "TrimToPeriodOfExistence",
    "OrderBy",
    "OrderDirection",
    "BoundingBox",
]


class QueryClient(object):
    """
    A client for querying the Unacast Catalog API.


    Example:
        >>> from unacatlib import QueryClient
        >>> client = QueryClient(token="your-token")
        >>> response = client.list_records("ml_visitation.foot_traffic_month")
        >>> df = response.records.to_df()
        >>> print(df.head())
    """

    def __init__(
        self,
        token: str = "",
        billing_context: str = "",
        server_address: str = SERVER_ADDRESS,
        port: int = PORT,
    ):
        self.token = token
        self.billing_context = billing_context
        self.server_address = server_address
        self.port = port

        metadata = [("authorization", "Bearer " + self.token)]

        self.channel = Channel(host=self.server_address, port=self.port, ssl=True)
        self.query_service = CatalogQueryStub(self.channel, metadata=metadata)
        self.query_service_alpha = CatalogQueryAlphaStub(
            self.channel, metadata=metadata
        )

        # TODO: do we need properties for ssl as the old client has?

    def get_data_reference(self, data_reference_name: str) -> GetDataReferenceResponse:
        """
        Get a specific data reference by name.

        Args:
            data_reference_name: The name of the data reference to get

        Returns:
            GetDataReferenceResponse with data_reference.fields as FieldDefinitionList
        """
        request = GetDataReferenceRequest(
            data_reference_name=data_reference_name,
            billing_context=self.billing_context,
        )

        response: GetDataReferenceResponse = sync(
            self.query_service.get_data_reference(request)
        )
        return response

    def list_data_references(self) -> ListDataReferencesResponse:
        """
        List available data references.

        Returns:
            ListDataReferencesResponse with data_references as DataReferenceList
        """
        request = ListDataReferencesRequest(billing_context=self.billing_context)
        response: ListDataReferencesResponse = sync(
            self.query_service.list_data_references(request)
        )
        wrap_data_references(response)
        return response

    def list_records(
        self,
        data_reference_name: str,
        fields: Optional[List[str]] = None,
        filters: Optional[List[FilterClause]] = None,
        options: Optional[Options] = None,
        limit: Optional[int] = None,
    ) -> PaginatedListRecordsResponse:
        """
        List records from a data reference with automatic pagination handling.


        Args:
            data_reference_name: The name of the data reference to query.  Use `client.list_data_references().data_references.to_df()` to get the available `data_reference_name`.
            filters: Optional list of filters to apply. Use `client.get_data_reference(data_reference_name).data_reference.fields.to_df()` to get the available `field` and `operator` to use in the `FilterClause`. Use the `search_field_values` endpoint to get the available `values` to use in the `FilterClause`.
            options: Optional query options

        Returns:
            PaginatedListRecordsResponse containing all records and field definitions,
            inheriting all ListRecordsResponse functionality but without exposing pagination details

        Example:
            >>> from unacatlib import QueryClient
            >>> client = QueryClient(token="your-token")
            >>> response = client.list_records(
            ...     "ml_visitation.foot_traffic_month",
            ...     filters=[
            ...         FilterClause(
            ...             field_name="brands",
            ...             operator="==",
            ...             value="Target"
            ...         )
            ...     ],
            ...     limit=500
            ... )
            >>> df = response.records.to_df()
            >>> print(df.head())
        """

        if limit and limit > ABSOLUTE_MAX_NUMBER_OF_RECORDS:
            raise ValueError(
                f"The limit is {limit:,}, which is more than the max number of records: {ABSOLUTE_MAX_NUMBER_OF_RECORDS:,}. Please use a smaller limit. {OVER_ABSOLUTE_MAX_NUMBER_OF_RECORDS_MESSAGE}"
            )

        all_records = []
        page_token = None
        field_definitions = None
        total_size = 0
        page_size = (
            limit
            if limit and limit < LIST_RECORDS_PAGE_SIZE
            else LIST_RECORDS_PAGE_SIZE
        )

        field_objects = [Field(name=field) for field in fields] if fields else None

        while True:
            if options is None:
                options = Options()

            request = ListRecordsRequest(
                data_reference_name=data_reference_name,
                fields=field_objects,
                filters=filters,
                options=options,
                billing_context=self.billing_context,
                page_token=page_token,
                page_size=page_size,
            )

            response: ListRecordsResponse = sync(
                self.query_service.list_records(request)
            )

            # Store field definitions and total size from first response
            if field_definitions is None:
                field_definitions = response.field_definitions
                total_size = response.total_size

            # Accumulate records from this page
            if response.records:
                all_records.extend(response.records)

            # Check if we've reached the max number of records
            if ABSOLUTE_MAX_NUMBER_OF_RECORDS <= response.total_size:
                raise ValueError(
                    f"The response contains {response.total_size:,} records, which is more than the max number of records: {ABSOLUTE_MAX_NUMBER_OF_RECORDS:,}. Please use more specific filters or options to reduce the number of records. {OVER_ABSOLUTE_MAX_NUMBER_OF_RECORDS_MESSAGE}"
                )

            if limit and len(all_records) >= limit:
                if limit < len(all_records):
                    all_records = all_records[:limit]
                break

            # Check if there are more pages
            if not response.next_page_token:
                break

            page_token = response.next_page_token

        # Create a new response without pagination details
        resp = PaginatedListRecordsResponse(
            records=all_records,
            field_definitions=field_definitions,
            total_size=total_size,
        )

        return resp

    # Create an alias for list_records
    query = list_records

    def search_field_values(
        self,
        data_reference_name: str,
        field: str,
        term: Optional[str] = None,
        filters: Optional[List[FilterClause]] = None,
        options: Optional[Options] = None,
        limit: Optional[int] = None,
    ) -> PaginatedSearchFieldValuesResponse:
        """
        Search for distinct values of a field.


        Args:
            data_reference_name: The name of the data reference to query.  Use `client.list_data_references().data_references.to_df()` to get the available `data_reference_name`.
            field: The field to search values for. Use `client.get_data_reference(data_reference_name).data_reference.fields.to_df()` to get the available `field`.
            term: Optional search term to filter values
            filters: Optional list of filters to apply. Use `client.get_data_reference(data_reference_name).data_reference.fields.to_df()` to get the available `field` and `operator` to use in the `FilterClause`. Use the `search_field_values` endpoint to get the available `values` to use in the `FilterClause`.
            options: Optional query options
            limit: Optional limit on the number of values to return
        Returns:
            List of distinct values

        Example:
            >>> from unacatlib import QueryClient
            >>> client = QueryClient(token="your-token")
            >>> response = client.search_field_values("ml_visitation.foot_traffic_month", "brands", "Target")
            >>> print(response)
        """
        if limit and limit > ABSOLUTE_MAX_NUMBER_OF_RECORDS:
            raise ValueError(
                f"The limit is {limit:,}, which is more than the max number of values: {ABSOLUTE_MAX_NUMBER_OF_RECORDS:,}. Please use a smaller limit. {OVER_ABSOLUTE_MAX_NUMBER_OF_RECORDS_MESSAGE}"
            )

        all_values = []
        page_token = None
        field_definitions = None
        # total_size = 0
        page_size = (
            limit
            if limit and limit < SEARCH_FIELD_VALUES_PAGE_SIZE
            else SEARCH_FIELD_VALUES_PAGE_SIZE
        )

        field_object = Field(name=field)
        while True:
            request = SearchFieldValuesRequest(
                data_reference_name=data_reference_name,
                field=field_object,
                term=term,
                filters=filters,
                options=options,
                billing_context=self.billing_context,
                page_token=page_token,
                page_size=page_size,
            )

            response: SearchFieldValuesResponse = sync(
                self.query_service.search_field_values(request)
            )

            # TODO: change this to be using total_size instead
            if len(all_values) > ABSOLUTE_MAX_NUMBER_OF_RECORDS:
                raise ValueError(
                    f"The response contains {len(all_values):,} values, which is more than the max number of values: {ABSOLUTE_MAX_NUMBER_OF_RECORDS:,}. Please use more specific filters or options to reduce the number of values. {OVER_ABSOLUTE_MAX_NUMBER_OF_RECORDS_MESSAGE}"
                )

            # Store field definitions and total size from first response
            if field_definitions is None:
                field_definitions = response.field_definition
                # total_size = response.total_size

            # Accumulate values from this page
            if response.values:
                all_values.extend(response.values)

            if limit and len(all_values) >= limit:
                if limit < len(all_values):
                    all_values = all_values[:limit]
                break

            # Check if there are more pages
            if not response.next_page_token:
                break

            page_token = response.next_page_token

        return PaginatedSearchFieldValuesResponse(
            values=all_values,
            field_definition=field_definitions,
            total_size=len(all_values),
        )

    def file_download(
        self,
        data_reference_name: str,
        fields: Optional[List[Field]] = None,
        filters: Optional[List[FilterClause]] = None,
        options: Optional[Options] = None,
    ):
        """
        Download a file from a data reference.

        Args:
            data_reference_name: The name of the data reference to query
            fields: Optional list of fields to include in the download
            filters: Optional list of filters to apply
            options: Optional query options

        Note:
            This method is currently in alpha and may change.
        """

        print("Warning: Endpoint is currently in alpha and may change.")

        request = FileDownloadRequest(
            data_reference_name=data_reference_name,
            options=options,
            billing_context=self.billing_context,
            filters=filters,
            fields=fields,
        )
        response: FileDownloadResponse = sync(
            self.query_service_alpha.file_download(request)
        )
        return response

    def list_records_statistics(
        self,
        data_reference_name: str,
        filters: Optional[List[FilterClause]] = None,
        options: Optional[Options] = None,
    ) -> ListRecordsStatisticsResponse:
        """
        List statistics for a data reference.

        Note:
            This method is currently in alpha and may change.
        """
        print("Warning: Endpoint is currently in alpha and may change.")

        request = ListRecordsRequest(
            data_reference_name=data_reference_name,
            filters=filters,
            options=options,
            billing_context=self.billing_context,
        )
        response: ListRecordsStatisticsResponse = sync(
            self.query_service_alpha.list_records_statistics(request)
        )
        return response

    # Create an alias for list_records_statistics
    query_statistics = list_records_statistics
