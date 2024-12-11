#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
import asyncio
import copy
from datetime import datetime
import http.client
import json
import logging
import os
import posixpath
import random
import shutil
import ssl
import sys
import tempfile
import time
from urllib.parse import quote, urlencode
import zipfile

import aiohttp  # pylint: disable=import-error
import certifi
import charset_normalizer
from requests import Timeout as requests_timeout  # pylint: disable=requests-import

from ngcbase.api import utils as rest_utils
from ngcbase.constants import (
    ASYNC_BATCH_SIZE,
    KiB,
    MiB,
    RESUME_DOWNLOAD_FILENAME,
    SEMAPHORE_VALUE,
    UMASK_GROUP_OTHERS_READ_EXECUTE,
)
from ngcbase.environ import NGC_CLI_DOWNLOAD_RETRIES
from ngcbase.errors import (
    DownloadFileSizeMismatch,
    NgcException,
    ResourceNotFoundException,
)
from ngcbase.printer.transfer import TransferPrinter
from ngcbase.transfer import utils as xfer_utils
from ngcbase.util.datetime_utils import human_time
from ngcbase.util.file_utils import (
    get_incremented_filename,
    mkdir_path,
    TemporaryFileCreator,
)
from ngcbase.util.utils import MaskGranter

ASYNC_CLIENT_ERRORS = (
    aiohttp.ClientResponseError,
    aiohttp.client_exceptions.ClientResponseError,
)
ASYNC_DOWNLOAD_ERRORS = ASYNC_CLIENT_ERRORS + (
    aiohttp.ClientConnectionError,
    aiohttp.ClientPayloadError,
    aiohttp.ClientConnectorError,
    aiohttp.ServerConnectionError,
    aiohttp.ServerTimeoutError,
    asyncio.exceptions.TimeoutError,
    ConnectionResetError,
    requests_timeout,
)

TOKEN_EXPIRY_TIME = 5 * 60
SOCK_READ_TIMEOUT_SECONDS = 5 * 60
UNKNOWN_FILE_SIZE = 100 * MiB
RETRY_SLEEP_SECONDS = 5
INITIAL_DELAY = 10
BACKOFF = 2
MAX_DELAY = 80
MAX_RETRIES = 15
CHUNK_SIZE = 64 * KiB

logger = logging.getLogger(__name__)


failed_count = 0
failed_size = 0
file_count = 0
download_count = 0
download_size = 0
download_total_size = 0
# This needs to be in the global namespace for tracing
download_operation_name = None
# This is read-only, so make it visible globally
files_with_size = {}
# Progress output
printer = None
# There is only ever a single progress_bar and a single task.
progress_bar = None
task = None


async def _update_progress(advance):
    if progress_bar:
        async with asyncio.Lock():
            printer.update_task(task, advance=advance)


async def _update_file_column():
    if progress_bar:
        file_text = f"[blue]Total: {file_count} - Completed: {download_count} - Failed: {failed_count}"
        progress_bar.file_column.text_format = file_text


async def _update_stats(pth, size, success, resp_status):
    global failed_count, failed_size, download_count, download_size
    async with asyncio.Lock():
        if resp_status:
            if success:
                logger.debug("Finished file '%s':  %s", pth, resp_status)
                download_count += 1
                download_size += size
            else:
                logger.debug("Failed to download '%s'; status=%s", pth, resp_status)
                failed_count += 1
                failed_size += size
        else:
            # An exception occurred before this value could be set
            logger.debug("Failed to download %s", pth)
            failed_count += 1
            failed_size += size
        await _update_progress(advance=0)
        await _update_file_column()


