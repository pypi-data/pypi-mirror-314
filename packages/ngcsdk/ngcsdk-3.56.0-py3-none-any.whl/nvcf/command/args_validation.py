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
import argparse
import json


def check_invoke_payload_file():
    """Returns the Job from a given."""  # noqa: D401

    class CheckJSONInvocationPayload(argparse.Action):
        # pylint: disable=arguments-differ
        # method adds args to base method

        def __call__(self, parser, namespace, value, *args, **kwargs):
            with open(value) as json_file:
                try:
                    json_data = json.load(json_file)
                    if "stream" not in json_data:
                        raise AttributeError("Payload must include field 'stream'")
                except (ValueError, TypeError) as e:
                    raise ValueError("ERROR: Json file is not valid: {0}".format(str(e))) from None
                except IOError as e:
                    raise argparse.ArgumentError(self, e) from None
                except AttributeError as e:
                    raise argparse.ArgumentError(self, e) from None
            setattr(namespace, self.dest, json_data)

    return CheckJSONInvocationPayload
