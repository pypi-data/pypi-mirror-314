#
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. ALL RIGHTS RESERVED.
#
# This software product is a proprietary product of Nvidia Corporation and its affiliates
# (the "Company") and all right, title, and interest in and to the software
# product, including all associated intellectual property rights, are and
# shall remain exclusively with the Company.
#
# This software product is governed by the End User License Agreement
# provided with the software product.
#

import getpass

from nvcf.command.args_validation import check_invoke_payload_file
from nvcf.command.cloud_function import CloudFunctionCommand
from nvcf.command.utils import check_function_name, FunctionTarget
from nvcf.printer.function_printer import FunctionPrinter

from ngcbase.command.args_validation import check_key_value_pattern
from ngcbase.command.clicommand import CLICommand
from ngcbase.constants import DISABLE_TYPE, ENABLE_TYPE, STAGING_ENV
from ngcbase.environ import NVCF_SAK
from ngcbase.util.utils import get_environ_tag

INVOKE_FLAG = ENABLE_TYPE if (get_environ_tag() <= STAGING_ENV) else DISABLE_TYPE


class FunctionCommand(CloudFunctionCommand):  # noqa: D101

    CMD_NAME = "function"
    DESC = "description of the function command"
    HELP = "function Help"
    CMD_ALIAS = ["fn"]

    FUNCTION_ID_HELP = "Function ID"
    FUNCTION_ID_METAVAR = "[<function-id>]"
    TARGET_HELP = "Function. Format: function-id:[version]"
    FUNCTION_METAVAR = "<function-id>:[<function-version-id>]"
    VERSION_METAVAR = "<function-id>:<function-version-id>"
    INVOKE_HELP = "Invoke a given function with a given payload, set NVCF_SAK to prevent the ask for STDIN"
    PAYLOAD_FILE_HELP = (
        "JSON file in format expected by given function. When stream is true, you may need to modify this payload."
    )
    FILTER_AUTHORIZATION_CHOICES = ["private", "public", "authorized"]
    CLI_HELP = ENABLE_TYPE

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser
        self.config = self.client.config
        self.printer = FunctionPrinter(self.client.config)

    @CLICommand.arguments(
        "target",
        metavar=FUNCTION_ID_METAVAR,
        nargs="?",
        help=FUNCTION_ID_HELP,
        type=str,
        default=None,
    )
    @CLICommand.arguments(
        "--access-filter",
        metavar="<filter>",
        help=f"Filter functions by access, choices are: [{','.join(FILTER_AUTHORIZATION_CHOICES)}]",
        type=str,
        default=None,
        action="append",
        choices=FILTER_AUTHORIZATION_CHOICES,
    )
    @CLICommand.arguments(
        "--name-pattern",
        metavar="<name>",
        help="Filter functions by names, supports globs.",
        type=str,
        default=None,
    )
    @CLICommand.command(help="List a function help", description="List a function description", aliases=["ls"])
    def list(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(
            args.target,
            id_required=False,
            version_required=False,
            version_allowed=False,
        )
        resp = self.client.cloud_function.functions.list(
            function_id=ft.id,
            name_pattern=args.name_pattern,
            access_filter=args.access_filter,
        )
        self.printer.print_list(resp.get("functions", {}))

    @CLICommand.arguments("target", metavar=VERSION_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.command(help="Info about a version", description="Info about a version")
    def info(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(
            args.target,
            id_required=True,
            version_required=True,
        )
        resp = self.client.cloud_function.functions.info(function_id=ft.id, function_version_id=ft.version)
        self.printer.print_info(resp.get("function", {}))

    @CLICommand.arguments("target", metavar=FUNCTION_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.command(
        help="Delete a version help", description="Delete a version description", aliases=["rm", "delete"]
    )
    def remove(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(args.target)
        self.client.cloud_function.functions.delete(function_id=ft.id, function_version_id=ft.version)
        print("Delete successful")

    @CLICommand.arguments("target", metavar=FUNCTION_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--secret",
        metavar="<name:value>",
        type=check_key_value_pattern,
        default=None,
        help="Secret name/value pair",
        action="append",
        required=True,
    )
    @CLICommand.command(
        name="update-secret",
        help="Update a function's secret values",
        description="Update a function's secret values. Can specify multiple times.",
    )
    def update_secret(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(args.target)
        self.client.cloud_function.functions.update_secrets(
            function_id=ft.id, function_version_id=ft.version, secrets=args.secret
        )
        self.printer.print_ok("Secret update successful.")

    @CLICommand.arguments(
        "--name",
        metavar="<name>",
        help=(
            "Function name must start with lowercase/uppercase/digit and can only contain lowercase, uppercase, digit,"
            " hyphen, and underscore characters"
        ),
        type=check_function_name,
        required=True,
        default=None,
    )
    @CLICommand.arguments(
        "--helm-chart",
        metavar="<org>/[<team>/]<helm-chart>:<tag>",
        help="Helm Chart in NGC used for deployment.",
        default=None,
    )
    @CLICommand.arguments(
        "--helm-chart-service",
        metavar="<helm-chart-service-name>",
        help="Must be provided if a helm chart function.",
        default=None,
    )
    @CLICommand.arguments(
        "--inference-url",
        metavar="<inference-url>",
        help="Serves as entrypoint for Triton to Custom container",
        type=str,
        required=True,
        default=None,
    )
    @CLICommand.arguments(
        "--health-uri",
        metavar="<health-uri>",
        help="Health endpoint for inferencing",
        type=str,
        default=None,
    )
    @CLICommand.arguments(
        "--health-port",
        metavar="<health-port>",
        help="Health port for inferencing",
        type=int,
        default=None,
    )
    @CLICommand.arguments(
        "--health-timeout",
        metavar="<health-port>",
        help="Health timeout for inferencing",
        default=None,
        type=str,
    )
    @CLICommand.arguments(
        "--health-protocol",
        metavar="<health-protocol>",
        help="Health timeout for inferencing",
        type=str,
        default=None,
        choices=[
            "HTTP",
            "gRPC",
        ],
    )
    @CLICommand.arguments(
        "--health-expected-status-code",
        metavar="<health-expected-status-code>",
        help="Health status code.",
        type=int,
        default=None,
    )
    @CLICommand.arguments(
        "--inference-port",
        metavar="<inference-port>",
        help="Optional port number where the inference listener is running - defaults to 8000 for HTTPS, 8001 for GRPC",
        type=int,
        default=None,
    )
    @CLICommand.arguments(
        "--container-args",
        metavar="<container-args>",
        help="Args to be passed in for inferencing",
        type=str,
        default=None,
    )
    @CLICommand.arguments(
        "--container-environment-variable",
        metavar="<key:value>",
        type=check_key_value_pattern,
        default=None,
        help="Environment settings for inferencing",
        action="append",
    )
    @CLICommand.arguments(
        "--secret",
        metavar="<name:value>",
        type=check_key_value_pattern,
        default=None,
        help="Secret name/value pair",
        action="append",
    )
    @CLICommand.arguments(
        "--model",
        metavar="[<override-name>:]<org>/[<team>/]<image>:version",
        help="List of models - could be empty with custom container, can accept multiple",
        action="append",
        default=None,
    )
    @CLICommand.arguments(
        "--resource",
        metavar="<org>/[<team>/]<resource>:version",
        help="Optional List of resources, can accept multiple",
        action="append",
        default=None,
    )
    @CLICommand.arguments(
        "--tag",
        metavar="<tag>",
        help="Tag to identify the function by, can accept multiple",
        action="append",
        default=None,
    )
    @CLICommand.arguments(
        "--description",
        metavar="<description>",
        help="Optional description for function/version",
        type=str,
        default=None,
    )
    @CLICommand.arguments(
        "--container-image",
        metavar="<org>/[<team>/]<image>:<tag>",
        help="Custom container Image",
        type=str,
        default=None,
    )
    @CLICommand.arguments(
        "--api-body-format",
        metavar="<api-body-format>",
        help="Information about the request body format",
        type=str,
        choices=[
            "PREDICT_V2",
            "CUSTOM",
        ],
        default=None,
    )
    @CLICommand.arguments(
        "--function-type",
        metavar="<function-type>",
        help="Health timeout for inferencing",
        type=str,
        default=None,
        choices=[
            "DEFAULT",
            "STREAMING",
        ],
    )
    @CLICommand.arguments(
        "target", metavar=FUNCTION_ID_METAVAR, help=FUNCTION_ID_HELP, type=str, default=None, nargs="?"
    )
    @CLICommand.command(
        help="Create a new function or function version if an id is specified",
        description="Create a new function description",
    )
    @CLICommand.mutex(["container_image", "model"], ["helm_chart", "helm_chart_service"])
    def create(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(
            args.target, id_required=False, version_required=False, version_allowed=False
        )
        response = self.client.cloud_function.functions.create(
            function_id=ft.id,
            name=args.name,
            inference_url=args.inference_url,
            health_uri=args.health_uri,
            inference_port=args.inference_port,
            container_args=args.container_args,
            container_environment_variables=args.container_environment_variable,
            models=args.model,
            container_image=args.container_image,
            api_body_format=args.api_body_format,
            helm_chart=args.helm_chart,
            helm_chart_service=args.helm_chart_service,
            tags=args.tag,
            resources=args.resource,
            function_type=args.function_type,
            health_port=args.health_port,
            health_timeout=args.health_timeout,
            health_protocol=args.health_protocol,
            health_expected_status_code=args.health_expected_status_code,
            description=args.description,
            secrets=args.secret,
        )
        self.printer.print_info(response.get("function", {}))

    @CLICommand.arguments(
        "-f",
        "--file",
        metavar="<file>",
        help=PAYLOAD_FILE_HELP,
        action=check_invoke_payload_file(),
        required=True,
    )
    @CLICommand.arguments(
        "-s",
        "--stream",
        help="Invoke function with text/event-stream in the header",
        action="store_true",
    )
    @CLICommand.arguments("target", metavar=FUNCTION_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.command(
        help=INVOKE_HELP,
        description="Inference a given function,",
        feature_tag=INVOKE_FLAG,
    )
    def invoke(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(
            target_string=args.target,
            id_required=True,
            version_required=False,
        )
        starfleet_api_key = NVCF_SAK if NVCF_SAK else getpass.getpass("Please provide your NVCF SAK: ")
        payload = args.file

        if args.stream:
            # Streaming will write output one at a time
            stream = self.client.cloud_function.functions.invoke_stream(
                function_id=ft.id,
                function_version_id=ft.version,
                payload=payload,
                starfleet_api_key=starfleet_api_key,
            )
            for line in stream:
                print(line.decode("utf-8"))
        else:
            resp = self.client.cloud_function.functions.invoke(
                function_id=ft.id,
                function_version_id=ft.version,
                payload=payload,
                starfleet_api_key=starfleet_api_key,
            )
            self.printer.print_json(resp, ensure_ascii=False)
