#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from argparse import Namespace
import ctypes
import functools
import logging
import re
from urllib.parse import parse_qs, unquote, urlparse

from opentelemetry import propagate, trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.span import NonRecordingSpan

# pylint: disable=requests-import
import requests

from ngcbase.constants import (
    BUILD_TYPE,
    CANARY_ENV,
    LRU_CACHE_SIZE,
    OPENTELEMETRY_COLLECTOR_HOST_MAPPING,
    OPENTELEMETRY_COLLECTOR_PORT,
    OPENTELEMETRY_COMPONENT_NAME,
    OPENTELEMETRY_PRIVATE_TAGS,
    PRODUCTION_ENV,
)
from ngcbase.environ import NGC_CLI_TRACE_DISABLE
from ngcbase.errors import ValidationException
from ngcbase.singleton import Singleton
from ngcbase.util import curl_logging
from ngcbase.util.ssh_utils import is_port_open
from ngcbase.util.utils import get_dll_path, get_environ_tag, get_system_info

logger = logging.getLogger(__name__)
ENVIRON = get_environ_tag()
PROPAGATOR = propagate.get_global_textmap()


@functools.lru_cache(maxsize=LRU_CACHE_SIZE)
def get_opentelemetry_token() -> str:  # noqa: D103
    # should never get here, but just in case.
    if BUILD_TYPE == "sdk":
        return ""
    env = "prod" if ENVIRON in (PRODUCTION_ENV, CANARY_ENV) else "stg"
    ex_lib = ctypes.CDLL(get_dll_path())
    fnc = getattr(ex_lib, env)
    setattr(fnc, "restype", ctypes.c_char_p)
    token = fnc().decode("utf-8")
    return token


@functools.lru_cache(maxsize=LRU_CACHE_SIZE)
def get_opentelemetry_host():  # noqa: D103
    if ENVIRON in (PRODUCTION_ENV, CANARY_ENV):
        return OPENTELEMETRY_COLLECTOR_HOST_MAPPING["prod"]
    return OPENTELEMETRY_COLLECTOR_HOST_MAPPING["stg"]


def is_enabled():  # noqa: D103
    if NGC_CLI_TRACE_DISABLE or BUILD_TYPE == "sdk":
        return False
    # Check that there is no firewall blocking the required port
    return is_port_open(get_opentelemetry_host(), OPENTELEMETRY_COLLECTOR_PORT)


class GetTracer(metaclass=Singleton):
    """Singleton to hold a global tracer and parent span to account for multithreading
    This context manager will return the tracer from a with block, but if invoked
    directly will expose its fields.
    """  # noqa: D205

    def __init__(self):
        if is_enabled():
            resource = Resource(attributes={SERVICE_NAME: OPENTELEMETRY_COMPONENT_NAME})
            endpoint = f"{get_opentelemetry_host()}:{OPENTELEMETRY_COLLECTOR_PORT}"
            provider = TracerProvider(resource=resource)
            exporter = OTLPSpanExporter(
                endpoint=endpoint,
                headers=f"Lightstep-Access-Token={get_opentelemetry_token()}",
            )
            processor = BatchSpanProcessor(exporter)
            provider.add_span_processor(processor)
            trace.set_tracer_provider(provider)
            self.tracer = trace.get_tracer("ngc-cli-instumentation")
        else:
            self.tracer = trace.get_tracer("ngc-cli-notracing")
        self.__current_span = None

    def __enter__(self):  # noqa: D105
        return self.tracer

    def __exit__(self, _exc_type, _exc_val, _exc_tb):  # noqa: D105
        # We used to call `self.tracer.flush()` here, but there's no opentelemetry equivalent.
        pass

    def get_span(self):  # noqa: D102
        curr = trace.get_current_span()
        return self.__current_span if isinstance(curr, NonRecordingSpan) else curr

    def update_span(self, span=None):  # noqa: D102
        if span is not None:
            self.__current_span = span
        elif self.active_span is not None:
            self.__current_span = self.active_span
        else:
            # we should not be throwing any exception as tracing for user should not be a critical feature
            logger.debug("no span found")

    @property
    def active_span(self):  # noqa: D102
        curr = trace.get_current_span()
        if isinstance(curr, NonRecordingSpan):
            return None
        return curr


def add_tags(span, tags_dict):
    """Adds tags to given span if they are not in the private tags set."""  # noqa: D401
    if span is None or tags_dict is None:
        return
    for key, value in tags_dict.items():
        if value is not None and key not in OPENTELEMETRY_PRIVATE_TAGS:
            span.set_attribute(key, str(value))


