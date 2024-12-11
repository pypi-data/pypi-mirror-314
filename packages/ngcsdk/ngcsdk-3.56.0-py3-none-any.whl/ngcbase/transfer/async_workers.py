#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from abc import ABC, abstractmethod
import asyncio
import base64
import collections
from concurrent.futures import ProcessPoolExecutor
from contextlib import asynccontextmanager
import functools
import hashlib
import json
import logging
import math
import multiprocessing
import os
import signal
import ssl
import sys
import threading
import time
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Dict,
    Generic,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)
import warnings

import aiofiles
import aiohttp
import certifi
import charset_normalizer
from opentelemetry import trace
from opentelemetry.instrumentation.asyncio import AsyncioInstrumentor

from ngcbase.api.utils import add_scheme
from ngcbase.constants import UMASK_GROUP_OTHERS_READ_EXECUTE
from ngcbase.environ import (
    NGC_CLI_MAX_CONCURRENCY,
    NGC_CLI_PROGRESS_UPDATE_FREQUENCY,
    NGC_CLI_TRANSFER_CHUNK_SIZE,
    NGC_CLI_UPLOAD_RETRIES,
)
from ngcbase.errors import NgcException
from ngcbase.tracing import GetTracer
from ngcbase.transfer.utils import (
    async_retry,
    bitmask_clear_bit,
    bitmask_get_set_bits,
    bitmask_is_bit_set,
    bitmask_set_bit_in_size,
    get_full_paths,
    get_sha256_file_checksum,
    log_debug,
    sanitize_path,
    use_noncanonical_url,
)
from ngcbase.util.file_utils import get_cli_config_dir, mkdir_path
from ngcbase.util.utils import format_org_team, get_current_user_version, MaskGranter

TRANSFER_CONNECTION_TIMEOUT = 30
TRANSFER_RETRY_EXCEPTIONS = (aiohttp.ClientError, asyncio.TimeoutError, OSError)

# contractral constant, cannot be modified without agreement
PARTITION_SIZE = 500000000
MAX_FILE_SIZE_LIMIT = 5 * 1024 * 1024 * 1024 * 1024  # 5TB

NGC_CONTENT_TYPE = "application/json"
ENDPOINT_VERSION = "v2"

# This line instruments aiohttp client sessions and requests, enabling tracing functionality.
# It adds default trace configuration options to all aiohttp requests
# AioHttpClientInstrumentor().instrument() #opentelemetry#instrumentation#aiohttp_client#AioHttpClientInstrumentor


# This line instruments all asyncio functions, enabling tracing without the need to pass a tracer explicitly.
# In asyncio workers, where different contexts may exist for the overall execution and individual worker tasks,
# this instrumentation ensures that tracing captures and respects the distinct contexts of each worker's execution.
AsyncioInstrumentor().instrument()
logger = logging.getLogger(__name__)

NodeT = TypeVar("NodeT", bound="BaseFileNode")


class ModelVersionIntegrityError(Exception):
    """Error when a model version gets a mixed encryption scheme due to rollbacks."""


class AsyncTransferProgress:
    """Tracks the state of a file during async transfer.

    Track overall transfer progress for a transfer, providing safe async updates and callback
    at a specified maximum update rate.
    """

    def __init__(
        self,
        completed_bytes: int = 0,
        failed_bytes: int = 0,
        total_bytes: int = 0,
        completed_count: int = 0,
        failed_count: int = 0,
        total_count: int = 0,
        callback_func: Optional[  # pylint: disable=unsubscriptable-object
            Callable[[int, int, int, int, int, int], Any]
        ] = None,
        update_rate=NGC_CLI_PROGRESS_UPDATE_FREQUENCY,
    ):
        """Initialize the AsyncTransferProgress instance.

        Args:
            completed_bytes (int): The number of completed bytes.
            failed_bytes (int): The number of failed bytes.
            total_bytes (int): The total number of bytes.
            completed_count (int): The number of completed items.
            failed_count (int): The number of failed items.
            total_count (int): The total number of items.
            callback_func (Optional[Callable[[int, int, int, int, int, int], Any]]):
                A callback function that accepts six integers representing
                completed_bytes, failed_bytes, total_bytes, completed_count,
                failed_count, and total_count respectively. If provided,
                this function will be called to report progress.
                If set to None, progress updates will not be reported.
            update_rate (float): The maximum update rate for the callback function,
                in seconds. Progress updates will be reported at most once per
                this duration. Ignored if callback_func is None.

        """
        self.lock = asyncio.Lock()
        self.completed_bytes = completed_bytes
        self.failed_bytes = failed_bytes
        self.total_bytes = total_bytes
        self.completed_count = completed_count
        self.failed_count = failed_count
        self.total_count = total_count
        self.callback_func = callback_func

        self.update_rate = update_rate if callback_func else -1

    async def monitor_progress(self):
        """Update progress with configured maximum update_rate."""
        try:
            while self.callback_func:
                self.update_progress()
                await asyncio.sleep(self.update_rate)
        except asyncio.CancelledError:
            self.update_progress()

    def update_progress(self):
        """Call the update progress callback function with the current progress metrics."""
        if self.callback_func:
            self.callback_func(
                self.completed_bytes,
                self.failed_bytes,
                self.total_bytes,
                self.completed_count,
                self.failed_count,
                self.total_count,
            )

    async def advance(self, size_in_bytes: int, count: int):
        """Advance the progress by adding completed bytes and item count.

        use negatives to undo
        """
        async with self.lock:
            self.completed_bytes += size_in_bytes
            self.completed_count += count

    async def fail(self, size_in_bytes: int, count: int):
        """Update the progress by adding failed bytes and item count.

        use negatives to undo
        """
        async with self.lock:
            self.failed_bytes += size_in_bytes
            self.failed_count += count

    def read_progress(self):
        """Read the current progress metrics."""
        return (
            self.completed_bytes,
            self.failed_bytes,
            self.total_bytes,
            self.completed_count,
            self.failed_count,
            self.total_count,
        )


class BaseFileNode:  # noqa: D101
    def __init__(
        self,
        file_path: str = "",
        size: int = -1,
        ftime: float = -1.0,
        bitmask: int = -1,
    ):
        """This base file node object tracks the state of a file during transfer.

        FileNode-level asynchronous access should be handled in child classes.
        Read operations typically do not require locking, while write operations usually do.
        Users can implement their own logic for bitmask manipulation if needed.

        Args:
            file_path (str): The path to the file being tracked.
            size (int): The size of the file in bytes.
            ftime (float): A time of the file (Unix timestamp) to record for syncing.
            bitmask (int): The progress bitmask, default intepretation:
                           - 1 represents incomplete status,
                           - 0 represents complete status,
                           - A bitmask value of 0 indicates that all partitions are completed.
        """  # noqa: D401, D404
        self.lock = asyncio.Lock()

        # file metadata
        self.file_path = file_path
        self.size = size
        self.ftime = ftime

        # progress states
        self.bitmask = bitmask

        # temporay states
        # write_change is for AOF persistence
        # are there changes since load | should we persist this node
        self.write_change = False
        # has this file node caused a failure already
        self.failed = False

    @abstractmethod
    def serialize(self) -> str:
        """Serialize the instance state to a string for persistence. concrete method should choose what to persist."""

    @abstractmethod
    def is_match(self) -> bool:
        """Set condition for the instance matches the system file to ensure it is the same file."""

    @abstractmethod
    def is_sync(self) -> bool:
        """Set condition for the instance matches the system file and it is synced(same file and done)."""

    @classmethod
    def deserialize(cls, state: str):
        """Deserialize a JSON string to a file node.

        This method loads the state of the file node from a JSON string.
        """
        data = json.loads(state)
        ins = cls()
        for key, val in data.items():
            setattr(ins, key, val)
        return ins

    def is_partition_complete(self, partition_id: int) -> bool:
        """Check if a partition is completed."""
        return not bitmask_is_bit_set(self.bitmask, partition_id)

    def get_completed_size(self) -> int:
        """Provide the sum of completed partition sizes in bytes."""
        # the max(x,1) compensates for EMPTY FILE
        return max(self.size, 1) - bitmask_set_bit_in_size(self.bitmask, max(self.size, 1), PARTITION_SIZE)

    async def set_partition_complete(self, partition_id: int):
        """Mark one partition complete."""
        async with self.lock:
            self.bitmask = bitmask_clear_bit(self.bitmask, partition_id)
            self.write_change = True


