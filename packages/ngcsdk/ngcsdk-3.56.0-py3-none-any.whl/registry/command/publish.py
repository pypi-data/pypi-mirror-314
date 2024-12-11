#
# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
# Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.
import argparse

from registry.data.registry.AccessTypeEnum import AccessTypeEnum

METADATA_HELP = "Only perform a shallow copy of the metadata instead of a deep copy of the objects referenced"
VERSION_ONLY_HELP = "Only copy the specified version of the object without copying any metadata"
ALLOW_GUEST_HELP = "Allow anonymous users to download the published object"
DISCOVERABLE_HELP = "Allow the published object to be discoverable in searches"
PUBLIC_HELP = "Allow access to the published object by everyone instead of just those with specific roles"
PRODUCT_HELP = "Publish the object under a Product. Choose from: "
ACCESS_TYPE_HELP = f"Publish the object with a specific access type. Choose from: {', '.join(AccessTypeEnum)}"
PUBTYPE_MAPPING = {
    "models": "MODEL",
    "helm-charts": "HELM_CHART",
    "resources": "RESOURCE",
    "collections": "COLLECTION",
}
GET_STATUS_HELP = "Get the status of publishing based on provide workflow id."
VISIBILITY_HELP = "Only change the visibility qualities of the target. Metadata and version files are not affected."
publish_action_args = [
    "source",
    "metadata_only",
    "version_only",
    "visibility_only",
    "allow_guest",
    "discoverable",
    "public",
    "sign",
    "product_name",
    "access_type",
]
publish_status_args = ["status"]


def validate_command_args(args):
    """Validate the command line arguments of the publishing sub command.

    There are two types of publishing commands: \
        1.publish <target> for publish actions against a target. \
        2.publish --status <workflow ID> for getting publishing status.
    """
    _status = getattr(args, "status", None)
    _publish = getattr(args, "target", None)
    if (_status is None) and (_publish is None):
        raise argparse.ArgumentError(
            None,
            "Invalid arguments. Either `<target>` must be specified for publishing actions, "
            "or `--status <workflow ID>` must be used for publishing status.",
        )
