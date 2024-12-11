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
#

import isodate

from ngcbase.printer.nvPrettyPrint import NVPrettyPrint
from ngcbase.util.datetime_utils import human_time


class TaskPrinter(NVPrettyPrint):
    """NVCF Task Printer."""

    def print_list(self, task_list):  # noqa: D102
        if self.format_type == "json":
            self.print_data(task_list)
        else:
            columns = [
                ("name", "Name"),
                ("status", "Status"),
                ("id", "Id"),
                ("created_at", "Created At"),
                ("last_updated_at", "Last Updated"),
            ]
            cols, disp = zip(*columns)
            output = [list(disp)]
            for task in task_list:
                out = TaskOutput(task)
                output.append([getattr(out, col, "") for col in cols])
            self.print_data(output, True)

    def print_info(self, task):  # noqa: D102
        if self.format_type == "json":
            self.print_data(task)
        else:
            output = TaskOutput(task)
            outline_tbl = self.create_output(header=False, outline=True)
            tbl = self.add_sub_table(parent_table=outline_tbl, header=False, outline=False)
            tbl.add_separator_line()
            tbl.set_title("Task Information")
            tbl.add_label_line("Name", output.name)
            tbl.add_label_line("ID", output.id)
            tbl.add_label_line("Status", output.status)
            tbl.add_label_line("Description", output.description)
            if output.tags:
                label_tbl = self.add_sub_table(outline=False, detail_style=False, level=0)
                label_tbl.set_title("Tags:", level=1)
                for tag in output.tags:
                    label_tbl.add_label_line("", tag, level=1)
            tbl.add_label_line("Created", output.created_at)
            tbl.add_label_line("Last Updated", output.last_updated_at)

            configuration_tbl = self.add_sub_table(parent_table=tbl, header=False, outline=False)
            configuration_tbl.set_title("Configuration Details")
            configuration_tbl.add_label_line("Container", output.container_image)
            if output.models:
                model_tbl = self.add_sub_table(outline=False, detail_style=False, level=0)
                model_tbl.set_title("Models:", level=1)
                for model in output.models:
                    model_tbl.add_label_line("", model, level=1)
            if output.resources:
                resource_tbl = self.add_sub_table(outline=False, detail_style=False, level=0)
                resource_tbl.set_title("Resources:", level=1)
                for resource in output.resources:
                    resource_tbl.add_label_line("", resource, level=1)
            if output.gpu_specification:
                configuration_tbl.add_label_line("GPU Type", output.gpu_specification.gpu)
                configuration_tbl.add_label_line("Instance Type", output.gpu_specification.instanceType)
            configuration_tbl.add_label_line("Max Runtime Duration", output.max_runtime_duration)
            configuration_tbl.add_label_line("Max Queued Duration", output.max_queued_duration)
            configuration_tbl.add_label_line("Termination Grace Period", output.termination_grace_period_duration)
            configuration_tbl.add_label_line("Result Handling", output.result_handling_strategy)
            configuration_tbl.add_label_line("Result Path", output.results_location)

            tbl.add_separator_line()
            tbl.print()

    def print_task_events(self, task_events, columns=None):
        """Print task events into a table or json."""
        if self.format_type == "json":
            output = task_events
        else:
            if not columns:
                columns = [
                    ("id", "Event Id"),
                    ("created_at", "Created At"),
                    ("message", "Message"),
                ]

            output = self.generate_task_events_list(list(task_events), columns)

        self.print_data(output, True)

    def generate_task_events_list(self, gen, columns):  # pylint: disable=no-self-use
        """Helps aggregate event lists that requires multiple queries."""  # noqa: D401
        cols, disp = zip(*columns)
        yield list(disp)

        for task_event in list(gen):
            out = TaskEventOutput(task_event)
            yield [getattr(out, col, None) for col in cols]


class TaskOutput:  # noqa: D101
    def __init__(self, task):
        self.task = task

    @property
    def id(self):  # noqa: D102
        return self.task.get("id", "")

    @property
    def nca_id(self):  # noqa: D102
        return self.task.get("ncaId", "")

    @property
    def name(self):  # noqa: D102
        return self.task.get("name", "")

    @property
    def status(self):  # noqa: D102
        return self.task.get("status", "")

    @property
    def gpu_specification(self):  # noqa: D102
        return self.task.get("gpuSpecification", None)

    @property
    def container_image(self):  # noqa: D102
        return self.task.get("containerImage", "")

    @property
    def models(self):  # noqa: D102
        return self.task.get("models", None)

    @property
    def resources(self):  # noqa: D102
        return self.task.get("resources", None)

    @property
    def tags(self):  # noqa: D102
        return self.task.get("tags", None)

    @property
    def description(self):  # noqa: D102
        return self.task.get("description", "")

    @property
    def result_handling_strategy(self):  # noqa: D102
        return self.task.get("resultHandlingStrategy", "")

    @property
    def results_location(self):  # noqa: D102
        return self.task.get("resultsLocation", "")

    @property
    def max_runtime_duration(self):  # noqa: D102
        if hasattr(self.task, "maxRuntimeDuration"):
            return human_time(isodate.parse_duration(self.task.get("maxRuntimeDuration")).total_seconds())
        return "Run forever"

    @property
    def max_queued_duration(self):  # noqa: D102
        if hasattr(self.task, "maxQueuedDuration"):
            return human_time(isodate.parse_duration(self.task.get("maxRuntimeDuration")).total_seconds())
        return ""

    @property
    def termination_grace_period_duration(self):  # noqa: D102
        if hasattr(self.task, "terminationGracePeriodDuration"):
            return human_time(isodate.parse_duration(self.task.get("terminationGracePeriodDuration")).total_seconds())
        return ""

    @property
    def secrets(self):  # noqa: D102
        return self.task.get("secrets", None)

    @property
    def last_updated_at(self):  # noqa: D102
        return self.task.get("lastUpdatedAt", "")

    @property
    def created_at(self):  # noqa: D102
        return self.task.get("createdAt", "")


class TaskEventOutput:  # noqa: D101
    def __init__(self, task_event):
        self.task_event = task_event

    @property
    def id(self):  # noqa: D102
        return self.task_event.get("eventId", "")

    @property
    def message(self):  # noqa: D102
        return self.task_event.get("message", "")

    @property
    def created_at(self):  # noqa: D102
        return self.task_event.get("createdAt", "")
