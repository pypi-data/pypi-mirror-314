import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import logging
import os
from typing import Any, Callable, Dict

import msgspec

from webai_element_sdk.comms.utils import get_default_gateway
from webai_element_sdk.runner import WebSocketServer

ELEMENT_KEY = os.getenv("ELEMENT_KEY")
ELEMENT_NAME = os.getenv("ELEMENT_NAME")
ELEMENT_VERSION = os.getenv("ELEMENT_VERSION")
DEPLOYMENT_ID = os.getenv("DEPLOYMENT_ID")
AGENT_HOST = os.getenv("AGENT_HOST")
PREVIEW_PORT = os.getenv("PREVIEW_PORT")

encoder = msgspec.json.Encoder()  # type: ignore
decoder = msgspec.json.Decoder()  # type: ignore

executor = ThreadPoolExecutor()

class AgentComms:
    """Websocket client used to connect with the runtime agent

    Attributes:
        ws (WebSocketServer): The websocket server instance
        response_map (Mapping[str, Any]): TODO - doc
        wait_until_begin (bool): TODO - doc
    """

    def __init__(self):
        self.ws = WebSocketServer(
            {
                "name": ELEMENT_NAME or "",
                "version": ELEMENT_VERSION or "",
                "key": ELEMENT_KEY or "",
                "deploymentId": DEPLOYMENT_ID or "",
            }
        )
        self.response_map = {}
        self.wait_until_begin = None

    def get_agent_host(self):
        if AGENT_HOST is None or AGENT_HOST == "":
            return get_default_gateway()
        return AGENT_HOST

    async def wait_for_refresh(self, reset_values: Callable):
        if getattr(self.ws, "on_refresh", None) is None:
            print("refresh settings not possible in this version of runtime agent")
            return
        loop = asyncio.get_running_loop()
        self.ws.on_refresh(lambda t=reset_values: loop.create_task(t()))
        loop.run_in_executor(executor, self.ws.wait_for_refresh)

    def connect(self):
        """Connect to agent"""
        print("Connecting to the server")
        self.ws.start("ws://" + self.get_agent_host() + ":10105")

        self.wait_until_begin = self.ws.wait_until_begin

        print("Connected to the server")

    async def log(self, message: str) -> None:
        """Method for logging messages back to the runtime agent from the element

        Args:
            message: The message to log
        """
        self._log(message)

    def _log(self, message):
        """Send log message"""
        self.ws.send("log", encoder.encode({"message": message}), True)

    def exception(self, ex: Exception, stacktrace: str):
        """Send exception details"""
        # generate_latest returns a byte array
        self.ws.send("exception", encoder.encode({  # type: ignore
            "type": type(ex).__name__,
            "message": str(ex),
            "stacktrace": stacktrace,
            "args": ex.args
        }), True)  # type: ignore

    def open(self, port: str):
        """ ""Send open message"""
        self.ws.send("open", encoder.encode({"port": port}), True)  # type: ignore

    def startup(self):
        """Send startup message"""
        self._log("Sending ready message")
        self.ws.send("startup", "{}", False)

    def ready(self):
        """Send ready message"""
        self._log("Sending ready message")
        self.ws.send("ready", "{}", False)

    def init_training_metrics(self, metrics_schema: Dict[str, Any]):
        """Send init_training_metrics message"""
        self.ws.send("init_training_metrics", json.dumps(metrics_schema), True)

    def update_training_metrics(self, metrics_step: Dict[str, Any]):
        """Send update_training_metrics message"""
        logging.warning(
            "update_training_metrics is deprecated and will be removed. Use update_metrics."
        )
        self.ws.send("update_training_metrics", json.dumps(metrics_step), True)

    def update_metrics(self, metrics_step: Dict[str, Any]):
        """Send update_metrics message"""
        self.ws.send("update_training_metrics", json.dumps(metrics_step), True)

    def complete(self):
        """send complete"""
        self.ws.send("complete", "{}", True)

    def setup(self):
        """Setup agent websocket connection"""
        self.connect()

    def shutdown(self):
        self.ws.shutdown()
