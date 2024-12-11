import asyncio
from contextlib import AsyncExitStack
from datetime import UTC, datetime
from random import random
from typing import cast

import structlog
from langgraph.pregel.debug import CheckpointPayload, TaskResultPayload

from langgraph_api.config import BG_JOB_NO_DELAY, STATS_INTERVAL_SECS
from langgraph_api.errors import (
    UserInterrupt,
    UserRollback,
)
from langgraph_api.http import get_http_client
from langgraph_api.js.remote import RemoteException
from langgraph_api.metadata import incr_runs
from langgraph_api.schema import Run
from langgraph_api.stream import (
    astream_state,
    consume,
)
from langgraph_api.utils import AsyncConnectionProto
from langgraph_storage.database import connect
from langgraph_storage.ops import Runs, Threads
from langgraph_storage.retry import RETRIABLE_EXCEPTIONS

logger = structlog.stdlib.get_logger(__name__)

WORKERS: set[asyncio.Task] = set()
MAX_RETRY_ATTEMPTS = 3
SHUTDOWN_GRACE_PERIOD_SECS = 5


def ms(after: datetime, before: datetime) -> int:
    return int((after - before).total_seconds() * 1000)


async def queue(concurrency: int, timeout: float):
    loop = asyncio.get_running_loop()
    last_stats_secs: int | None = None
    semaphore = asyncio.Semaphore(concurrency)

    def cleanup(task: asyncio.Task):
        WORKERS.remove(task)
        semaphore.release()
        try:
            if exc := task.exception():
                logger.exception("Background worker failed", exc_info=exc)
        except asyncio.CancelledError:
            pass

    await logger.ainfo(f"Starting {concurrency} background workers")
    try:
        while True:
            try:
                if calc_stats := (
                    last_stats_secs is None
                    or loop.time() - last_stats_secs > STATS_INTERVAL_SECS
                ):
                    last_stats_secs = loop.time()
                    active = len(WORKERS)
                    await logger.ainfo(
                        "Worker stats",
                        max=concurrency,
                        available=concurrency - active,
                        active=active,
                    )
                await semaphore.acquire()
                exit = AsyncExitStack()
                conn = await exit.enter_async_context(connect())
                if calc_stats:
                    stats = await Runs.stats(conn)
                    await logger.ainfo("Queue stats", **stats)
                if tup := await exit.enter_async_context(Runs.next(conn)):
                    task = asyncio.create_task(
                        worker(timeout, exit, conn, *tup),
                        name=f"run-{tup[0]['run_id']}-attempt-{tup[1]}",
                    )
                    task.add_done_callback(cleanup)
                    WORKERS.add(task)
                else:
                    semaphore.release()
                    await exit.aclose()
                    await asyncio.sleep(0 if BG_JOB_NO_DELAY else random())
            except Exception as exc:
                # keep trying to run the scheduler indefinitely
                logger.exception("Background worker scheduler failed", exc_info=exc)
                semaphore.release()
                await exit.aclose()
                await asyncio.sleep(0 if BG_JOB_NO_DELAY else random())
    finally:
        logger.info("Shutting down background workers")
        for task in WORKERS:
            task.cancel()
        await asyncio.wait_for(
            asyncio.gather(*WORKERS, return_exceptions=True), SHUTDOWN_GRACE_PERIOD_SECS
        )