class UploadFileNode(BaseFileNode):  # noqa: D101
    def __init__(
        self,
        file_path: str = "",
        size: int = -1,
        ftime: float = -1.0,
        bitmask: int = -1,
        upload_id="",
        hash="",
        hash_exist=False,
        race_flag=False,
        complete=False,
    ):
        """Initialize the upload file node with additional attributes for upload management.

        This class extends BaseFileNode to include attributes specific to upload management.

        Attributes:
            upload_id (str): Identifier set after initiating a multipart upload.
            hash (str): Hash computed by the worker for the file.
            race_flag (bool): Flag necessary to prevent racing condition when multiple producers
                              send the same workload to the consumer. Only one should succeed.
            complete (bool): Marked complete state unique to multipart upload.
        """
        super().__init__(file_path=file_path, size=size, ftime=ftime, bitmask=bitmask)
        self.upload_id = upload_id
        self.hash = hash
        self.hash_exist = hash_exist
        self.race_flag = race_flag
        self.complete = complete

    def serialize(self):
        """Convert the upload file node state to a string.

        This method converts the upload filenode states to a JSON string representation.
        Unnecessary fields are removed to conserve space in serialization.
        """
        include_fields = ["size", "ftime", "bitmask", "upload_id", "hash", "complete", "file_path"]
        state = {field: getattr(self, field) for field in include_fields}
        return json.dumps(state)

    def is_match(self) -> bool:
        """Check if the instance matches the system file to ensure it is still the same file."""
        # this is the same aws upload sync strategy
        # https://github.com/aws/aws-cli/blob/master/awscli/customizations/s3/syncstrategy/base.py#L226
        return (
            os.path.isfile(self.file_path)
            and self.size == os.path.getsize(self.file_path)
            and self.ftime == os.path.getmtime(self.file_path)
        )

    def is_sync(self) -> bool:
        """Check if the instance still matches the system file and synced with remote."""
        return self.is_match() and self.complete

    async def set_file_hash(self, hash):
        """Set the hash for the file."""
        async with self.lock:
            self.hash = hash
            self.write_change = True

    async def set_complete(self):
        """Mark the file as complete."""
        async with self.lock:
            self.complete = True
            self.write_change = True

    async def set_race_flag_once(self) -> bool:
        """Determine whether the file should be send to mark completion.

        This method determines whether the file should be send to the consumer
        for further processing. It requires a lock since multiple producers may
        concurrently attempt to send the same workload to the consumer, and the
        consumer take time to perform mark completion.

        Returns:
            bool: True if the file is not yet send to the consumer and additional action is needed,
            False if the file is already or will be send to the consumer no additional action is needed.
        """
        async with self.lock:
            should_mark_complete = bool(
                (self.bitmask == 0)  # All partitions uploaded
                and self.hash  # Hashing completed
                and (not self.complete)  # Not already marked as complete
                and (not self.race_flag)  # No other worker marking completion
            )
            if should_mark_complete:
                # Block further attempts to mark as complete
                self.race_flag = True
            return should_mark_complete

    async def set_failed_once(self) -> bool:
        """Determine whether the file should be marked as failed.

        This method determines whether the file should be marked as failed and
        further processing. It requires a lock since multiple consumers may concurrently
        attempt to fail the same file, but only one consumer should mark it as failed.

        Returns:
            bool: True if the file is marked as failed and additional action is needed,
            False if the file is already marked as failed and no additional action is needed.
        """
        async with self.lock:
            if self.failed:
                # If already marked as failed, no additional action needed
                return False
            # Mark the file as failed and perform additional action
            self.failed = True
            return True


class DownloadFileNode(BaseFileNode):
    """Placeholder class for extending type hinting and code structure.

    This class serves as a placeholder for extending type hinting and code structure.
    It will be further developed in the future.
    """

    def __init__(self):
        """Initialize the download file node."""
        raise NotImplementedError()

    def serialize(self):
        """Convert the download file node state to a string."""
        raise NotImplementedError()

    def is_match(self) -> bool:
        """Check if the instance matches the system file to ensure it is still the same file."""
        raise NotImplementedError()

    def is_sync(self) -> bool:
        """Check if the instance still matches the system file and synced with remote."""
        raise NotImplementedError()


class BaseCompletionTable(Generic[NodeT], ABC):
    """A base class for managing a completion table for file nodes during file transfer.

    The Completion table manages file nodes using a dictionary (absolute_file_path: file_node),
    tracks their state during file transfer, and provides high-level operations for managing
    file nodes, such as creating, deleting, and checking the status of file nodes.
    """

    def __init__(self, table_file_path=None):
        """Initialize the base completion table.

        Args:
            table_file_path (Optional[str]): The file path to store the table data.

        """
        self.table: Dict[str, NodeT] = {}
        self.table_file_path = table_file_path

    # High level managed file node operations
    @abstractmethod
    def create_file_node(self, file_path: str) -> NodeT:
        """Create a file node for the type of completion table.

        This method should be implemented in child classes to create a specific
        type of file node (e.g., upload or download) based on the transfer type.
        """

    def is_file_match(self, file_path: str) -> bool:
        """Check if the file path is matched with an existing file node."""
        return file_path in self.table and self.table[file_path].is_match()

    def is_file_sync(self, file_path: str) -> bool:
        """Check if the file path is synchronized with an existing file node."""
        return file_path in self.table and self.table[file_path].is_sync()

    def get_file_node(self, file_path: str) -> Union[NodeT, None]:
        """Retrieve the file node for the given file path."""
        return self.table.get(file_path, None)

    def calculate_checked_file_completion(self, file_path: str) -> Tuple[int, int]:
        """Calculate the completion status of a file with integrity check.

        This method calculates the completion status of a file by retrieving the
        file node, checking if it matches the actual file, and then return the
        completed size and completed count.
        """
        fn = self.get_file_node(file_path)
        if fn is None:
            return 0, 0
        if not fn.is_match():
            return 0, 0
        return fn.get_completed_size(), fn.is_sync() * 1

    def get_checked_file_node(self, file_path: str) -> Union[NodeT, None]:
        """Retrieve a checked file node for the given file path with integrity check.

        If the file is synced, it deletes the file node entry from table and return None.
        If the file matches but not synced, it returns the file node.
        If the file does not match or not in table, it creates and returns a new file node.
        """
        if self.is_file_match(file_path):  # filenode matches os file
            if self.is_file_sync(file_path):  # filenode synced, transfer complete
                self.delete_file_node(file_path)  # clear this entry
                return None  # transfer complete, nothing to do
            return self.get_file_node(file_path)  # return this filenode
        return self.create_file_node(file_path)  # get a new file node

    def delete_file_node(self, file_path: str):
        """Delete the file node for the given file path from the table."""
        if file_path in self.table:
            self.table.pop(file_path)

    def save_all_file_nodes(self):
        """Save all file nodes in the table to the `table_file_path` file.

        This method saves the state of all file nodes in the table to file.
        It skips nodes that do not need to write changes.

        This method is typically used during emergency stops to ensure the state
        of the table is preserved.
        """
        if self.table_file_path is None:
            return
        if self.table:  # do not create cache file on empty table
            with open(self.table_file_path, "a", encoding="utf-8") as f:
                for _, fn in self.table.items():
                    if fn.write_change:
                        f.write(fn.serialize() + "\n")
                # no cleanup, this is probably an emergency stop
            logger.debug("\nSaving progress to the resumable cache file: %s", self.table_file_path)

    async def async_save_file_node(self, file_path: str):
        """Asynchronously save a specific file node to the `table_file_path` file.

        This method saves the state of a specific file node to file asynchronously.
        It skips nodes that do not have write changes and deletes the file node after a successful write.
        This is typically used in async loop to incrementally write completed file nodes to file,
        so table size is bound.
        """
        if self.table_file_path is None:
            return
        fn = self.get_file_node(file_path)
        if fn is not None and fn.write_change:
            async with aiofiles.open(self.table_file_path, "a", encoding="utf-8") as f:
                await f.write(fn.serialize() + "\n")

            # cleanup on successful write,
            # still in async loop
            self.delete_file_node(file_path)

    def is_table_file_exist(self) -> bool:
        """Check if the `table_file_path` file exists."""
        if self.table_file_path is None:
            return False
        return os.path.isfile(self.table_file_path)

    def remove_table_file(self):
        """Remove the `table_file_path` file from the file system if it exists."""
        if (self.table_file_path is not None) and self.is_table_file_exist():
            os.remove(self.table_file_path)

    def __baseenter__(self, node_class: Type[NodeT]):
        """Handle entering the context for the completion table.

        If the completion table file path is set, this method ensures the file exists and is
        properly formatted. If the file already exists, it reads and deserializes the file
        nodes into the table. Outputting message indicating the use of a resumable cache file.
        """
        if self.table_file_path is None:
            return self
        if os.path.isfile(self.table_file_path):
            with open(self.table_file_path, "r", encoding="utf-8") as f:
                for line in f.readlines():
                    _file_node = node_class.deserialize(line)
                    # let later entries overwrite earlier entries
                    self.table[_file_node.file_path] = _file_node
        else:
            with MaskGranter(UMASK_GROUP_OTHERS_READ_EXECUTE):
                mkdir_path(os.path.dirname(self.table_file_path))
                open(self.table_file_path, "w", encoding="utf-8").close()

        logger.debug("\nUsing resumable cache file: %s", self.table_file_path)
        return self

    def __exit__(self, exec_type, exc_val, exc_tb):
        """Handle exiting the context for the completion table.

        Saves all file nodes in the completion table to the file when the context is exited.
        """
        self.save_all_file_nodes()


