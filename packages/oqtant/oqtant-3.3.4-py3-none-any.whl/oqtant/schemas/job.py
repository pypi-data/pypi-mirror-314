# Copyright 2024 Infleqtion
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from typing import Any
from uuid import UUID

from bert_schemas import job as job_schema
from dateutil import parser as date_parser
from dateutil import tz

SIG_ABS = 0.297


def print_keys(subject: Any, indent: int = 0, drill_lists: bool = False) -> None:
    """Print the keys of a nested dictionary or list

    Args:
        subject (Any): The subject to print the keys of
        indent (int, optional): The number of spaces to indent. Defaults to 0
        drill_lists (bool, optional): Whether to drill into lists. Defaults to False
    """
    if isinstance(subject, dict):
        for key, value in subject.items():
            print(f"{' ' * indent}- {key}")
            if isinstance(value, dict):
                print_keys(value, indent=indent + 2, drill_lists=drill_lists)
            if isinstance(value, list) and drill_lists:
                for list_value in value:
                    if isinstance(list_value, dict):
                        print_keys(
                            list_value, indent=indent + 2, drill_lists=drill_lists
                        )


class OqtantJob(job_schema.JobBase):
    """A class that represents a job submitted to Oqtant"""

    external_id: UUID | None = None
    time_submit: str | datetime | None = None
    time_start: str | datetime | None = None
    time_complete: str | datetime | None = None

    @property
    def truncated_name(self) -> str:
        """Property to truncate a job's name

        Returns:
            str: The truncated job name
        """
        if len(self.name) > 40:
            return f"{self.name[:37]}..."
        return self.name

    @property
    def id(self) -> UUID:
        """Property to get the id of an OqtantJob object

        Returns:
            uuid.UUID: The id of the OqtantJob object
        """
        return self.external_id

    @property
    def formatted_time_submit(self) -> str:
        """Property to format the job submit datetime and ensure it is in caller's local timezone

        Returns:
            str: The formatted datetime string
        """
        return self.format_datetime(self.time_submit)

    @staticmethod
    def format_datetime(datetime_value: str | datetime) -> str:
        """Method to format any datetime and ensure it is in caller's local timezone

        Args:
            datetime_value (str | datetime.datetime): The datetime value to format

        Returns:
            str: The formatted datetime string
        """
        try:
            parsed_datetime = date_parser.parse(datetime_value)
            parsed_datetime = parsed_datetime.replace(tzinfo=tz.tzutc())
            parsed_datetime = parsed_datetime.astimezone(tz.tzlocal())
        except Exception:
            parsed_datetime = datetime_value
        return parsed_datetime.strftime("%d %b %Y, %H:%M:%S")

    @property
    def input_fields(self) -> None:
        """Property to print out all of the input fields for an OqtantJob"""
        print_keys(self.input.model_dump(), drill_lists=True)

    @property
    def input(self) -> job_schema.InputValues:
        """Property to get the input values for the current run of an OqtantJob

        Returns:
            bert_schemas.job.InputValues: The input values for the current run
        """
        return self.inputs[0].values

    @property
    def lifetime(self) -> int:
        """Property to get the lifetime value for the current run

        Returns:
            int: The lifetime value for the current run
        """
        return self.input.end_time_ms

    @property
    def run(self) -> int:
        """Property to get the current run value for the job's input

        Returns:
            int: The current run value for the job's input
        """
        return self.inputs[0].run

    def add_notes_to_input(self, notes: str) -> None:
        """Method to add notes to the current run

        Args:
            notes (str): The notes to add to the input
        """
        self.inputs[0].notes = notes