def trace_command(name=None, config=None):
    """Annotation meant to wrap CLICommands that traces its execution
    invoked as @trace_command() or @trace_command(name="name")
    it is important to maintain @functools.wraps over CLICommand functions because they have extra
    attributes that CLICommand is expecting.
    """  # noqa: D205

    def decorator_span(func):
        @functools.wraps(func)
        def wrapper_span(*args, **kwargs):
            with GetTracer() as tracer:
                operation_name = name if name is not None else func.__name__
                has_parent = GetTracer().get_span() is not None
                with tracer.start_as_current_span(operation_name) as scope:
                    tags = {
                        "configuration.ace_name": config.ace_name,
                        "configuration.org_name": config.org_name,
                        "configuration.team_name": config.team_name,
                        "span.kind": "client",
                    }

                    # only add debug tags if this is a top level span (there are no parents to get the debug tags from)
                    if not has_parent:
                        system_info = get_system_info()
                        tagged_system_info = {
                            key: system_info.pop(key) for key in ("os", "ngc-cli version", "python version")
                        }

                        logged_system_info = {k: v for k, v in system_info.items() if v is not None}
                        tags.update(tagged_system_info)
                        scope.set_attributes(logged_system_info)

                    # CLICommand arguments are stored in the Namespace object
                    for arg in args:
                        if isinstance(arg, Namespace):
                            for key, value in arg.__dict__.items():
                                if key not in OPENTELEMETRY_PRIVATE_TAGS and key != "func":
                                    tags[f"args.{key}"] = value

                    add_tags(scope, tags)

                    try:
                        ret_val = func(*args, **kwargs)
                    except Exception as e:
                        # error is a special tag that causes the span to be marked as failed in lightstep
                        add_tags(
                            scope,
                            {
                                "error": True,
                            },
                        )
                        scope.set_attributes({"exception": str(e)})
                        raise
            return ret_val

        return wrapper_span

    return decorator_span


def _generate_url_tags(method, url, **kwargs):
    parsed_url = urlparse(url)
    query = parse_qs(parsed_url.query, True)
    tags = {
        "method": method,
        "scheme": parsed_url.scheme,
        "host": parsed_url.netloc,
        "path": parsed_url.path,
        "timeout": kwargs.get("timeout", None),
    }
    for key, value in query.items():
        if isinstance(value, list) and len(value) == 1:
            tags[f"params.{key}"] = value[0]
        else:
            tags[f"params.{key}"] = value
    return tags


def set_url_tags(span, method, url, **kwargs):  # noqa: D103
    tags = _generate_url_tags(method, url, **kwargs)
    add_tags(span, tags)


def traced_request(method, url, operation_name=None, **kwargs):  # noqa: D103
    with TracedSession() as session:
        return session.request(method, url, operation_name=operation_name, **kwargs)


class TracedSession(requests.Session):  # noqa: D101
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hooks["response"].append(curl_logging.on_response_print_curl_request)

    @staticmethod
    def _validate_url(url):
        _pattern = r"^[^%]+$"
        if not re.search(_pattern, unquote(url)):
            # These encoded characters are disallowed by the backend system so we filter them here
            logger.debug(
                r"Attempted to request url with encoded values for %% (%%25) or ^ " r"(%%E5) in it: %s (%s)",
                url,
                unquote(url),
            )
            raise ValidationException(
                "Double encoding the url ({}) is not allowed. Request aborted.\n"
                "This may have occurred if a filename contains '^' or '%' characters.".format(url)
            )

    # pylint: disable=arguments-differ
    # method adds args to base method
    def request(self, method, url, operation_name=None, headers=None, **kwargs):
        """Inject operation_name into send by passing it through the headers."""
        headers_with_operation_name = {} if headers is None else headers
        if operation_name is not None:
            headers_with_operation_name["operation_name"] = operation_name
        return super().request(method, url, headers=headers_with_operation_name, **kwargs)

    # pylint: disable=arguments-differ
    # method adds args to base method
    def send(self, request, operation_name=None, check_operation_name=False, **kwargs):
        """Adds opentelemetry functionality to requests.send.

        All requests are passed through this method, so it is only necessary to trace this function.
        """  # noqa: D401
        headers = {} if not hasattr(request, "headers") or request.headers is None else request.headers
        # ignore header if operation name was explicitly passed in
        if "operation_name" in headers and operation_name is None:
            operation_name = headers["operation_name"]
        if "operation_name" in headers and not kwargs.get("allow_redirects", False):
            headers.pop("operation_name")
        # added a check as operation name is popped on redirect and the send call fails
        if operation_name is None and check_operation_name:
            raise ValueError("operation_name is a required argument")

        with GetTracer() as tracer:
            with tracer.start_as_current_span(operation_name) as scope:
                set_url_tags(scope, request.method, request.url, **kwargs)

                PROPAGATOR.inject(carrier=headers)
                request.prepare_headers(headers)

                add_tags(scope, headers)
                add_tags(scope, {"span.kind": "client"})

                try:
                    self._validate_url(request.url)
                    ret_val = super().send(request, **kwargs)
                    scope.set_attributes(ret_val.headers)
                    add_tags(scope, {"http.status_code": ret_val.status_code})
                    if ret_val.status_code >= 400:
                        add_tags(scope, {"error": True})
                    # save request id header as a tag so it is searchable
                    if ret_val.headers is not None and "nv-request-id" in ret_val.headers:
                        add_tags(scope, {"request-id": ret_val.headers["nv-request-id"]})
                except Exception as e:
                    # error is a special tag that causes the span to be marked as failed in lightstep
                    add_tags(scope, {"error": True})
                    scope.set_attributes({"exception": str(e)})
                    raise
        return ret_val