def _check_windows_async():
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith("win"):
        # Windows has been unable to close the asyncio loop successfully. This line of code is a fix
        # to handle the asyncio loop failures. Without it, code is unable to CTRL-C or finish.
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class AsyncDownload:  # noqa: D101
    def __init__(self, api_client, download_id, org_name, team_name=None):
        self.client = api_client
        self.download_id = download_id
        self.org_name = org_name
        self.team_name = team_name
        self.files_to_download = []
        self.files_downloaded = []
        self.files_failed_to_download = []
        self.files_not_found = []
        self.total_download_size_bytes = 0
        self.total_download_files = 0
        self.printer = TransferPrinter(self.client.config)
        self.time_started = None
        self.download_path = None
        self.zip_directory = None
        self.counter = 0
        self.final_status = None
        self._timer = None
        self._need_unzip = False
        self._save_state = True
        self._get_auth_header(renew=True)
        _check_windows_async()

    def _get_auth_header(self, renew=False):
        return self.client.authentication.auth_header(
            auth_org=self.org_name,
            auth_team=self.team_name,
            renew=renew,
        )

    @staticmethod
    def _remove_file(filename, logged=True):
        # TODO: improve handling other exceptions and provide better message to user.
        try:
            if os.path.exists(filename):
                os.remove(filename)
            elif logged:
                logger.debug("%s doesn't exist.", filename)
        except (OSError, TypeError):
            logger.debug("Removing %s failed.", filename)

    def _unzip_file(self, file_name, destination):
        """Unzip a zip file to download path."""
        # TODO: Add files names back to failed if unzip is incomplete or fails, zip_ref.namelist.
        # TODO: Improve handling exceptions, reference UnzipFileSubmission.
        try:
            with zipfile.ZipFile(file_name) as zip_ref:
                zip_ref.extractall(destination)
                self.total_download_files += len(zip_ref.namelist() or []) - 1
        except (zipfile.BadZipfile, FileNotFoundError, AttributeError):
            logger.debug("Bad zip file %s", file_name)
        finally:
            self._remove_file(file_name)

    def _unzip_zip_directory(self):
        """Unzip zip files saved by batch downloads."""
        # TODO: Improve handling exceptions on removing zip directory.
        self.printer.print_download_message("Unzipping zip files.")
        if self.zip_directory and os.path.exists(self.zip_directory):
            files = os.listdir(self.zip_directory) or []
            for file in files:
                file_name = os.path.join(self.zip_directory, file)
                self._unzip_file(file_name, self.download_path)
            try:
                shutil.rmtree(self.zip_directory)
            except (OSError, TypeError):
                logger.debug("Removing %s failed.", self.zip_directory)

    def _print_download_progress(self):
        """Show download progress."""
        # TODO: Add logic to show download progress only once for all concurrent downloads.
        # TODO: Fix (Task exception was never retrieved), error on KeyboardInterrupt.
        # TypeError and ValueError handle None and empty values incase an async call sets incorrect values.
        try:
            if self.total_download_size_bytes > 0:
                self.printer.print_download_progress(self.total_download_size_bytes, self.time_started)
        except (TypeError, ValueError, KeyboardInterrupt):
            return

    @staticmethod
    def _track_download_progress(list_of_files, files):
        """Update failed list, or success list after a file(s) fails or succeeds to download."""
        # TODO: Add files in zipfile to list after unzip.
        if files and list_of_files is not None:
            list_of_files.extend(files if isinstance(files, (list, tuple)) else [files])

    def _save_files_to_download(self):
        """Files failed to download are saved to a json file for resuming download."""
        # TODO: Pass download type and use in printing info.
        files_downloaded = set(self.files_downloaded or [])
        files_not_found = set(self.files_not_found or [])
        files_to_download = set(self.files_to_download or [])
        # We don't want to retry successful downloads as well as the failures that can't succeed
        files_not_to_retry = files_downloaded.union(files_not_found)
        self.files_to_download = list(files_to_download.symmetric_difference(files_not_to_retry))
        try:
            files_path = os.path.join(
                self.download_path,
                f"{RESUME_DOWNLOAD_FILENAME}-{self.download_id}.json",
            )
            if self.files_to_download:
                mkdir_path(os.path.dirname(files_path))
                with open(files_path, "w") as f:
                    json.dump(self.files_to_download, f)
                self.final_status = "Incomplete."
                self.printer.print_resume_download_information(
                    number_files=len(self.files_to_download),
                    files_path=files_path,
                )
            else:
                self._remove_file(files_path)
        except (OSError, TypeError):
            logger.debug("Saving filenames for resuming download failed.")

    def _print_status(self):
        """Show the final status before exiting."""
        # TODO: Show correct total download files and size for all cases, try reading info from disk.
        completion_time = datetime.now()
        self.printer.print_ok("")
        self.printer.print_download_final_status(
            storage_id=self.download_id,
            status=self.final_status,
            download_path=self.download_path,
            files_downloaded=self.total_download_files,
            downloaded_size=self.total_download_size_bytes,
            failed_files=self.files_failed_to_download,
            files_not_found=self.files_not_found,
            start_time=self.time_started,
            completion_time=completion_time,
        )

    def _handle_interrupt(self):
        """Handle keyboard interrupt."""
        # TODO: Pass download type and use in printing info.
        self.final_status = "Terminated"
        self.printer.print_ok(f"\nStopping download of '{self.download_id}'.")
        if self._need_unzip:
            self._unzip_zip_directory()
        if self._save_state:
            self._save_files_to_download()
        self._print_status()

    @staticmethod
    def _calculate_batch_size(filenames_list):
        """Calculate number of files in each batch download."""
        len_files = len(filenames_list or [])
        if len_files <= 50:
            batch_size = 1
        elif len_files <= 25000:
            batch_size = len_files // 50
        else:
            batch_size = ASYNC_BATCH_SIZE
        counter_size = len_files // batch_size
        return batch_size, counter_size

    async def _get_headers(self):
        """Headers update on token expiry using a timer."""
        header_override = self._get_auth_header()
        return rest_utils.default_headers(header_override)

    @staticmethod
    async def _sleep_before_resume(attempts):
        """Jitter wait before retrying the download."""
        backoff = int(INITIAL_DELAY * BACKOFF ** (MAX_RETRIES - attempts + 1))
        mdelay = random.randrange(0, min(MAX_DELAY, backoff))
        await asyncio.sleep(mdelay)

    async def _yield_filenames_from_list(self, filenames_list):
        """`async` method yields batch of files from a list for the `asyncio.gather` tasks."""
        if filenames_list:
            batch_size, counter_size = self._calculate_batch_size(filenames_list)
            for i in range(counter_size):
                yield filenames_list[i * batch_size : i * batch_size + batch_size], self.counter  # noqa: E203
                self.counter += 1
            if filenames_list[counter_size * batch_size :]:  # noqa: E203
                yield filenames_list[counter_size * batch_size :], self.counter + counter_size  # noqa: E203
                self.counter += 1

    async def _yield_filename_from_list(self, filenames_list):
        """`async` method yields a file from a list for the `asyncio.gather` tasks."""
        for file in filenames_list or []:
            yield file, None

    async def _get_file_content(self, session, dest, file_url, params=None):
        """Download filenames file and read filenames list."""
        read_entire_content = False
        attempts = 1
        file_content = None

        while attempts <= NGC_CLI_DOWNLOAD_RETRIES:
            dest = tempfile.mkdtemp() if not dest else dest
            temp_path = get_incremented_filename(os.path.join(dest, f"{self.download_id}_file_content.json"))
            temp_name = os.path.basename(temp_path)
            with TemporaryFileCreator(temp_name, dest) as temp_file:
                read_entire_content = await self._download(
                    session,
                    file_url,
                    outfile=temp_file,
                    params=params,
                    raise_status=True,
                )
                if attempts >= NGC_CLI_DOWNLOAD_RETRIES and not read_entire_content:
                    raise NgcException(f"Unable to download {file_url}. Reached maximum retries.") from None
                if read_entire_content:
                    try:
                        file_content = json.loads(open(temp_file, "r").read())
                    except (
                        OSError,
                        FileNotFoundError,
                        ValueError,
                        TypeError,
                        json.decoder.JSONDecodeError,
                    ):
                        raise NgcException(f"Unable to read {file_url}.") from None
                    break
            attempts += 1
            await asyncio.sleep(RETRY_SLEEP_SECONDS)
            continue

        return file_content

    async def _download(
        self,
        session,
        url,
        files=None,
        counter=None,
        outfile=None,
        params=None,
        raise_status=False,
    ):
        """Main download with url and file names."""  # noqa: D401
        # TODO: Improve handling file not found on server, downloads stop cleanly and show message to user.
        # TODO: Download single file to temp and move if download is complete, handes incomplete, removing or CTRL-C.
        current_batch_size = 0
        read_entire_content = False
        headers = await self._get_headers()
        try:
            timeout_time = aiohttp.ClientTimeout(sock_read=SOCK_READ_TIMEOUT_SECONDS)
            if files:
                if counter is not None:
                    session_download_url = posixpath.join(*list(filter(None, [url, params])))
                    logger.debug("POST %s", session_download_url)
                    payload = json.dumps(files)
                    session_download = session.post(
                        session_download_url,
                        data=payload,
                        headers=headers,
                        timeout=timeout_time,
                    )
                    outfile = os.path.join(self.zip_directory, f"{counter}.zip")
                else:
                    file = quote(files.lstrip("/")) if files else files
                    session_download_url = posixpath.join(*list(filter(None, [url, file, params])))
                    logger.debug("GET %s", session_download_url)
                    session_download = session.get(
                        session_download_url,
                        headers=headers,
                        timeout=timeout_time,
                    )
                    outfile = os.path.join(self.download_path, file)
                mkdir_path(os.path.dirname(outfile))
            else:
                session_download_url = posixpath.join(*list(filter(None, [url, params])))
                logger.debug("GET %s", session_download_url)
                session_download = session.get(
                    session_download_url,
                    headers=headers,
                    timeout=timeout_time,
                    raise_for_status=raise_status,
                )
            async with session_download as response:
                if response.status != 200:
                    self.total_download_size_bytes -= current_batch_size
                    self._remove_file(outfile, logged=False)
                    logger.debug("Response status: %s", response.status)
                    if response.status == 404:
                        # File does not exist; log it and return
                        try:
                            logger.info("File '%s' was not found.", file)
                        except NameError:
                            logger.info("File was not found.")
                        self._track_download_progress(self.files_not_found, files)
                    else:
                        self._track_download_progress(self.files_failed_to_download, files)
                    return read_entire_content
                # TODO: improve handling file open errors, reference open_file_for_write
                with open(outfile, "wb") as f:
                    while True:
                        chunk = await response.content.readany()
                        self.total_download_size_bytes += len(chunk)
                        current_batch_size += len(chunk)
                        if not chunk:
                            read_entire_content = True
                            self._track_download_progress(self.files_downloaded, files)
                            self.total_download_files += 1
                            return read_entire_content
                        f.write(chunk)
                        self._print_download_progress()
        except ASYNC_DOWNLOAD_ERRORS as e:
            self.total_download_size_bytes -= current_batch_size
            self._track_download_progress(self.files_failed_to_download, files)
            self._remove_file(outfile, logged=False)
            logger.debug("Download error: %s", str(e))
            if e in ASYNC_CLIENT_ERRORS and e.status == 404 and raise_status:
                raise ResourceNotFoundException("Resource not found.") from None

        return read_entire_content

    async def _semaphore(self, semaphore, session, url, files=None, counter=None, params=None):
        """Controls concurrent downloads."""  # noqa: D401
        async with semaphore:
            return await self._download(session, url, files, counter, params=params)

    async def _download_files(
        self,
        dest,
        files,
        url=None,
        part_url=None,
        params=None,
        resume=False,
    ):
        """Downloads by file or group of files."""  # noqa: D401
        # TODO: Explore higher values for semaphore, downloads by each file are slow if files > 10000.
        # TODO: Explore launching multiple loops with run_in_executor whens tasks > 10000.
        # TODO: Pass download session and tempfile to _download, move away outfile logic from _download.

        self.files_to_download = files
        self.files_downloaded = []
        self.files_failed_to_download = []
        self.files_not_found = []
        self.time_started = datetime.now()
        dest = os.path.abspath(dest or ".")
        attempts = 1
        yield_files = self._yield_filename_from_list
        self.download_path = get_incremented_filename(os.path.join(dest, f"{self.download_id}"))
        self.zip_directory = get_incremented_filename(f"{self.download_path}_zip")

        if resume:
            self.download_path = dest

        if part_url:
            url = part_url
            yield_files = self._yield_filenames_from_list

        if not self.files_to_download:
            raise NgcException("There are no files to download.") from None

        url = rest_utils.add_scheme(url)
        while attempts <= MAX_RETRIES:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            semaphore = asyncio.Semaphore(SEMAPHORE_VALUE)
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
                await asyncio.gather(
                    *[
                        asyncio.create_task(
                            self._semaphore(
                                semaphore=semaphore,
                                session=session,
                                url=url,
                                files=files,
                                counter=counter,
                                params=params,
                            )
                        )
                        async for (files, counter) in yield_files(self.files_to_download)
                    ]
                )
            if attempts >= MAX_RETRIES and self.files_failed_to_download:
                logger.debug("Unable to complete download. Reached maximum retries.")
                self.final_status = "Incomplete."
                if self._need_unzip:
                    self._unzip_zip_directory()
                if self._save_state:
                    self._save_files_to_download()
                self._print_status()
            if not self.files_failed_to_download:
                self.final_status = "Completed"
                if self._need_unzip:
                    self._unzip_zip_directory()
                if self._save_state:
                    self._save_files_to_download()
                self._print_status()
                break
            random.shuffle(self.files_failed_to_download)
            self.files_to_download = copy.copy(self.files_failed_to_download)
            self.files_failed_to_download = []
            self.files_downloaded = []
            attempts += 1
            # TODO: unzip downloaded zipfiles instead of await sleep
            await self._sleep_before_resume(attempts)
            continue

    async def _download_zip(self, dest, url, do_zip=False, params=None):
        """Downloads single URL as zip and unzip or move the zipfile."""  # noqa: D401
        # TODO: Pass download session and tempfile to _download, remove outfile logic from _download.

        self.total_download_size_bytes = 0
        self.time_started = datetime.now()
        dest = os.path.abspath(dest or ".")
        attempts = 1
        temp_name = "{}.zip".format(self.download_id)
        read_entire_content = False
        self.download_path = get_incremented_filename(os.path.join(dest, f"{self.download_id}"))

        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        while attempts <= MAX_RETRIES:
            with TemporaryFileCreator(temp_name, dest) as temp_file:
                async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
                    read_entire_content = await self._download(session, url, outfile=temp_file, params=params)
                if attempts >= MAX_RETRIES and not read_entire_content:
                    logger.debug("Unable to complete download. Reached maximum retries.")
                    self.final_status = "Incomplete."
                if read_entire_content:
                    self.final_status = "Completed."
                    mkdir_path(self.download_path)
                    if do_zip:
                        dest_file = os.path.join(self.download_path, os.path.basename(temp_file))
                        shutil.move(temp_file, dest_file)
                    else:
                        self._unzip_file(temp_file, self.download_path)
                    self._print_status()
                    break
            attempts += 1
            await self._sleep_before_resume(attempts)
            continue

    async def _download_file_content(self, dest, url, params=None):
        file_content = None
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector, trust_env=True) as session:
            file_content = await self._get_file_content(session, dest, url, params=params)

        return file_content

    def download_files(self, dest, url, files, params=None, resume=False, save_state=True):
        """Downloads files by each file."""  # noqa: D401
        self._save_state = save_state
        try:
            asyncio.run(self._download_files(dest=dest, url=url, files=files, params=params, resume=resume))
        except KeyboardInterrupt:
            self._handle_interrupt()
            sys.exit()

    def download_parts(
        self,
        dest,
        part_url,
        files,
        params=None,
        resume=False,
        save_state=True,
    ):
        """Downloads files by groups of files."""  # noqa: D401
        self._need_unzip = True
        self._save_state = save_state
        try:
            asyncio.run(
                self._download_files(
                    dest=dest,
                    part_url=part_url,
                    files=files,
                    params=params,
                    resume=resume,
                )
            )
        except KeyboardInterrupt:
            self._handle_interrupt()
            sys.exit()

    def download_zip(self, dest, url, do_zip=False, params=None):
        """Downloads single URL to zip."""  # noqa: D401
        self._need_unzip = True
        try:
            asyncio.run(self._download_zip(dest=dest, url=url, do_zip=do_zip, params=params))
        except KeyboardInterrupt:
            self._handle_interrupt()
            sys.exit()

    def download_file_content(self, dest, url, params=None):
        """Downloads and returns file content."""  # noqa: D401
        try:
            file_content = asyncio.run(self._download_file_content(dest=dest, url=url, params=params))
            return file_content
        except KeyboardInterrupt:
            self._handle_interrupt()
            sys.exit()


