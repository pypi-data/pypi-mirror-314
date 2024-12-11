import asyncio
import os
import shutil
from collections.abc import AsyncIterator
from typing import Any, Literal

import httpx
import orjson
import structlog
import uvicorn
from langchain_core.runnables import Runnable
from langchain_core.runnables.config import RunnableConfig
from langchain_core.runnables.graph import Edge, Node
from langchain_core.runnables.graph import Graph as DrawableGraph
from langchain_core.runnables.schema import (
    CustomStreamEvent,
    StandardStreamEvent,
    StreamEvent,
)
from langgraph.checkpoint.serde.base import SerializerProtocol
from langgraph.pregel.types import PregelTask, StateSnapshot
from langgraph.store.base import GetOp, Item, ListNamespacesOp, PutOp, SearchOp
from langgraph.types import Command, Interrupt
from pydantic import BaseModel
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Route

from langgraph_api.js.server_sent_events import aconnect_sse
from langgraph_api.route import ApiResponse
from langgraph_api.serde import json_dumpb
from langgraph_api.utils import AsyncConnectionProto

logger = structlog.stdlib.get_logger(__name__)

GRAPH_SOCKET = "./graph.sock"
CHECKPOINTER_SOCKET = "./checkpointer.sock"
STORE_SOCKET = "./store.sock"


class NoopModel(BaseModel):
    pass


class RemoteException(Exception):
    error: str

    def __init__(self, error: str, *args: object) -> None:
        super().__init__(*args)
        self.error = error

    # Used to nudge the serde to encode like BaseException
    # @see /api/langgraph_api/shared/serde.py:default
    def dict(self):
        return {"error": self.error, "message": str(self)}