class UploadCompletionTable(BaseCompletionTable[UploadFileNode]):
    """A class for managing the upload completion table for file nodes during file upload.

    This class specializes the BaseCompletionTable for managing upload-specific file nodes.
    """

    def create_file_node(self, fp) -> UploadFileNode:
        """Create an upload file node for the given file path.

        This method creates an upload file node based on the file path, size,
        last modified time, and partition count, then adds this entry to the table.
        """
        if not os.path.isfile(fp):
            # normal workflow should never get here
            raise NgcException(f"File path: {fp} which used to create file index is invalid.")

        _file_size = os.path.getsize(fp)
        #  EMPTY FILE gets 1 partition
        number_of_file_partitions = max(math.ceil(_file_size / PARTITION_SIZE), 1)

        self.table[fp] = UploadFileNode(
            file_path=fp, size=_file_size, ftime=os.path.getmtime(fp), bitmask=2**number_of_file_partitions - 1
        )
        return self.table[fp]

    def __enter__(self):
        """Load the table of upload file nodes from the `table_file_path` file."""
        return super().__baseenter__(UploadFileNode)


class DownloadCompletionTable(BaseCompletionTable[DownloadFileNode]):
    """A class for managing the download completion table for file nodes during file download.

    This class specializes the BaseCompletionTable for managing download-specific file nodes.
    """

    def create_file_node(self, fp) -> DownloadFileNode:
        """Create a download file node for the given file path."""
        raise NotImplementedError()

    def __enter__(self):
        """Load the table of download file nodes from the `table_file_path` file."""
        return super().__baseenter__(DownloadFileNode)


class AsyncTransferWorkerPoolBase(ABC):
    """Base class for managing a pool of asynchronous transfer workers.

    This abstract base class defines the structure and common functionality
    for a worker pool that perform asynchronous file transfers. It handles
    the initialization of worker attributes, including artifact details,
    local directory, worker count, and coordination tables. All workers of
    the same worker type are coroutines of the same function.
    """

    def __init__(
        self,
        api_client,
        artifact_type: str,
        artifact_org: str,
        artifact_team: str,
        artifact_name: str,
        artifact_version: str,
        local_dir: str,
        worker_count: int,
        c_table: BaseCompletionTable,
        progress: AsyncTransferProgress,
    ):
        self.consumers = []
        self.api_client = api_client

        # every worker is going to get access to all the resources
        # writables should ensure safety

        # read-only
        self.artifact_type = artifact_type
        self.artifact_org = artifact_org
        self.artifact_team = artifact_team
        self.artifact_name = artifact_name
        self.artifact_version = artifact_version

        self.local_dir = local_dir
        self.worker_count = worker_count

        # writables/executables cordinations required
        self.c_table = c_table
        self.progress = progress

        self.queue: asyncio.Queue
        self.auth_lock: asyncio.Lock
        self.executor: ProcessPoolExecutor
        self.session: aiohttp.ClientSession
        self.tracer = trace.get_tracer(__name__)
        self.future_exception: Optional[asyncio.Future] = None
        self.base_url = add_scheme(self.api_client.config.base_url)

    @property
    @abstractmethod
    def worker_type(self) -> str:
        """Abstract read-only property that must be implemented by subclasses."""

    async def make_auth_headers(self):
        """Create authentication headers for API requests."""
        async with self.auth_lock:
            return self.api_client.authentication.auth_header(auth_org=self.artifact_org, auth_team=self.artifact_team)

    async def file_reader(
        self, file_path: str, start: int, end: int, mutable_progress_buffer: List[int]
    ) -> AsyncGenerator[bytes, None]:
        """Read a file asynchronously in chunks."""
        _loop, _mod = divmod(end - start, NGC_CLI_TRANSFER_CHUNK_SIZE)
        try:
            async with aiofiles.open(file_path, "rb", buffering=0) as f:
                await f.seek(start)
                for _ in range(_loop):
                    yield await f.read(NGC_CLI_TRANSFER_CHUNK_SIZE)
                    await self.progress.advance(NGC_CLI_TRANSFER_CHUNK_SIZE, 0)
                    mutable_progress_buffer[0] += NGC_CLI_TRANSFER_CHUNK_SIZE
                yield await f.read(_mod)
                await self.progress.advance(_mod, 0)
                mutable_progress_buffer[0] += _mod
        except asyncio.CancelledError:
            await f.close()
            log_debug(self.worker_type, "cancel", f"canceled file_reader {file_path,start,end}, reraise")
            raise

    async def fetch_workload(self) -> Tuple[Any, ...]:
        """Fetch a workload from the queue."""
        x = await self.queue.get()
        return x

    async def fetch_workload_batch(self, batch_timeout=0.25, batch_size=100):
        """Fetch workloads from the queue, until times out or size full."""
        workloads = []
        try:
            _start_time = asyncio.get_event_loop().time()
            while len(workloads) < batch_size:
                _remain_time = batch_timeout - (asyncio.get_event_loop().time() - _start_time)
                if _remain_time <= 0:
                    break
                _workload = await asyncio.wait_for(self.queue.get(), timeout=_remain_time)
                if _workload:
                    workloads.append(_workload)
        except asyncio.TimeoutError:
            pass  # Expected timeout, get workloads

        return workloads

    async def dispatch_workload(self, workload: Tuple[Any, ...]):
        """Dispatch a workload to consumer workerpools' queue."""
        if not self.consumers:
            raise NgcException(f"{self.worker_type} is a leaf in the consumer tree.")
        for consumer in self.consumers:
            await consumer.queue.put(workload)
            log_debug(
                self.worker_type,
                "queue",
                f"Queue to {consumer.worker_type} workload: [{workload}]",
            )

    @abstractmethod
    async def process_workload(self, trace_scope: trace.Span):
        """Process a workload.

        Abstract method that must be implemented by subclasses to define how
        a workload should be processed. This method represents the core
        long-running work function for the worker.
        """

    async def long_running_work(self, worker_name, parent):
        """Execute long-running work for a worker.

        Continuously fetches and processes workloads in an infinite loop until
        cancelled. Handles cancellation and other exceptions appropriately.
        Worker pools do not cancel by themselves, cancel after queue join
        to allow workloads to complete.
        """
        try:
            while True:
                with self.tracer.start_as_current_span(
                    worker_name, context=trace.set_span_in_context(parent)
                ) as trace_scope:
                    await self.process_workload(trace_scope)
        except asyncio.CancelledError:
            log_debug(f"{self.worker_type}", "exception", f"canceled worker {worker_name}, no reraise.")

        except Exception as e:
            log_debug(f"{self.worker_type}", "exception", f"{str(e)}--{type(e)}")
            raise e

    @staticmethod
    def get_upload_url(org: str, team: str):
        """Generate the URL for file uploads."""
        parts = [ENDPOINT_VERSION, format_org_team(org, team), "files/multipart"]
        return "/".join([part for part in parts if part])

    @staticmethod
    def get_file_url(org: str, team: str, artifact_type: str, name: str, ver: str, rel_path: str):
        """Generate the URL for accessing a file."""
        parts = [ENDPOINT_VERSION, format_org_team(org, team), artifact_type, name, "versions", ver, "files", rel_path]
        return "/".join([part for part in parts if part])

    @staticmethod
    def get_is_hash_exist_url(org: str, team: str, artifact_type: str):
        """Generate the URL for checking if a file checksum already exist.

        v2/org/org/[team/team/][models|resources]/files
        """
        parts = [ENDPOINT_VERSION, format_org_team(org, team), artifact_type, "files"]
        return "/".join([part for part in parts if part])

    @staticmethod
    def get_file_commit_url(org: str, team: str):
        """Generate the URL for commit files to an artifact version.

        v2/org/org/[team/team]/files/commit
        """
        parts = [ENDPOINT_VERSION, format_org_team(org, team), "files/commit"]
        return "/".join([part for part in parts if part])