async def worker(
    timeout: float,
    exit: AsyncExitStack,
    conn: AsyncConnectionProto,
    run: Run,
    attempt: int,
):
    run_id = run["run_id"]
    if attempt == 1:
        incr_runs()
    async with Runs.enter(run_id) as done, exit:
        temporary = run["kwargs"].get("temporary", False)
        webhook = run["kwargs"].pop("webhook", None)
        checkpoint: CheckpointPayload | None = None
        exception: Exception | None = None
        status: str | None = None
        run_started_at = datetime.now(UTC)
        run_created_at = run["created_at"].isoformat()
        await logger.ainfo(
            "Starting background run",
            run_id=str(run_id),
            run_attempt=attempt,
            run_created_at=run_created_at,
            run_started_at=run_started_at.isoformat(),
            run_queue_ms=ms(run_started_at, run["created_at"]),
        )

        def on_checkpoint(checkpoint_arg: CheckpointPayload):
            nonlocal checkpoint
            checkpoint = checkpoint_arg

        def on_task_result(task_result: TaskResultPayload):
            if checkpoint is not None:
                for task in checkpoint["tasks"]:
                    if task["id"] == task_result["id"]:
                        task.update(task_result)
                        break

        try:
            if attempt > MAX_RETRY_ATTEMPTS:
                raise RuntimeError(f"Run {run['run_id']} exceeded max attempts")
            if temporary:
                stream = astream_state(
                    AsyncExitStack(), conn, cast(Run, run), attempt, done
                )
            else:
                stream = astream_state(
                    AsyncExitStack(),
                    conn,
                    cast(Run, run),
                    attempt,
                    done,
                    on_checkpoint=on_checkpoint,
                    on_task_result=on_task_result,
                )
            await asyncio.wait_for(consume(stream, run_id), timeout)
            await logger.ainfo(
                "Background run succeeded",
                run_id=str(run_id),
                run_attempt=attempt,
                run_created_at=run_created_at,
                run_started_at=run_started_at.isoformat(),
                run_ended_at=datetime.now().isoformat(),
                run_exec_ms=ms(datetime.now(UTC), run_started_at),
            )
            status = "success"
            await Runs.set_status(conn, run_id, "success")
        except TimeoutError as e:
            exception = e
            status = "timeout"
            await logger.awarning(
                "Background run timed out",
                run_id=str(run_id),
                run_attempt=attempt,
                run_created_at=run_created_at,
                run_started_at=run_started_at.isoformat(),
                run_ended_at=datetime.now().isoformat(),
                run_exec_ms=ms(datetime.now(UTC), run_started_at),
            )
            await Runs.set_status(conn, run_id, "timeout")
        except UserRollback as e:
            exception = e
            status = "rollback"
            await logger.ainfo(
                "Background run rolled back",
                run_id=str(run_id),
                run_attempt=attempt,
                run_created_at=run_created_at,
                run_started_at=run_started_at.isoformat(),
                run_ended_at=datetime.now().isoformat(),
                run_exec_ms=ms(datetime.now(UTC), run_started_at),
            )
            await Runs.delete(conn, run_id, thread_id=run["thread_id"])
        except UserInterrupt as e:
            exception = e
            status = "interrupted"
            await logger.ainfo(
                "Background run interrupted",
                run_id=str(run_id),
                run_attempt=attempt,
                run_created_at=run_created_at,
                run_started_at=run_started_at.isoformat(),
                run_ended_at=datetime.now().isoformat(),
                run_exec_ms=ms(datetime.now(UTC), run_started_at),
            )
            await Runs.set_status(conn, run_id, "interrupted")
        except RETRIABLE_EXCEPTIONS as e:
            exception = e
            status = "retry"
            await logger.awarning(
                "Background run failed, will retry",
                exc_info=True,
                run_id=str(run_id),
                run_attempt=attempt,
                run_created_at=run_created_at,
                run_started_at=run_started_at.isoformat(),
                run_ended_at=datetime.now().isoformat(),
                run_exec_ms=ms(datetime.now(UTC), run_started_at),
            )
            raise
            # Note we re-raise here, thus marking the run
            # as available to be picked up by another worker
        except Exception as exc:
            exception = exc
            status = "error"
            await logger.aexception(
                "Background run failed",
                exc_info=not isinstance(exc, RemoteException),
                run_id=str(run_id),
                run_attempt=attempt,
                run_created_at=run_created_at,
                run_started_at=run_started_at.isoformat(),
                run_ended_at=datetime.now().isoformat(),
                run_exec_ms=ms(datetime.now(UTC), run_started_at),
            )
            await Runs.set_status(conn, run_id, "error")
        # delete or set status of thread
        if temporary:
            await Threads.delete(conn, run["thread_id"])
        else:
            await Threads.set_status(conn, run["thread_id"], checkpoint, exception)
        if webhook:
            # TODO add error, values to webhook payload
            # TODO add retries for webhook calls
            try:
                await get_http_client().post(
                    webhook, json={**run, "status": status}, total_timeout=5
                )
            except Exception as e:
                logger.warning("Failed to send webhook", exc_info=e)
        # Note we don't handle asyncio.CancelledError here, as we want to
        # let it bubble up and rollback db transaction, thus marking the run
        # as available to be picked up by another worker