# Shim for the Pregel API. Will connect to GRAPH_SOCKET
# UNIX socket to communicate with the JS process.
class RemotePregel(Runnable):
    # TODO: implement name overriding
    name: str = "LangGraph"

    # TODO: implement graph_id overriding
    graph_id: str

    _async_client: httpx.AsyncClient

    @staticmethod
    async def load(graph_id: str):
        model = RemotePregel()

        model.graph_id = graph_id
        model._async_client = httpx.AsyncClient(
            base_url="http://graph",
            timeout=httpx.Timeout(None),
            limits=httpx.Limits(),
            transport=httpx.AsyncHTTPTransport(uds=GRAPH_SOCKET),
        )

        return model

    async def astream_events(
        self,
        input: Any,
        config: RunnableConfig | None = None,
        *,
        version: Literal["v1", "v2"],
        **kwargs: Any,
    ) -> AsyncIterator[StreamEvent]:
        if version != "v2":
            raise ValueError("Only v2 of astream_events is supported")

        data = {
            "command" if isinstance(input, Command) else "input": input,
            "config": config,
            **kwargs,
        }

        async with aconnect_sse(
            self._async_client,
            "POST",
            f"/{self.graph_id}/streamEvents",
            headers={"Content-Type": "application/json"},
            data=orjson.dumps(data),
        ) as event_source:
            async for sse in event_source.aiter_sse():
                event = orjson.loads(sse["data"])
                if sse["event"] == "error":
                    raise RemoteException(event["error"], event["message"])
                elif event["event"] == "on_custom_event":
                    yield CustomStreamEvent(**event)
                else:
                    yield StandardStreamEvent(**event)

    async def fetch_state_schema(self):
        schema = await self._async_client.post(f"/{self.graph_id}/getSchema")
        return orjson.loads(schema.content)

    async def fetch_graph(
        self,
        config: RunnableConfig | None = None,
        *,
        xray: int | bool = False,
    ) -> DrawableGraph:
        response = (
            await self._async_client.post(
                f"/{self.graph_id}/getGraph",
                headers={"Content-Type": "application/json"},
                data=orjson.dumps({"config": config, "xray": xray}),
            )
        ).json()

        nodes: list[Any] = response.pop("nodes")
        edges: list[Any] = response.pop("edges")

        return DrawableGraph(
            {
                data["id"]: Node(
                    data["id"], data["id"], NoopModel(), data.get("metadata")
                )
                for data in nodes
            },
            {
                Edge(
                    data["source"],
                    data["target"],
                    data.get("data"),
                    data.get("conditional", False),
                )
                for data in edges
            },
        )

    async def fetch_subgraphs(
        self, *, namespace: str | None = None, recurse: bool = False
    ) -> dict[str, dict]:
        return (
            await self._async_client.post(
                f"/{self.graph_id}/getSubgraphs",
                headers={"Content-Type": "application/json"},
                data=orjson.dumps({"namespace": namespace, "recurse": recurse}),
            )
        ).json()

    def _convert_state_snapshot(self, item: dict) -> StateSnapshot:
        def _convert_tasks(tasks: list[dict]) -> tuple[PregelTask, ...]:
            result: list[PregelTask] = []
            for task in tasks:
                state = task.get("state")

                if state and isinstance(state, dict) and "config" in state:
                    state = self._convert_state_snapshot(state)

                result.append(
                    PregelTask(
                        task["id"],
                        task["name"],
                        tuple(task["path"]) if task.get("path") else tuple(),
                        # TODO: figure out how to properly deserialise errors
                        task.get("error"),
                        (
                            tuple(
                                Interrupt(
                                    value=interrupt["value"],
                                    when=interrupt["when"],
                                    resumable=interrupt.get("resumable", True),
                                    ns=interrupt.get("ns"),
                                )
                                for interrupt in task.get("interrupts")
                            )
                            if task.get("interrupts")
                            else []
                        ),
                        state,
                    )
                )
            return tuple(result)

        return StateSnapshot(
            item.get("values"),
            item.get("next"),
            item.get("config"),
            item.get("metadata"),
            item.get("createdAt"),
            item.get("parentConfig"),
            _convert_tasks(item.get("tasks", [])),
        )

    async def aget_state(
        self, config: RunnableConfig, *, subgraphs: bool = False
    ) -> StateSnapshot:
        response = await self._async_client.post(
            f"/{self.graph_id}/getState",
            headers={"Content-Type": "application/json"},
            data=orjson.dumps({"config": config, "subgraphs": subgraphs}),
        )
        return self._convert_state_snapshot(response.json())

    async def aupdate_state(
        self,
        config: RunnableConfig,
        values: dict[str, Any] | Any,
        as_node: str | None = None,
    ) -> RunnableConfig:
        response = await self._async_client.post(
            f"/{self.graph_id}/updateState",
            headers={"Content-Type": "application/json"},
            data=orjson.dumps({"config": config, "values": values, "as_node": as_node}),
        )
        return RunnableConfig(**response.json())

    async def aget_state_history(
        self,
        config: RunnableConfig,
        *,
        filter: dict[str, Any] | None = None,
        before: RunnableConfig | None = None,
        limit: int | None = None,
    ) -> AsyncIterator[StateSnapshot]:
        async with aconnect_sse(
            self._async_client,
            "POST",
            f"/{self.graph_id}/getStateHistory",
            headers={"Content-Type": "application/json"},
            data=orjson.dumps(
                {"config": config, "limit": limit, "filter": filter, "before": before}
            ),
        ) as event_source:
            async for sse in event_source.aiter_sse():
                yield self._convert_state_snapshot(orjson.loads(sse["data"]))

    def get_graph(
        self,
        config: RunnableConfig | None = None,
        *,
        xray: int | bool = False,
    ) -> dict[str, Any]:
        raise Exception("Not implemented")

    def get_input_schema(self, config: RunnableConfig | None = None) -> type[BaseModel]:
        raise Exception("Not implemented")

    def get_output_schema(
        self, config: RunnableConfig | None = None
    ) -> type[BaseModel]:
        raise Exception("Not implemented")

    def config_schema(self) -> type[BaseModel]:
        raise Exception("Not implemented")

    async def invoke(self, input: Any, config: RunnableConfig | None = None):
        raise Exception("Not implemented")


