#
# Copyright (c) 2018-2021, NVIDIA CORPORATION.  All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
from builtins import int
import logging

from ngcbase.command.args_validation import (
    check_url,
    check_valid_columns,
    SingleUseAction,
)
from ngcbase.command.clicommand import CLICommand
from ngcbase.constants import (
    CANARY_ENV,
    CONFIG_TYPE,
    DISABLE_TYPE,
    ENABLE_TYPE,
    PRODUCT_NAMES,
)
from ngcbase.errors import InvalidArgumentError, NgcException, ResourceNotFoundException
from ngcbase.printer.nvPrettyPrint import NVPrettyPrint
from ngcbase.printer.transfer import TransferPrinter
from ngcbase.util.utils import (
    confirm_remove,
    find_case_insensitive,
    get_columns_help,
    get_environ_tag,
)
from registry.api.utils import ModelRegistryTarget
from registry.command.publish import (
    ACCESS_TYPE_HELP,
    ALLOW_GUEST_HELP,
    DISCOVERABLE_HELP,
    GET_STATUS_HELP,
    METADATA_HELP,
    PRODUCT_HELP,
    PUBLIC_HELP,
    publish_action_args,
    publish_status_args,
    validate_command_args,
    VERSION_ONLY_HELP,
    VISIBILITY_HELP,
)
from registry.command.registry import RegistryCommand
from registry.data.model.SortOrderEnum import SortOrderEnum
from registry.data.registry.AccessTypeEnum import AccessTypeEnum
from registry.printer.model import ModelPrinter
from registry.printer.publish import PublishPrinter

logger = logging.getLogger(__name__)

# TODO: As of 2020-02-25, these are hard-coded in the UI and CLI. If they become part of the schema,
# reference that and remove this class.
LINK_TYPE_VALUES = ["NGC", "Github", "Other"]
PUBLISH_TYPE = ENABLE_TYPE if (get_environ_tag() <= CANARY_ENV) else DISABLE_TYPE


def verify_link_type(args):
    """If a link_type has been specified, make sure it is valid, and if so, convert to the canonical capitalization."""
    if args.link_type:
        args.link_type = find_case_insensitive(args.link_type, LINK_TYPE_VALUES, "link_type")


