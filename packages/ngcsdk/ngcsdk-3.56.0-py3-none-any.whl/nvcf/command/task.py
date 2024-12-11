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

from nvcf.api.deployment_spec import GPUSpecification
from nvcf.command.cloud_function import CloudFunctionCommand
from nvcf.printer.task_printer import TaskPrinter

from ngcbase.command.args_validation import check_dhms_duration, check_key_value_pattern
from ngcbase.command.clicommand import CLICommand
from ngcbase.constants import DISABLE_TYPE, ENABLE_TYPE, STAGING_ENV
from ngcbase.util.utils import get_environ_tag

TASK_FLAG = ENABLE_TYPE if (get_environ_tag() <= STAGING_ENV) else DISABLE_TYPE
RESULTS_HANDLING_STRATEGY_ENUM = ["UPLOAD", "NONE"]


class TaskCommand(CloudFunctionCommand):  # noqa: D101

    CMD_NAME = "task"
    DESC = "description of the task command"
    HELP = "Task Help"
    CMD_ALIAS = []
    COMMAND_DISABLE = get_environ_tag() > STAGING_ENV

    TASK_ID_HELP = "Task ID"
    TASK_ID_METAVAR = "<task-id>"

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser
        self.config = self.client.config
        self.printer = TaskPrinter(self.client.config)

    @CLICommand.arguments(
        "--name",
        metavar="<name>",
        help=("Task name"),
        type=str,
        required=True,
        default=None,
    )
    @CLICommand.arguments(
        "--container-image",
        metavar="<org>/[<team>/]<image>:<tag>",
        help="Custom container image",
        type=str,
        required=True,
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
        "--gpu-specification",
        metavar="<gpu:instance_type[:backend]>",
        help="GPU specification. Format: gpu:instance_type[:backend]",
        type=str,
        required=True,
        default=None,
    )
    @CLICommand.arguments(
        "--model",
        metavar="<model>",
        help="Name of model(s) to use in the task.",
        default=None,
        action="append",
    )
    @CLICommand.arguments(
        "--resource",
        metavar="<resource>",
        help="Name of resource(s) to use in the task.",
        action="append",
        default=None,
    )
    @CLICommand.arguments(
        "--tag",
        metavar="<tag>",
        help="Tags to identify the function by, can accept multiple",
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
        "--max-runtime-duration",
        metavar="<max-runtime-duration>",
        help=("Specifies the maximum runtime duration. Format: [nD][nH][nM][nS]."),
        type=str,
        action=check_dhms_duration(),
    )
    @CLICommand.arguments(
        "--max-queued-duration",
        metavar="<max-queued-duration>",
        help=("Specifies the maximum queued duration. Format: [nD][nH][nM][nS]."),
        type=str,
        action=check_dhms_duration(),
    )
    @CLICommand.arguments(
        "--termination-grace-period-duration",
        metavar="<termination-grave-period-duration>",
        help=("Specifies the duration for grace period after termination. Format: [nD][nH][nM][nS]."),
        type=str,
        action=check_dhms_duration(),
    )
    @CLICommand.arguments(
        "--result-handling-strategy",
        metavar="<result-handling-strategy>",
        help=("Specifies how results will be handled. Choices: {}".format(", ".join(RESULTS_HANDLING_STRATEGY_ENUM))),
        type=str,
    )
    @CLICommand.arguments(
        "--result-location",
        metavar="<result-location>",
        help=("Specifies where result will be stored.}"),
        type=str,
    )
    @CLICommand.arguments(
        "--secret",
        metavar="<name:value>",
        type=check_key_value_pattern,
        default=None,
        help="Secret name/value pair",
        action="append",
    )
    @CLICommand.command(help="Create a new task", description="Create a new task", feature_tag=TASK_FLAG)
    def create(self, args):  # noqa: D102
        gpu_spec = GPUSpecification.from_str(args.gpu_specification)
        resp = self.client.cloud_function.tasks.create(
            name=args.name,
            container_image=args.container_image,
            container_args=args.container_args,
            container_environment_variables=args.container_environment_variable,
            gpu_specification=gpu_spec,
            models=args.model,
            resources=args.resource,
            tags=args.tag,
            description=args.description,
            max_runtime_duration=args.max_runtime_duration,
            max_queued_duration=args.max_queued_duration,
            termination_grace_period_duration=args.termination_grace_period_duration,
            result_handling_strategy=args.result_handling_strategy,
            result_location=args.result_location,
            secrets=args.secret,
        )
        self.printer.print_info(resp.get("task", {}))

    @CLICommand.command(help="List of tasks", description="List of tasks", feature_tag=TASK_FLAG)
    def list(self, _):  # noqa: D102
        resp = self.client.cloud_function.tasks.list()
        self.printer.print_list(resp)

    @CLICommand.arguments("target", metavar=TASK_ID_METAVAR, help=TASK_ID_HELP, type=str, default=None)
    @CLICommand.command(help="Info about a task", description="Info about a task", feature_tag=TASK_FLAG)
    def info(self, args):  # noqa: D102
        resp = self.client.cloud_function.tasks.info(args.target)
        self.printer.print_info(resp.get("task", {}))

    @CLICommand.arguments("target", metavar=TASK_ID_METAVAR, help=TASK_ID_HELP, type=str, default=None)
    @CLICommand.command(
        help="Delete a task", description="Delete a task", aliases=["remove", "rm"], feature_tag=TASK_FLAG
    )
    def delete(self, args):  # noqa: D102
        self.client.cloud_function.tasks.delete(args.target)
        self.printer.print_ok(f"Successfully deleted task {args.target}.")

    @CLICommand.arguments("target", metavar=TASK_ID_METAVAR, help=TASK_ID_HELP, type=str, default=None)
    @CLICommand.command(
        help="List of events for a task", description="List of events for a task", feature_tag=TASK_FLAG
    )
    def events(self, args):  # noqa: D102
        resp = self.client.cloud_function.tasks.events(args.target)
        self.printer.print_task_events(resp)

    @CLICommand.arguments("target", metavar=TASK_ID_METAVAR, help=TASK_ID_HELP, type=str, default=None)
    @CLICommand.command(help="Cancel a task", description="Cancel a task", feature_tag=TASK_FLAG)
    def cancel(self, args):  # noqa: D102
        self.client.cloud_function.tasks.cancel(args.target)
        self.printer.print_ok(f"Successfully canceled task: {args.target}")
