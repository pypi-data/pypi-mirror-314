from functools import lru_cache

import orjson

from langgraph_api.config import LANGGRAPH_AUTH_TYPE
from langgraph_api.graph import GRAPHS
from langgraph_api.validation import openapi


@lru_cache(maxsize=1)
def get_openapi_spec() -> str:
    # patch the graph_id enums
    graph_ids = list(GRAPHS.keys())
    for schema in (
        "Assistant",
        "AssistantCreate",
        "AssistantPatch",
        "GraphSchema",
        "AssistantSearchRequest",
    ):
        openapi["components"]["schemas"][schema]["properties"]["graph_id"]["enum"] = (
            graph_ids
        )
    # patch the auth schemes
    if LANGGRAPH_AUTH_TYPE == "langsmith":
        openapi["security"] = [
            {"x-api-key": []},
        ]
        openapi["components"]["securitySchemes"] = {
            "x-api-key": {"type": "apiKey", "in": "header", "name": "x-api-key"}
        }
    return orjson.dumps(openapi)