class AsyncFilePreSignUrlWorkerPool(AsyncTransferWorkerPoolBase):
    """Handle the generation of pre-signed URLs for file uploads in an asynchronous worker pool.

    This class extends AsyncTransferWorkerPoolBase and is responsible for obtaining pre-signed URLs necessary for
    clients to upload files directly to AWS s3 without further authentication.
    """

    def __init__(
        self,
        api_client,
        artifact_type: str,
        artifact_org: str,
        artifact_team: str,
        artifact_name: str,
        artifact_version: str,
        local_dir: str,
        worker_count: int,
        c_table: UploadCompletionTable,
        progress: AsyncTransferProgress,
    ):
        super().__init__(
            api_client,
            artifact_type,
            artifact_org,
            artifact_team,
            artifact_name,
            artifact_version,
            local_dir,
            worker_count,
            c_table,
            progress,
        )
        self.queue: asyncio.Queue[Tuple[str]]

    @property
    def worker_type(self) -> str:
        """Return the type of worker."""
        return "file-worker"

    async def process_workload(self, trace_scope: trace.Span):
        """Process a workload by generating pre-signed URLs for file parts.

        Extracts a file path from the workload and retrieves its progress from completion table.
        If all file parts are uploaded, it skips processing.
        Otherwise, it requests pre-signed URLs for the incomplete parts and dispatches
        pre-signed URLs to cusomer worker pool (upload-worker) queue.
        """
        (file_path,) = await self.fetch_workload()
        trace_scope.set_attribute("file_path", file_path)

        file_node = self.c_table.get_file_node(file_path)
        assert file_node is not None

        # If all file partitions are uploaded, nothing to do by this worker
        # If this file needs to be marked complete, hash worker will send it
        if file_node.bitmask == 0:
            log_debug(self.worker_type, "complete", f"{file_path} all parts uploaded,omit here in pre-sign-url-request")

        # If not all file partitions are upload,
        # get uncompleted part_numbers and request pre-signed urls for partnumbers only
        else:
            part_numbers = [  # part numbers are 1 indexed
                idx + 1
                for idx in bitmask_get_set_bits(file_node.bitmask, max(math.ceil(file_node.size / PARTITION_SIZE), 1))
            ]  # the max(x,0) compensates for empty files
            try:
                resp_json = await self._request_file_upload_urls(
                    file_path, file_node.size, file_node.upload_id, part_numbers
                )
                # Async GAP on resume: If only requested pre-signed urls but got interrupted here. No impact.
                # On resume, it is ok to forget the old upload_id and request a new one.
                # Partially uploaded, it is ok to request new pre-signed urls for incompleted partitions.
                urls = resp_json["urls"]
                upload_id = resp_json["uploadID"]
                file_node.upload_id = upload_id
                for idx, url in zip(part_numbers, urls):
                    await self.dispatch_workload((file_path, idx - 1, url))  # response partnumbers are also 1 indexed

            except aiohttp.ClientError:
                _failed_size_in_bytes = bitmask_set_bit_in_size(file_node.bitmask, file_node.size, PARTITION_SIZE)
                # fail only incompleted size if fails at this worker
                await self.progress.fail(_failed_size_in_bytes, 1)
                log_debug(
                    self.worker_type,
                    "failure",
                    f"{file_path} request_file_upload_urls failed, mark failure",
                )
        self.queue.task_done()

    @async_retry(exception_to_check=TRANSFER_RETRY_EXCEPTIONS, tries=NGC_CLI_UPLOAD_RETRIES, delay=500, backoff=2)
    async def _request_file_upload_urls(
        self, file_path: str, size: int, upload_id: Union[str, None], part_numbers: List[int]
    ) -> Dict[str, Union[str, List[str]]]:
        """Request pre-signed URLs for file uploads.

        Sends an HTTP POST request to obtain pre-signed URLs for uploading file parts,
        by agreed parition size PARTITION_SIZE.
        The request includes details such as the file path, size, upload ID, and part numbers.
        """
        body = {
            "name": self.artifact_name,
            "version": self.artifact_version,
            "artifactType": self.artifact_type,
            "filePath": os.path.relpath(file_path, self.local_dir),
            "size": size,
        }
        if upload_id:  # resuming an upload
            body["uploadID"] = upload_id
            if part_numbers:  # provide partitions IDs 1-indexed
                body["partNumberList"] = part_numbers

        url = self.base_url + "/" + self.get_upload_url(self.artifact_org, self.artifact_team)
        response = await self.session.post(
            url=url,
            json=body,
            headers=await self.make_auth_headers(),
        )
        log_debug(
            self.worker_type,
            "_request_file_upload_urls",
            f"{response.status} - {file_path}, {upload_id}, {self.artifact_type} ",
        )
        resp_json = await response.json(content_type=NGC_CONTENT_TYPE)
        log_debug(
            self.worker_type,
            "_request_file_upload_urls",
            f"{response.status} - {file_path} - response: " + str(resp_json),
        )

        response.raise_for_status()
        return resp_json


