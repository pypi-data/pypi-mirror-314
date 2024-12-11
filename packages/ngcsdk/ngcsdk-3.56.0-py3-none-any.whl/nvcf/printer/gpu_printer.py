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

#
# NVIDIA CORPORATION and its licensors retain all intellectual property
# and proprietary rights in and to this software, related documentation
# and any modifications thereto.  Any use, reproduction, disclosure or
# distribution of this software and related documentation without an express
# license agreement from NVIDIA CORPORATION is strictly prohibited.

from ngcbase.printer.nvPrettyPrint import NVPrettyPrint


class GPUPrinter(NVPrettyPrint):
    """GPU Printer."""

    def print_list(self, gpu_list):  # noqa: D102
        if self.format_type == "json":
            output = gpu_list
            self.print_data(output, True)
        else:
            outline_tbl = self.create_output(header=False, outline=True)
            outline_tbl.set_title("Allocated GPUs")
            for gpu_name, gpus in gpu_list.items():
                gpu_tbl = self.add_sub_table(parent_table=outline_tbl, header=False, outline=False)
                gpu_tbl.set_title(gpu_name)
                for instance_type in gpus:
                    instance_tbl = self.add_sub_table(parent_table=gpu_tbl, header=False, outline=False)
                    instance_tbl.set_title(f"  Instance Type {instance_type.value}")
                    instance_tbl.add_label_line("\tDescription", instance_type.description)
                    instance_tbl.add_label_line("\tCurrent Instances", instance_type.currentInstances)
                    instance_tbl.add_label_line("\tSystem Memory", instance_type.systemMemory)
                    instance_tbl.add_label_line("\tGPU Memory", instance_type.gpuMemory)
                    instance_tbl.add_label_line("\tCluster Group Name", instance_type.clusterGroupName)
                    instance_tbl.add_label_line("\tRegions", ", ".join(instance_type.regions))
                    instance_tbl.add_label_line("\tAttributes", ", ".join(instance_type.attributes))
                gpu_tbl.add_separator_line()
            outline_tbl.print()

    def print_info(self, gpu):  # noqa: D102
        if self.format_type == "json":
            self.print_data(gpu)
        else:
            outline_tbl = self.create_output(header=False, outline=True)
            gpu_tbl = self.add_sub_table(parent_table=outline_tbl, header=False, outline=False)
            for gpu_name, instance_types in gpu.items():
                gpu_tbl.set_title(gpu_name)
                for instance_type in instance_types:
                    instance_tbl = self.add_sub_table(parent_table=gpu_tbl, header=False, outline=False)
                    instance_tbl.set_title(f"  Instance Type {instance_type.value}")
                    instance_tbl.add_label_line("\tDescription", instance_type.description)
                    instance_tbl.add_label_line("\tCurrent Instances", instance_type.currentInstances)
                    instance_tbl.add_label_line("\tSystem Memory", instance_type.systemMemory)
                    instance_tbl.add_label_line("\tGPU Memory", instance_type.gpuMemory)
                    instance_tbl.add_label_line("\tCluster Group Name", instance_type.clusterGroupName)
                    instance_tbl.add_label_line("\tRegions", ", ".join(instance_type.regions))
                    instance_tbl.add_label_line("\tAttributes", ", ".join(instance_type.attributes))

            gpu_tbl.add_separator_line()
            outline_tbl.print()
