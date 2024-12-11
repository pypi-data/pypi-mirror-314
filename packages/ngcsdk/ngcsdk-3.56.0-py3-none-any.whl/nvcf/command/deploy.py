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

import json

from nvcf.api.deployment_spec import (
    DeploymentSpecification,
    TargetedDeploymentSpecification,
)
from nvcf.command.function import FunctionCommand
from nvcf.command.utils import FunctionTarget
from nvcf.printer.deploy_printer import DeploymentPrinter

from ngcbase.api.configuration import get_environ_tag
from ngcbase.command.args_validation import check_ymd_hms_datetime
from ngcbase.command.clicommand import CLICommand
from ngcbase.constants import DISABLE_TYPE, ENABLE_TYPE, STAGING_ENV


class DeployCommand(FunctionCommand):  # noqa: D101

    CMD_NAME = "deploy"
    DESC = "Description of the deployment command"
    HELP = "Get information about deployed functions"
    CMD_ALIAS = []
    TARGETED_DEPLOY_FLAG = ENABLE_TYPE if (get_environ_tag() <= STAGING_ENV) else DISABLE_TYPE

    FUNCTION_ID_HELP = "Function ID"
    FUNCTION_VERSION_OPTIONAL_METAVAR = "function-id:[<function-id>]"
    TARGET_HELP = "Function. Format: function-id:function-version"
    FUNCTION_METAVAR = "<function-id>:<function-version-id>"
    DEPLOYMENT_SPECIFICATION_HELP = (
        "PENDING DEPRECATION. Deployment specs with GPU and Backend details, can specify multiple times."
    )
    CLI_HELP = ENABLE_TYPE

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser
        self.config = self.client.config
        self.printer = DeploymentPrinter(self.client.config)

    @CLICommand.arguments("target", metavar=FUNCTION_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.command(help="Info about a function deployment", description="Info about a function deployment")
    def info(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=True)
        resp = self.client.cloud_function.functions.deployments.info(ft.id, ft.version)
        self.printer.print_info(resp.get("deployment", {}))

    @CLICommand.arguments(
        "--graceful",
        help="Allow current tasks to complete before deleting deployment.",
        action="store_true",
    )
    @CLICommand.arguments("target", metavar=FUNCTION_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.command(help="Undeploy A function", description="Undeploy a function", aliases=["rm", "delete"])
    def remove(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=True)
        self.client.cloud_function.functions.deployments.delete(ft.id, ft.version, graceful=args.graceful)
        self.printer.print_ok("Delete successful")

    @CLICommand.arguments("target", metavar=FUNCTION_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.command(help="Restart a currently deployed function", description="restart", aliases=["redeploy"])
    def restart(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=True)
        resp = self.client.cloud_function.functions.deployments.restart(ft.id, ft.version)
        self.printer.print_info(resp.get("deployment", {}))

    @CLICommand.arguments("target", metavar=FUNCTION_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--configuration",
        dest="configuration",
        help="Helm chart overrides json will apply cross the functions, only for Helm chart deployment",
        type=str,
        default=None,
        required=False,
    )
    @CLICommand.arguments(
        "--deployment-specification",
        "--dep-spec",
        metavar="<backend:gpu:instance_type:min_instances:max_instances[:max_request_concurrency]>",
        action="append",
        help="Deployment specs with GPU and Backend details, can specify multiple times",
        default=None,
    )
    @CLICommand.arguments(
        "--targeted-deployment-specification",
        "--targeted-dep-spec",
        metavar=(
            "<gpu:instance_type:min_instances:max_instances[:max_request_concurrency]"
            "[:regions(region_1,region_2)][:attributes(attribute_1,attribute_2)][:preferredOrder]>",
        ),
        action="append",
        help="Deployment specs with GPU and instance type, can specify multiple times",
        default=None,
        feature_tag=TARGETED_DEPLOY_FLAG,
    )
    @CLICommand.mutex(["deployment_specification"], ["targeted_deployment_specification"])
    @CLICommand.command(help="Update an existing deployment", description="Update an existing deployment")
    def update(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=True)
        dep_specs = [DeploymentSpecification.from_str(dep_spec) for dep_spec in args.deployment_specification or []]
        targeted_dep_specs = [
            TargetedDeploymentSpecification.from_str(dep_spec)
            for dep_spec in args.targeted_deployment_specification or []
        ]

        if args.configuration is not None:
            helm_overrides_values = json.loads(args.configuration)
            for dep_spec in dep_specs:
                dep_spec.configuration = helm_overrides_values

        if args.configuration is not None:
            helm_overrides_values = json.loads(args.configuration)
            for dep_spec in targeted_dep_specs:
                dep_spec.configuration = helm_overrides_values

        resp = self.client.cloud_function.functions.deployments.update(ft.id, ft.version, dep_specs)
        self.printer.print_info(resp.get("deployment", {}))

    @CLICommand.arguments("target", metavar=FUNCTION_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--configuration",
        dest="configuration",
        help="Helm chart overrides json will apply cross the functions, only for Helm chart deployment",
        type=str,
        default=None,
        required=False,
    )
    @CLICommand.arguments(
        "--deployment-specification",
        "--dep-spec",
        metavar="<backend:gpu:instance_type:min_instances:max_instances[:maxRequestConcurrency]>",
        action="append",
        help="Deployment specs with GPU and Backend details, can specify multiple times",
        default=None,
    )
    @CLICommand.arguments(
        "--targeted-deployment-specification",
        "--targeted-dep-spec",
        metavar=(
            "<gpu:instance_type:min_instances:max_instances[:max_request_concurrency]"
            "[:regions(region_1,region_2)][:attributes(attribute_1,attribute_2)][:preferredOrder]>"
        ),
        action="append",
        help="Deployment specs with GPU and instance type, can specify multiple times",
        default=None,
        feature_tag=TARGETED_DEPLOY_FLAG,
    )
    @CLICommand.command(help="Create a deployment", description="Create a deployment")
    @CLICommand.mutex(["deployment_specification"], ["targeted_deployment_specification"])
    def create(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=True)
        dep_specs = [DeploymentSpecification.from_str(dep_spec) for dep_spec in args.deployment_specification or []]
        targeted_dep_specs = [
            TargetedDeploymentSpecification.from_str(dep_spec)
            for dep_spec in args.targeted_deployment_specification or []
        ]
        if args.configuration is not None:
            helm_overrides_values = json.loads(args.configuration)
            for dep_spec in dep_specs:
                dep_spec.configuration = helm_overrides_values
        resp = self.client.cloud_function.functions.deployments.create(ft.id, ft.version, dep_specs, targeted_dep_specs)
        self.printer.print_info(resp.get("deployment", {}))

    @CLICommand.arguments("target", metavar=FUNCTION_VERSION_OPTIONAL_METAVAR, help=TARGET_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--start-time",
        metavar="<t>",
        help="Specifies the start time for querying logs. Format: [yyyy-MM-dd::HH:mm:ss].",
        type=str,
        action=check_ymd_hms_datetime(),
    )
    @CLICommand.arguments(
        "--end-time",
        metavar="<t>",
        help="Specifies the end time for querying logs. Format: [yyyy-MM-dd::HH:mm:ss]. Default: now",
        type=str,
        action=check_ymd_hms_datetime(),
    )
    @CLICommand.arguments(
        "--duration",
        metavar="<t>",
        help=(
            "Specifies the duration of time, either after begin-time or before end-timelogs. Format: [nD][nH][nM][nS]."
            " Default 1 day, doesn't respect decimal measurements"
        ),
        type=str,
    )
    @CLICommand.command(help="Query Logs for NVCF Deployment", description="Query Logs for Deployment")
    def log(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=True)
        logs = self.client.cloud_function.functions.deployments.query_logs(
            function_id=ft.id,
            function_version_id=ft.version,
            duration=args.duration,
            start_time=args.start_time,
            end_time=args.end_time,
        )
        self.printer.print_logs(logs)