class AsyncFileExistCheckWorkerPool(AsyncTransferWorkerPoolBase):
    """Check if batche file hashes already exist in the registry.

    This class extends AsyncTransferWorkerPoolBase and is responsible for checking if a file hash is already existed
    so downstream workers can skip uploading this file.
    """

    def __init__(
        self,
        api_client,
        artifact_type: str,
        artifact_org: str,
        artifact_team: str,
        artifact_name: str,
        artifact_version: str,
        local_dir: str,
        worker_count: int,
        c_table: UploadCompletionTable,
        progress: AsyncTransferProgress,
    ):
        super().__init__(
            api_client,
            artifact_type,
            artifact_org,
            artifact_team,
            artifact_name,
            artifact_version,
            local_dir,
            worker_count,
            c_table,
            progress,
        )
        self.queue: asyncio.Queue[Tuple[str]]

    @property
    def worker_type(self) -> str:
        """Return the type of worker."""
        return "file-exist-batch-worker"

    async def process_workload(self, trace_scope: trace.Span):
        """Process one or more workload that already has checksum to determine if their hash already in registry.

        Extracts one or more file path from the workload and check if the file content is already in registry.

        If file hash already in registry, set file node flag, no upload is required.
        Otherwise, queue to request pre-signed url work queue.
        """
        # since all workload needs to be eventually dispatched, perform the neccessary steps for hash existing cases
        workload_list = await self.fetch_workload_batch()
        hash_to_filepath_map: Dict[str, Tuple[str, int]] = {}  # request and response does not contain file path
        for file_path_tuple in workload_list:
            file_node = self.c_table.get_file_node(file_path_tuple[0])
            assert file_node is not None
            if not file_node.hash_exist:
                # check previously not existing hash
                # check newly calculated hash
                hash_to_filepath_map[file_node.hash] = (file_path_tuple[0], file_node.size)

        if hash_to_filepath_map:
            trace_scope.set_attribute("hash_count", len(hash_to_filepath_map))
            responsed_file_list = await self._request_check_if_hash_exists(list(hash_to_filepath_map.keys()))
            for file in responsed_file_list["files"]:
                if file["exists"]:
                    file_path, size = hash_to_filepath_map[file["sha256"]]
                    if size == file["size"]:
                        file_node = self.c_table.get_file_node(file_path)
                        assert file_node is not None
                        file_node.hash_exist = True
                        file_node.write_change = True

        # all remaining needs to be uploaded
        for file_path_tuple in workload_list:
            await self.dispatch_workload(file_path_tuple)
            self.queue.task_done()

    @async_retry(exception_to_check=TRANSFER_RETRY_EXCEPTIONS, tries=NGC_CLI_UPLOAD_RETRIES, delay=500, backoff=2)
    async def _request_check_if_hash_exists(self, hashes: List[str]):
        url = (
            self.base_url + "/" + self.get_is_hash_exist_url(self.artifact_org, self.artifact_team, self.artifact_type)
        )
        body = {"files": [{"sha256": h} for h in hashes]}
        response = await self.session.post(
            url=url,
            json=body,
            headers=await self.make_auth_headers(),
        )
        log_debug(
            self.worker_type,
            "_request_check_if_hash_exists",
            f"{response.status} head 5 hashes [{hashes[:5]}] ",
        )

        resp_json = await response.json(content_type=NGC_CONTENT_TYPE)
        log_debug(
            self.worker_type,
            "_request_check_if_hash_exists",
            f"{response.status} - response: " + str(resp_json),
        )

        response.raise_for_status()
        return resp_json


class AsyncFileS3UploadWorkerPool(AsyncTransferWorkerPoolBase):
    """Manage the direct upload of files to AWS S3 storage using pre-signed URLs.

    This class is part of the asynchronous transfer worker pool and deals with
    the actual transfer of file partitions to the cloud, managing retries
    and handling upload failures.
    """

    def __init__(
        self,
        api_client,
        artifact_type: str,
        artifact_org: str,
        artifact_team: str,
        artifact_name: str,
        artifact_version: str,
        local_dir: str,
        worker_count: int,
        c_table: UploadCompletionTable,
        progress: AsyncTransferProgress,
    ):
        super().__init__(
            api_client,
            artifact_type,
            artifact_org,
            artifact_team,
            artifact_name,
            artifact_version,
            local_dir,
            worker_count,
            c_table,
            progress,
        )

        self.c_table: UploadCompletionTable
        self.queue: asyncio.Queue[Tuple[str, int, str]]

    @property
    def worker_type(self) -> str:
        """Return the type of worker."""
        return "upload-worker"

    async def process_workload(self, trace_scope: trace.Span):
        """Process a workload by uploading a file partition to S3.

        Extracts the file path, partition index, and pre-signed URL from the workload.
        Uploads the specified partition to S3 and updates the completion table.
        Handles client errors and logs failures appropriately.
        """
        (file_path, idx, url) = await self.fetch_workload()
        trace_scope.set_attribute("file_path", file_path)
        trace_scope.set_attribute("file_partition_idx", idx)
        trace_scope.set_attribute("pre-signed url", url)

        file_node = self.c_table.get_file_node(file_path)
        assert file_node is not None
        assert bitmask_is_bit_set(file_node.bitmask, idx), "Partition already complete"

        start = PARTITION_SIZE * idx
        end = min(PARTITION_SIZE + start, file_node.size)
        try:
            await self._request_s3_upload(file_path, start, end, url)
            # Async GAP on resume: If partition is upload succeeded but interrupted here. No impact
            # It is ok to request url for this partition and reupload
            await file_node.set_partition_complete(idx)
            log_debug(
                self.worker_type,
                "complete",
                f"{file_path}:{idx} completed partition upload.",
            )
            if await file_node.set_race_flag_once():
                await self.dispatch_workload((file_path,))
        except aiohttp.ClientError as e:
            await self.progress.fail(end - start, (await file_node.set_failed_once()) * 1)
            log_debug(self.worker_type, "failure", f"{file_path}:{idx} upload failure {str(e)}")
        self.queue.task_done()

    @async_retry(
        exception_to_check=TRANSFER_RETRY_EXCEPTIONS,
        tries=NGC_CLI_UPLOAD_RETRIES,
        delay=500,
        backoff=2,
    )
    async def _request_s3_upload(self, file_path, start, end, url):
        """Upload a file partition to S3.

        Sends an HTTP PUT request to upload a range of file bytes to S3 using the provided pre-signed URL.
        Manages retries and handles HTTP errors. Incrementally advance progress, reset progress on failure.
        """
        # To ensure a responsive progress bar and accurate speed calculations,
        # we increment progress as each file chunk (not file partition) is consumed by the PUT request.
        # The file_reader() advances progress as iterator gets consumed,
        # but it cannot undo progress on PUT request termination.
        # A mutable object is used to track temporary progress, enabling reset if partition retries upload.
        # There might be better solution in the future.
        mutable_progress_buffer = [0]

        try:  # there are exceptions wont reach log
            response = await self.session.put(
                use_noncanonical_url(url),
                data=self.file_reader(file_path, start, end, mutable_progress_buffer),
                headers={"Content-Length": f"{end-start}"},
            )
            log_debug(
                self.worker_type,
                "_request_s3_upload",
                f"{response.status} - {file_path},  partition [{start},{end}], [{url}] ",
            )
            response.raise_for_status()
        except Exception as e:  # pylint: disable=broad-except
            log_debug(
                self.worker_type,
                "_request_s3_upload",
                f"upload facing [{str(e)}], undo progress for {file_path}, {mutable_progress_buffer[0]} bytes.",
            )
            await self.progress.advance(-mutable_progress_buffer[0], 0)
            raise e


def hash_file(file_path: str, cancel_event=None) -> str:
    """Calculate the SHA-256 hash of a file and returns it as a base64 encoded string.

    This function computes the SHA-256 hash of the specified file. It is designed to be
    pickleable so that it can be executed in a separate process using `run_in_executor`.
    """
    # on aynsio.task cancel, this subprocess will recieve SIGINT before we get to handle it
    # causing trace_coroutine to await an additional time
    # we want to this sub process to be terminated from main process gracefully
    # ignore sigint here and call shutdown() from main process
    if sys.platform in ("linux", "darwin"):
        signal.signal(signal.SIGINT, signal.SIG_IGN)

    sha256_bstr: bytes = get_sha256_file_checksum(file_path, canceling_event=cancel_event)
    return base64.b64encode(sha256_bstr).decode("utf-8")


