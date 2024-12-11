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

from argparse import ArgumentTypeError
import json
import re


class FunctionTarget:
    """This class represents a NVCF function.

    target pattern: <function-id>:function-version>
    """  # noqa: D404

    def __init__(self, target_string, id_required=True, version_required=True, version_allowed=True):
        self._target = target_string
        self._id = None
        self._version = None
        self._parse_target(id_required=id_required, version_required=version_required, version_allowed=version_allowed)

    def _parse_target(self, id_required=True, version_required=True, version_allowed=True):
        _error = "Invalid target: '{}', ".format(self._target)
        if version_required:
            _error = _error + "Pattern should be in format <function-id>:<version>"

        if id_required and not version_required:
            _error = _error + "Pattern should be in format <function-id>"

        if self._target:
            _pattern = self._target.split(":")

            if len(_pattern) > 2:
                raise ArgumentTypeError(_error)

            self._id = _pattern[0]
            if not self._id and id_required:
                raise ArgumentTypeError(_error)

            try:
                self._version = _pattern[1]
            except IndexError:
                self._system = ""

            if version_required and not self._version:
                raise ArgumentTypeError(_error)

            if not version_allowed and self._version:
                raise ArgumentTypeError(_error)

        # TODO: support glob
        # _glob_id = contains_glob(self._id)
        # _glob_vers = contains_glob(self._version)
        # if _glob_id and _glob_vers:
        #     raise ArgumentTypeError(
        #         "Invalid target: '{}', pattern matching is not allowed on both location "
        #         "and system at the same time.".format(self._target)
        #     )

    def __str__(self):  # noqa: D105
        return self._target

    @property
    def id(self) -> str:  # noqa: D102
        return self._id

    @property
    def version(self) -> str:  # noqa: D102
        return self._version


def nested_object(value, keys, optional_keys=None):  # noqa: D103
    data = json.loads(value)
    parsed_data = {}
    for key in keys:
        if key not in data:
            raise ArgumentTypeError(f'"{key}" must be in object.')
        parsed_data[key] = data[key]
    for key in optional_keys or []:
        if key in data:
            parsed_data[key] = data[key]
    return parsed_data


def check_function_name(value):  # noqa: D103
    if not isinstance(value, str):
        raise ArgumentTypeError("Function name must be string.")
    if len(value) < 10 or len(value) > 36:
        raise ArgumentTypeError("Function name must be between 10 and 36 characters long.")
    if not re.match(r"^[a-z0-9A-Z][a-z0-9A-Z\-_]*$", value):
        raise ArgumentTypeError("Function name can only contain letters, numbers, hyphens and underscores.")
    return value