# pylint: disable=unused-argument
async def on_request_start(session, trace_config_ctx, params):
    """Set the operation name for this request."""
    params.headers["operation_name"] = download_operation_name


def _remove_local_file(outfile):
    """Remove local file, supress exceptions.

    Args:
        outfile (str): output file full path
    """
    try:
        os.remove(outfile)
    except (OSError, FileNotFoundError):
        pass


async def _write_bytes_to_file(resp, outfile, file_size):
    """Given http response, write content to the outfile
       if exception:
       1. undo progress
       2. reraise failure

    Args:
        resp (ClientResponse): Response of the request
        outfile (str): fullpath of output file
        file_size (int): target file size to match

    Returns:
        None
    """  # noqa: D205, D415
    logger.debug("response is %s", None if resp is None else resp.status)
    dl_size = 0
    try:
        with open(outfile, "wb") as ff:
            async for chunk in resp.content.iter_chunked(CHUNK_SIZE):
                ff.write(chunk)
                chunk_size = len(chunk)
                dl_size += chunk_size
                await _update_progress(advance=chunk_size)
                if resp.content.at_eof():
                    logger.debug("Finished writing %s/%s bytes to file '%s'", dl_size, file_size, outfile)
                    if dl_size != file_size:
                        logger.debug(
                            "downloaded file %s size %s mismatch target file size %s", outfile, dl_size, file_size
                        )
                        raise DownloadFileSizeMismatch()
    except Exception as _e:  # pylint: disable=broad-except
        logger.debug("Error retrieving '%s': %s, %s,", outfile, type(_e), str(_e))
        # revert progresses
        _remove_local_file(outfile)
        await _update_progress(advance=-dl_size)
        raise