async def run_js_process(paths_str: str, watch: bool = False):
    # check if tsx is available
    tsx_path = shutil.which("tsx")
    if tsx_path is None:
        raise FileNotFoundError("tsx not found in PATH")
    attempt = 0
    while True:
        client_file = os.path.join(os.path.dirname(__file__), "client.mts")
        args = ("tsx", client_file)
        if watch:
            args = ("tsx", "watch", client_file, "--skip-schema-cache")
        try:
            process = await asyncio.create_subprocess_exec(
                *args,
                env={
                    "LANGSERVE_GRAPHS": paths_str,
                    "LANGCHAIN_CALLBACKS_BACKGROUND": "true",
                    "CHOKIDAR_USEPOLLING": "true",
                    **os.environ,
                },
            )
            code = await process.wait()
            raise Exception(f"JS process exited with code {code}")
        except asyncio.CancelledError:
            logger.info("Terminating JS graphs process")
            try:
                process.terminate()
                await process.wait()
            except (UnboundLocalError, ProcessLookupError):
                pass
            raise
        except Exception:
            if attempt >= 3:
                raise
            else:
                logger.warning(f"Retrying JS process {3 - attempt} more times...")
                attempt += 1


def _get_passthrough_checkpointer(conn: AsyncConnectionProto):
    from langgraph_storage.checkpoint import Checkpointer

    class PassthroughSerialiser(SerializerProtocol):
        def dumps(self, obj: Any) -> bytes:
            return json_dumpb(obj)

        def dumps_typed(self, obj: Any) -> tuple[str, bytes]:
            return "json", json_dumpb(obj)

        def loads(self, data: bytes) -> Any:
            return orjson.loads(data)

        def loads_typed(self, data: tuple[str, bytes]) -> Any:
            type, payload = data
            if type != "json":
                raise ValueError(f"Unsupported type {type}")
            return orjson.loads(payload)

    checkpointer = Checkpointer(conn)

    # This checkpointer does not attempt to revive LC-objects.
    # Instead, it will pass through the JSON values as-is.
    checkpointer.serde = PassthroughSerialiser()

    return checkpointer


# Setup a HTTP server on top of CHECKPOINTER_SOCKET unix socket
# used by `client.mts` to communicate with the Python checkpointer
async def run_remote_checkpointer():
    from langgraph_storage.database import connect

    # Search checkpoints
    async def list(request: Request):
        payload = orjson.loads(await request.body())
        result = []
        async with connect() as conn:
            checkpointer = _get_passthrough_checkpointer(conn)
            async for item in checkpointer.alist(
                config=payload.get("config"),
                limit=payload.get("limit"),
                before=payload.get("before"),
                filter=payload.get("filter"),
            ):
                result.append(item)

        return ApiResponse(result)

    # Put the new checkpoint metadata
    async def put(request: Request):
        payload = orjson.loads(await request.body())
        async with connect() as conn:
            checkpointer = _get_passthrough_checkpointer(conn)
            result = await checkpointer.aput(
                payload["config"],
                payload["checkpoint"],
                payload["metadata"],
                payload.get("new_versions", {}),
            )
        return ApiResponse(result)

    # Get actual checkpoint values (reads)
    async def get_tuple(request: Request):
        payload = orjson.loads(await request.body())

        async with connect() as conn:
            checkpointer = _get_passthrough_checkpointer(conn)
            result = await checkpointer.aget_tuple(config=payload["config"])
        return ApiResponse(result)

    # Put actual checkpoint values (writes)
    async def put_writes(request: Request):
        payload = orjson.loads(await request.body())

        async with connect() as conn:
            checkpointer = _get_passthrough_checkpointer(conn)
            result = await checkpointer.aput_writes(
                payload["config"],
                payload["writes"],
                payload["taskId"],
            )

        return ApiResponse(result)

    remote = Starlette(
        routes=[
            Route("/get_tuple", get_tuple, methods=["POST"]),
            Route("/list", list, methods=["POST"]),
            Route("/put", put, methods=["POST"]),
            Route("/put_writes", put_writes, methods=["POST"]),
            Route("/ok", lambda _: ApiResponse({"ok": True}), methods=["GET"]),
        ]
    )

    server = uvicorn.Server(
        uvicorn.Config(
            remote,
            uds=CHECKPOINTER_SOCKET,
            # We need to _explicitly_ set these values in order
            # to avoid reinitialising the logger, which removes
            # the structlog logger setup before.
            # See: https://github.com/encode/uvicorn/blob/8f4c8a7f34914c16650ebd026127b96560425fde/uvicorn/config.py#L357-L393
            log_config=None,
            log_level=None,
            access_log=True,
        )
    )
    await server.serve()


