
from asyncio import run
from datetime import datetime
from unacatlib.unacast.byo.v1 import MetricProductionOrchestrationServiceStub, MetricProductionStatusUpdate, MetricProductionStatusUpdateStarted, MetricProductionStatusUpdateDelayed, MetricProductionStatusUpdateProduced, MetricProductionStatusUpdateRejected, MetricProductionStatusUpdateFailed, MetricProductionStatusUpdateFinished

# Helper-Class for updating status on a BYO Metric Job
class ByoMetricJob(object):
    def __init__(self, orchestrator: MetricProductionOrchestrationServiceStub, service_name: str, job_id: str):
        self.service_name = service_name
        self.job_id = job_id
        # self._client = client
        # self._service = client.byo_metric_orchestrator_service
        self._orchestrator = orchestrator

    def _getStatusBase(self):
      return MetricProductionStatusUpdate(
        job_id=self.job_id,
        service_ref = self.service_name,
        timestamp=datetime.utcnow().isoformat(),
      )

    def MarkAsRejected(self, reason: str):
      req = self._getStatusBase()
      req.rejected = MetricProductionStatusUpdateRejected(reason=reason)
      run(self._orchestrator.update_metric_production_status(req))

    def MarkAsStarted(self):
      req = self._getStatusBase()
      req.started = MetricProductionStatusUpdateStarted()
      run(self._orchestrator.update_metric_production_status(req))

    def MarkAsDelayed(self, error_reason: str, error_message: str):
      req = self._getStatusBase()
      req.delayed = MetricProductionStatusUpdateDelayed(error_reason=error_reason, error_message=error_message)
      run(self._orchestrator.update_metric_production_status(req))

    def MarkAsProduced(self, prod_revision: str):
      req = self._getStatusBase()
      req.produced = MetricProductionStatusUpdateProduced(metric_process_revision=prod_revision)
      run(self._orchestrator.update_metric_production_status(req))

    def MarkAsFinished(self, prod_revision: str):
      req = self._getStatusBase()
      req.finished = MetricProductionStatusUpdateFinished(metric_process_revision=prod_revision)
      run(self._orchestrator.update_metric_production_status(req))
  
    def MarkAsFailed(self, error_reason: str, error_message: str):
      req = self._getStatusBase()
      req.failed = MetricProductionStatusUpdateFailed(error_reason=error_reason, error_message=error_message)
      run(self._orchestrator.update_metric_production_status(req))
  