class ModelSubCommand(RegistryCommand):  # noqa: D101
    CMD_NAME = "model"
    HELP = "Model Commands"
    DESC = "Model Commands"
    CLI_HELP = ENABLE_TYPE

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser

        self.model_printer = ModelPrinter(self.client.config)
        self.transfer_printer = TransferPrinter(self.client.config)
        self.config = self.client.config
        self.model_api = self.client.registry.model
        self.search_api = self.client.registry.search
        self.label_set_api = self.client.registry.label_set
        self.publish_api = self.client.registry.publish
        self.resource_type = "MODEL"
        self.publish_printer = PublishPrinter(self.client.config)

    if CLICommand.CLI_CLIENT and bool(CLICommand.CLI_CLIENT.config.product_names):
        product_names = CLICommand.CLI_CLIENT.config.product_names
    else:
        product_names = PRODUCT_NAMES

    # Model specific
    model_target_arg_help = "Model.  Format: org/[team/]model_name."

    # Model version specific
    download_version_target_arg_help = (
        "Model version. Format: org/[team/]model_name[:version].  "
        "If no version specified, the latest version will be targeted."
    )

    upload_version_target_arg_help = "Model version. Format: org/[team/]model_name:version."

    # Model or Model version specific
    model_version_target_arg_help = (
        "Model or model version.  Format: org/[team/]model_name[:version]. "
        'To target a model version, use "org/[team/]model_name:version".  '
        'To target a model, use "org/[team/]model_name".'
    )

    default_version_sort = "SEMVER_DESC"
    model_version_sort_arg_help = "Sort model versions.  Allowed values: {}.  Default: {}.".format(
        ", ".join(SortOrderEnum), default_version_sort
    )

    # list specific
    list_target_arg_help = (
        "Filter the search by allowing wildcards for "
        "Model(s) or model version(s). Format: org/[team/]name[:version]. To target model version(s), "
        'use "org/[team/]name:version". To target model(s), use "org/[team/]name". Name and version also supports '
        'the wildcards "*" and "?". Examples: '
        '"my_org/my_model" - target my_model in my_org namespace. '
        '"my_org/my_team/my_model" - target my_model in my_org/my_team namespace. '
        '"my_org/my_team/*" - target all models in my_org/my_team namespace. '
        '"my_org/my_model*" - target models starting with my_model in my_org namespace. '
    )
    list_help = "List model(s) or model version(s)."

    columns_dict = {
        "name": "Name",
        "org": "Org",
        "team": "Team",
        "description": "Description",
        "updated": "Last Modified",
        "created": "Created Date",
        "shared": "Shared",
        "size": "File Size",
        "repository": "Repository",
        "version": "Latest Version",
        "application": "Application",
        "framework": "Framework",
        "precision": "Precision",
        "permission": "Permission",
        "accuracy": "Accuracy",
        "epochs": "Epochs",
        "batch": "Batch Size",
        "gpu": "GPU Model",
        "memory": "Memory Footprint",
        "status": "Status",
        "labels": "Labels",
    }
    columns_default_model = ("repository", "Repository")
    columns_default_version = ("version", "Version")
    columns_help = get_columns_help(columns_dict, [columns_default_model, columns_default_version])
    ACCESS_TYPE_LIST_HELP = "Filter the list of resources to only resources that have specified access type."
    PRODUCT_NAME_LIST_HELP = (
        "Filter the list of resources to only resources that are under the product name. Multiple product-name"
        f" arguments are allowed. Choose from: {', '.join(product_names)}"
    )

    @CLICommand.arguments("target", metavar="<target>", help=list_target_arg_help, type=str, nargs="?", default=None)
    # pylint:disable=undefined-variable
    @CLICommand.arguments(
        "--column",
        metavar="<column>",
        help=columns_help,
        default=None,
        action="append",
        type=lambda value, columns_dict=columns_dict: check_valid_columns(value, columns_dict),
    )
    @CLICommand.arguments(
        "--sort",
        metavar="<order>",
        help=model_version_sort_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
        choices=SortOrderEnum,
    )
    @CLICommand.arguments(
        "--access-type",
        metavar="<access_type>",
        help=ACCESS_TYPE_LIST_HELP,
        choices=AccessTypeEnum,
        default=None,
    )
    @CLICommand.arguments(
        "--product-name",
        metavar="<product_name>",
        help=PRODUCT_NAME_LIST_HELP,
        default=None,
        action="append",
    )
    @CLICommand.command(help=list_help, description=list_help)
    def list(self, args):
        """Lists models."""  # noqa: D401
        mrt = ModelRegistryTarget(args.target, glob_allowed=True)
        product_names_args = args.product_name if args.product_name else []
        product_names_args = [name.replace("-", "_") for name in product_names_args]

        model_list = self.model_api.list(
            args.target, mrt.org, mrt.team, args.sort, args.access_type, product_names_args
        )
        if mrt.version is None:
            self.model_printer.print_model_list(model_list, args.column)
        else:
            self.model_printer.print_model_version_list(model_list, columns=args.column)

    info_help = "Retrieve metadata for a model or model version."
    credentials_help = "List model credentials in addition to details for a version."
    metrics_help = f"{credentials_help} DEPRECATED; will be removed after May 2021. Please use '--credentials' instead."

    @CLICommand.command(help=info_help, description=info_help)
    @CLICommand.arguments("target", metavar="<target>", help=model_version_target_arg_help, type=str, default=None)
    @CLICommand.arguments(
        "--files", help="List files in addition to details for a version.", dest="list_files", action="store_true"
    )
    @CLICommand.arguments("--credentials", help=credentials_help, action="store_true")
    @CLICommand.arguments("--metrics", help=metrics_help, action="store_true")
    @CLICommand.mutex(["credentials"], ["metrics"])
    def info(self, args):
        """Retrieve metadata for a model or version."""
        mrt = ModelRegistryTarget(args.target, org_required=True, name_required=True)
        if args.metrics:
            self.model_printer.print_metrics_deprecation_warning("--metrics")
        if not mrt.version:
            arg_name = ""
            if args.credentials:
                arg_name = "credentials"
            elif args.metrics:
                arg_name = "metrics"
            if args.list_files:
                arg_name = "files"
            if arg_name:
                raise InvalidArgumentError(
                    f"--{arg_name} argument is not valid for a model target; please specify a version"
                )

        model = self.model_api.info(target=args.target)

        if mrt.version:
            # TODO: Collapse List Files into Info API function
            credentials = args.credentials or args.metrics
            file_list = self.get_version_files(args.target, mrt.org, mrt.team) if args.list_files else None
            self.model_printer.print_model_version(
                version=model.modelVersion, model=model.model, file_list=file_list, credentials=credentials
            )
        else:
            self.model_printer.print_model(model.model)

    def get_version_files(self, target, org_name, team_name):  # noqa: D102
        try:
            file_list = self.model_api.list_files(target=target, org=org_name, team=team_name)
        except ResourceNotFoundException:
            mrt = ModelRegistryTarget(target, org_required=True, name_required=True)
            raise ResourceNotFoundException(
                f"Files could not be found for target '{mrt.name}:{mrt.version}'."
            ) from None
        return file_list

    # TODO group by model/version in help output
    # model specific
    application_arg_help = "Model application."
    framework_arg_help = "Framework used to train the model."
    format_arg_help = "Format of the model."
    precision_arg_help = "Precision the model was trained with."
    short_desc_arg_help = "Short description of the model."
    display_name_arg_help = "Display name for the model."
    ADD_LABEL_HELP = (
        "Label for the model to add. Can be used multiple times."
        "Imperative label argument, not to be used with declarative label arguments --label or --label-set"
    )
    REMOVE_LABEL_HELP = (
        "Label for the model to remove. Can be used multiple times."
        "Imperative label argument, not to be used with declarative label arguments --label or --label-set"
    )
    LABEL_HELP = (
        "Label for the model to declare. Can be used multiple times."
        "Declarative label argument, not to be used with declarative label arguments —add-label or —remove-label"
    )
    LABEL_SET_HELP = (
        "Name of the label set for the model to declare. Can be used multiple times. Format: org/[team/]name. "
        "Declarative label argument, not to be used with declarative label arguments —add-label or —remove-label"
    )
    logo_arg_help = "URL for the model logo image."
    public_dataset_name_help = "Name of public dataset used in the model."
    public_dataset_link_help = "Link to public dataset used in the model."
    public_dataset_license_help = "License for public dataset used in the model."
    built_by_help = "Builder of the model."
    publisher_help = "Publisher of the model."
    # Note: model level overview attribute is stored in description in the schema.
    # UI diverged and we need to quickly match them now.
    overview_arg_help = "Overview. Provide the path to a file that contains the overview for the model."
    bias_arg_help = "Bias. Provide the path to a file that contains the bias in the model."
    explainability_arg_help = (
        "Explainability.  Provide the path to a file that contains the explainability for this model."
    )
    privacy_arg_help = "Privacy. Provide the path to a file that contains the privacy for this model."
    safety_arg_help = (
        "Safety and Security. Provide the path to a file that contains the safety and security in the model."
    )

    # version specific
    gpu_model_arg_help = "The GPU used to train the model version."
    desc_arg_help = "Description for the model version."
    mem_footprint_arg_help = "The memory footprint of the model version."
    num_epochs_arg_help = "The number of epochs for the model version."
    batch_size_arg_help = "The batch size of the model version."
    accuracy_reached_arg_help = "Accuracy reached with model version."
    link_type_help = "Type of link to a resource or other toolsets for the model. Choices: {}.".format(
        ", ".join(LINK_TYPE_VALUES)
    )
    credentials_file_help = (
        "A JSON file containing a single object with 'name' and 'attributes' fields. Attributes are a list of "
        "key-value pair each takes the form of {'key': KEY, 'value': VALUE}. "
        "A maximum of twelve attributes may be used per file, and up to three files may be specified."
    )
    metrics_file_help = (
        f"{credentials_file_help} DEPRECATED; will be removed after May 2021. Please use --credentials-file instead."
    )

    create_help = "Create a model."

    @CLICommand.command(help=create_help, description=create_help, feature_tag=CONFIG_TYPE)
    @CLICommand.arguments("target", metavar="<target>", help=model_target_arg_help, type=str, default=None)
    @CLICommand.arguments(
        "--application",
        metavar="<app>",
        help=application_arg_help,
        type=str,
        default=None,
        required=True,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--framework",
        metavar="<fwk>",
        help=framework_arg_help,
        type=str,
        default=None,
        required=True,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--format",
        metavar="<fmt>",
        help=format_arg_help,
        dest="model_format",
        type=str,
        default=None,
        required=True,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--precision",
        metavar="<prec>",
        help=precision_arg_help,
        type=str,
        default=None,
        required=True,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--short-desc",
        metavar="<desc>",
        help=short_desc_arg_help,
        type=str,
        default=None,
        required=True,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--overview-filename", metavar="<path>", help=overview_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--bias-filename",
        metavar="<path>",
        help=bias_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--explainability-filename",
        metavar="<path>",
        help=explainability_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--privacy-filename",
        metavar="<path>",
        help=privacy_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--safety-security-filename",
        metavar="<path>",
        help=safety_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--display-name", metavar="<name>", help=display_name_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments("--label", metavar="<label>", help=LABEL_HELP, action="append", type=str, default=None)
    @CLICommand.arguments(
        "--label-set", metavar="<label-set>", help=LABEL_SET_HELP, action="append", type=str, default=None
    )
    @CLICommand.arguments(
        "--logo", metavar="<url>", help=logo_arg_help, type=check_url, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--public-dataset-name",
        metavar="<name>",
        help=public_dataset_name_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--public-dataset-link",
        metavar="<link>",
        help=public_dataset_link_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--public-dataset-license",
        metavar="<lcs>",
        help=public_dataset_license_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--built-by", metavar="<name>", help=built_by_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--publisher", metavar="<name>", help=publisher_help, type=str, default=None, action=SingleUseAction
    )
    def create(self, args):
        """Create a model."""
        created_model = self.model_api.create(
            target=args.target,
            application=args.application,
            framework=args.framework,
            model_format=args.model_format,
            precision=args.precision,
            short_description=args.short_desc,
            overview_filename=args.overview_filename,
            bias_filename=args.bias_filename,
            explainability_filename=args.explainability_filename,
            privacy_filename=args.privacy_filename,
            safety_security_filename=args.safety_security_filename,
            display_name=args.display_name,
            label=args.label,
            label_set=args.label_set,
            logo=args.logo,
            public_dataset_name=args.public_dataset_name,
            public_dataset_license=args.public_dataset_license,
            public_dataset_link=args.public_dataset_link,
            built_by=args.built_by,
            publisher=args.publisher,
        )
        self.model_printer.print_head(f"Successfully created model '{args.target}'.")
        self.model_printer.print_model(created_model)

    update_help = "Update a model or model version."

    # FIXME - we are suppressing metavar for optional args to match help output of globals
    @CLICommand.command(help=update_help, description=update_help, feature_tag=CONFIG_TYPE)
    @CLICommand.arguments("target", metavar="<target>", help=model_version_target_arg_help, type=str, default=None)
    @CLICommand.arguments(
        "--application", metavar="<app>", help=application_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--framework", metavar="<fwk>", help=framework_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--format",
        metavar="<fmt>",
        help=format_arg_help,
        dest="model_format",
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--precision", metavar="<prec>", help=precision_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--short-desc", metavar="<desc>", help=short_desc_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--desc", metavar="<desc>", help=desc_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--overview-filename", metavar="<path>", help=overview_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--bias-filename",
        metavar="<path>",
        help=bias_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--explainability-filename",
        metavar="<path>",
        help=explainability_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--privacy-filename",
        metavar="<path>",
        help=privacy_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--safety-security-filename",
        metavar="<path>",
        help=safety_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--display-name", metavar="<name>", help=display_name_arg_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--add-label",
        metavar="<add-label>",
        help=ADD_LABEL_HELP,
        type=str,
        default=None,
        action="append",
    )
    @CLICommand.arguments(
        "--remove-label",
        metavar="<remove-label>",
        help=REMOVE_LABEL_HELP,
        type=str,
        default=None,
        action="append",
    )
    @CLICommand.arguments("--label", metavar="<label>", help=LABEL_HELP, action="append", type=str, default=None)
    @CLICommand.arguments(
        "--label-set", metavar="<label-set>", help=LABEL_SET_HELP, action="append", type=str, default=None
    )
    @CLICommand.arguments(
        "--logo", metavar="<url>", help=logo_arg_help, type=check_url, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--public-dataset-name",
        metavar="<name>",
        help=public_dataset_name_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--public-dataset-link",
        metavar="<url>",
        help=public_dataset_link_help,
        type=check_url,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--public-dataset-license",
        metavar="<lcs>",
        help=public_dataset_license_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--built-by", metavar="<name>", help=built_by_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--publisher", metavar="<name>", help=publisher_help, type=str, default=None, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--gpu-model",
        metavar="<model>",
        dest="gpu_model",
        help=gpu_model_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--memory-footprint",
        dest="mem_footprint",
        metavar="<footprint>",
        help=mem_footprint_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--num-epochs",
        metavar="<num>",
        dest="num_epoch",
        help=num_epochs_arg_help,
        type=int,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--batch-size",
        metavar="<size>",
        dest="batch_size",
        help=batch_size_arg_help,
        type=int,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--accuracy-reached",
        metavar="<accuracy>",
        dest="accuracy_reached",
        help=accuracy_reached_arg_help,
        type=float,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--set-latest", help="Set this version to be the latest version.", default=None, action="store_true"
    )
    @CLICommand.mutex(["label", "label_set"], ["add_label", "remove_label"])
    def update(self, args):
        """Update a model or version."""
        _mrt = ModelRegistryTarget(args.target, org_required=True, name_required=True)

        model = self.model_api.update(
            target=args.target,
            application=args.application,
            framework=args.framework,
            model_format=args.model_format,
            precision=args.precision,
            short_description=args.short_desc,
            overview_filename=args.overview_filename,
            bias_filename=args.bias_filename,
            explainability_filename=args.explainability_filename,
            privacy_filename=args.privacy_filename,
            safety_security_filename=args.safety_security_filename,
            display_name=args.display_name,
            labels=args.label,
            add_label=args.add_label,
            remove_label=args.remove_label,
            label_set=args.label_set,
            logo=args.logo,
            public_dataset_name=args.public_dataset_name,
            public_dataset_license=args.public_dataset_license,
            public_dataset_link=args.public_dataset_link,
            built_by=args.built_by,
            publisher=args.publisher,
            num_epochs=args.num_epoch,
            batch_size=args.batch_size,
            accuracy_reached=args.accuracy_reached,
            set_latest=args.set_latest,
            gpu_model=args.gpu_model,
            memory_footprint=args.mem_footprint,
        )

        if _mrt.version is None:
            self.model_printer.print_head("Successfully updated model '{}'.".format(args.target))
            self.model_printer.print_model(model)
        else:
            self.model_printer.print_head(f"Successfully updated model version '{args.target}'.")
            self.model_printer.print_model_version(model.modelVersion)

    delete_help = "Remove a model or model version."

    # TODO - don't allow model removal if versions still exist.
    @CLICommand.command(help=delete_help, description=delete_help, feature_tag=CONFIG_TYPE)
    @CLICommand.arguments("target", metavar="<target>", help=model_version_target_arg_help, type=str, default=None)
    @CLICommand.arguments(
        "-y",
        "--yes",
        help="Automatically say yes to all interactive questions.",
        dest="default_yes",
        action="store_true",
    )
    def remove(self, args):
        """Delete a model."""
        confirm_remove(printer=self.model_printer, target=args.target, default=args.default_yes)
        mrt = ModelRegistryTarget(args.target, org_required=True, name_required=True)
        self.model_api.remove(target=args.target)
        if mrt.version:
            self.model_printer.print_ok(f"Successfully removed model version '{args.target}'.")
        else:
            self.model_printer.print_ok(f"Successfully removed model '{args.target}'.")

    download_version_help = "Download a model version."

    @CLICommand.command(name="download-version", help=download_version_help, description=download_version_help)
    @CLICommand.arguments("target", metavar="<target>", help=download_version_target_arg_help, type=str, default=None)
    @CLICommand.arguments(
        "--dest",
        metavar="<path>",
        help="Destination to download the current model.  Default: .",
        type=str,
        default="",
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--file",
        metavar="<wildcard>",
        action="append",
        help=(
            "Specify individual files to download from the model.\n"
            "Supports standard Unix shell-style wildcards like (?, [abc], [!a-z], etc..) "
            "May be used multiple times in the same command."
        ),
    )
    @CLICommand.arguments(
        "--exclude",
        metavar="<wildcard>",
        action="append",
        help=(
            "Exclude files or directories from the downloaded model.\n"
            "Supports standard Unix shell-style wildcards like (?, [abc], [!a-z], etc..). "
            "May be used multiple times in the same command."
        ),
    )
    def download_version(self, args):
        """Download the specified model version."""
        self.model_api.download_version(
            target=args.target, destination=args.dest, file_patterns=args.file, exclude_patterns=args.exclude
        )

    def _get_latest_version(self, target):
        try:
            model_resp = self.model_api.get(target.org, target.team, target.name)
        except ResourceNotFoundException:
            raise ResourceNotFoundException("Target '{}' could not be found.".format(target)) from None
        if not model_resp.model.latestVersionIdStr:
            raise NgcException("Target '{}' has no version available for download.".format(target))

        return model_resp.model.latestVersionIdStr

    upload_version_help = "Upload a model version."

    @CLICommand.command(
        name="upload-version", help=upload_version_help, description=upload_version_help, feature_tag=CONFIG_TYPE
    )
    @CLICommand.arguments("target", metavar="<target>", help=upload_version_target_arg_help, type=str, default=None)
    @CLICommand.arguments(
        "--source",
        metavar="<path>",
        help="Provide source directory of the model or path of single file to be uploaded.  Default: .",
        type=str,
        default=".",
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--gpu-model",
        metavar="<model>",
        dest="gpu_model",
        help=gpu_model_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--memory-footprint",
        dest="mem_footprint",
        metavar="<footprint>",
        help=mem_footprint_arg_help,
        type=str,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--num-epochs",
        metavar="<num>",
        dest="num_epoch",
        help=num_epochs_arg_help,
        type=int,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--batch-size",
        metavar="<size>",
        dest="batch_size",
        help=batch_size_arg_help,
        type=int,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments(
        "--accuracy-reached",
        metavar="<accuracy>",
        dest="accuracy_reached",
        help=accuracy_reached_arg_help,
        type=float,
        default=None,
        action=SingleUseAction,
    )
    @CLICommand.arguments("--desc", metavar="<desc>", help=desc_arg_help, type=str, default="", action=SingleUseAction)
    @CLICommand.arguments(
        "--dry-run",
        help="List file paths, total upload size and file count without performing the upload.",
        action="store_true",
        default=False,
        dest="dry_run",
    )
    @CLICommand.arguments(
        "--link-type", metavar="<type>", default=None, help=link_type_help, type=str, action=SingleUseAction
    )
    @CLICommand.arguments(
        "--link",
        metavar="<url>",
        help="Link to resource or other toolsets for the model",
        action=SingleUseAction,
        type=check_url,
    )
    @CLICommand.arguments(
        "--credentials-file", metavar="<file>", help=credentials_file_help, action="append", default=None
    )
    @CLICommand.arguments("--metrics-file", metavar="<file>", help=metrics_file_help, action="append", default=None)
    @CLICommand.arguments(
        "--force",
        help="Append and overwrite files for a model version that have been marked UPLOAD_PENDING.",
        action="store_true",
        default=False,
        dest="force",
    )
    @CLICommand.arguments(
        "--base-version",
        help=(
            "Include files from a specific version."
            "Files with the same path are overwritten in order of arguments, then by source."
        ),
        action="append",
        default=None,
        metavar="<model version>",
        dest="base_version",
        feature_tag=PUBLISH_TYPE,
    )
    @CLICommand.mutex(["credentials_file"], ["metrics_file"])
    def upload_version(self, args):
        """Upload a model version."""
        if args.metrics_file:
            self.model_printer.print_metrics_deprecation_warning("--metrics_file")

        printer = NVPrettyPrint(self.config)
        progress_bar = printer.create_transfer_progress_bar()
        task_id = progress_bar.add_task("Uploading...", start=True, total=0, completed=0)

        def callback(completed_bytes, _, total_bytes, completed_count, failed_count, total_count):
            file_text = f"[blue]Total: {total_count} - Completed: {completed_count} - Failed: {failed_count}"
            progress_bar.file_column.text_format = file_text
            printer.update_task(task_id, total=total_bytes, completed=completed_bytes)

        upload_res = ("", "", "", 0.0, 0, 0, "", "")
        with progress_bar:
            upload_res = (
                self.model_api.upload_version(
                    target=args.target,
                    source=args.source,
                    gpu_model=args.gpu_model,
                    memory_footprint=args.mem_footprint,
                    num_epochs=args.num_epoch,
                    batch_size=args.batch_size,
                    accuracy_reached=args.accuracy_reached,
                    description=args.desc,
                    link=args.link,
                    link_type=args.link_type,
                    dry_run=args.dry_run,
                    credential_files=args.credentials_file,
                    metric_files=args.metrics_file,
                    force=args.force,
                    base_versions=args.base_version,
                    progress_callback_func=callback,
                )
                or upload_res
            )
        # print statement will add additional output for progress_bar,
        # thus print statement after progress_bar close
        self.transfer_printer.print_async_upload_transfer_summary("model", *upload_res)

    model_metavar = "org/[team/]model_name[:version]"
    publish_help = (
        "Publish a model from the NGC model registry to catalog.  If no version is provided, 'latest' is assumed."
    )
    publish_target_help = (
        "The the target model and version you want to publish to.  "
        "Optional when getting publishing status using the `--status` flag.  "
        f"Format: {model_metavar}"
    )
    source_help = f"The source model and version you want to publish.  Format: {model_metavar}"
    product_help = PRODUCT_HELP + ", ".join(product_names)

    @CLICommand.command(help=publish_help, description=publish_help, feature_tag=PUBLISH_TYPE)
    @CLICommand.arguments("target", metavar=model_metavar, nargs="?", help=publish_target_help, type=str)
    @CLICommand.arguments("--source", metavar=model_metavar, help=source_help, type=str, default=None)
    @CLICommand.arguments("--metadata-only", help=METADATA_HELP, action="store_true")
    @CLICommand.arguments("--version-only", help=VERSION_ONLY_HELP, action="store_true")
    @CLICommand.arguments("--visibility-only", help=VISIBILITY_HELP, action="store_true")
    @CLICommand.arguments("--allow-guest", help=ALLOW_GUEST_HELP, action="store_true")
    @CLICommand.arguments("--discoverable", help=DISCOVERABLE_HELP, action="store_true")
    @CLICommand.arguments("--public", help=PUBLIC_HELP, action="store_true")
    @CLICommand.arguments(
        "--product-name",
        metavar="<product_name>",
        help=product_help,
        action="append",
        default=None,
    )
    @CLICommand.arguments("--status", metavar="<workflow_id>", help=GET_STATUS_HELP, type=str, default=None)
    @CLICommand.arguments(
        "--access-type", metavar="<access_type>", help=ACCESS_TYPE_HELP, type=str, default=None, choices=AccessTypeEnum
    )
    @CLICommand.mutex(["metadata_only"], ["version_only"], ["visibility_only"])
    @CLICommand.mutex(publish_action_args, publish_status_args)
    @CLICommand.mutex(["access_type", "product_name"], ["allow_guest", "discoverable", "public"])
    @CLICommand.any_of(publish_action_args + publish_status_args)
    def publish(self, args):  # noqa: D102
        validate_command_args(args)
        if args.status:
            status = self.publish_api.status(args.status)
            self.publish_printer.print_publishing_status(status)
            return
        workflow_id = self.model_api.publish(
            args.target,
            args.source,
            args.metadata_only,
            args.version_only,
            args.visibility_only,
            args.allow_guest,
            args.discoverable,
            args.public,
            args.access_type,
            args.product_name,
        )
        self.publish_printer.print_publishing_success(args.target, self.CMD_NAME, workflow_id)
