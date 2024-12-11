import asyncio

from uncountable.integration.queue_runner.command_server import serve
from uncountable.integration.queue_runner.command_server.types import CommandQueue
from uncountable.integration.queue_runner.job_scheduler import start_scheduler


async def queue_runner_loop() -> None:
    command_queue: CommandQueue = asyncio.Queue()

    command_server = asyncio.create_task(serve(command_queue))

    scheduler = asyncio.create_task(start_scheduler(command_queue))

    await scheduler
    await command_server


def start_queue_runner() -> None:
    loop = asyncio.new_event_loop()
    loop.run_until_complete(queue_runner_loop())
    loop.close()


if __name__ == "__main__":
    start_queue_runner()