class AsyncFileHashWorkerPool(AsyncTransferWorkerPoolBase):
    """Responsible for computing the hash of files utilizing multiprocessing to verify integrity post-transfer.

    This worker is part of the asynchronous transfer worker pool and uses processpoolexecutors,
    wrapped by coroutines to perform computationally intensive hashing operations
    without blocking the main asynchronous event loop.
    """

    def __init__(
        self,
        api_client,
        artifact_type: str,
        artifact_org: str,
        artifact_team: str,
        artifact_name: str,
        artifact_version: str,
        local_dir: str,
        worker_count: int,
        c_table: UploadCompletionTable,
        progress: AsyncTransferProgress,
    ):
        super().__init__(
            api_client,
            artifact_type,
            artifact_org,
            artifact_team,
            artifact_name,
            artifact_version,
            local_dir,
            worker_count,
            c_table,
            progress,
        )
        self.queue: asyncio.Queue[Tuple[str]]
        self.cancel_event: threading.Event

    @property
    def worker_type(self) -> str:
        """Return the type of worker."""
        return "hash-worker"

    async def process_workload(self, trace_scope: trace.Span):
        """Process a workload by computing the hash of a file.

        Summary:
        Extracts a file path from the workload and retrieves its progress from the completion table.
        Computes the hash of the file if it is not already computed,
        using an external executor to avoid blocking the event loop.
        Logs the completion of the hashing operation and handles race conditions with the upload worker.
        """
        (file_path,) = await self.fetch_workload()
        trace_scope.set_attribute("file_path", file_path)

        file_node = self.c_table.get_file_node(file_path)
        assert file_node is not None

        if not file_node.hash:
            loop = asyncio.get_running_loop()
            _hash = await loop.run_in_executor(self.executor, hash_file, file_path, self.cancel_event)
            # Async GAP on resume: If interrupted, restart hashing from begining of content
            # Right now hash has to be done in one go, constraint discussed in design
            file_node.hash = _hash
            file_node.write_change = True
        trace_scope.set_attribute("file_hash", file_node.hash)
        log_debug(self.worker_type, "complete", f"{file_path} completed hash {file_node.hash}")

        if await file_node.set_race_flag_once():  # race with upload worker
            await self.dispatch_workload((file_path,))  # if wins the race, this worker send to mark completion
        self.queue.task_done()


class AsyncFileCompletionWorkerPool(AsyncTransferWorkerPoolBase):
    """Responsible for marking files as complete once all transfer operations are successfully.

    This worker ensures that file states are updated to reflect their completion status in the system.
    """

    def __init__(
        self,
        api_client,
        artifact_type: str,
        artifact_org: str,
        artifact_team: str,
        artifact_name: str,
        artifact_version: str,
        local_dir: str,
        worker_count: int,
        c_table: UploadCompletionTable,
        progress: AsyncTransferProgress,
    ):
        super().__init__(
            api_client,
            artifact_type,
            artifact_org,
            artifact_team,
            artifact_name,
            artifact_version,
            local_dir,
            worker_count,
            c_table,
            progress,
        )
        self.queue: asyncio.Queue[Tuple[str]]

    @property
    def worker_type(self) -> str:
        """Return the type of worker."""
        return "completion-worker"

    async def process_workload(self, trace_scope: trace.Span):
        """Process a workload by marking a file as complete.

        Extracts the file path from the workload and retrieves its progress from the completion table.
        Marks the file as complete in the system once all parts are successfully uploaded and verified.
        """
        (file_path,) = await self.fetch_workload()
        trace_scope.set_attribute("file_path", file_path)

        file_node = self.c_table.get_file_node(file_path)
        assert file_node is not None

        try:
            await self._request_mark_complete(file_path, file_node.upload_id, file_node.hash)
            log_debug(self.worker_type, "complete", f"{file_path} done, note and pop")
            # Async GAP: If interrupted after marked complete suceeded, before writing to file node,
            # resume will retry completion, reuse the same upload_id which gets http 400 from BE
            # On http 400, check if file is already uploaded with _request_is_file_completed()
            await file_node.set_complete()
            await self.progress.advance(0, 1)
        except aiohttp.ClientError:
            await self.progress.fail(0, 1)
            log_debug(
                self.worker_type,
                "failure",
                f"{file_path} request_mark_complete failed, mark failure {file_node.upload_id}",
            )
        except ModelVersionIntegrityError as e:
            if self.future_exception and not self.future_exception.done():
                log_debug(self.worker_type, "exception", f"{file_path} upload fails, model integrity is challenged.")
                self.future_exception.set_exception(e)
            raise asyncio.CancelledError from e  # we want to exit current task by graceful cancelling.
        finally:
            await self.c_table.async_save_file_node(file_path)
            self.queue.task_done()

    @async_retry(exception_to_check=TRANSFER_RETRY_EXCEPTIONS, tries=NGC_CLI_UPLOAD_RETRIES, delay=500, backoff=2)
    async def _request_mark_complete(self, file_path, upload_id, chksum):
        """Send a request to mark a file as complete.

        Sends an HTTP PUT request to mark a file as complete for the BE to add entry. If the request fails
        with a 400 status, verifies if the file is already marked as complete.
        """
        url = self.base_url + "/" + self.get_upload_url(self.artifact_org, self.artifact_team)
        body = {
            "name": self.artifact_name,
            "version": self.artifact_version,
            "artifactType": self.artifact_type,
            "filePath": os.path.relpath(file_path, self.local_dir),
            "uploadID": upload_id,
            "sha256": chksum,
        }
        response = await self.session.put(url=url, json=body, headers=await self.make_auth_headers())
        log_debug(
            self.worker_type,
            "_request_mark_complete",
            f"{response.status} - {file_path}, {upload_id}, {self.artifact_type} " + f" [{chksum}]",
        )
        if response.status != 200:
            log_debug(
                self.worker_type,
                "_request_mark_complete",
                f"{response.status} - {file_path}, {upload_id}, {self.artifact_type}"
                + str(await response.json(content_type=NGC_CONTENT_TYPE)),
            )
            if response.status == 400:
                # see above `Async GAP`
                # make sure file is already uploaded by get_file
                return await self._request_is_file_completed(file_path)
            if response.status == 409:
                # This is an en/decryption edge case:
                # Existing files in version were uploaded in new encryption scheme,
                # but service rollsbacks cause new scheme no longer exists.
                # Ensure artifact version consistency here.
                # raise and exit to sync workflow then clean up

                raise ModelVersionIntegrityError(
                    f"{file_path}, {upload_id}, {self.artifact_type}"
                    + str(await response.json(content_type=NGC_CONTENT_TYPE))
                )
        response.raise_for_status()

    @async_retry(exception_to_check=TRANSFER_RETRY_EXCEPTIONS, tries=NGC_CLI_UPLOAD_RETRIES, delay=500, backoff=2)
    async def _request_is_file_completed(self, file_path):  # this is an edge case, not to be nested in retries
        """Verify if a file is already marked as complete.

        Sends an HTTP GET request to check if a file is downloadable(already marked as complete) in the system.
        This is used as a fallback check if the completion request fails with a 400 status.
        """
        log_debug(self.worker_type, "_request_is_file_completed", f"{file_path}")
        rel_path = os.path.relpath(file_path, self.local_dir)
        url = (
            self.base_url
            + "/"
            + self.get_file_url(
                self.artifact_org,
                self.artifact_team,
                self.artifact_type,
                self.artifact_name,
                self.artifact_version,
                rel_path,
            )
        )

        response = await self.session.get(
            url=url,
            headers=await self.make_auth_headers(),
        )
        log_debug(
            self.worker_type,
            "_request_is_file_completed",
            f"{response.status} - {file_path}, {self.artifact_type},{url}",
        )  # do not want to log response content, response content is file in binary
        response.raise_for_status()


