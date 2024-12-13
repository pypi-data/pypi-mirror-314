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

from __future__ import annotations

import copy
import json
import sys
import time
import warnings
from datetime import datetime
from importlib.metadata import version
from typing import TYPE_CHECKING

import jwt
import numpy as np
import pandas as pd
import requests
import semver
from bert_schemas import job as job_schema
from pydantic import ValidationError
from requests.exceptions import RequestException
from tabulate import tabulate

from oqtant.fixtures.jobs import barrier_manipulator_job, ultracold_matter_job
from oqtant.schemas.job import OqtantJob
from oqtant.settings import Settings
from oqtant.simulator import QMPotential, Simulator
from oqtant.util import exceptions as api_exceptions
from oqtant.util.auth import get_user_token

if TYPE_CHECKING:
    from oqtant.schemas.quantum_matter import QuantumMatter

settings = Settings()


class OqtantClient:
    """Python class for interacting with Oqtant
    This class contains tools for:
        - Accessing all of the functionality of the Oqtant Web App (https://oqtant.infleqtion.com)
            - BARRIER (Barrier Manipulator) jobs
            - BEC (Ultracold Matter) jobs
        - Building parameterized (i.e. optimization) experiments using QuantumMatter
        - Submitting and retrieve results
    How Oqtant works:
        - Instantiate a QuantumMatterFactory and log in with your Oqtant account
        - Create QuantumMatter objects with the QuantumMatterFactory
            - 1D parameter sweeps are supported
        - Submit the QuantumMatter to Oqtant to be run on the hardware in a FIFO queue
            - Once submitted a job is created and associated with the QuantumMatter object
        - Retrieve the results of the job from Oqtant into the QuantumMatter object
            - These results are available in future python sessions
        - Extract, visualize, and analyze the results
    Need help? Found a bug? Contact oqtant@infleqtion.com for support. Thank you!
    """

    def __init__(self, *, settings, token, debug: bool = False):
        self.token: str = token
        self.max_ind_var: int = settings.max_ind_var
        self.run_list_limit: int = settings.run_list_limit
        self.debug: bool = debug
        self.version = version("oqtant")
        self.verbosity: int = 1

        self.base_url: str = f"{settings.base_url}/users/{self.external_user_id}"

        if not self.debug:
            sys.tracebacklimit = 0

    @property
    def external_user_id(self) -> str:
        try:
            token_data = jwt.decode(self.token, key=None, options={"verify_signature": False})
            external_user_id = token_data["sub"].replace("auth0|", "")
        except Exception as err:
            raise api_exceptions.OqtantTokenError(
                "Unable to decode JWT token. Please confirm that your token is correct."
            ) from err
        return external_user_id

    def __get_headers(self) -> dict:
        """Method to generate headers for use in calls to the REST API with requests

        Returns:
            dict: A dict of header information
        """
        return {
            "Authorization": f"Bearer {self.token}",
            "X-Client-Version": version("oqtant"),
        }

    def __print(self, message: str) -> None:
        """Method to control the verbosity of the print statements

        Args:
            message (str): The message to print
        """
        if self.verbosity >= 1:
            print(message)

    def convert_matter_to_job(self, matter: QuantumMatter) -> OqtantJob | None:
        """Method to convert a QuantumMatter object to an OqtantJob object

        Args:
            matter (oqtant.schemas.quantum_matter.QuantumMatter): The QuantumMatter object to be converted

        Returns:
            oqtant.schemas.job.OqtantJob: The resulting OqtantJob object
        """

        if matter.result:
            return matter.result

        if matter.output:
            inputs = {
                "values": matter.input.model_dump(),
                "notes": matter.note,
                "output": {"values": matter.output.model_dump()},
            }
        else:
            inputs = {"values": matter.input.model_dump(), "notes": matter.note}

        job_data = {
            "name": matter.name,
            "inputs": [job_schema.Input(**inputs)],
        }

        return OqtantJob(**job_data)

    def get_sim_result(self, sim: Simulator, image_type: job_schema.ImageType) -> Simulator:
        """Method to get the result of a simulation

        Args:
            sim (oqtant.simulator.Simulator): The Simulator object

        Returns:
            oqtant.simulator.Simulator: The Simulator object
        """
        print("ground state calculation in progress       ", end="\n")
        sim.set_ground_state()
        print("ground state calculation complete          ")
        print("trapped simulation in progress             ", end="\n")
        sim.run_evolution()
        print("trapped simulation complete                ")

        if image_type == job_schema.ImageType.TIME_OF_FLIGHT:
            print("time-of-flight simulation in progress              ")
            sim.run_TOF()

        return sim

    def submit_sim(self, matter: QuantumMatter) -> Simulator:
        """Method to submit a QuantumMatter object for simulation

        Args:
            matter (oqtant.schemas.quantum_matter.QuantumMatter): A QuantumMatter object

        Returns:
            oqtant.simulator.Simulator: The Simulator object
        """
        potential = QMPotential(matter)
        sim = Simulator(potential)  # wavefunction, potential).  wavefunction is no longer needed to be passed.
        return sim

    def submit(self, matter: QuantumMatter, track: bool = False, sim: bool = False) -> str:
        """Method to submit a QuantumMatter object for execution, returns the resulting job id

        Args:
            matter (oqtant.schemas.quantum_matter.QuantumMatter): The QuantumMatter object to submit for execution
            track (bool, optional): Flag to track the status of the resulting job
            sim (bool, optional): Flag to submit job as a simulation

        Returns:
            str: The Job ID of the submitted job
        """
        matter.result = None
        if sim:
            self.submit_sim(matter)

        job = self.convert_matter_to_job(matter)
        return self.run_jobs(job_list=[job], track_status=track)[0]

    def submit_list_as_batch(
        self,
        matter_list: list[QuantumMatter],
        track: bool = False,
        name: str | None = None,  # optional global name for resulting job
        sim: bool = False,
    ) -> QuantumMatter:
        """Method to submit a list of QuantumMatter objects as a batch job for execution

        Args:
            matter_list (list[oqtant.schemas.quantum_matter.QuantumMatter]): The list of QuantumMatter objects to
                submit as a single batch job
            track (bool, optional): Whether to track the status of the job
            name (str | None, optional): The name of the batch job. If None, the name of the first program will be used
            sim (bool): If the user intended to submit a sim job as batch or not. Will throw an exception as we
            do not allow simulator jobs as batch.
        Returns:
            str: The ID of the submitted job
        """

        if sim:
            raise api_exceptions.SimSubmitError

        mattersmost = matter_list[0]
        if name:
            mattersmost.name = name

        inputs = []
        master_job_type = self.convert_matter_to_job(mattersmost).job_type
        for matter in matter_list:
            job_type = self.convert_matter_to_job(matter).job_type
            if job_type is not master_job_type:
                raise api_exceptions.OqtantError("All input objects must map to the same job type.")
            inputs.append({"values": matter.input.model_dump(), "notes": matter.note})
        job_data = {
            "name": name,
            "inputs": inputs,
        }
        job = OqtantJob(**job_data)
        id = self.run_jobs(job_list=[job], track_status=track)[0]
        mattersmost.job_id = id
        return mattersmost

    def get_job(self, job_id: str, run: int = 1) -> OqtantJob:
        """Method to get an OqtantJob from the Oqtant REST API. This will always be a targeted query
        for a specific run. If the run is omitted then this will always return the first run of the
        job. Will return results for any job regardless of it's status

        Args:
            job_id (str): This is the external_id of the job to fetch
            run (int, optional): The run to target, this defaults to the first run if omitted

        Returns:
            oqtant.schemas.job.OqtantJob: An OqtantJob instance with the values of the job queried
        """
        request_url = f"{self.base_url}/jobs/{job_id}"
        params = {"run": run}
        response = requests.get(
            url=request_url,
            params=params,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.OqtantAuthorizationError
        try:
            response.raise_for_status()
        except RequestException as err:
            raise api_exceptions.OqtantRequestError(f"Failed to get job '{job_id}' from Oqtant") from err
        job_data = response.json()
        try:
            job = OqtantJob(**job_data)
        except ValidationError as err:
            raise api_exceptions.OqtantJobValidationError(f"Failed to validate job '{job_id}'") from err
        except (KeyError, Exception) as err:
            raise api_exceptions.OqtantJobParameterError(f"Failed to parse job '{job_id}'") from err
        return job

    # necessary?
    def generate_oqtant_job(self, *, job: dict) -> OqtantJob:
        """Method to generate an instance of OqtantJob from the provided dictionary that contains the job
        details and input. Will validate the values and raise an informative error if any
        violations are found

        Args:
            job (dict): Dictionary containing job details and input

        Returns:
            oqtant.schemas.job.OqtantJob: an OqtantJob instance containing the details and input from the
                provided dictionary
        """
        try:
            oqtant_job = OqtantJob(**job)
        except (KeyError, ValidationError) as err:
            raise api_exceptions.OqtantJobValidationError("Failed to generate OqtantJob") from err
        return oqtant_job

    def create_job(
        self,
        name: str,
        job_type: job_schema.JobType,
        runs: int = 1,
        job: dict | None = None,
    ) -> OqtantJob:
        """Method to create an instance of OqtantJob. When not providing a dictionary of job data this method will
        return an OqtantJob instance containing predefined input data based on the value of job_type and runs.
        If a dictionary is provided an OqtantJob instance will be created using the data contained within it.

        Args:
            name (str): The name of the job to be created
            job_type (bert_schemas.job.JobType): The type of job to be created
            runs (int): The number of runs to include in the job
            job (dict | None, optional): Dictionary of job inputs to use instead of the defaults

        Returns:
            oqtant.schemas.job.OqtantJob: an OqtantJob instance of the provided dictionary or predefined input data
        """
        if job:
            job["name"] = name
            job["job_type"] = job_type
            job = self.generate_oqtant_job(job=job)
            return job
        if job_type == job_schema.JobType.BARRIER:
            job = barrier_manipulator_job
        elif job_type == job_schema.JobType.BEC:
            job = ultracold_matter_job
        else:
            raise api_exceptions.OqtantJobUnsupportedTypeError(
                f"Job type '{job_type}' is either invalid or unsupported"
            )
        job = self.generate_oqtant_job(job=job)
        job.inputs = [copy.deepcopy(job.inputs[0].model_dump())] * runs
        job.name = name
        return job

    def submit_job(self, *, job: OqtantJob, write: bool = False) -> dict:
        """Method to submit a single OqtantJob to the Oqtant REST API. Upon successful submission this method will
        return a dictionary containing the external_id of the job and it's position in the queue. Will write the job
        data to file when the write argument is True.



        Args:
            job (oqtant.schemas.job.OqtantJob): The OqtantJob instance to submit for processing
            write (bool, optional): Flag to write job data to file

        Returns:
            dict: Dictionary containing the external_id of the job and it's queue position
        """
        if not isinstance(job, OqtantJob):
            try:
                job = OqtantJob(**job)
            except (TypeError, AttributeError, ValidationError) as err:
                raise api_exceptions.OqtantJobValidationError("OqtantJob is invalid") from err
        data = {
            "name": job.name,
            "job_type": job.job_type,
            "input_count": len(job.inputs),
            "inputs": [input.model_dump() for input in job.inputs],
        }
        response = requests.post(
            url=f"{self.base_url}/jobs",
            json=data,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.OqtantAuthorizationError
        try:
            response.raise_for_status()
        except RequestException as err:
            raise api_exceptions.OqtantRequestError("Failed to submit job to Oqtant") from err
        response_data = response.json()
        if write:
            job.status = job_schema.JobStatus.PENDING
            job.external_id = response_data["job_id"]
            self.write_job_to_file(job)
        return response_data

    def cancel_job(self, job_id: str) -> None:
        """Method to cancel a single job with the Oqtant REST API

        Args:
           job_id (str): The job id of the job to cancel
        """
        response = requests.put(
            url=f"{self.base_url}/jobs/{job_id}/cancel",
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.OqtantAuthorizationError
        try:
            response.raise_for_status()
        except RequestException as err:
            raise api_exceptions.OqtantRequestError("Failed to cancel job") from err

    def delete_job(self, job_id: str) -> None:
        """Method to delete a single job with the Oqtant REST API

        Args:
           job_id (str): The job id of the job to delete
        """
        response = requests.delete(
            url=f"{self.base_url}/jobs/{job_id}",
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.OqtantAuthorizationError
        try:
            response.raise_for_status()
        except RequestException as err:
            raise api_exceptions.OqtantRequestError("Failed to delete job") from err

    def run_jobs(self, job_list: list[OqtantJob], track_status: bool = False, write: bool = False) -> list[str]:
        """Method to submit a list of OqtantJobs to the Oqtant REST API. This method provides some optional
        functionality to alter how it behaves. Providing it with an argument of track_status=True will make it wait
        and poll the Oqtant REST API until all jobs in the list have completed. Providing it with and argument of
        write=True  will make it write the results of the jobs to file when they complete (only applies when the
        track_status argument is True)

        Args:
            job_list (list[oqtant.schemas.job.OqtantJob]): The list of OqtantJob instances to submit for processing
            track_status (bool, optional): Flag to return immediately or wait and poll until all jobs have completed
            write (bool, optional): Flag to write job results to file

        Returns:
            list[str]: List of the external_id(s) returned for each submitted job in job_list
        """
        if len(job_list) > self.run_list_limit:
            raise api_exceptions.OqtantJobListLimitError(
                f"Maximum number of jobs submitted per run is {self.run_list_limit}."
            )
        pending_jobs = []
        submitted_jobs = []
        self.__print(f"Submitting {len(job_list)} job(s):")
        for job in job_list:
            response = self.submit_job(job=job, write=write)
            external_id = response["job_id"]
            job.external_id = external_id
            pending_jobs.append(job)
            submitted_jobs.append(job)
            self.__print(f"\n- Job: {job.name}")
            self.__print(f"  Job ID: {job.external_id}")
        if track_status:
            self.track_jobs(pending_jobs=pending_jobs, write=write)
        return [str(job.external_id) for job in submitted_jobs]

    def search_jobs(
        self,
        *,
        job_type: job_schema.JobType | None = None,
        name: job_schema.JobName | None = None,
        submit_start: str | None = None,
        submit_end: str | None = None,
        notes: str | None = None,
        limit: int = 100,
        show_results: bool = False,
    ) -> list[dict]:
        """Method to submit a query to the Oqtant REST API to search for jobs that match the provided criteria.
        The search results will be limited to jobs that meet your Oqtant account access

        Args:
           job_type (bert_schemas.job.JobType | None, optional): The type of the jobs to search for
           name (bert_schemas.job.JobName | None, optional): The name of the job to search for
           submit_start (str | None, optional): The earliest submit date of the jobs to search for
           submit_start (str | None, optional): The latest submit date of the jobs to search for
           notes (str | None, optional): The notes of the jobs to search for
           limit (int, optional): The limit for the number of jobs returned (max: 100)
           show_results (bool, optional): Flag to print out the results of the search

        Returns:
           list[dict]: A list of jobs matching the provided search criteria
        """
        params = {"limit": limit}
        for param in ["job_type", "name", "submit_start", "submit_end", "notes"]:
            if locals()[param] is not None:
                params[param] = locals()[param]

        response = requests.get(
            url=f"{self.base_url}/jobs",
            params=params,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.OqtantAuthorizationError
        try:
            response.raise_for_status()
        except RequestException as err:
            raise api_exceptions.OqtantRequestError("Failed to search jobs in Oqtant") from err
        job_data = response.json().get("items", [])
        if show_results and job_data:
            self.__print(f"Search returned {len(job_data)} job(s):\n")
            rows = [
                [
                    (job.get("name") if len(job.get("name", [])) < 40 else f"{job.get('name')[:37]}..."),
                    job.get("job_type"),
                    job.get("status"),
                    job.get("external_id"),
                ]
                for job in job_data
            ]
            table = [
                ["Name", "Job Type", "Status", "ID"],
                *rows,
            ]
            self.__print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
        return job_data

    def track_jobs(self, pending_jobs: list[OqtantJob], write: bool = False) -> None:
        """Method that polls the Oqtant REST API with a list of OqtantJobs and waits until all of them have
        completed. Will output each job's status while it is polling and will output a message when
        all jobs have completed. When the write argument is True it will also write the jobs' data
        to file when they complete

        Args:
           pending_jobs (list[oqtant.schemas.job.OqtantJob]): List of OqtantJobs to track
           write (bool, optional): Flag to write job results to file
        """
        self.__print(f"\nTracking {len(pending_jobs)} job(s):")
        pending_jobs = {str(job.external_id): job for job in pending_jobs}
        running_job = None
        while pending_jobs:
            if not running_job:
                for external_id, pending_job in pending_jobs.items():
                    job = self.get_job(job_id=external_id)
                    if job.status != pending_job.status:
                        pending_jobs[external_id].status = job.status
                        running_job = pending_jobs[external_id]
                        self.__print(f"\n- Job: {job.name}")
                        self.__print(f"  - {job.status}")
                        break
            else:
                job = self.get_job(job_id=running_job.external_id)
                if job.status != running_job.status:
                    if job.status in [
                        job_schema.JobStatus.INCOMPLETE,
                        job_schema.JobStatus.FAILED,
                        job_schema.JobStatus.COMPLETE,
                    ]:
                        pending_jobs.pop(str(running_job.external_id), None)
                        running_job = None
                    else:
                        running_job.status = job.status
                    self.__print(f"  - {job.status}")
                    if not running_job and write:
                        self.write_job_to_file(job)
            time.sleep(2)
        self.__print("\nAll job(s) complete")

    def write_job_to_file(
        self,
        job: OqtantJob,
        file_name: str | None = None,
        file_path: str | None = None,
    ) -> None:
        """Method to write an OqtantJob instance to a file

        Args:
            job (oqtant.schemas.job.OqtantJob): The OqtantJob instance to write to file
            file_name (str | None, optional): custom name of the file
            file_path (str | None, optional): full path to the file to write, including
                the name of the file
        """
        if file_path:
            target = file_path
        else:
            if job.input_count > 1:
                target = f"{file_name if file_name else str(job.external_id)}"
                target = f"{target}_run_{job.run}_of_{job.input_count}.txt"
            else:
                target = f"{file_name if file_name else str(job.external_id)}.txt"
        try:
            with open(target, "w+") as f:
                f.write(str(job.model_dump_json()))
                print(f'Wrote file: "{target}"')
        except Exception as err:
            raise api_exceptions.JobWriteError(f"Failed to write job to '{target}'") from err

    def load_job_from_file(self, file_path: str, refresh: bool = True) -> OqtantJob:
        """Method to load an OqtantJob instance from a file. Will refresh the job data from the
        Oqtant REST API by default

        Args:
            file_path (str): The full path to the file to read
            refresh (bool, optional): Flag to refresh the job data from Oqtant

        Returns:
            OqtantJob: An OqtantJob instance of the loaded job
        """
        try:
            with open(file_path) as json_file:
                data = json.load(json_file)
                job = OqtantJob(**data)
                run = job.inputs[0].run
                if refresh:
                    job = self.get_job(job.external_id, run=run)
                    self.write_job_to_file(job, file_path=file_path)
                return job
        except FileNotFoundError as err:
            raise api_exceptions.JobReadError(f"Failed to load job from {file_path}") from err
        except (ValidationError, KeyError) as err:
            raise api_exceptions.JobReadError(f"Failed to parse job from {file_path}") from err
        except RequestException as err:
            raise api_exceptions.JobReadError(f"Failed to refresh job from {file_path}") from err

    def get_raw_images(self, job_id: str) -> list:
        """Method to get raw images from the Oqtant REST API

        Args:
            job_id (str): The external_id of the job to fetch

        Returns:
            dict: Dictionary of raw images
        """
        url = f"{self.base_url}/jobs/{job_id}/raw_images"
        response = requests.get(
            url=url,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.OqtantAuthorizationError
        try:
            response.raise_for_status()
        except RequestException as err:
            raise api_exceptions.OqtantRequestError("Failed to get raw images from Oqtant") from err
        raw_images = response.json()
        return raw_images

    def get_job_limits(self, show_results: bool = False) -> dict:
        """Method to get job limits from the Oqtant REST API

        Args:
            show_results (bool, optional): Flag to print out the results

        Returns:
            dict: Dictionary of job limits
        """
        url = f"{self.base_url}/job_limits"
        response = requests.get(
            url=url,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.OqtantAuthorizationError()
        try:
            response.raise_for_status()
        except RequestException as err:
            raise api_exceptions.OqtantRequestError("Failed to get job limits from Oqtant") from err
        job_limits = response.json()
        if show_results:
            limit_table = [
                [
                    "Daily Limit",
                    "Daily Remaining",
                    "Standard Credits",
                    "Priority Credits",
                ],
                [
                    job_limits["daily_limit"],
                    job_limits["daily_remaining"],
                    job_limits["standard_credits"],
                    job_limits["priority_credits"],
                ],
            ]
            self.__print("Job Limits:\n" + tabulate(limit_table, headers="firstrow", tablefmt="fancy_grid"))
        return job_limits

    def show_job_limits(self) -> None:
        """Method to print out job limit information
        Wrapper for OqtantClient.get_job_results
        """
        self.get_job_limits(show_results=True)

    def get_queue_status(
        self,
        job_type: job_schema.JobType | None = None,
        name: job_schema.JobName | None = None,
        submit_start: str | None = None,
        submit_end: str | None = None,
        note: str | None = None,
        limit: int = 50,
        include_complete: bool = False,
        show_results: bool = False,
    ) -> list:
        """Method to get the queue status of jobs submitted by the authenticated user

        Args:
            job_type (bert_schemas.job.JobType | None, optional): The type of jobs to filter results on
            name (bert_schemas.job.JobName | None, optional): The name of the job(s) to filter results on
            submit_start (str, optional): The earliest job submission date to filter results on
            submit_end (str, optional): The latest job submission date to filter results on
            note (str | None, optional): The notes value to filter results on
            limit (int, optional): The limit on the number of results to be returned
            include_complete (bool, optional): Flag to include completed jobs in results
            show_results (bool, optional): Flag to print out the results

        Returns:
            list[dict]: List of jobs that matched the provided query parameters
        """
        now = datetime.now().isoformat()
        start = submit_start if submit_start else now
        end = submit_end if submit_end else now
        search_results = list(
            filter(
                lambda job: (True if include_complete else job.get("status") != job_schema.JobStatus.COMPLETE),
                self.search_jobs(
                    job_type=job_type,
                    name=name,
                    submit_start=start,
                    submit_end=end,
                    notes=note,
                    limit=limit,
                ),
            )
        )
        if show_results:
            self.__print(f"{len(search_results)} job(s) queued:\n")
            rows = [
                [
                    (job.get("name") if len(job.get("name", [])) < 40 else f"{job.get('name')[:37]}..."),
                    job.get("status"),
                    OqtantJob.format_datetime(job.get("time_submit")),
                    job.get("external_id"),
                ]
                for job in search_results
            ]
            table = [
                ["Name", "Status", "Submit", "ID"],
                *rows,
            ]
            self.__print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
        return search_results

    def show_queue_status(self, *args, **kwargs) -> None:
        """Method to show queue status information
        Wrapper for OqtantClient.get_queue_status
        """
        self.get_queue_status(*args, **kwargs, show_results=True)

    def check_version(self) -> bool:
        """Method to compare the currently installed version of Oqtant with the latest version in PyPi
        and will raise a warning if it is older

        Returns:
            bool: True if current version is latest, False if it is older
        """
        resp = requests.get("https://pypi.org/pypi/oqtant/json", timeout=5)
        current = True
        if resp.status_code == 200:
            current_version = resp.json()["info"]["version"]
            if semver.compare(self.version, current_version) < 0:
                current = False
                warnings.warn(
                    f"Please upgrade to Oqtant version {current_version}. "
                    f"You are currently using version {self.version}"
                )
        return current


def get_oqtant_client(token: str) -> OqtantClient:
    """Method to create a new OqtantClient instance.

    Args:
        token (str): The auth0 token required for interacting with the Oqtant REST API

    Returns:
        OqtantClient: Authenticated instance of OqtantClient
    """
    client = OqtantClient(settings=settings, token=token)
    client.check_version()
    client.show_job_limits()
    return client


def get_client(port: int = 8080) -> OqtantClient:
    """Method to get both an authentication token and an instance of OqtantClient

    Args:
        port (int, optional): Specific port to run the authentication server on

    Returns:
        OqtantClient: An authenticated instance of OqtantClient
    """
    token = get_user_token(auth_server_port=port)
    client = OqtantClient(settings=settings, token=token)
    return client
