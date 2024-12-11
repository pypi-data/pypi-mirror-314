
from syncer import sync
from unacatlib.unacast.operator.v1 import GetJobStatusRequest, IndexJobOperatorServiceStub, GetJobStatusResponse
import time

from halo import Halo

from unacatlib.unacast.index.v1 import IndexStatus, IndexEvent, Index

class IndexJob(object):

    def __init__(self, catalog: 'Catalog', job_id: str):
      self._catalog = catalog
      self._index_job_operator_service: IndexJobOperatorServiceStub = catalog._client.index_job_operator_service

      self._job_id = job_id
      self._last_status: GetJobStatusResponse | None = None

    def status(self, refresh=False) -> str:
      if (self._last_status is None or refresh):
        return self._fetch_status().status_string
      return self._last_status.status_string

    def _fetch_status(self) -> GetJobStatusResponse:
      res = sync(
        self._index_job_operator_service.get_index_job_status(GetJobStatusRequest(
          job_id = self._job_id
        ))
      )

      self._last_status = res

      return res
