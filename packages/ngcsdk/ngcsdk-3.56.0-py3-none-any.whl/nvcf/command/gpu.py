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


from nvcf.command.cloud_function import CloudFunctionCommand
from nvcf.printer.gpu_printer import GPUPrinter

from ngcbase.command.clicommand import CLICommand


class GPUCommand(CloudFunctionCommand):  # noqa: D101

    CMD_NAME = "gpu"
    DESC = "Description of the gpu command"
    HELP = "Get information about available gpus"
    CMD_ALIAS = ["instance-type"]

    def __init__(self, parser):
        super().__init__(parser)
        self.parser = parser
        self.config = self.client.config
        self.printer = GPUPrinter(self.client.config)

    @CLICommand.command(help="List GPUs", description="List allocated gpus.", aliases=["ls"])
    def list(self, _):  # noqa: D102
        gpus = self.client.cloud_function.gpus.list()
        self.printer.print_list(gpus)

    @CLICommand.arguments("target", metavar="", help="", type=str, default=None)
    @CLICommand.command(help="Info for a given GPU", description="Info for a given gpu.", aliases=["get"])
    def info(self, args):  # noqa: D102
        gpu = self.client.cloud_function.gpus.info(args.target)
        self.printer.print_info(gpu)
