import asyncio
import json
import requests
from asyncio import Queue
from enum import Enum
from socketio import AsyncClient
from typing import Callable, Dict, List, Optional, Union
from hyperion.types import (
    EventListener,
    HyperionClientOptions,
    StreamActionsRequest,
    StreamDeltasRequest,
    EventData,
)
from loguru import logger


class StreamClientEvents(Enum):
    DATA = "data"
    LIBUPDATE = "libUpdate"
    FORK = "fork"
    EMPTY = "empty"
    CONNECT = "connect"
    DRAIN = "drain"
    LIBDATA = "libData"


class HyperionStreamClient:
    def __init__(self, options: HyperionClientOptions):
        self.socket_url = None
        self.options = options
        self.online = False
        self.socket = AsyncClient()
        self.saved_requests: List[Dict] = list()
        self.reversible_buffer = list()
        self.last_received_block = 0
        self.event_listeners: Dict[str, List[EventListener]] = dict()
        self.temp_event_listeners: Dict[str, List[EventListener]] = dict()

        # DATA QUEUE
        self.data_queue = Queue()
        self.lib_data_queue = asyncio.Queue()

        if options.endpoint:
            self.set_endpoint(self.options.endpoint)

        self.async_data_handler = None
        self.async_lib_data_handler = None

    def set_endpoint(self, endpoint: str):
        if endpoint.endswith("/"):
            endpoint = endpoint.rstrip("/")
        self.socket_url = endpoint

    async def disconnect(self):
        if self.socket:
            self.last_received_block = 0
            await self.socket.disconnect()
            self.saved_requests = []

        else:
            logger.info("No active socket connection to disconnect.")

    def last_block_num(self) -> int:
        return self.last_received_block

    def push_to_buffer(self, task):
        if self.options.lib_stream:
            self.reversible_buffer.append(task)

    async def queue_worker(self):
        while True:
            task = await self.data_queue.get()
            if task is None:
                break

            task["irreversible"] = False
            self.emit(StreamClientEvents.DATA, task)
            self.push_to_buffer(task)

            if self.async_data_handler:
                await self.async_data_handler(task)

            self.data_queue.task_done()

    async def lib_queue_worker(self):
        while True:
            task = await self.lib_data_queue.get()
            if task is None:
                break
            task["irreversible"] = True
            self.emit(StreamClientEvents.LIBDATA, task)
            if self.async_lib_data_handler:
                await self.async_lib_data_handler(task)
            self.lib_data_queue.task_done()

    def setup_incoming_queue(self):
        self.worker_task = asyncio.create_task(self.queue_worker())

    def setup_irreversible_queue(self):
        if self.options.lib_stream:
            self.lib_worker_task = asyncio.create_task(self.lib_queue_worker())

    async def handle_lib_update(self, msg):
        if self.options.lib_stream:
            while self.reversible_buffer:
                if self.reversible_buffer[0]:
                    if (
                        self.reversible_buffer[0]["content"]["block_num"]
                        <= msg["block_num"]
                    ):
                        if self.lib_data_queue:
                            data = self.reversible_buffer.pop(0)
                            if data:
                                await self.lib_data_queue.put(data)
                            else:
                                break
                    else:
                        break
                else:
                    break

        self.emit(StreamClientEvents.LIBUPDATE, msg)

        for request in self.saved_requests:
            if request["req"].get("read_until") and request["req"]["read_until"] != 0:
                if request["req"]["read_until"] < msg["block_num"]:
                    await self.disconnect()

    async def setup_socket(self):
        if not self.socket_url:
            raise ValueError("Socket URL is not set")

        try:

            @self.socket.event
            async def connect():
                logger.success(f"Connected to the server {self.socket_url}")
                self.online = True
                self.emit(StreamClientEvents.CONNECT, {})
                await self.resend_requests()

            @self.socket.event
            async def error(msg):
                logger.error(msg)

            @self.socket.event
            async def lib_update(msg):
                await self.handle_lib_update(msg)

            @self.socket.event
            async def fork_event(msg):
                self.emit(StreamClientEvents.FORK, msg)

            @self.socket.event
            async def message(msg):
                if (self.async_data_handler or self.async_lib_data_handler) and (
                    "message" in msg or "messages" in msg
                ):
                    if msg.get("type") == "delta_trace":
                        if "messages" in msg:
                            for message in msg["messages"]:
                                await self.process_delta_trace(message, msg.get("mode"))
                        else:
                            await self.process_delta_trace(
                                json.loads(msg["message"]), msg.get("mode")
                            )

                    elif msg.get("type") == "action_trace":
                        if "messages" in msg:
                            for message in msg["messages"]:
                                await self.process_action_trace(
                                    message, msg.get("mode")
                                )
                        else:
                            await self.process_action_trace(
                                json.loads(msg["message"]), msg.get("mode")
                            )

            @self.socket.event
            async def status(status):
                if status == "relay_restored":
                    if not self.online:
                        self.online = True
                        try:
                            await self.resend_requests()
                        except Exception as e:
                            logger.error(e)
                elif status == "relay_down":
                    self.online = False
                else:
                    logger.info(f"Unknown status: {status}")

            @self.socket.event
            async def disconnect():
                logger.debug("Disconnected")
                self.online = False

            await self.socket.connect(
                self.socket_url, transports=["websocket"], socketio_path="/stream"
            )

        except Exception as e:
            logger.error("Failed to connect")
            self.disconnect()

    async def connect(self):
        self.setup_incoming_queue()
        self.setup_irreversible_queue()
        if not self.socket_url:
            raise ValueError("endpoint was not defined!")

        logger.debug(f"Connecting to {self.socket_url}...")
        await self.setup_socket()

    async def process_action_trace(self, action: dict, mode: str):
        meta_key = f"@{action['act']['name']}"
        if meta_key in action:
            parsed_data = action[meta_key]
            if "act" not in action:
                action["act"] = {}
            if "data" not in action["act"]:
                action["act"]["data"] = {}

            for key, value in parsed_data.items():
                action["act"]["data"][key] = value

            del action[meta_key]

        if self.data_queue:
            try:
                await self.data_queue.put(
                    {
                        "type": "action",
                        "mode": mode,
                        "content": action,
                        "irreversible": False,
                    }
                )
                self.last_received_block = action["block_num"]
            except Exception as e:
                logger.error(f"Action trace: {e}")

    async def process_delta_trace(self, delta: dict, mode: str):
        meta_key = f"@{delta['table']}"
        if f"{meta_key}.data" in delta:
            meta_key = f"{meta_key}.data"

        if meta_key in delta:
            parsed_data = delta[meta_key]
            if "data" not in delta:
                delta["data"] = {}

            for key, value in parsed_data.items():
                delta["data"][key] = value

            del delta[meta_key]

        if self.data_queue:
            try:
                await self.data_queue.put(
                    {
                        "type": "delta",
                        "mode": mode,
                        "content": delta,
                        "irreversible": False,
                    }
                )
                self.last_received_block = delta["block_num"]
            except Exception as e:
                logger.error(f"Error while processing delta trace: {e}")

    async def resend_requests(self):
        if not self.saved_requests:
            return

        self.debug_log(f"Sending {len(self.saved_requests)} saved requests`")

        saved_reqs = self.saved_requests.copy()
        self.saved_requests.clear()

        for r in saved_reqs:
            if r["type"] == "action":
                await self.stream_actions(r["req"])
            elif r["type"] == "delta":
                await self.stream_deltas(r["req"])

    async def stream_actions(self, request: StreamActionsRequest):
        if self.socket and self.socket.connected:
            try:
                request = await self.check_last_block(request)
            except Exception as e:
                return {"status": "ERROR", "error": str(e)}

            if self.socket and self.socket.connected:
                try:
                    response = await self.socket.emit(
                        "action_stream_request",
                        request,
                        callback=lambda res: logger.success(res),
                    )

                    if response["status"] == "OK":
                        self.saved_requests.append({"type": "action", "req": request})
                        response["startingBlock"] = request["start_from"]
                        return response
                    else:
                        raise Exception(f"Failed response: {response}")

                except Exception as e:
                    return {"status": "ERROR", "error": str(e)}
            else:
                raise Exception("Socket was not created")
        else:
            raise Exception(
                "Client is not connected! Please call connect before sending requests"
            )

    async def stream_deltas(self, request: StreamDeltasRequest):
        if self.socket and self.socket.connected:
            try:
                await self.check_last_block(request)
            except Exception as e:
                return {"status": "ERROR", "error": str(e)}
            if self.socket:
                try:
                    response = await self.socket.emit(
                        "delta_stream_request",
                        request,
                        callback=lambda res: logger.success(res),
                    )

                    if response["status"] == "OK":
                        self.saved_requests.append({"type": "delta", "req": request})
                        response["startingBlock"] = request["start_from"]
                        return response
                    else:
                        raise Exception(f"Failed response: {response}")
                except Exception as e:
                    return {"status": "ERROR", "error": str(e)}
            else:
                raise Exception("Socket was not created")

    async def check_last_block(
        self, request: Union[StreamDeltasRequest, StreamActionsRequest]
    ):

        url = self.options.chain_api if self.options.chain_api else self.socket_url
        url += "/v1/chain/get_info"

        try:
            response = requests.get(url)
            response.raise_for_status()
            json = response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"get_info failed on: {url} | error: {str(e)}")

        if str(request["start_from"]).upper() == "LIB":

            if json and "last_irreversible_block_num" in json:
                request["start_from"] = json["last_irreversible_block_num"]
                self.debug_log(
                    f"Stream starting at lib (block {request['start_from']})"
                )

        elif request["start_from"] != 0 and self.last_received_block:
            if request["start_from"] < self.last_received_block:
                request["start_from"] = self.last_received_block
        else:
            if json and "head_block_num" in json:
                request["start_from"] = json["head_block_num"]
                self.debug_log(
                    f"Stream starting at head block (block {request['start_from']})"
                )
        return request

    def emit(
        self, event: Union[StreamClientEvents, str], data: Optional[EventData] = None
    ):
        listeners = self.event_listeners.get(event)
        if listeners:
            for listener in listeners:
                listener(data)

        temp_listeners = self.temp_event_listeners.get(event)
        if temp_listeners and len(temp_listeners) > 0:
            listener = temp_listeners.pop(0)
            if listener:
                listener(data)

    def once(self, event: str, listener: Callable):
        if not callable(listener):
            raise ValueError("Event listener must be a function")

        if event not in self.temp_event_listeners:
            self.temp_event_listeners[event] = [listener]
        else:
            self.temp_event_listeners[event].append(listener)

    def on(self, event: str, listener: Callable):
        if not callable(listener):
            raise ValueError("Event listener must be a function")
        if event not in self.event_listeners:
            self.event_listeners[event] = [listener]
        else:
            self.event_listeners[event].append(listener)

    def off(self, event: str, listener: Callable):
        listeners = self.event_listeners.get(event)
        if listeners:
            try:
                listeners.remove(listener)
            except ValueError:
                pass

        temp_listeners = self.temp_event_listeners.get(event)
        if temp_listeners:
            try:
                temp_listeners.remove(listener)
            except ValueError:
                pass

    def debug_log(self, *args):
        if self.options.debug:
            logger.debug(f"[hyperion:debug] {args}")
