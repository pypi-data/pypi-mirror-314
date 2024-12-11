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

from nvcf.api.deployment_spec import get_available_gpus_from_cluster_groups

from ngcbase.api.utils import DotDict
from ngcbase.printer.nvPrettyPrint import NVPrettyPrint


class DeploymentPrinter(NVPrettyPrint):  # noqa: D101
    def print_info(self, dep):  # noqa: D102
        if self.format_type == "json":
            self.print_data(dep)
        else:
            output = DeploymentOutput(dep)
            outline_tbl = self.create_output(header=False, outline=True)
            tbl = self.add_sub_table(parent_table=outline_tbl, header=False, outline=False)
            tbl.add_separator_line()
            tbl.set_title("Function Deployment Information")
            tbl.add_label_line("ID", output.functionId)
            tbl.add_label_line("Version", output.versionId)
            tbl.add_label_line("Status", output.functionStatus)
            tbl.add_label_line("Request Queue", output.requestQueueUrl)
            for dep_spec in output.deploymentSpecifications:
                tbl = self.add_sub_table(parent_table=outline_tbl, header=False, outline=False)
                tbl.set_title("Deployment Specification")
                tbl.add_label_line("GPU", dep_spec.gpu)
                if "backend" in dep_spec:
                    tbl.add_label_line("Backend", dep_spec.backend)
                tbl.add_label_line("Instance Type", dep_spec.instanceType)
                tbl.add_label_line("Min Instances", dep_spec.minInstances)
                tbl.add_label_line("Max Instances", dep_spec.maxInstances)
                if "maxRequestConcurrency" in dep_spec:
                    tbl.add_label_line("Max Request Concurrency", dep_spec.maxRequestConcurrency)
            tbl.add_separator_line()
            tbl.print()

    def print_gpus(self, cluster_groups):  # noqa: D102
        if self.format_type == "json":
            output = cluster_groups
            self.print_data(output, True)
        else:
            gpus = get_available_gpus_from_cluster_groups(cluster_groups)
            outline_tbl = self.create_output(header=False, outline=True)
            outline_tbl.set_title("Available GPUs")
            for gpu in gpus:
                tbl = self.add_sub_table(parent_table=outline_tbl, header=False, outline=False)
                tbl.set_title(gpu.name)
                tbl.add_label_line("Backend", gpu.backend)
                tbl.add_label_line("Instances", ", ".join(gpu.instances))
            tbl.add_separator_line()
            tbl.print()

    def print_logs(self, logs):  # noqa: D102
        if self.format_type == "json":
            self.print_data(logs)
            return

        headers = [("Timestamp", "Source", "Message")]
        data = [(log.get("timestamp"), log.get("source"), log.get("message")) for log in logs]
        headers.extend(data)
        self.print_data(headers, True)

    def print_available_gpus_deprecation_warning(self):  # noqa: D102
        self.print_ok("Warning! 'ngc cf available-gpus' is deprecated. Please use the 'ngc cf gpu ls' instead.")


class ClusterGroupOutput:  # noqa: D101
    def __init__(self, cluster_group):
        self.cluster_group: dict = cluster_group

    @property
    def clusters(self):  # noqa: D102
        return [ClusterOutput(cluster) for cluster in self.cluster_group.get("clusters", [])]

    @property
    def gpus(self):  # noqa: D102
        return [GPUOutput(gpu) for gpu in self.cluster_group.get("gpus", [])]

    @property
    def id(self):  # noqa: D102
        return self.cluster_group.get("id", "")

    @property
    def name(self):  # noqa: D102
        return self.cluster_group.get("name", "")


class ClusterOutput:  # noqa: D101
    def __init__(self, cluster):
        self.cluster = cluster

    @property
    def id(self):  # noqa: D102
        return self.cluster.get("id", "")

    @property
    def k8sVersion(self):  # noqa: D102
        return self.cluster.get("k8sVersion", "")

    @property
    def name(self):  # noqa: D102
        return self.cluster.get("name", "")


class GPUOutput:  # noqa: D101
    def __init__(self, gpu):
        self.gpu = gpu

    @property
    def instances(self):  # noqa: D102
        return self.gpu.get("instanceTypes")

    @property
    def name(self):  # noqa: D102
        return self.gpu.get("name", "")


class DeploymentOutput:  # noqa: D101
    def __init__(self, dep):
        self.dep = dep

    @property
    def name(self):  # noqa: D102
        return self.dep.get("name", None)

    @property
    def functionId(self):  # noqa: D102
        return self.dep.get("functionId", None)

    @property
    def versionId(self):  # noqa: D102
        return self.dep.get("functionVersionId", None)

    @property
    def functionStatus(self):  # noqa: D102
        return self.dep.get("functionStatus", None)

    @property
    def requestQueueUrl(self):  # noqa: D102
        return self.dep.get("requestQueueUrl", None)

    @property
    def deploymentSpecifications(self):  # noqa: D102
        return [DotDict(dep_spec) for dep_spec in self.dep.get("deploymentSpecifications", [])]
