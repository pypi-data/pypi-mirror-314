import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Protocol, TypeAlias, TypeVar

from starlette.exceptions import HTTPException

T = TypeVar("T")
Row: TypeAlias = dict[str, Any]


class AsyncCursorProto(Protocol):
    async def fetchone(self) -> Row: ...

    async def fetchall(self) -> list[Row]: ...

    async def __aiter__(self) -> AsyncIterator[Row]:
        yield ...


class AsyncPipelineProto(Protocol):
    async def sync(self) -> None: ...


class AsyncConnectionProto(Protocol):
    @asynccontextmanager
    async def pipeline(self) -> AsyncIterator[AsyncPipelineProto]:
        yield ...

    async def execute(self, query: str, *args, **kwargs) -> AsyncCursorProto: ...


async def fetchone(
    it: AsyncIterator[T],
    *,
    not_found_code: int = 404,
    not_found_detail: str | None = None,
) -> T:
    """Fetch the first row from an async iterator."""
    try:
        return await anext(it)
    except StopAsyncIteration:
        raise HTTPException(
            status_code=not_found_code, detail=not_found_detail
        ) from None


def validate_uuid(uuid_str: str, invalid_uuid_detail: str | None) -> uuid.UUID:
    try:
        return uuid.UUID(uuid_str)
    except ValueError:
        raise HTTPException(status_code=422, detail=invalid_uuid_detail) from None


def next_cron_date(schedule: str, base_time: datetime) -> datetime:
    import croniter

    cron_iter = croniter.croniter(schedule, base_time)
    return cron_iter.get_next(datetime)