async def _direct_download_get_write_file(url, filename, download_dir):
    """Request and write to file with retries, If any exception is encountered,
    retry after 100ms.

    Args:
        url (str): _description_
        filename (str): _description_
        download_dir (str): _description_

    Raises:
        Exception: raised exceptions is retried internally

    Returns:
        None
    """  # noqa: D205
    # retry loop nonlocals
    _retry = 1
    file_resp = None

    # retry loop invariants
    file_size = files_with_size.get(filename, UNKNOWN_FILE_SIZE)
    file_timeout = float(file_size) / MiB
    outfile = os.path.join(download_dir, filename)
    mkdir_path(os.path.dirname(outfile))
    # retry on any exceptions
    while _retry <= NGC_CLI_DOWNLOAD_RETRIES:
        try:
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            timeout = max(SOCK_READ_TIMEOUT_SECONDS, file_timeout)
            logger.debug("\nTimeout for file '%s': %s", filename, human_time(timeout))
            client_timeout = aiohttp.ClientTimeout(total=timeout, sock_read=60)
            async with aiohttp.ClientSession(
                connector=connector,
                trace_configs=[],
                timeout=client_timeout,
                trust_env=True,
            ) as session:
                resp = await session.get(xfer_utils.use_noncanonical_url(url))
                file_resp = None if resp is None else resp.status
                logger.debug("File direct GET response for file '%s': %s", filename, file_resp)
                await _write_bytes_to_file(resp, outfile, file_size)
                dled_size = files_with_size.get(filename, UNKNOWN_FILE_SIZE)
                await _update_stats(filename, dled_size, True, file_resp)
                # breakout loop
                return
        except Exception as _e:  # pylint: disable=broad-except
            logger.debug("Error downloading '%s': %s, %s", filename, type(_e), _e)
            if _retry == NGC_CLI_DOWNLOAD_RETRIES:  # pylint: disable=no-else-return
                logger.debug(
                    "Retry _direct_download_get_write_file %s exhausted, input %s, %s, %s",
                    NGC_CLI_DOWNLOAD_RETRIES,
                    url,
                    filename,
                    download_dir,
                )
                await _update_stats(filename, 0, False, file_resp)
                # breakout loop
                return
            else:
                await asyncio.sleep(0.1)
                logger.debug(
                    "Retry _direct_download_get_write_file %s/%s, input %s, %s, %s",
                    _retry,
                    NGC_CLI_DOWNLOAD_RETRIES,
                    url,
                    filename,
                    download_dir,
                )
                _retry += 1


