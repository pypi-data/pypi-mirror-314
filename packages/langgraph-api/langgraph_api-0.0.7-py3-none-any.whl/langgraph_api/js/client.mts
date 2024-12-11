import { z } from "zod";
import { Hono } from "hono";
import { serve } from "@hono/node-server";
import { zValidator } from "@hono/zod-validator";
import { streamSSE } from "hono/streaming";
import { HTTPException } from "hono/http-exception";
import pRetry from "p-retry";
import {
  BaseStore,
  Item,
  Operation,
  Command,
  OperationResults,
  type Checkpoint,
  type CheckpointMetadata,
  type CheckpointTuple,
  type CompiledGraph,
} from "@langchain/langgraph";
import {
  BaseCheckpointSaver,
  type ChannelVersions,
  type ChannelProtocol,
} from "@langchain/langgraph-checkpoint";
import { createHash } from "node:crypto";
import * as fs from "node:fs/promises";
import * as path from "node:path";
import { serialiseAsDict } from "./src/utils/serde.mjs";
import * as importMap from "./src/utils/importMap.mjs";

import { createLogger, format, transports } from "winston";
import { Agent, fetch } from "undici";

import { load } from "@langchain/core/load";
import { BaseMessageChunk, isBaseMessage } from "@langchain/core/messages";
import type { PyItem, PyResult } from "./src/utils/pythonSchemas.mts";
import type { RunnableConfig } from "@langchain/core/runnables";
import {
  runGraphSchemaWorker,
  GraphSchema,
  resolveGraph,
  GraphSpec,
} from "./src/graph.mts";

const logger = createLogger({
  level: "debug",
  format: format.combine(
    format.errors({ stack: true }),
    format.timestamp(),
    format.json(),
    format.printf((info) => {
      const { timestamp, level, message, ...rest } = info;

      let event;
      if (typeof message === "string") {
        event = message;
      } else {
        event = JSON.stringify(message);
      }

      if (rest.stack) {
        rest.message = event;
        event = rest.stack;
      }

      return JSON.stringify({ timestamp, level, event, ...rest });
    })
  ),
  transports: [
    new transports.Console({
      handleExceptions: true,
      handleRejections: true,
    }),
  ],
});

let GRAPH_SCHEMA: Record<string, Record<string, GraphSchema>> = {};
const GRAPH_RESOLVED: Record<string, CompiledGraph<string>> = {};
const GRAPH_SPEC: Record<string, GraphSpec> = {};

function getGraph(graphId: string) {
  if (!GRAPH_RESOLVED[graphId])
    throw new HTTPException(404, { message: `Graph "${graphId}" not found` });
  return GRAPH_RESOLVED[graphId];
}

async function getOrExtractSchema(graphId: string) {
  if (!(graphId in GRAPH_SPEC)) {
    throw new Error(`Spec for ${graphId} not found`);
  }

  if (!GRAPH_SCHEMA[graphId]) {
    try {
      const timer = logger.startTimer();
      GRAPH_SCHEMA[graphId] = await runGraphSchemaWorker(GRAPH_SPEC[graphId]);
      timer.done({ message: `Extracting schema for ${graphId} finished` });
    } catch (error) {
      throw new Error(`Failed to extract schema for "${graphId}": ${error}`);
    }
  }

  return GRAPH_SCHEMA[graphId];
}

const GRAPH_SOCKET = "./graph.sock";
const CHECKPOINTER_SOCKET = "./checkpointer.sock";
const STORE_SOCKET = "./store.sock";

const checkpointerDispatcher = new Agent({
  connect: { socketPath: CHECKPOINTER_SOCKET },
});
const storeDispatcher = new Agent({ connect: { socketPath: STORE_SOCKET } });

const RunnableConfigSchema = z.object({
  tags: z.array(z.string()).optional(),
  metadata: z.record(z.unknown()).optional(),
  run_name: z.string().optional(),
  max_concurrency: z.number().optional(),
  recursion_limit: z.number().optional(),
  configurable: z.record(z.unknown()).optional(),
  run_id: z.string().uuid().optional(),
});

const getRunnableConfig = (
  userConfig: z.infer<typeof RunnableConfigSchema> | null | undefined
) => {
  if (!userConfig) return {};
  return {
    configurable: userConfig.configurable,
    tags: userConfig.tags,
    metadata: userConfig.metadata,
    runName: userConfig.run_name,
    maxConcurrency: userConfig.max_concurrency,
    recursionLimit: userConfig.recursion_limit,
    runId: userConfig.run_id,
  };
};

