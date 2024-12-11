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

from nvcf.printer.deploy_printer import DeploymentPrinter

from ngcbase.command.clicommand import CLICommand
from ngcbase.constants import ENABLE_TYPE


class CloudFunctionCommand(CLICommand):  # noqa: D101
    CMD_NAME = "cloud-function"
    HELP = "Cloud Function Commands"
    DESC = "Cloud Function Commands"
    CMD_ALIAS = ["cf", "picasso"]
    CLI_HELP = ENABLE_TYPE

    def __init__(self, parser):
        super().__init__(parser)
        self.make_bottom_commands(parser)
        self.printer = DeploymentPrinter(self.client.config)

    @CLICommand.command(
        name="available-gpus",
        help="List available GPUs in your Org, Admin Only. Pending deprecation.",
        description="List available GPUs in your Org, Admin Only",
    )
    def available_gpus(self, _):  # noqa: D102
        self.printer.print_available_gpus_deprecation_warning()
        resp = self.client.cloud_function.deployments.list_cluster_groups()
        self.printer.print_gpus(resp.get("clusterGroups", {}))
