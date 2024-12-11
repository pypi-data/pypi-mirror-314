import argparse

from opentelemetry.trace import get_current_span

from uncountable.core.environment import get_local_admin_server_port
from uncountable.integration.queue_runner.command_server.command_client import (
    send_job_queue_message,
)
from uncountable.integration.telemetry import Logger
from uncountable.types import queued_job_t


def main() -> None:
    logger = Logger(get_current_span())

    parser = argparse.ArgumentParser(
        description="Process a job with a given command and job ID."
    )

    parser.add_argument(
        "command",
        type=str,
        choices=["run"],
        help="The command to execute (e.g., 'run')",
    )

    parser.add_argument("job_id", type=str, help="The ID of the job to process")

    parser.add_argument(
        "--host", type=str, default="localhost", nargs="?", help="The host to run on"
    )

    args = parser.parse_args()

    with logger.push_scope(args.command):
        if args.command == "run":
            send_job_queue_message(
                job_ref_name=args.job_id,
                payload=queued_job_t.QueuedJobPayload(
                    invocation_context=queued_job_t.InvocationContextManual()
                ),
                host=args.host,
                port=get_local_admin_server_port(),
            )
        else:
            parser.print_usage()


main()