function tryFetch(...args: Parameters<typeof fetch>) {
  return pRetry(
    async () => {
      const response = await fetch(...args).catch((error) => {
        throw new Error(`${args[0]} connecfailed: ${error}`);
      });

      if (!response.ok) {
        let errorMessage = `${args[0]} failed: HTTP ${response.status}`;
        try {
          errorMessage += `: ${await response.text()}`;
        } catch {}
        throw new Error(errorMessage);
      }

      return response;
    },
    {
      retries: 3,
      factor: 2,
      minTimeout: 1000,
      onFailedAttempt: (error) => void logger.error(error),
    }
  );
}

class RemoteCheckpointer extends BaseCheckpointSaver<number | string> {
  async getTuple(config: RunnableConfig): Promise<CheckpointTuple | undefined> {
    const res = await tryFetch("http://checkpointer/get_tuple", {
      dispatcher: checkpointerDispatcher,
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ config }),
    });

    const text = await res.text();
    const result = (await load(text, {
      importMap,
      optionalImportEntrypoints: [],
      optionalImportsMap: {},
      secretsMap: {},
    })) as any;

    if (!result) return undefined;
    return {
      checkpoint: result.checkpoint,
      config: result.config,
      metadata: result.metadata,
      parentConfig: result.parent_config,
      pendingWrites: result.pending_writes,
    };
  }
  async *list(
    config: RunnableConfig,
    options?: {
      limit?: number;
      before?: RunnableConfig;
      filter?: Record<string, any>;
    }
  ): AsyncGenerator<CheckpointTuple> {
    const res = await tryFetch("http://checkpointer/list", {
      dispatcher: checkpointerDispatcher,
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ config, ...options }),
    });

    const text = await res.text();
    const result = (await load(text, {
      importMap,
      optionalImportEntrypoints: [],
      optionalImportsMap: {},
      secretsMap: {},
    })) as any;

    for (const item of result) {
      yield {
        checkpoint: item.checkpoint,
        config: item.config,
        metadata: item.metadata,
        parentConfig: item.parent_config,
        pendingWrites: item.pending_writes,
      } satisfies CheckpointTuple;
    }
  }
  async put(
    config: RunnableConfig,
    checkpoint: Checkpoint,
    metadata: CheckpointMetadata,
    newVersions: ChannelVersions
  ): Promise<RunnableConfig> {
    const response = await tryFetch("http://checkpointer/put", {
      dispatcher: checkpointerDispatcher,
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        config,
        checkpoint,
        metadata,
        new_versions: newVersions,
      }),
    });

    return (await response.json()) as RunnableConfig;
  }

  async putWrites(
    config: RunnableConfig,
    writes: [string, unknown][],
    taskId: string
  ): Promise<void> {
    // Implementation of the inherited abstract member 'putWrites'
    await tryFetch("http://checkpointer/put_writes", {
      dispatcher: checkpointerDispatcher,
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ config, writes, taskId }),
    });
  }

  getNextVersion(
    current: number | string | undefined,
    _channel: ChannelProtocol
  ): string {
    let currentVersion = 0;

    if (current == null) {
      currentVersion = 0;
    } else if (typeof current === "number") {
      currentVersion = current;
    } else if (typeof current === "string") {
      currentVersion = Number.parseInt(current.split(".")[0], 10);
    }

    const nextVersion = String(currentVersion + 1).padStart(32, "0");
    try {
      const hash = createHash("md5")
        .update(serialiseAsDict(_channel.checkpoint()))
        .digest("hex");
      return `${nextVersion}.${hash}`;
    } catch {}

    return nextVersion;
  }
}

function camelToSnake(operation: Operation) {
  const snakeCaseKeys = (obj: Record<string, any>): Record<string, any> => {
    return Object.fromEntries(
      Object.entries(obj).map(([key, value]) => {
        const snakeKey = key.replace(
          /[A-Z]/g,
          (letter) => `_${letter.toLowerCase()}`
        );
        if (
          typeof value === "object" &&
          value !== null &&
          !Array.isArray(value)
        ) {
          return [snakeKey, snakeCaseKeys(value)];
        }
        return [snakeKey, value];
      })
    );
  };

  if ("namespace" in operation && "key" in operation) {
    return {
      namespace: operation.namespace,
      key: operation.key,
      ...("value" in operation ? { value: operation.value } : {}),
    };
  } else if ("namespacePrefix" in operation) {
    return {
      namespace_prefix: operation.namespacePrefix,
      filter: operation.filter,
      limit: operation.limit,
      offset: operation.offset,
    };
  } else if ("matchConditions" in operation) {
    return {
      match_conditions: operation.matchConditions?.map((condition) => ({
        match_type: condition.matchType,
        path: condition.path,
      })),
      max_depth: operation.maxDepth,
      limit: operation.limit,
      offset: operation.offset,
    };
  }

  return snakeCaseKeys(operation) as Operation;
}

