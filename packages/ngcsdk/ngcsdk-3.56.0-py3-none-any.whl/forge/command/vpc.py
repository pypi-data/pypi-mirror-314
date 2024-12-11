# Copyright (c) 2019-2022, NVIDIA CORPORATION.  All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from forge.command.forge import ForgeCommand
from forge.printer.vpc import VpcPrinter
from ngcbase.command.args_validation import check_add_args_columns, check_valid_columns
from ngcbase.command.clicommand import CLICommand
from ngcbase.util.utils import get_columns_help


class VpcCommand(ForgeCommand):  # noqa: D101

    CMD_NAME = "vpc"
    HELP = "VPC Commands"
    DESC = "VPC Commands"

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser
        self.config = self.client.config
        self.api = self.client.forge.vpc
        self.printer = VpcPrinter(self.client.config)

    LIST_HELP = "List VPCs."

    columns_dict = {
        "name": "Name",
        "description": "Description",
        "org": "Org",
        "tenantId": "Tenant Id",
        "tenantName": "Tenant Name",
        "infrastructureProviderId": "Infrastructure Provider Id",
        "infrastructureProviderName": "Infrastructure Provider Name",
        "siteId": "Site Id",
        "siteName": "Site Name",
        "status": "Status",
        "created": "Created",
        "updated": "Updated",
    }
    columns_default = ("id", "Id")
    columns_help = get_columns_help(columns_dict, columns_default)
    status_enum = ["Pending", "Provisioning", "Ready", "Deleting", "Error"]

    @CLICommand.arguments(
        "target",
        metavar="<target>",
        help="Filter by matches across all VPCs. Input will be matched against name, description and status fields.",
        type=str,
        nargs="?",
        default=None,
    )
    @CLICommand.arguments(
        "--status",
        metavar="<status>",
        help=f"Filter by status. Choices are: {', '.join(status_enum)}",
        type=str,
        default=None,
        choices=status_enum,
    )
    @CLICommand.arguments(
        "--column",
        metavar="<column>",
        help=columns_help,
        default=None,
        action="append",
        type=lambda value, columns_dict=columns_dict: check_valid_columns(value, columns_dict),
    )
    @CLICommand.arguments("--site", metavar="<site>", help="Filter by site id.", type=str)
    @CLICommand.command(help=LIST_HELP, description=LIST_HELP)
    def list(self, args):
        """List VPCs."""
        resp = self.api.list(args.org, args.team, args.site, args.target, args.status)
        check_add_args_columns(args.column, VpcCommand.columns_default)
        self.printer.print_list(resp, args.column)

    INFO_HELP = "VPC information."

    @CLICommand.arguments("vpc", metavar="<vpc>", help="VPC id.", type=str)
    @CLICommand.arguments("--status-history", help="Show status history.", action="store_true")
    @CLICommand.command(help=INFO_HELP, description=INFO_HELP)
    def info(self, args):
        """Vpc info."""
        resp = self.api.info(args.vpc, args.org, args.team)
        self.printer.print_info(resp, args.status_history)

    CREATE_HELP = "Create VPC."

    @CLICommand.arguments("name", metavar="<name>", help="VPC name.", type=str)
    @CLICommand.arguments("--description", metavar="<desc>", help="Specify VPC description.", type=str)
    @CLICommand.arguments("--site", metavar="<site>", help="Specify site id.", type=str, required=True)
    @CLICommand.command(help=CREATE_HELP, description=CREATE_HELP)
    def create(self, args):
        """Create VPC."""
        resp = self.api.create(args.name, args.site, args.org, args.team, args.description)
        self.printer.print_info(resp)

    UPDATE_HELP = "Update VPC."

    @CLICommand.arguments("vpc", metavar="<vpc>", help="VPC id.", type=str)
    @CLICommand.arguments("--name", metavar="<name>", help="Specify VPC name.", type=str)
    @CLICommand.arguments("--description", metavar="<desc>", help="Specify VPC description.", type=str)
    @CLICommand.command(help=UPDATE_HELP, description=UPDATE_HELP)
    def update(self, args):
        """Update VPC."""
        resp = self.api.update(args.vpc, args.org, args.team, args.name, args.description)
        self.printer.print_info(resp)

    REMOVE_HELP = "Remove VPC."

    @CLICommand.arguments("vpc", metavar="<vpc>", help="VPC id.", type=str)
    @CLICommand.command(help=REMOVE_HELP, description=REMOVE_HELP)
    def remove(self, args):
        """Remove VPC."""
        resp = self.api.remove(args.vpc, args.org, args.team)
        self.printer.print_ok(f"{resp}")
