import typing

from uncountable.integration.job import JobArguments, WebhookJob, register_job
from uncountable.types.job_definition_t import JobResult


@register_job
class WebhookExample(WebhookJob):
    @property
    def payload_type(self) -> typing.Any:
        return super().payload_type

    def run(self, args: JobArguments, payload: typing.Any) -> JobResult:
        args.logger.log_info(f"webhook invoked with payload: {payload}")
        return JobResult(success=True)