function pyItemToJs(item?: PyItem): Item | undefined {
  if (!item) {
    return undefined;
  }
  return {
    namespace: item.namespace,
    key: item.key,
    value: item.value,
    createdAt: item.created_at,
    updatedAt: item.updated_at,
  };
}

export class RemoteStore extends BaseStore {
  async batch<Op extends Operation[]>(
    operations: Op
  ): Promise<OperationResults<Op>> {
    const response = await tryFetch("http://store/items/batch", {
      dispatcher: storeDispatcher,
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ operations: operations.map(camelToSnake) }),
    });

    const results = (await response.json()) as PyResult[];
    return results.map((result) => {
      if (Array.isArray(result)) {
        return result.map((item) => pyItemToJs(item));
      } else if (
        result &&
        typeof result === "object" &&
        "value" in result &&
        "key" in result
      ) {
        return pyItemToJs(result);
      }
      return result;
    }) as OperationResults<Op>;
  }

  async get(namespace: string[], key: string): Promise<Item | null> {
    const queryParams = new URLSearchParams({
      namespace: namespace.join("."),
      key,
    });
    const urlWithParams = `http://store/items?${queryParams.toString()}`;
    const response = await tryFetch(urlWithParams, {
      dispatcher: storeDispatcher,
      method: "GET",
    });
    return (await response.json()) as Item | null;
  }

  async search(
    namespacePrefix: string[],
    options?: {
      filter?: Record<string, any>;
      limit?: number;
      offset?: number;
    }
  ): Promise<Item[]> {
    const response = await tryFetch("http://store/items/search", {
      dispatcher: storeDispatcher,
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ namespace_prefix: namespacePrefix, ...options }),
    });
    return (await response.json()) as Item[];
  }

  async put(
    namespace: string[],
    key: string,
    value: Record<string, any>
  ): Promise<void> {
    await tryFetch("http://store/items", {
      dispatcher: storeDispatcher,
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ namespace, key, value }),
    });
  }

  async delete(namespace: string[], key: string): Promise<void> {
    await tryFetch("http://store/items", {
      dispatcher: storeDispatcher,
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ namespace, key }),
    });
  }

  async listNamespaces(options: {
    prefix?: string[];
    suffix?: string[];
    maxDepth?: number;
    limit?: number;
    offset?: number;
  }): Promise<string[][]> {
    const response = await tryFetch("http://store/list/namespaces", {
      dispatcher: storeDispatcher,
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ max_depth: options?.maxDepth, ...options }),
    });

    const data = (await response.json()) as { namespaces: string[][] };
    return data.namespaces;
  }
}

const StreamModeSchema = z.union([
  z.literal("updates"),
  z.literal("debug"),
  z.literal("values"),
]);

const ExtraStreamModeSchema = z.union([
  StreamModeSchema,
  z.literal("messages"),
]);

const __dirname = new URL(".", import.meta.url).pathname;