async def _direct_download_file(
    url,
    filename,
    download_dir,
    headers,
    auth_org=None,
    auth_team=None,
    api_client=None,
):
    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    url = f"{url}?" + urlencode({"path": filename})
    # Get the direct download URL
    async with aiohttp.ClientSession(trace_configs=[trace_config], connector=connector, trust_env=True) as session:
        dl_url_resp = await session.get(xfer_utils.use_noncanonical_url(url), headers=headers)
        status = dl_url_resp.status
        logger.debug("File direct URL response for file '%s': %s", filename, status)
        if status == http.client.UNAUTHORIZED:
            # Auth token expired; fetch a fresh one and retry
            headers = xfer_utils.get_headers(api_client, headers or {}, auth_org, auth_team)
            dl_url_resp = await session.get(url, headers=headers)
            status = dl_url_resp.status
            logger.debug("File direct URL retry response for file '%s': %s", filename, status)
        elif status >= 300:
            file_size = files_with_size.get(filename, UNKNOWN_FILE_SIZE)
            _update_stats(filename, file_size, False, status)
            return
        direct_url_dict = await dl_url_resp.json()
    direct_url = direct_url_dict["urls"][0]
    logger.debug("File direct URL for file '%s': %s", filename, direct_url)
    with MaskGranter(UMASK_GROUP_OTHERS_READ_EXECUTE):
        await _direct_download_get_write_file(direct_url, filename, download_dir)


