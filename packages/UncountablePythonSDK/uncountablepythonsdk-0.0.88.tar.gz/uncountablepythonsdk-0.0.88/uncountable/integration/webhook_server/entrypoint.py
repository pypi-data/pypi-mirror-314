import hmac
import typing
from dataclasses import dataclass

import flask
import simplejson
from flask.typing import ResponseReturnValue
from flask.wrappers import Response
from opentelemetry.trace import get_current_span
from uncountable.core.environment import (
    get_local_admin_server_port,
    get_server_env,
    get_webhook_server_port,
)
from uncountable.integration.queue_runner.command_server.command_client import (
    send_job_queue_message,
)
from uncountable.integration.queue_runner.command_server.types import (
    CommandServerException,
)
from uncountable.integration.scan_profiles import load_profiles
from uncountable.integration.secret_retrieval.retrieve_secret import retrieve_secret
from uncountable.integration.telemetry import Logger
from uncountable.types import base_t, job_definition_t, queued_job_t, webhook_job_t

from pkgs.argument_parser import CachedParser

app = flask.Flask(__name__)


@dataclass(kw_only=True)
class WebhookResponse:
    pass


webhook_payload_parser = CachedParser(webhook_job_t.WebhookEventBody)


class WebhookException(BaseException):
    error_code: int
    message: str

    def __init__(self, *, error_code: int, message: str) -> None:
        self.error_code = error_code
        self.message = message

    @staticmethod
    def payload_failed_signature() -> "WebhookException":
        return WebhookException(
            error_code=401, message="webhook payload did not match signature"
        )

    @staticmethod
    def no_signature_passed() -> "WebhookException":
        return WebhookException(error_code=400, message="missing signature")

    @staticmethod
    def body_parse_error() -> "WebhookException":
        return WebhookException(error_code=400, message="body parse error")

    @staticmethod
    def unknown_error() -> "WebhookException":
        return WebhookException(error_code=500, message="internal server error")

    def __str__(self) -> str:
        return f"[{self.error_code}]: {self.message}"

    def make_error_response(self) -> Response:
        return Response(
            status=self.error_code, response={"error": {"message": str(self)}}
        )


def _parse_webhook_payload(
    *, raw_request_body: bytes, signature_key: str, passed_signature: str
) -> base_t.JsonValue:
    request_body_signature = hmac.new(
        signature_key.encode("utf-8"), msg=raw_request_body, digestmod="sha256"
    ).hexdigest()

    if request_body_signature != passed_signature:
        raise WebhookException.payload_failed_signature()

    try:
        request_body = simplejson.loads(raw_request_body.decode())
        return typing.cast(base_t.JsonValue, request_body)
    except (simplejson.JSONDecodeError, ValueError) as e:
        raise WebhookException.body_parse_error() from e


def register_route(
    *,
    server_logger: Logger,
    profile_meta: job_definition_t.ProfileMetadata,
    job: job_definition_t.WebhookJobDefinition,
) -> None:
    route = f"/{profile_meta.name}/{job.id}"

    def handle_webhook() -> ResponseReturnValue:
        with server_logger.push_scope(route):
            try:
                signature_key = retrieve_secret(
                    profile_metadata=profile_meta,
                    secret_retrieval=job.signature_key_secret,
                )

                passed_signature = flask.request.headers.get(
                    "Uncountable-Webhook-Signature"
                )
                if passed_signature is None:
                    raise WebhookException.no_signature_passed()

                webhook_payload = _parse_webhook_payload(
                    raw_request_body=flask.request.data,
                    signature_key=signature_key,
                    passed_signature=passed_signature,
                )

                try:
                    send_job_queue_message(
                        job_ref_name=job.id,
                        payload=queued_job_t.QueuedJobPayload(
                            invocation_context=queued_job_t.InvocationContextWebhook(
                                webhook_payload=webhook_payload
                            )
                        ),
                        port=get_local_admin_server_port(),
                    )
                except CommandServerException as e:
                    raise WebhookException.unknown_error() from e

                return flask.jsonify(WebhookResponse())
            except WebhookException as e:
                server_logger.log_exception(e)
                return e.make_error_response()
            except Exception as e:
                server_logger.log_exception(e)
                return WebhookException.unknown_error().make_error_response()

    app.add_url_rule(
        route,
        endpoint=f"handle_webhook_{job.id}",
        view_func=handle_webhook,
        methods=["POST"],
    )

    server_logger.log_info(f"job {job.id} webhook registered at: {route}")


def main() -> None:
    profiles = load_profiles()
    for profile_metadata in profiles:
        server_logger = Logger(get_current_span())
        for job in profile_metadata.jobs:
            if isinstance(job, job_definition_t.WebhookJobDefinition):
                register_route(
                    server_logger=server_logger, profile_meta=profile_metadata, job=job
                )


main()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=get_webhook_server_port(),
        debug=get_server_env() == "playground",
        exclude_patterns=[],
    )