class AsyncFileCommitWorkerPool(AsyncTransferWorkerPoolBase):
    """Responsible for commit files to artifact version.

    This worker ensures that files are commited to artifact version. Last step of file level workflow.
    """

    def __init__(
        self,
        api_client,
        artifact_type: str,
        artifact_org: str,
        artifact_team: str,
        artifact_name: str,
        artifact_version: str,
        local_dir: str,
        worker_count: int,
        c_table: UploadCompletionTable,
        progress: AsyncTransferProgress,
    ):
        super().__init__(
            api_client,
            artifact_type,
            artifact_org,
            artifact_team,
            artifact_name,
            artifact_version,
            local_dir,
            worker_count,
            c_table,
            progress,
        )
        self.queue: asyncio.Queue[Tuple[str]]

    @property
    def worker_type(self) -> str:
        """Return the type of worker."""
        return "commit-worker"

    async def process_workload(self, trace_scope: trace.Span):
        """Process a workload by marking a file as complete.

        Extracts the file path from the workload and retrieves its progress from the completion table.
        Marks the file as complete in the system once all parts are successfully uploaded and verified.
        """
        file_path_list = await self.fetch_workload_batch()
        file_path_list = [file_path_tuple[0] for file_path_tuple in file_path_list]
        trace_scope.set_attribute("file_path_list", file_path_list[:5])

        # we handle all workloads in the list here, because commited items should not reach this queue
        request_file_dicts = []
        for file_path in file_path_list:
            file_node = self.c_table.get_file_node(file_path)
            assert file_node is not None
            request_file_dicts.append(
                {
                    "commitType": "addition",
                    "filePath": os.path.relpath(file_path, self.local_dir),
                    "sha256": file_node.hash,
                }
            )
        try:
            await self._request_commit_files(request_file_dicts)
            log_debug(self.worker_type, "complete", f"{len(file_path_list)} done, note and pop")
            for file_path in file_path_list:
                await file_node.set_complete()
                await self.progress.advance(0, 1)
        except aiohttp.ClientError:
            await self.progress.fail(0, len(file_path_list))
            log_debug(
                self.worker_type,
                "failure",
                f"request_commit_files failed, mark failures for {len(file_path_list)} files.",
            )
        finally:
            for file_path in file_path_list:
                await self.c_table.async_save_file_node(file_path)
                self.queue.task_done()

    @async_retry(exception_to_check=TRANSFER_RETRY_EXCEPTIONS, tries=NGC_CLI_UPLOAD_RETRIES, delay=500, backoff=2)
    async def _request_commit_files(self, request_file_dicts):
        """Send a request to commit files to an artifact version.

        Sends an HTTP POST request to commit files to an artifact version, for the BE to add entry.
        """
        url = self.base_url + "/" + self.get_file_commit_url(self.artifact_org, self.artifact_team)
        body = {
            "name": self.artifact_name,
            "version": self.artifact_version,
            "artifactType": self.artifact_type,
            "files": request_file_dicts,
        }
        response = await self.session.post(url=url, json=body, headers=await self.make_auth_headers())
        log_debug(
            self.worker_type,
            "_request_commit_files",
            f"{response.status} - committed {len(request_file_dicts)} files. ",
        )

        if response.status != 200:
            log_debug(
                self.worker_type,
                "_request_commit_files",
                f"{response.status} - " + str(await response.json(content_type=NGC_CONTENT_TYPE)),
            )
        response.raise_for_status()


@asynccontextmanager
async def aiohttp_session_context():
    """Create an asynchronous context manager for an aiohttp ClientSession.

    This context manager configures the SSL context, TCP connector, and client timeout settings
    for the aiohttp session. It yields the created aiohttp.ClientSession to the caller.
    """
    _ssl_context = ssl.create_default_context(cafile=certifi.where())
    _connector = aiohttp.TCPConnector(ssl=_ssl_context, ttl_dns_cache=TRANSFER_CONNECTION_TIMEOUT * 100)
    _timeout = aiohttp.ClientTimeout(
        sock_connect=TRANSFER_CONNECTION_TIMEOUT,
        sock_read=TRANSFER_CONNECTION_TIMEOUT,
        total=TRANSFER_CONNECTION_TIMEOUT * 1000,
    )
    async with aiohttp.ClientSession(
        timeout=_timeout,
        connector=_connector,
        trust_env=True,
    ) as session:
        yield session


@asynccontextmanager
async def start_as_current_span_async(tracer, *args, **kwargs):
    """Create an asynchronous context manager for starting a tracing span.

    This context manager starts a new span using the provided tracer and yields the span
    to the caller. It ensures that the span is properly ended when the context is exited.
    """
    with tracer.start_as_current_span(*args, **kwargs) as span:
        yield span


