from haizelabs.logger.types import SpanType, LogBase, Span, Trace
from haizelabs_api import HaizeLabs as HaizeLabsAPI
from typing import Callable, List, Optional
from threading import Thread, Event, RLock

from contextlib import contextmanager
from queue import Empty, Queue
from functools import wraps

import contextvars
import inspect
import signal
import atexit
import json
import uuid
import sys
import os


class BackgroundLogger:
    def __init__(
        self, base_url: Optional[str] = None, batch_size: int = 16, api_key: str = ""
    ):
        self.batch_size = batch_size
        self._queue: Queue = Queue()
        self._submission_thread: Thread = Thread(target=self.submit_logs, daemon=True)
        self._started = False
        self._start_thread_lock = RLock()
        self._is_shutdown: Event = Event()

        self.api_key = api_key
        self.base_url = base_url
        self.api_client = HaizeLabsAPI(base_url=base_url)

        signal.signal(signal.SIGINT, self.handle_signal)
        signal.signal(signal.SIGTERM, self.handle_signal)
        atexit.register(self.shutdown)

    def _start(self):
        if not self._started:
            with self._start_thread_lock:
                if not self._started:
                    self._submission_thread.start()
                    self._started = True

    def handle_signal(self, signum, frame):
        self.shutdown()

    def log(self, log: LogBase):
        self._start()
        try:
            self._queue.put_nowait(log)
        except:
            # TODO: catch errors
            ...

    # TODO: normal logging here
    def _log_input(self, log: LogBase):
        headers = {"x-api-key": self.api_key}
        try:
            self.api_client.monitoring.log(**log.model_dump(), extra_headers=headers)
        except Exception as e:
            print(f"Error logging span: {str(e)}")
            # TODO: retry logic

    def submit_logs(self):
        while not self._is_shutdown.is_set():
            batch_logs: List[LogBase] = []
            while len(batch_logs) < self.batch_size:
                try:
                    log = self._queue.get(block=False)
                except Empty:
                    break
                else:
                    batch_logs.append(log)

            if batch_logs:
                for log in batch_logs:
                    self._log_input(log)

    def shutdown(self):
        if not self._started:
            try:
                sys.exit(0)
            except SystemExit:
                ...
        if not self._is_shutdown.is_set():
            self._is_shutdown.set()
            while not self._queue.empty():
                try:
                    log = self._queue.get_nowait()
                    self._log_input(log)
                except Empty:
                    break
        if self._submission_thread.is_alive():
            self._submission_thread.join()


def load_logger(batch_size=16):
    api_url = os.environ.get("HAIZE_LABS_BASE_URL", "https://api.haizelabs.com")
    api_key = os.environ.get("HAIZE_LABS_API_KEY")

    if api_key is None:
        raise Exception(
            "HAIZE_LABS_API_KEY not found. Generate an api key on https://platform.haizelabs.com/app/settings and save as HAIZE_API_KEY in your enviornment"
        )

    _logger = BackgroundLogger(base_url=api_url, batch_size=batch_size, api_key=api_key)
    return _logger


def _get_default_args(func: Callable):
    defaults = inspect.getfullargspec(func).defaults

    if not defaults:
        return {}

    args = inspect.getfullargspec(func).args
    return dict(zip(args[-len(defaults) :], defaults))


def _generate_id():
    return uuid.uuid4().hex


class _Tracer:
    def __init__(self):
        self._background_logger: BackgroundLogger = load_logger()
        self._current_span: contextvars.ContextVar[Span] = contextvars.ContextVar(
            "current_span", default=Span(name="root")
        )

        self._root_id_lock = RLock()
        self._root_token: contextvars.Token = None
        self.root_id: Optional[str] = None

    def log(self, log: LogBase):
        self._background_logger.log(log)

    def _prepare_outputs(self, ret):
        output = ret
        try:
            json.dumps(ret)
        except Exception as e:
            output = ""

        return output

    def _prepare_inputs(self, func_sig, func_args, func_kwargs, default_args):
        bound_args = func_sig.bind(*func_args, **func_kwargs).arguments
        serialized = {**default_args, **bound_args}
        try:
            json.dumps(serialized)
        except Exception as e:
            serialized = ""

        return serialized

    def get_current_span(self, name: str):
        span = self._current_span.get()
        if span.name == "root" and not self.root_id:
            with self._root_id_lock:
                span.id = _generate_id()
                span.trace_id = _generate_id()
                self.root_id = span.id
        return span.create_child(name)

    @contextmanager
    def trace(self, name: str, log_trace: bool = True):
        span = self.get_current_span(name)
        token = self._current_span.set(span)

        span.set_token(token)
        span.begin()
        yield span
        span.finish()

        if span.parent_id == self.root_id:
            span.parent_id = None
            trace = Trace.create_from_span(span)
            if log_trace:
                self.log(trace)
            self.root_id = None

        if log_trace:
            self.log(span)
            self.log(span.content)

        try:
            self._current_span.reset(span.get_token())
        except:
            ...
        span.reset_token()


def reset_tracer():
    global _tracer
    _tracer = _Tracer()


reset_tracer()


def get_tracer() -> _Tracer:
    return _tracer


def trace(
    name: Optional[str] = None,
    log_trace=True,
    span_type: SpanType = SpanType.APP,
):
    def decorator(func: Callable):
        sig = inspect.signature(func)
        default_args = _get_default_args(func)

        @wraps(func)
        def wrapper_sync(*args, **kwargs):
            with _tracer.trace(name, log_trace) as span:
                f_inputs = _tracer._prepare_inputs(sig, args, kwargs, default_args)
                ret = func(*args, **kwargs)
                f_outputs = _tracer._prepare_outputs(ret)
                span.span_type = span_type
                span.set_input(f_inputs)
                span.set_output(f_outputs)

                return ret

        @wraps(func)
        async def wrapper_async(*args, **kwargs):
            with _tracer.trace(name, log_trace) as span:
                f_inputs = _tracer._prepare_inputs(sig, args, kwargs, default_args)
                ret = await func(*args, **kwargs)
                f_outputs = _tracer._prepare_outputs(ret)
                span.span_type = span_type
                span.set_input(f_inputs)
                span.set_output(f_outputs)

                return ret

        if not log_trace:
            return func

        if inspect.iscoroutinefunction(func):
            return wrapper_async
        else:
            return wrapper_sync

    return decorator