async function main() {
  const app = new Hono();
  const checkpointer = new RemoteCheckpointer();
  const store = new RemoteStore();

  const specs = z
    .record(z.string())
    .parse(JSON.parse(process.env.LANGSERVE_GRAPHS ?? "{}"));

  if (!process.argv.includes("--skip-schema-cache")) {
    try {
      GRAPH_SCHEMA = JSON.parse(
        await fs.readFile(path.resolve(__dirname, "client.schemas.json"), {
          encoding: "utf-8",
        })
      );
    } catch {
      // pass
    }
  }

  await Promise.all(
    Object.entries(specs).map(async ([graphId, rawSpec]) => {
      logger.info(`Resolving graph ${graphId}`);
      const { resolved, ...spec } = await resolveGraph(rawSpec);

      // TODO: make sure the types do not need to be upfront
      // @ts-expect-error Overriding checkpointer with different value type
      resolved.checkpointer = checkpointer;
      resolved.store = store;

      // registering the graph runtime
      GRAPH_RESOLVED[graphId] = resolved;
      GRAPH_SPEC[graphId] = spec;
    })
  );

  app.post(
    "/:graphId/streamEvents",
    zValidator(
      "json",
      z.object({
        input: z.unknown(),
        command: z.object({ resume: z.unknown() }).nullish(),
        stream_mode: z
          .union([ExtraStreamModeSchema, z.array(ExtraStreamModeSchema)])
          .optional(),
        config: RunnableConfigSchema.nullish(),
        interrupt_before: z
          .union([z.array(z.string()), z.literal("*")])
          .nullish(),
        interrupt_after: z
          .union([z.array(z.string()), z.literal("*")])
          .nullish(),
        subgraphs: z.boolean().optional(),
      })
    ),
    async (c) => {
      const graph = getGraph(c.req.param("graphId"));
      const payload = c.req.valid("json");

      const input = payload.command
        ? // @ts-expect-error Update LG.js to mark `resume as optional
          new Command(payload.command)
        : payload.input;

      const userStreamMode =
        payload.stream_mode == null
          ? []
          : Array.isArray(payload.stream_mode)
            ? payload.stream_mode
            : [payload.stream_mode];

      const graphStreamMode: Set<"updates" | "debug" | "values"> = new Set();
      if (payload.stream_mode) {
        for (const mode of userStreamMode) {
          if (mode === "messages") {
            graphStreamMode.add("values");
          } else {
            graphStreamMode.add(mode);
          }
        }
      }

      const config = getRunnableConfig(payload.config);

      return streamSSE(c, async (stream) => {
        const messages: Record<string, BaseMessageChunk> = {};
        const completedIds = new Set<string>();

        let interruptBefore: typeof payload.interrupt_before =
          payload.interrupt_before ?? undefined;

        if (Array.isArray(interruptBefore) && interruptBefore.length === 0)
          interruptBefore = undefined;

        let interruptAfter: typeof payload.interrupt_after =
          payload.interrupt_after ?? undefined;

        if (Array.isArray(interruptAfter) && interruptAfter.length === 0)
          interruptAfter = undefined;

        const streamMode = [...graphStreamMode];

        try {
          for await (const data of graph.streamEvents(input, {
            ...config,
            version: "v2",
            streamMode,
            subgraphs: payload.subgraphs,
            interruptBefore,
            interruptAfter,
          })) {
            // TODO: upstream this fix to LangGraphJS
            if (streamMode.length === 1 && !Array.isArray(data.data.chunk)) {
              data.data.chunk = [streamMode[0], data.data.chunk];
            }

            if (payload.subgraphs) {
              if (
                Array.isArray(data.data.chunk) &&
                data.data.chunk.length === 2
              ) {
                data.data.chunk = [[], ...data.data.chunk];
              }
            }

            await stream.writeSSE({
              event: "streamLog",
              data: serialiseAsDict(data),
            });

            if (userStreamMode.includes("messages")) {
              if (
                data.event === "on_chain_stream" &&
                data.run_id === config.runId
              ) {
                const newMessages: Array<BaseMessageChunk> = [];
                const [_, chunk]: [string, any] = data.data.chunk;

                let chunkMessages: Array<BaseMessageChunk> = [];
                if (
                  typeof chunk === "object" &&
                  chunk != null &&
                  "messages" in chunk &&
                  !isBaseMessage(chunk)
                ) {
                  chunkMessages = chunk?.messages;
                }

                if (!Array.isArray(chunkMessages)) {
                  chunkMessages = [chunkMessages];
                }

                for (const message of chunkMessages) {
                  if (!message.id || completedIds.has(message.id)) continue;
                  completedIds.add(message.id);
                  newMessages.push(message);
                }

                if (newMessages.length > 0) {
                  await stream.writeSSE({
                    event: "streamLog",
                    data: serialiseAsDict({
                      event: "on_custom_event",
                      name: "messages/complete",
                      data: newMessages,
                    }),
                  });
                }
              } else if (
                data.event === "on_chat_model_stream" &&
                !data.tags?.includes("nostream")
              ) {
                const message: BaseMessageChunk = data.data.chunk;

                if (!message.id) continue;

                if (messages[message.id] == null) {
                  messages[message.id] = message;
                  await stream.writeSSE({
                    event: "streamLog",
                    data: serialiseAsDict({
                      event: "on_custom_event",
                      name: "messages/metadata",
                      data: { [message.id]: { metadata: data.metadata } },
                    }),
                  });
                } else {
                  messages[message.id] = messages[message.id].concat(message);
                }

                await stream.writeSSE({
                  event: "streamLog",
                  data: serialiseAsDict({
                    event: "on_custom_event",
                    name: "messages/partial",
                    data: [messages[message.id]],
                  }),
                });
              }
            }
          }
        } catch (error) {
          const errorName = error instanceof Error ? error.name : "Error";
          const errorMessage =
            error instanceof Error ? error.message : JSON.stringify(error);

          await stream.writeSSE({
            event: "error",
            data: serialiseAsDict({
              error: errorName,
              message: errorMessage,
            }),
          });

          // Still print out the error, as the stack
          // trace is not carried over in Python
          logger.error(error);
        }
      });
    }
  );

  app.post(
    "/:graphId/getGraph",
    zValidator(
      "json",
      z.object({
        config: RunnableConfigSchema.nullish(),
        xray: z.union([z.number(), z.boolean()]).nullish(),
      })
    ),
    async (c) => {
      const graphId = c.req.param("graphId");
      const graph = getGraph(graphId);
      return c.json(
        graph
          .getGraph({
            ...getRunnableConfig(c.req.valid("json").config),
            xray: c.req.valid("json").xray ?? undefined,
          })
          .toJSON()
      );
    }
  );

  app.post(
    "/:graphId/getSubgraphs",
    zValidator(
      "json",
      z.object({
        namespace: z.string().nullish(),
        recurse: z.boolean().nullish(),
      })
    ),

    async (c) => {
      const graphId = c.req.param("graphId");
      const graph = getGraph(graphId);

      const payload = c.req.valid("json");
      const result: Array<[name: string, Record<string, any>]> = [];

      const graphSchema = await getOrExtractSchema(graphId);
      const rootGraphId = Object.keys(graphSchema).find(
        (i) => !i.includes("|")
      );

      if (!rootGraphId)
        throw new HTTPException(500, { message: "Failed to find root graph" });

      for (const [name] of graph.getSubgraphs(
        payload.namespace ?? undefined,
        payload.recurse ?? undefined
      )) {
        const schema =
          graphSchema[`${rootGraphId}|${name}`] || graphSchema[rootGraphId];
        result.push([name, schema]);
      }

      return c.json(Object.fromEntries(result));
    }
  );

  app.post(
    "/:graphId/getState",
    zValidator(
      "json",
      z.object({
        config: RunnableConfigSchema,
        subgraphs: z.boolean().nullish(),
      })
    ),
    async (c) => {
      const graph = getGraph(c.req.param("graphId"));
      const payload = c.req.valid("json");

      const state = await graph.getState(getRunnableConfig(payload.config), {
        subgraphs: payload.subgraphs ?? undefined,
      });
      // TODO: just send the JSON directly, don't ser/de twice
      return c.json(JSON.parse(serialiseAsDict(state)));
    }
  );

  app.post(
    "/:graphId/updateState",
    zValidator(
      "json",
      z.object({
        config: RunnableConfigSchema,
        values: z.unknown(),
        as_node: z.string().nullish(),
      })
    ),
    async (c) => {
      const graph = getGraph(c.req.param("graphId"));
      const payload = c.req.valid("json");

      const config = await graph.updateState(
        getRunnableConfig(payload.config),
        payload.values,
        payload.as_node ?? undefined
      );

      return c.json(config);
    }
  );

  app.post("/:graphId/getSchema", async (c) => {
    const schemas = await getOrExtractSchema(c.req.param("graphId"));
    const rootGraphId = Object.keys(schemas).find((i) => !i.includes("|"));
    if (!rootGraphId) {
      throw new HTTPException(500, { message: "Failed to find root graph" });
    }
    return c.json(schemas[rootGraphId]);
  });

  app.post(
    "/:graphId/getStateHistory",
    zValidator(
      "json",
      z.object({
        config: RunnableConfigSchema,
        limit: z.number().nullish(),
        before: RunnableConfigSchema.nullish(),
        filter: z.record(z.unknown()).nullish(),
      })
    ),
    async (c) => {
      const graph = getGraph(c.req.param("graphId"));
      const payload = c.req.valid("json");

      return streamSSE(c, async (stream) => {
        for await (const item of graph.getStateHistory(
          getRunnableConfig(payload.config),
          {
            limit: payload.limit ?? undefined,
            before: payload.before
              ? getRunnableConfig(payload.before)
              : undefined,
            filter: payload.filter ?? undefined,
          }
        )) {
          await stream.writeSSE({
            data: serialiseAsDict(item),
            event: "getStateHistory",
          });
        }
      });
    }
  );

  app.get("/ok", (c) => c.json({ ok: true }));

  app.onError((err, c) => {
    logger.error(err);
    if (err instanceof HTTPException && err.status === 401) {
      return err.getResponse();
    }
    return c.text("Internal server error", 500);
  });

  await fs.unlink(GRAPH_SOCKET).catch(() => void 0);
  serve(
    {
      fetch: app.fetch,
      hostname: "localhost",
      port: GRAPH_SOCKET as any,
    },
    (c) => logger.info(`Listening to ${c}`)
  );
}

process.on("uncaughtExceptionMonitor", (error) => {
  logger.error(error);
  process.exit(1);
});

main();
