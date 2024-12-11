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

from nvcf.command.function import FunctionCommand
from nvcf.command.utils import FunctionTarget

from ngcbase.api.utils import NgcException
from ngcbase.command.clicommand import CLICommand
from ngcbase.constants import ENABLE_TYPE


class FunctionAuthorizationCommand(FunctionCommand):  # noqa: D101

    CMD_NAME = "authorization"
    HELP = "Function Authorization Commands. Admin Only."
    DESC = "Function Authorization Commands. Admin Only."
    CMD_ALIAS = ["auth"]
    CLI_HELP = ENABLE_TYPE
    FUNCTION_ID_HELP = "Function ID with optional function version ID"
    TARGET_HELP = "Function. Format: function-id:function-version"
    AP_HELP = "Authorized Party. NCA ID"
    FUNCTION_METAVAR = "<function-id>:[<function-version-id>]"
    VERSION_METAVAR = "<function-id>:<function-version-id>"
    AUTHORIZED_PARTY_METAVAR = "<nca-id>"

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser
        self.config = self.client.config

    @CLICommand.command(
        help="Get account authorizations for function version or function",
        description="Gets NVIDIA Cloud Account IDs that are authorized to invoke specified functions/function versions",
    )
    @CLICommand.arguments("target", metavar=FUNCTION_METAVAR, help=TARGET_HELP, type=str, default=None)
    def info(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=False)
        resp = self.client.cloud_function.functions.authorizations.info(ft.id, ft.version)
        self.printer.print_auth_info(resp)

    @CLICommand.command(
        help="Clear all function's extra authorizations", description="Clear all function's extra authorizations"
    )
    @CLICommand.arguments("target", metavar=FUNCTION_METAVAR, help=TARGET_HELP, type=str, default=None)
    def clear(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=False)
        self.client.cloud_function.functions.authorizations.clear(ft.id, ft.version)
        resp = self.client.cloud_function.functions.authorizations.info(ft.id, ft.version)
        self.printer.print_auth_info(resp)

    @CLICommand.arguments(
        "--authorized-party",
        metavar=AUTHORIZED_PARTY_METAVAR,
        help=AP_HELP,
        type=str,
        default=None,
        required=True,
    )
    @CLICommand.command(
        help="Unauthorize account from invoking function or function version",
        description="Unauthorize account from invoking function or function version",
        aliases=["delete", "rm"],
    )
    @CLICommand.arguments(
        "target",
        metavar=FUNCTION_METAVAR,
        help=TARGET_HELP,
        type=str,
        default=None,
    )
    def remove(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=False)
        resp = self.client.cloud_function.functions.authorizations.remove(ft.id, ft.version, args.authorized_party)
        self.printer.print_auth_info(resp)

    @CLICommand.arguments(
        "--authorized-party",
        metavar=AUTHORIZED_PARTY_METAVAR,
        help=AP_HELP,
        type=str,
        default=None,
        required=True,
    )
    @CLICommand.command(
        help="Authorize accounts to function version or function",
        description="Authorize accounts to function version or function",
    )
    @CLICommand.arguments("target", metavar=VERSION_METAVAR, help=TARGET_HELP, type=str, default=None)
    def add(self, args):  # noqa: D102
        ft: FunctionTarget = FunctionTarget(args.target, id_required=True, version_required=True)
        if args.authorized_party == "*":
            raise NgcException("This operation is not allowed")
        resp = self.client.cloud_function.functions.authorizations.add(ft.id, ft.version, args.authorized_party)
        self.printer.print_auth_info(resp)
