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

import warnings
from typing import Annotated

from bert_schemas import job as job_schema
from bert_schemas.job import RfInterpolationType, interpolate_1d_list
from pydantic import BaseModel, ConfigDict, Field, model_validator


class ConversionError(Exception): ...


class RfSequence(job_schema.RfEvaporation):
    """A class that represents a sequence of radio frequency powers/frequencies in time"""

    @classmethod
    def new(
        cls,
        times: list[float] = [0],
        powers: list[float] = [0],
        frequencies: list[float] = [0],
        interpolation: job_schema.InterpolationType = "LINEAR",
    ) -> RfSequence:
        """Method to create a new RfSequence object

        Args:
            times (list[float], optional): List of times, in ms
            powers (list[float], optional): List of powers, in MHz
            frequencies (list[float], optional): List of powers, mW
            interpolation (bert_schemas.job.InterpolationType, optional): Interpolation type of the RF sequence

        Returns:
            RfSequence: A new RfSequence object
        """
        return cls(
            times_ms=times,
            powers_mw=powers,
            frequencies_mhz=frequencies,
            interpolation=interpolation,
        )

    @classmethod
    def from_input(cls, rf_evaporation: job_schema.RfEvaporation) -> RfSequence:
        """Method to create a RfSequence object using the input values of a job

        Args:
            rf_evaporation (bert_schemas.job.RfEvaporation): The input values

        Returns:
            RfSequence: A new RfSequence object created using the input data
        """
        return cls(**rf_evaporation.model_dump())

    def get_frequencies(self, times: list[float]) -> list[float]:
        """Method to calculate the RF evaporation frequencies of a RfSequence object at the specified times

        Args:
            times (list[float]): The times, in ms, at which the RF frequencies are calculated

        Returns:
            list[float]: The calculated frequencies, in MHz, at the specified times
        """
        return interpolate_1d_list(
            self.times_ms,
            self.frequencies_mhz,
            times,
            self.interpolation,
        )

    def get_powers(self, times: list[float]) -> list[float]:
        """Method to calculate the RF evaporation powers at of a RfSequence object at the specified times

        Args:
            times (list[float]): The times, in ms, at which the RF powers are calculated

        Returns:
            list[float]: The RF powers, in mW, at the specified times
        """
        return interpolate_1d_list(self.times_ms, self.powers_mw, times, self.interpolation)


class RfEvap(RfSequence):
    """A class that represents the forced RF evaporation that cools atoms to quantum degeneracy."""

    @classmethod
    def new(
        cls,
        times: list[float] = [0],
        powers: list[float] = [0],
        frequencies: list[float] = [0],
        interpolation: job_schema.InterpolationType = "LINEAR",
    ) -> RfEvap:
        """Method to create a new RfEvap object

        Args:
            times (list[float], optional): List of times, in ms
            powers (list[float], optional): List of powers, in MHz
            frequencies (list[float], optional): List of powers, mW
            interpolation (bert_schemas.job.InterpolationType, optional): Interpolation type of the RF evaporation

        Returns:
            RfEvap: A new RfEvap object
        """
        return cls(
            times_ms=[t - max(times) for t in times],
            powers_mw=powers,
            frequencies_mhz=frequencies,
            interpolation=interpolation,
        )

    @classmethod
    def from_input(cls, rf_evaporation: job_schema.RfEvaporation) -> RfEvap:
        """Method to create a RfEvap object using the input values of a job

        Args:
            rf_evaporation (bert_schemas.job.RfEvaporation): The input values

        Returns:
            RfEvap: A new RfEvap object created using the input data
        """
        rf_evap_times = [t for t in rf_evaporation.times_ms if t <= 0.0]
        if rf_evap_times == []:
            raise ConversionError()

        rf_evap_freqs = [f for t, f in zip(rf_evaporation.times_ms, rf_evaporation.frequencies_mhz) if t <= 0.0]

        rf_evap_pows = [p for t, p in zip(rf_evaporation.times_ms, rf_evaporation.powers_mw) if t <= 0.0]
        return cls.new(
            times=rf_evap_times,
            frequencies=rf_evap_freqs,
            powers=rf_evap_pows,
            interpolation=rf_evaporation.interpolation,
        )


