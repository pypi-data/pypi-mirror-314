import queue
from threading import Lock, Timer
import threading
from typing import Any, Callable, Dict, List

from modelmetry import openapi
from modelmetry.observability.ingest import build_ingest_batch_from_traces
from modelmetry.observability.trace import Trace
import sys

from modelmetry.openapi import (
    AuthenticatedClient,
    IngestSignalsV1RequestBody,
)
from modelmetry.openapi.api.default import ingest_signals_v1


class FlushManager:
    def __init__(
        self,
        client: AuthenticatedClient,
        on_failure: Callable[[List[Trace], Exception], None],
        on_flushed: Callable[[List[Trace]], None],
    ):
        self.client = client
        self._running = True
        self.queue = queue.Queue()
        self.on_failure = on_failure
        self.on_flushed = on_flushed
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()

    def process(self, list_of_traces: List[Trace]):
        self.queue.put(list_of_traces)

    def _worker(self):
        while self._running or not self.queue.empty():
            try:
                list_of_traces = self.queue.get(timeout=1)  # Wait for 1 second
                batch = build_ingest_batch_from_traces(list_of_traces)
                self._send_batch(batch)
                self.on_flushed(list_of_traces)
                self.queue.task_done()

            except queue.Empty:
                continue  # If queue is empty, continue the loop

            except Exception as e:
                print(
                    f"Error sending traces: {e} / {type(e)}"
                )  # also show the typeof the erorr
                self.on_failure(list_of_traces, e)
                self.queue.task_done()

    def _send_batch(self, batch: IngestSignalsV1RequestBody):
        with self.client as client:
            try:
                ingest_signals_v1.sync_detailed(client=client, body=batch)
            except Exception as e:
                raise e

    def shutdown(self):
        self._running = False

        if self.queue.empty():
            # print("FlushManager.shutdown queue is empty, returning")
            return

        self.worker_thread.join(timeout=2)

        if self.worker_thread.is_alive():
            pass
            # print("Warning: Worker thread did not exit cleanly")


class ObservabilityClient:
    tenant_id: str = None
    client: AuthenticatedClient = None

    traces: List[Trace] = []
    in_transit: Dict[str, Trace] = {}

    traces_lock: Lock = None
    flush_manager: FlushManager = None
    flush_interval: int = None
    flush_timer: Timer = None
    max_size_kb: int = 5

    on_flush_success_callback: Callable[[List[Trace]], None] = None
    on_flush_failure_callback: Callable[[List[Trace], Exception], None] = None

    def __init__(
        self,
        # backend
        api_key: str,
        tenant_id: str,
        host: str = None,
        # opts
        max_size_kb: int = None,
        flush_interval: int = None,
        on_flush_success_callback: Callable[[List[Trace]], None] = None,
        on_flush_failure_callback: Callable[[List[Trace], Exception], None] = None,
    ) -> None:
        self.tenant_id = tenant_id
        self.traces = []
        self.max_size_kb = max_size_kb
        self.flush_interval = flush_interval

        self.client = AuthenticatedClient(
            base_url=host,
            token=api_key,
            auth_header_name="X-API-Key",
            prefix="",
        )

        # Initialize the flushing mechanism
        self.traces_lock = threading.Lock()
        self.task_manager = FlushManager(
            client=self.client,
            on_failure=self._on_batch_failure,
            on_flushed=self._on_batch_flushed,
        )
        self.flush_timer = threading.Timer(self.flush_interval, self._timed_flush)
        self.flush_timer.start()

        self.on_flush_success_callback = on_flush_success_callback
        self.on_flush_failure_callback = on_flush_failure_callback

    def flush_batch(self, traces_to_flush: List[Trace]):
        batch = []

        with self.traces_lock:
            # select the traces that have ended to transit
            ready_traces = [
                t
                for t in traces_to_flush
                if t.has_ended() and not self.in_transit.get(t.xid)
            ]

            for trace in ready_traces:
                # mark them as in transit
                self.in_transit[trace.xid] = trace
                # remove them from the list of traces to be flushed
                self.traces.remove(trace)
                # add the traces to the batch, if they have ended and are not currently in transit
                batch.append(trace)

        if batch:
            self.task_manager.process(batch)

    def _timed_flush(self):
        self.flush_timer.cancel()
        if self.traces:
            self.flush_batch(self.traces)
        self.flush_timer = threading.Timer(self.flush_interval, self._timed_flush)
        self.flush_timer.start()

    def _on_batch_flushed(self, flushed_traces: List[Trace]):
        # with self.traces_lock:
        for trace in flushed_traces:
            del self.in_transit[trace.xid]
        if self.on_flush_success_callback:
            self.on_flush_success_callback(flushed_traces)

    def _on_batch_failure(self, failed_traces: List[Trace], problem: Exception):
        print(f"_on_batch_failure: {problem} / {type(problem)}")
        # with self.traces_lock:
        self.traces.extend(failed_traces)
        if self.on_flush_failure_callback:
            self.on_flush_failure_callback(failed_traces, problem)

    def flush_all(self):
        self.flush_batch(self.traces)

    def flush_sync(self):
        self.flush_all()
        self.task_manager.queue.join()

    def shutdown(self):
        self.flush_timer.cancel()
        self.flush_sync()
        self.task_manager.shutdown()
        self.traces_lock = None

    def get_traces(self) -> List[Trace]:
        return self.traces

    def get_in_transit(self) -> Dict[str, Trace]:
        return self.in_transit

    def trace(self, name: str, metadata: Dict[str, Any] = None) -> Trace:
        trace = Trace(name=name, tenant_id=self.tenant_id, metadata=metadata)
        self.traces.append(trace)
        return trace

    def get_queued_traces(self) -> List[Trace]:
        return [
            t for t in self.traces if t.has_ended() and not self.in_transit.get(t.xid)
        ]

    def calculate_kilobyte_size(self, anything: Any) -> int:
        return sys.getsizeof(anything) // 1024
