from __future__ import annotations

import importlib
import importlib.metadata as imd
import json
import os
import select
import subprocess
import threading
import time
import uuid
from functools import wraps
from typing import TYPE_CHECKING

from bec_lib.client import BECClient
from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger
from bec_lib.utils.import_utils import isinstance_based_on_class_name, lazy_import, lazy_import_from

import bec_widgets.cli.client as client
from bec_widgets.cli.auto_updates import AutoUpdates

if TYPE_CHECKING:
    from bec_lib.device import DeviceBase

messages = lazy_import("bec_lib.messages")
# from bec_lib.connector import MessageObject
MessageObject = lazy_import_from("bec_lib.connector", ("MessageObject",))
BECDispatcher = lazy_import_from("bec_widgets.utils.bec_dispatcher", ("BECDispatcher",))

logger = bec_logger.logger


def rpc_call(func):
    """
    A decorator for calling a function on the server.

    Args:
        func: The function to call.

    Returns:
        The result of the function call.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # we could rely on a strict type check here, but this is more flexible
        # moreover, it would anyway crash for objects...
        out = []
        for arg in args:
            if hasattr(arg, "name"):
                arg = arg.name
            out.append(arg)
        args = tuple(out)
        for key, val in kwargs.items():
            if hasattr(val, "name"):
                kwargs[key] = val.name
        if not self.gui_is_alive():
            raise RuntimeError("GUI is not alive")
        return self._run_rpc(func.__name__, *args, **kwargs)

    return wrapper


def _get_output(process, logger) -> None:
    log_func = {process.stdout: logger.debug, process.stderr: logger.error}
    stream_buffer = {process.stdout: [], process.stderr: []}
    try:
        os.set_blocking(process.stdout.fileno(), False)
        os.set_blocking(process.stderr.fileno(), False)
        while process.poll() is None:
            readylist, _, _ = select.select([process.stdout, process.stderr], [], [], 1)
            for stream in (process.stdout, process.stderr):
                buf = stream_buffer[stream]
                if stream in readylist:
                    buf.append(stream.read(4096))
                output, _, remaining = "".join(buf).rpartition("\n")
                if output:
                    log_func[stream](output)
                    buf.clear()
                    buf.append(remaining)
    except Exception as e:
        logger.error(f"Error reading process output: {str(e)}")


def _start_plot_process(gui_id: str, gui_class: type, config: dict | str, logger=None) -> None:
    """
    Start the plot in a new process.

    Logger must be a logger object with "debug" and "error" functions,
    or it can be left to "None" as default. None means output from the
    process will not be captured.
    """
    # pylint: disable=subprocess-run-check
    command = ["bec-gui-server", "--id", gui_id, "--gui_class", gui_class.__name__, "--hide"]
    if config:
        if isinstance(config, dict):
            config = json.dumps(config)
        command.extend(["--config", str(config)])

    env_dict = os.environ.copy()
    env_dict["PYTHONUNBUFFERED"] = "1"

    if logger is None:
        stdout_redirect = subprocess.DEVNULL
        stderr_redirect = subprocess.DEVNULL
    else:
        stdout_redirect = subprocess.PIPE
        stderr_redirect = subprocess.PIPE

    process = subprocess.Popen(
        command,
        text=True,
        start_new_session=True,
        stdout=stdout_redirect,
        stderr=stderr_redirect,
        env=env_dict,
    )
    if logger is None:
        process_output_processing_thread = None
    else:
        process_output_processing_thread = threading.Thread(
            target=_get_output, args=(process, logger)
        )
        process_output_processing_thread.start()
    return process, process_output_processing_thread


class RepeatTimer(threading.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class BECGuiClientMixin:
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._auto_updates_enabled = True
        self._auto_updates = None
        self._gui_started_timer = None
        self._gui_started_event = threading.Event()
        self._process = None
        self._process_output_processing_thread = None
        self._target_endpoint = MessageEndpoints.scan_status()
        self._selected_device = None

    @property
    def auto_updates(self):
        if self._auto_updates_enabled:
            self._gui_started_event.wait()
        return self._auto_updates

    def shutdown_auto_updates(self):
        if self._auto_updates_enabled:
            if self._auto_updates is not None:
                self._auto_updates.shutdown()
                self._auto_updates = None

    def _get_update_script(self) -> AutoUpdates | None:
        eps = imd.entry_points(group="bec.widgets.auto_updates")
        for ep in eps:
            if ep.name == "plugin_widgets_update":
                try:
                    spec = importlib.util.find_spec(ep.module)
                    # if the module is not found, we skip it
                    if spec is None:
                        continue
                    return ep.load()(gui=self)
                except Exception as e:
                    logger.error(f"Error loading auto update script from plugin: {str(e)}")
        return None

    @property
    def selected_device(self):
        """
        Selected device for the plot.
        """
        return self._selected_device

    @selected_device.setter
    def selected_device(self, device: str | DeviceBase):
        if isinstance_based_on_class_name(device, "bec_lib.device.DeviceBase"):
            self._selected_device = device.name
        elif isinstance(device, str):
            self._selected_device = device
        else:
            raise ValueError("Device must be a string or a device object")

    def _start_update_script(self) -> None:
        self._client.connector.register(
            self._target_endpoint, cb=self._handle_msg_update, parent=self
        )

    @staticmethod
    def _handle_msg_update(msg: MessageObject, parent: BECGuiClientMixin) -> None:
        if parent.auto_updates is not None:
            # pylint: disable=protected-access
            parent._update_script_msg_parser(msg.value)

    def _update_script_msg_parser(self, msg: messages.BECMessage) -> None:
        if isinstance(msg, messages.ScanStatusMessage):
            if not self.gui_is_alive():
                return
            if self._auto_updates_enabled:
                self.auto_updates.msg_queue.put(msg)

    def _gui_post_startup(self):
        if self._auto_updates_enabled:
            if self._auto_updates is None:
                auto_updates = self._get_update_script()
                if auto_updates is None:
                    AutoUpdates.create_default_dock = True
                    AutoUpdates.enabled = True
                    auto_updates = AutoUpdates(gui=self)
                if auto_updates.create_default_dock:
                    auto_updates.start_default_dock()
                    # fig = auto_updates.get_default_figure()
                self._auto_updates = auto_updates
        self._gui_started_event.set()
        self.show_all()

    def start_server(self, wait=False) -> None:
        """
        Start the GUI server, and execute callback when it is launched
        """
        if self._process is None or self._process.poll() is not None:
            logger.success("GUI starting...")
            self._gui_started_event.clear()
            self._start_update_script()
            self._process, self._process_output_processing_thread = _start_plot_process(
                self._gui_id, self.__class__, self._client._service_config.config, logger=logger
            )

            def gui_started_callback(callback):
                try:
                    if callable(callback):
                        callback()
                finally:
                    threading.current_thread().cancel()

            self._gui_started_timer = RepeatTimer(
                1, lambda: self.gui_is_alive() and gui_started_callback(self._gui_post_startup)
            )
            self._gui_started_timer.start()

        if wait:
            self._gui_started_event.wait()

    def show_all(self):
        self._gui_started_event.wait()
        rpc_client = RPCBase(gui_id=f"{self._gui_id}:window", parent=self)
        rpc_client._run_rpc("show")

    def hide_all(self):
        self._gui_started_event.wait()
        rpc_client = RPCBase(gui_id=f"{self._gui_id}:window", parent=self)
        rpc_client._run_rpc("hide")

    def close(self) -> None:
        """
        Close the gui window.
        """
        if self._gui_started_timer is not None:
            self._gui_started_timer.cancel()
            self._gui_started_timer.join()

        if self._process is None:
            return

        if self._process:
            logger.success("Stopping GUI...")
            self._process.terminate()
            if self._process_output_processing_thread:
                self._process_output_processing_thread.join()
            self._process.wait()
            self._process = None
        self.shutdown_auto_updates()


class RPCResponseTimeoutError(Exception):
    """Exception raised when an RPC response is not received within the expected time."""

    def __init__(self, request_id, timeout):
        super().__init__(
            f"RPC response not received within {timeout} seconds for request ID {request_id}"
        )


class RPCBase:
    def __init__(self, gui_id: str = None, config: dict = None, parent=None) -> None:
        self._client = BECClient()  # BECClient is a singleton; here, we simply get the instance
        self._config = config if config is not None else {}
        self._gui_id = gui_id if gui_id is not None else str(uuid.uuid4())[:5]
        self._parent = parent
        self._msg_wait_event = threading.Event()
        self._rpc_response = None
        super().__init__()
        # print(f"RPCBase: {self._gui_id}")

    def __repr__(self):
        type_ = type(self)
        qualname = type_.__qualname__
        return f"<{qualname} object at {hex(id(self))}>"

    @property
    def _root(self):
        """
        Get the root widget. This is the BECFigure widget that holds
        the anchor gui_id.
        """
        parent = self
        # pylint: disable=protected-access
        while parent._parent is not None:
            parent = parent._parent
        return parent

    def _run_rpc(self, method, *args, wait_for_rpc_response=True, timeout=3, **kwargs):
        """
        Run the RPC call.

        Args:
            method: The method to call.
            args: The arguments to pass to the method.
            wait_for_rpc_response: Whether to wait for the RPC response.
            kwargs: The keyword arguments to pass to the method.

        Returns:
            The result of the RPC call.
        """
        request_id = str(uuid.uuid4())
        rpc_msg = messages.GUIInstructionMessage(
            action=method,
            parameter={"args": args, "kwargs": kwargs, "gui_id": self._gui_id},
            metadata={"request_id": request_id},
        )

        # pylint: disable=protected-access
        receiver = self._root._gui_id
        if wait_for_rpc_response:
            self._rpc_response = None
            self._msg_wait_event.clear()
            self._client.connector.register(
                MessageEndpoints.gui_instruction_response(request_id),
                cb=self._on_rpc_response,
                parent=self,
            )

        self._client.connector.set_and_publish(MessageEndpoints.gui_instructions(receiver), rpc_msg)

        if wait_for_rpc_response:
            try:
                finished = self._msg_wait_event.wait(10)
                if not finished:
                    raise RPCResponseTimeoutError(request_id, timeout)
            finally:
                self._msg_wait_event.clear()
                self._client.connector.unregister(
                    MessageEndpoints.gui_instruction_response(request_id), cb=self._on_rpc_response
                )
            # get class name
            if not self._rpc_response.accepted:
                raise ValueError(self._rpc_response.message["error"])
            msg_result = self._rpc_response.message.get("result")
            self._rpc_response = None
            return self._create_widget_from_msg_result(msg_result)

    @staticmethod
    def _on_rpc_response(msg: MessageObject, parent: RPCBase) -> None:
        msg = msg.value
        parent._msg_wait_event.set()
        parent._rpc_response = msg

    def _create_widget_from_msg_result(self, msg_result):
        if msg_result is None:
            return None
        if isinstance(msg_result, list):
            return [self._create_widget_from_msg_result(res) for res in msg_result]
        if isinstance(msg_result, dict):
            if "__rpc__" not in msg_result:
                return {
                    key: self._create_widget_from_msg_result(val) for key, val in msg_result.items()
                }
            cls = msg_result.pop("widget_class", None)
            msg_result.pop("__rpc__", None)

            if not cls:
                return msg_result

            cls = getattr(client, cls)
            # print(msg_result)
            return cls(parent=self, **msg_result)
        return msg_result

    def gui_is_alive(self):
        """
        Check if the GUI is alive.
        """
        heart = self._client.connector.get(MessageEndpoints.gui_heartbeat(self._root._gui_id))
        if heart is None:
            return False
        if heart.status == messages.BECStatus.RUNNING:
            return True
        return False