def _get_passthrough_store():
    from langgraph_storage.store import Store

    return Store()


async def run_remote_store():
    async def abatch(request: Request):
        payload = orjson.loads(await request.body())
        operations = payload.get("operations", [])

        if not operations:
            return ApiResponse({"error": "No operations provided"}, status_code=400)

        # Convert raw operations to proper objects
        processed_operations = []
        for op in operations:
            if "value" in op:
                processed_operations.append(
                    PutOp(
                        namespace=tuple(op["namespace"]),
                        key=op["key"],
                        value=op["value"],
                    )
                )
            elif "namespace_prefix" in op:
                processed_operations.append(
                    SearchOp(
                        namespace_prefix=tuple(op["namespace_prefix"]),
                        filter=op.get("filter"),
                        limit=op.get("limit", 10),
                        offset=op.get("offset", 0),
                    )
                )

            elif "namespace" in op and "key" in op:
                processed_operations.append(
                    GetOp(namespace=tuple(op["namespace"]), key=op["key"])
                )
            elif "match_conditions" in op:
                processed_operations.append(
                    ListNamespacesOp(
                        match_conditions=tuple(op["match_conditions"]),
                        max_depth=op.get("max_depth"),
                        limit=op.get("limit", 100),
                        offset=op.get("offset", 0),
                    )
                )
            else:
                return ApiResponse(
                    {"error": f"Unknown operation type: {op}"}, status_code=400
                )

        store = _get_passthrough_store()
        results = await store.abatch(processed_operations)

        # Handle potentially undefined or non-dict results
        processed_results = []
        # Result is of type: Union[Item, list[Item], list[tuple[str, ...]], None]
        for result in results:
            if isinstance(result, Item):
                processed_results.append(result.dict())
            elif isinstance(result, dict):
                processed_results.append(result)
            elif isinstance(result, list):
                coerced = []
                for res in result:
                    if isinstance(res, Item):
                        coerced.append(res.dict())
                    elif isinstance(res, tuple):
                        coerced.append(list(res))
                    elif res is None:
                        coerced.append(res)
                    else:
                        coerced.append(str(res))
                processed_results.append(coerced)
            elif result is None:
                processed_results.append(None)
            else:
                processed_results.append(str(result))
        return ApiResponse(processed_results)

    # List all stores
    async def aget(request: Request):
        namespaces_str = request.query_params.get("namespaces")
        key = request.query_params.get("key")

        if not namespaces_str or not key:
            return ApiResponse(
                {"error": "Both namespaces and key are required"}, status_code=400
            )

        namespaces = namespaces_str.split(".")

        store = _get_passthrough_store()
        result = await store.aget(namespaces, key)

        return ApiResponse(result)

    # Put the new store data
    async def aput(request: Request):
        payload = orjson.loads(await request.body())
        namespace = tuple(payload["namespace"].split("."))
        key = payload["key"]
        value = payload["value"]
        index = payload.get("index")

        store = _get_passthrough_store()
        await store.aput(namespace, key, value, index=index)

        return ApiResponse({"success": True})

    # Search stores
    async def asearch(request: Request):
        payload = orjson.loads(await request.body())
        namespace_prefix = tuple(payload["namespace_prefix"])
        filter = payload.get("filter")
        limit = payload.get("limit", 10)
        offset = payload.get("offset", 0)
        query = payload.get("query")

        store = _get_passthrough_store()
        result = await store.asearch(
            namespace_prefix, filter=filter, limit=limit, offset=offset, query=query
        )

        return ApiResponse([item.dict() for item in result])

    # Delete store data
    async def adelete(request: Request):
        payload = orjson.loads(await request.body())
        namespace = tuple(payload["namespace"])
        key = payload["key"]

        store = _get_passthrough_store()
        await store.adelete(namespace, key)

        return ApiResponse({"success": True})

    # List all namespaces
    async def alist_namespaces(request: Request):
        payload = orjson.loads(await request.body())
        prefix = tuple(payload.get("prefix", [])) or None
        suffix = tuple(payload.get("suffix", [])) or None
        max_depth = payload.get("max_depth")
        limit = payload.get("limit", 100)
        offset = payload.get("offset", 0)

        store = _get_passthrough_store()
        result = await store.alist_namespaces(
            prefix=prefix,
            suffix=suffix,
            max_depth=max_depth,
            limit=limit,
            offset=offset,
        )

        return ApiResponse([list(ns) for ns in result])

    remote = Starlette(
        routes=[
            Route("/items", aget, methods=["GET"]),
            Route("/items", aput, methods=["PUT"]),
            Route("/items", adelete, methods=["DELETE"]),
            Route("/items/search", asearch, methods=["POST"]),
            Route("/list/namespaces", alist_namespaces, methods=["POST"]),
            Route("/items/batch", abatch, methods=["POST"]),
            Route("/ok", lambda _: ApiResponse({"ok": True}), methods=["GET"]),
        ]
    )
    server = uvicorn.Server(
        uvicorn.Config(
            remote,
            uds=STORE_SOCKET,
            # We need to _explicitly_ set these values in order
            # to avoid reinitialising the logger, which removes
            # the structlog logger setup before.
            # See: https://github.com/encode/uvicorn/blob/8f4c8a7f34914c16650ebd026127b96560425fde/uvicorn/config.py#L357-L393
            log_config=None,
            log_level=None,
            access_log=True,
        )
    )
    await server.serve()