# A RfShield is a CONSTANT evaporation occurring during the entire experimental phase
# any non-negative time in the rf_evaporation object of a program indicates a
# rf shield is desired for the entire duration of the experiment stage
class RfShield(BaseModel):
    """A class that represents an RF shield (at fixed frequency and power)
    being applied during the 'experiment' phase/stage."""

    times_ms: Annotated[
        list[Annotated[int, Field(ge=-2000, le=200)]],
        Field(min_length=1, max_length=20),
    ] = list(range(-1600, 400, 400))
    frequencies_mhz: Annotated[
        list[Annotated[float, Field(ge=0.0, le=25.0)]],
        Field(min_length=1, max_length=20),
    ]
    powers_mw: Annotated[
        list[Annotated[float, Field(ge=0.0, le=1000.0)]],
        Field(min_length=1, max_length=20),
    ]
    interpolation: RfInterpolationType
    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    @model_validator(mode="after")
    def cross_validate(self) -> RfShield:
        if not len(self.times_ms) == len(self.frequencies_mhz) == len(self.powers_mw):
            raise ValueError("RfEvaporation data lists must have the same length.")

        if self.times_ms != sorted(self.times_ms):
            warnings.warn(
                "Evaporation times_ms list must be naturally ordered, re-ordering.",
                stacklevel=2,
            )
            self.times_ms, self.frequencies_mhz, self.powers_mw = zip(
                *sorted(
                    zip(
                        self.times_ms,
                        self.frequencies_mhz,
                        self.powers_mw,
                    )
                )
            )
        return self

    @classmethod
    def new(
        cls,
        lifetime: float,
        frequency: float,
        power: float,
        interpolation: job_schema.InterpolationType = "LINEAR",
    ) -> RfShield:
        """Method to create a new RfShield object

        Args:
            lifetime (float): Lifetime of the shield, in ms
            frequency (float | None): Frequency of the shield, in MHz
            power (float | None): Power of the shield, in mW
            interpolation (bert_schemas.job.InterpolationType, optional): Interpolation type of the shield

        Returns:
            RfShield: A new RfShield object
        """
        return cls(
            times_ms=[lifetime],
            powers_mw=[power],
            frequencies_mhz=[frequency],
            interpolation=interpolation,
        )

    @classmethod
    def from_input(cls, rf_evaporation: job_schema.RfEvaporation) -> RfShield:
        """Method to create a RfShield object using the input values of a job

        Args:
            rf_evaporation (bert_schemas.job.RfEvaporation): The input values

        Returns:
            RfShield: A new RfShield object created using the input data
        """
        if rf_evaporation.times_ms[-1] <= 0:
            raise ConversionError()
        else:
            return cls.new(
                lifetime=rf_evaporation.times_ms[-1],
                frequency=rf_evaporation.frequencies_mhz[-1],
                power=rf_evaporation.powers_mw[-1],
                interpolation=rf_evaporation.interpolation,
            )

    @property
    def lifetime(self) -> float:
        """Property to get the lifetime value of a RfShield object

        Returns:
            float: The amount of time, in ms, that the shield will exist
        """
        return self.times_ms[0]

    @property
    def frequency(self) -> float:
        """Property to get the frequency value of a RfShield object

        Returns:
            float: The shield's frequency, in MHz
        """
        return self.frequencies_mhz[0]

    def frequencies(self, times: list[float]) -> list[float]:
        """Method to generate a list of frequencies using the provided list of times

        Args:
            times (list[float]): The times, in ms, at which the frequencies are generated

        Returns:
            list(float): The calculated frequencies, in MHz, at the specified times
        """
        return [self.frequencies_mhz[0]] * len(times)

    @property
    def power(self) -> float:
        """Property to get the power value of a RfShield object

        Returns:
            float: The shield's power, in mW
        """
        return self.powers_mw[0]

    def powers(self, times: list[float]) -> list[float]:
        """Method to generate a list of powers using the provided list of times

        Args:
            times (list[float]): The times, in ms, at which the powers are generated

        Returns:
            list(float): The calculated powers, in mW, at the specified times
        """
        return [self.powers_mw[0]] * len(times)