class AsyncUploadWorkerManager:
    """Manages asynchronous upload process for artifacts to a s3 registry.

    Extends AsyncTransferTeamBase to handle specific logic related to uploads,
    including managing concurrency, tracking progress, and handling file resumes.
    Ensures efficient use of resources and robust error handling.
    """

    def __init__(
        self,
        source,
        artifact_type,
        artifact_org,
        artifact_team,
        artifact_name,
        artifact_version,
        operation_name,
        should_resume=True,
        progress_callback_func=None,
    ):
        super().__init__()
        self.leaders = []

        self.transfer_type = "upload"
        self.source = source
        self.source_dir = source if os.path.isdir(source) else os.path.dirname(source)

        self.artifact_type = artifact_type
        self.artifact_org = artifact_org
        self.artifact_team = artifact_team
        self.artifact_name = artifact_name
        self.artifact_version = artifact_version
        self.operation_name = operation_name

        self.should_resume = should_resume
        self.completion_table_file_path = self._get_completion_table_file_path()

        self.progress = AsyncTransferProgress(
            callback_func=progress_callback_func, update_rate=NGC_CLI_PROGRESS_UPDATE_FREQUENCY
        )
        self.c_table = UploadCompletionTable(self.completion_table_file_path)

        self.cancel_event: threading.Event

    async def signal_handler(self, loop: asyncio.AbstractEventLoop, executor: ProcessPoolExecutor):
        """Handle termination signals, shuts down the executor and event loop."""
        # https://docs.python.org/3/library/asyncio-runner.html#handling-keyboard-interruption
        # logger.info("\nTerminating, please wait.")
        if not self.cancel_event.is_set():
            self.cancel_event.set()
        log_debug(sys.platform, "signal", "signal handler intiated")
        executor.shutdown(wait=False, cancel_futures=True)
        tasks_to_cancel = [task for task in asyncio.all_tasks(loop) if task is not asyncio.current_task()]
        for task in tasks_to_cancel:
            task.cancel()

        await asyncio.gather(*tasks_to_cancel, return_exceptions=False)
        loop.stop()
        # sys.exit(1)

    def __enter__(self):
        """Enter the context manager, initializes the completion table and calculates progress."""
        self.c_table.__enter__()
        self.calculate_progress()
        return self

    def __exit__(self, exec_type, exc_val, exc_tb):
        """Handle exiting the context for the AsyncUploadWorkerManager.

        This method checks if the upload progress is complete.
        If all files have been uploaded, it removes the completion table file and output a message.
        If the upload is not complete, it delegates to the base class's __exit__ method to cleanup.
        Finally, it updates the progress to ensure progress up-to-date.
        """
        if self.progress.completed_count == self.progress.total_count:
            self.c_table.remove_table_file()
            logger.debug("\nTransfer complete, removed resumable cache file: %s", self.completion_table_file_path)
        else:
            self.c_table.__exit__(exec_type, exc_val, exc_tb)

    def _get_completion_table_file_path(self):
        """Generate a unique path for the completion table, ensures Windows compatible."""
        # we are doing this because windows system needs have file path less than 256 characters long
        root_dir = f"{get_cli_config_dir()}"
        sub_dir = "transfer-caches"
        _sha = hashlib.sha256()
        _sha.update(
            (
                f"<{self.artifact_type}-{self.transfer_type}-{get_current_user_version()}>"
                f"<{self.artifact_org}><{self.artifact_team}>"
                f"<{self.artifact_name}><{self.artifact_version}>"
                f"<{sanitize_path(self.source_dir)}>"
            ).encode()
        )
        file_name = _sha.hexdigest()[:128]
        return os.path.join(root_dir, sub_dir, file_name)

    def calculate_progress(self):
        """Calculate and updates the progress of file uploads based on the completion table."""
        for _full_path in get_full_paths(self.source):
            if _full_path == self.completion_table_file_path:
                continue
            _size, _ct = self.c_table.calculate_checked_file_completion(_full_path)
            self.progress.completed_bytes += _size
            self.progress.completed_count += _ct
            _file_size = os.path.getsize(_full_path)
            if _file_size > MAX_FILE_SIZE_LIMIT:
                raise NgcException(
                    f"File {_full_path}, exceeds maximum file size limit of {MAX_FILE_SIZE_LIMIT} bytes."
                )
            self.progress.total_bytes += _file_size
            self.progress.total_count += 1

            self.progress.update_progress()

        self.progress.update_progress()

    async def init_async_attributes(self, session, auth_lock, executor):
        """Initialize asynchronous attributes for each worker node."""
        q = collections.deque(self.leaders)
        visited = set(self.leaders)  # just in case of cycle
        while q:
            node = q.popleft()

            node.queue = asyncio.Queue(maxsize=NGC_CLI_MAX_CONCURRENCY)
            node.session = session
            node.auth_lock = auth_lock
            node.executor = executor
            for neigh in node.consumers:
                if neigh not in visited:
                    q.append(neigh)
                    visited.add(neigh)
            node.cancel_event = self.cancel_event

    async def populate_workload(self):
        """Populate the workload for each worker based on the source files and completion table."""
        # on upload resume, file nodes are loaded before this function
        #                                  Marked complete        |  did not mark complete
        # Same      file+filepath   |   (c1)skip, delete filenode |  (c2)reuse filenode,do nothing
        # Different file+filepath   |  (c3)create new filenode    |  (c4)create new filenode
        for _file_path in get_full_paths(self.source):
            # if not in record, this will create a new file_node
            if _file_path == self.completion_table_file_path:
                continue
            if self.c_table.get_checked_file_node(_file_path):
                for worker in self.leaders:
                    await worker.queue.put((_file_path,))

    def async_run(self):
        """Run the asynchronous worker tasks."""
        asyncio.run(self._start_workers())

    async def _start_workers(self):
        """Start the worker tasks and monitors their progress."""
        # reference pattern: https://docs.python.org/3/library/asyncio-queue.html#examples

        # Below is the runtimewarning suppressed on ctrl+c:
        # /opt/python/3.9.18/lib/python3.9/asyncio/unix_events.py:100:
        # RuntimeWarning: coroutine 'AsyncUploadWorkerManager.signal_handler' was never awaited
        # self._signal_handlers[sig] = handle
        # RuntimeWarning: Enable tracemalloc to get the object allocation traceback
        #
        # This warning is caused by add_signal_handler() recieved async callback and loop doesnot await it.
        # The async callback is intentional, sync callback cause each tasks to trigger the handler, vomiting output.
        # Could not easily silence this because has to pass in a single future: ensure_future.

        with multiprocessing.Manager() as m_manager:
            self.cancel_event = m_manager.Event()
            with GetTracer() as tracer:
                async with start_as_current_span_async(tracer, self.operation_name, end_on_exit=True) as parent_scope:
                    try:
                        async with aiohttp_session_context() as session:
                            with ProcessPoolExecutor(max_workers=NGC_CLI_MAX_CONCURRENCY) as executor:
                                _loop = asyncio.get_running_loop()
                                future_exception = asyncio.Future(
                                    loop=_loop
                                )  # set_exception for this future to get raised
                                if sys.platform in ("linux", "darwin"):
                                    warnings.simplefilter("ignore", RuntimeWarning)
                                    _loop.add_signal_handler(
                                        signal.SIGINT,
                                        functools.partial(asyncio.ensure_future, self.signal_handler(_loop, executor)),
                                    )
                                    _loop.add_signal_handler(
                                        signal.SIGTERM,
                                        functools.partial(asyncio.ensure_future, self.signal_handler(_loop, executor)),
                                    )
                                asyncio.set_event_loop(_loop)

                                await self.init_async_attributes(
                                    session=session, auth_lock=asyncio.Lock(), executor=executor
                                )

                                # bfs iterate all nodes
                                q = collections.deque(self.leaders)
                                _workers = []
                                _queues = []
                                visted = set(self.leaders)  # avoid cycle
                                while q:
                                    node = q.popleft()
                                    node.future_exception = future_exception
                                    for i in range(node.worker_count):
                                        _workers.append(
                                            asyncio.create_task(
                                                node.long_running_work(f"{node.worker_type}-{i}", parent_scope)
                                            )
                                        )
                                        _queues.append(node.queue)

                                    for child in node.consumers:
                                        if child not in visted:
                                            visted.add(child)
                                            q.append(child)

                                _workers.append(asyncio.create_task(self.progress.monitor_progress()))
                                _populate_workloads = asyncio.create_task(self.populate_workload())
                                _workers.append(_populate_workloads)

                                await asyncio.wait(
                                    [_populate_workloads, future_exception], return_when=asyncio.FIRST_COMPLETED
                                )
                                # An exception has been raised by one of the spanwned tasks.
                                if future_exception.done():
                                    raise future_exception.result()

                                for _queue in _queues:
                                    await _queue.join()

                                for _worker in _workers:
                                    _worker.cancel()

                                await asyncio.gather(*_workers, return_exceptions=True)
                    except asyncio.CancelledError:
                        pass


def upload_directory(
    api_client,
    source_path,
    artifact_name,
    artifact_version,
    artifact_org,
    artifact_team,
    artifact_type,
    operation_name,
    progress_callback_func: Optional[  # pylint: disable=unsubscriptable-object
        Callable[[int, int, int, int, int, int], Any]
    ] = None,
):
    """Upload source content to a specified artifact registry.

    This function manages the entire process of uploading files from a directory to a
    registry, using the AsyncUploadWorkerManager to handle concurrency, progress tracking,
    and resumable uploads. The upload process involves several worker pools, each handling
    different aspects of the upload process, such as presigning URLs, hashing files,
    uploading to S3, and marking completion.

    The function measures the total time taken for the upload and returns detailed
    progress metrics, including the number of completed and failed files and bytes.
    """
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    charset_normalizer.api.logger.setLevel(logging.INFO)
    time_started = time.monotonic()

    with AsyncUploadWorkerManager(
        source_path,
        artifact_type,
        artifact_org,
        artifact_team,
        artifact_name,
        artifact_version,
        operation_name,
        should_resume=True,
        progress_callback_func=progress_callback_func,
    ) as upload_manager:

        try:
            worker_args = {
                "api_client": api_client,
                "artifact_type": artifact_type,
                "artifact_org": artifact_org,
                "artifact_team": artifact_team,
                "artifact_name": artifact_name,
                "artifact_version": artifact_version,
                "local_dir": upload_manager.source_dir,
                "worker_count": NGC_CLI_MAX_CONCURRENCY,
                "c_table": upload_manager.c_table,
                "progress": upload_manager.progress,
            }
            file_worker_pool = AsyncFilePreSignUrlWorkerPool(**worker_args)
            upload_manager.leaders.append(file_worker_pool)

            hash_worker_pool = AsyncFileHashWorkerPool(**worker_args)
            upload_manager.leaders.append(hash_worker_pool)

            upload_worker_pool = AsyncFileS3UploadWorkerPool(**worker_args)
            file_worker_pool.consumers.append(upload_worker_pool)

            completion_worker_pool = AsyncFileCompletionWorkerPool(**worker_args)
            upload_worker_pool.consumers.append(completion_worker_pool)
            hash_worker_pool.consumers.append(completion_worker_pool)

            upload_manager.async_run()

        except KeyboardInterrupt:
            pass
        except ModelVersionIntegrityError:
            logger.debug(
                "\nTransfer integrity issue, removed resumable cache file: %s", upload_manager.c_table.table_file_path
            )
            upload_manager.c_table.table = {}
            upload_manager.c_table.remove_table_file()
            upload_manager.progress.completed_count = 0
            raise

        return (  # pylint: disable=lost-exception
            time.monotonic() - time_started,
            upload_manager.progress.completed_count,
            upload_manager.progress.completed_bytes,
            upload_manager.progress.failed_count,
            upload_manager.progress.total_bytes,
            upload_manager.progress.total_count,
            upload_manager.progress.failed_bytes,
        )
