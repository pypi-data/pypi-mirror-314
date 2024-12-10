import time
from unacatlib.unacast.v2.byo_external import MetricValuesOnPois, ReportDetails, ReportStatus

class ReportJob(object):
	def __init__(self, client, report_details: ReportDetails) -> None:
		self.client = client
		self.id: str = report_details.report_id
		self.metric_ids: list[str] = list(map(
			lambda metric_ref: metric_ref.metric_id, report_details.metric_reference
		))

		self.status: int = report_details.report_status

	def refresh(self):
		# If the report job has completed, with either failed for success just return.
		if self.is_complete:
			return self.status

		resp: MetricValuesOnPois = self.client.read_us_report(
			report_id=self.id, metric_id=self.metric_ids[0]
		)

		self.status = resp.report_status
		return self.status

	@property
	def is_complete(self):
		return self.status in [ReportStatus.Succeeded.value, ReportStatus.Failed.value]

	@property
	def is_success(self):
		return self.status == ReportStatus.Succeeded.value

	def wait_for_completion(self, timeout=10):
        # Waits for the job to complete
		while not self.is_complete:
			self.refresh()
			time.sleep(timeout)