async def _direct_download_paginated_files(url, download_dir, headers, auth_org=None, auth_team=None, api_client=None):
    trace_config = aiohttp.TraceConfig()
    trace_config.on_request_start.append(on_request_start)
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    # Get the direct download URL
    async with aiohttp.ClientSession(trace_configs=[trace_config], connector=connector, trust_env=True) as session:
        page_num = 0
        # This will be adjusted on the first call. For now, start with a large number
        total_pages = 999
        # page_num is zero-based, while total pages is one-based, so once it is equal we know we have gone through all
        # the pages available.
        while page_num < total_pages:
            page_url = f"{url}?page-number={page_num}&page-size=100"
            logger.debug("\nPage URL: %s", page_url)
            resp = await session.get(page_url, headers=headers)
            status = resp.status
            logger.debug("\nResponse for page %s: %s", page_num, status)
            if status == http.client.UNAUTHORIZED:
                headers = xfer_utils.get_headers(api_client, headers, auth_org, auth_team)
                resp = await session.get(page_url, headers=headers)
                status = resp.status
                logger.debug("\nResponse for retrying page %s: %s", page_num, status)
            elif status >= 300:
                text = await resp.text()
                logger.error("\nError getting pagination for file download:'%s'", text)
                # Update the failed count so the calling program sees the failure.
                global failed_count
                failed_count = file_count
                return
            resp_dict = await resp.json()
            page_info = resp_dict.get("paginationInfo", {})
            total_pages = page_info.get("totalPages", 1)
            urls = resp_dict["urls"]
            logger.debug("\nNumber of URLs for page %s: %s", page_num, len(urls))
            logger.debug("\n\n\n\n")
            logger.debug("Pagination Info: %s", page_info)
            logger.debug("\n\n\n\n")
            filenames = resp_dict["filepath"]
            file_urls = zip(filenames, urls)
            with MaskGranter(UMASK_GROUP_OTHERS_READ_EXECUTE):
                await xfer_utils.gather(
                    [
                        _direct_download_get_write_file(file_url, file_name, download_dir)
                        for file_name, file_url in file_urls
                    ],
                    count=20,
                )
            page_num += 1
        logger.debug("\nLast page complete")