async def wait_until_js_ready():
    async with (
        httpx.AsyncClient(
            base_url="http://graph",
            transport=httpx.AsyncHTTPTransport(uds=GRAPH_SOCKET),
            limits=httpx.Limits(),
        ) as graph_client,
        httpx.AsyncClient(
            base_url="http://checkpointer",
            transport=httpx.AsyncHTTPTransport(uds=CHECKPOINTER_SOCKET),
            limits=httpx.Limits(),
        ) as checkpointer_client,
        httpx.AsyncClient(
            base_url="http://store",
            transport=httpx.AsyncHTTPTransport(uds=STORE_SOCKET),
            limits=httpx.Limits(),
        ) as store_client,
    ):
        attempt = 0
        while True:
            try:
                res = await graph_client.get("/ok")
                res.raise_for_status()
                res = await checkpointer_client.get("/ok")
                res.raise_for_status()
                res = await store_client.get("/ok")
                res.raise_for_status()
                return
            except httpx.HTTPError:
                if attempt > 240:
                    raise
                else:
                    attempt += 1
                    await asyncio.sleep(0.5)


async def js_healthcheck():
    async with (
        httpx.AsyncClient(
            base_url="http://graph",
            transport=httpx.AsyncHTTPTransport(uds=GRAPH_SOCKET),
            limits=httpx.Limits(),
        ) as graph_client,
        httpx.AsyncClient(
            base_url="http://checkpointer",
            transport=httpx.AsyncHTTPTransport(uds=CHECKPOINTER_SOCKET),
            limits=httpx.Limits(),
        ) as checkpointer_client,
        httpx.AsyncClient(
            base_url="http://store",
            transport=httpx.AsyncHTTPTransport(uds=STORE_SOCKET),
            limits=httpx.Limits(),
        ) as store_client,
    ):
        try:
            res = await graph_client.get("/ok")
            res.raise_for_status()
            res = await checkpointer_client.get("/ok")
            res.raise_for_status()
            res = await store_client.get("/ok")
            res.raise_for_status()
            return True
        except httpx.HTTPError:
            return False