async def _direct_download_files(
    dl_type,
    name,
    org,
    team,
    version,
    url,
    paginated,
    download_dir,
    auth_org=None,
    auth_team=None,
    api_client=None,
):
    global printer, progress_bar, task, file_count, download_total_size
    auth_header = api_client.authentication.auth_header(auth_org=org, auth_team=team, renew=True)
    headers = rest_utils.default_headers(auth_header)
    printer = api_client.printer
    progress_bar = printer.create_transfer_progress_bar()
    task = progress_bar.add_task("Downloading...", start=True, total=download_total_size, completed=0)
    file_count = len(files_with_size)
    logger.debug("Preparing to download %s files...", file_count)
    await _update_progress(advance=0)
    await _update_file_column()

    with progress_bar:
        if paginated:
            await _direct_download_paginated_files(
                url,
                download_dir,
                headers,
                auth_org=org,
                auth_team=team,
                api_client=api_client,
            )
        else:
            await xfer_utils.gather(
                [
                    _direct_download_file(
                        url,
                        filename,
                        download_dir,
                        headers,
                        auth_org=org,
                        auth_team=team,
                        api_client=api_client,
                    )
                    for filename in files_with_size
                ],
                count=20,
            )


def direct_download_files(  # noqa: D103
    dl_type,
    name,
    org,
    team,
    version,
    url,
    paginated,
    dl_files_with_size,
    size,
    download_dir,
    api_client,
):
    global download_operation_name, download_total_size, files_with_size
    files_with_size = dl_files_with_size
    download_total_size = size
    download_operation_name = f"{dl_type} version download"
    _check_windows_async()
    # This is necessary because charset_normalizer emits a lot of DEBUG messages that we don't need.
    charset_normalizer.api.logger.setLevel(logging.INFO)
    time_started = time.monotonic()
    try:
        asyncio.run(
            _direct_download_files(
                dl_type,
                name,
                org,
                team,
                version,
                url,
                paginated,
                download_dir,
                auth_org=org,
                auth_team=team,
                api_client=api_client,
            )
        )
    except KeyboardInterrupt:
        api_client.printer.print_ok("\nTerminating download...\n")
        # Users don't need to see the python async warnings. Save and restore stdout to not break testing.
        sav_out = sys.stdout
        sav_err = sys.stderr
        sys.stdout = sys.stderr = open(os.devnull, "w")
        sys.exit()
        sys.stdout = sav_out
        sys.stderr = sav_err
    elapsed = time.monotonic() - time_started
    return (
        elapsed,
        download_count,
        download_size,
        failed_count,
        download_total_size,
        failed_size,
    )
