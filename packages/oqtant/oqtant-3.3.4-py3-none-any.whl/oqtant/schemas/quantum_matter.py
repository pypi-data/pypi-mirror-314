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

import os
import warnings
from copy import deepcopy
from dataclasses import dataclass
from typing import TYPE_CHECKING

import matplotlib.pyplot as plt
import numpy as np
from bert_schemas import job as job_schema
from bert_schemas import projected, timing
from bert_schemas.job import NonPlotOutput, PlotOutput
from bert_schemas.projected import Settings as ProjectedSettings
from ipyauth import Auth
from pydantic import BaseModel, confloat
from scipy.interpolate import interp1d

from oqtant import oqtant_client as oq
from oqtant.schemas.job import OqtantJob
from oqtant.schemas.optical import Barrier, Landscape, Laser, Pulse, Snapshot
from oqtant.schemas.output import OqtantNonPlotOutput, OqtantPlotOutput
from oqtant.schemas.rf import ConversionError, RfEvap, RfSequence, RfShield
from oqtant.simulator import Simulator
from oqtant.util import exceptions
from oqtant.util.auth import notebook_login

if TYPE_CHECKING:
    from oqtant.oqtant_client import OqtantClient

DEFAULT_RF_EVAP = RfEvap.new(
    times=[0, 50, 300, 800, 1100],
    powers=[600, 800, 600, 400, 400],
    frequencies=[21.12, 12.12, 5.12, 0.62, 0.02],
    interpolation=job_schema.InterpolationType.LINEAR,
)

DEFAULT_NAME = "quantum matter"
DEFAULT_LIFETIME = timing.EndTimeMs(10.0)  # ms
DEFAULT_TOF = timing.TimeOfFlightMs(12)  # ms
DEFAULT_IMAGE = job_schema.ImageType.TIME_OF_FLIGHT
TEMPERATURE_TO_EVAP_FREQUENCY = 0.067 / 200

pset = ProjectedSettings()


@dataclass
class OqtantLogin:
    access_token: str | None = None


class QuantumMatter(BaseModel):
    """A class that represents user inputs to create and manipulate quantum matter"""

    name: str | None = DEFAULT_NAME
    temperature: confloat(ge=0, le=500) | None = None
    lifetime: timing.EndTimeMs | None = DEFAULT_LIFETIME
    image: job_schema.ImageType | None = DEFAULT_IMAGE
    time_of_flight: timing.TimeOfFlightMs | None = DEFAULT_TOF
    rf_evap: RfEvap | None = None
    rf_shield: RfShield | None = None
    barriers: list[Barrier | job_schema.Barrier] | None = None
    landscape: Landscape | job_schema.OpticalLandscape | None = None
    lasers: list[Laser | job_schema.Laser] | None = None
    note: job_schema.JobNote | None = None
    client: object | None = None
    result: object | None = None
    job_id: str | None = None
    output: object | None = None
    is_sim: bool = False
    sim: Simulator | None = None
    run: int = 1

    def model_post_init(self, *args) -> None:
        if (self.temperature is not None) and (self.rf_evap is not None):
            warnings.warn(
                "Both 'temperature' and 'rf_evap' inputs provided, the last rf_evap frequency \
                will be altered."
            )
        end_time = 0.0
        lifetime = timing.decimal_to_float(self.lifetime)
        if self.barriers:
            for barrier in self.barriers:
                if isinstance(barrier, job_schema.Barrier):
                    barrier = Barrier.from_input(barrier)
                end_time = max(end_time, barrier.death)
            if end_time > lifetime:
                raise ValueError(
                    "Specified 'lifetime' not sufficient for constituent barrier object(s)."
                )
        if self.landscape:
            for snapshot in self.landscape.snapshots:
                if isinstance(snapshot, job_schema.Landscape):
                    snapshot = Snapshot.from_input(snapshot)
                end_time = max(end_time, timing.decimal_to_float(snapshot.time_ms))
            if end_time > lifetime:
                raise ValueError(
                    "Specified 'lifetime' not sufficient for constituent snapshot objects."
                )
        if self.lasers:
            for laser in self.lasers:
                if isinstance(laser, job_schema.Laser):
                    laser = Laser.from_input(laser)
                end_time = max(end_time, timing.decimal_to_float(max(laser.pulses[-1].times_ms)))
            if end_time > lifetime:
                raise ValueError(
                    "Specified 'lifetime' not sufficient for constituent laser pulse(s)."
                )

    @property
    def job_type(self) -> job_schema.JobType:
        """Property to get the job type of a submitted QuantumMatter object

        Returns:
            bert_schemas.job.JobType: The type of the job
        """
        if self.result:
            return self.result.job_type

    @property
    def status(self) -> job_schema.JobStatus:
        """Property to get the job status of a submitted QuantumMatter object

        Returns:
            bert_schemas.job.JobStatus: The status of the job
        """
        if self.result:
            return self.result.status

    @property
    def run_count(self) -> int:
        """Property to get the number of job runs for a submitted QuantumMatter object

        Returns:
            int: The total run number of the job
        """
        if self.result:
            return self.result.input_count

    @property
    def time_submit(self) -> int:
        """Property to get the time the current job was submitted

        Returns:
            str: The time the current job was submitted
        """
        if self.result:
            return self.result.time_submit

    @property
    def time_start(self) -> int:
        """Property to get the time the current job was run

        Returns:
            str: The time the current job was run
        """
        if self.result:
            return self.result.time_start

    @property
    def time_complete(self) -> int:
        """Property to get the time the current job was completed

        Returns:
            str: The time the current job was completed
        """
        if self.result:
            return self.result.time_complete

    @property
    def input(self) -> job_schema.InputValues:
        """Property to get the job input values of a QuantumMatter object

        Returns:
            bert_schemas.job.InputVales: The job input values of the QuantumMatter object's
            current result
        """
        return job_schema.InputValues(
            end_time_ms=self.lifetime,
            time_of_flight_ms=self.time_of_flight,
            image_type=self.image,
            rf_evaporation=self.rf_evaporation,
            optical_barriers=self.barriers,
            optical_landscape=self.landscape,
            lasers=self.lasers,
        )

    @property
    def rf_evaporation(self) -> job_schema.RfEvaporation:
        """Property to get the RF evaporation data of a QuantumMatter object

        Returns:
            bert_schemas.job.RfEvaporation: The RF evaporation values of the job's current result
        """
        rf_evap = deepcopy(self.rf_evap) if self.rf_evap is not None else DEFAULT_RF_EVAP
        if self.temperature is not None:
            rf_evap.frequencies_mhz[-1] = TEMPERATURE_TO_EVAP_FREQUENCY * self.temperature
        rf_evaporation = job_schema.RfEvaporation(
            times_ms=rf_evap.times_ms,
            frequencies_mhz=rf_evap.frequencies_mhz,
            powers_mw=rf_evap.powers_mw,
            interpolation=rf_evap.interpolation,
        )
        if self.rf_shield is not None:
            rf_evaporation.times_ms.append(self.lifetime)
            rf_evaporation.powers_mw.append(self.rf_shield.power)
            rf_evaporation.frequencies_mhz.append(self.rf_shield.frequency)

        return rf_evaporation

    @classmethod
    def from_input(
        cls,
        name: str,
        input: job_schema.InputValues,
        note: job_schema.JobNote | None = None,
        client: OqtantClient | None = None,
    ) -> QuantumMatter:
        """Method to create a new QuantumMatter object using the input values of an existing job

        Args:
            name (str): Name of the quantum matter
            input (bert_schemas.job.InputValues): The input values
            note (bert_schemas.job.JobNote | None): The notes for the input, can be None
            client (oqtant.oqtant_client.OqtantClient | None, optional): An instance of OqtantClient

        Returns:
            QuantumMatter: A new QuantumMatter object created using the input data
        """
        try:
            evap = RfEvap.from_input(input.rf_evaporation)
        except ConversionError:
            evap = None
        try:
            shield = RfShield.from_input(input.rf_evaporation)
        except ConversionError:
            shield = None

        barriers = None
        if input.optical_barriers:
            barriers = []
            for barrier in input.optical_barriers:
                barriers.append(Barrier.from_input(barrier))

        landscape = None
        if input.optical_landscape:
            landscape = Landscape.from_input(input.optical_landscape)

        return cls(
            name=name,
            lifetime=input.end_time_ms,
            image=input.image_type,
            time_of_flight=input.time_of_flight_ms,
            rf_evap=evap,
            rf_shield=shield,
            barriers=barriers,
            landscape=landscape,
            lasers=input.lasers,
            client=client,
            note=note,
        )

    @classmethod
    def from_oqtant_job(cls, job: OqtantJob, client: OqtantClient) -> QuantumMatter:
        """Method to create a new QuantumMatter object using an existing OqtantJob

        Args:
            job (oqtant.schemas.job.OqtantJob): The OqtantJob object to create from
            client (oqtant.oqtant_client.OqtantClient): An instance of OqtantClient
            run (int, optional): The specific run to use

        Returns:
            QuantumMatter: A new QuantumMatter object created using the OqtantJob data
        """
        inputs = job.inputs[0]
        qm = QuantumMatter.from_input(
            name=job.name, input=inputs.values, note=inputs.notes, client=client
        )
        qm.job_id = str(job.external_id)
        qm.result = job
        qm.run = job.run

        if inputs.output:
            qm.output = QuantumMatter.output_values_to_oqtant_output(inputs.output.values)
        return qm

    @staticmethod
    def output_values_to_oqtant_output(
        output_values: PlotOutput | NonPlotOutput,
    ) -> OqtantPlotOutput | OqtantNonPlotOutput:
        """Method to convert a completed job's output values to OqtantOutput

        Args:
            output_values (PlotOutput|NonPlotOutput):  The output values to convert
            to OqtantPlotOutput

        Returns:
            (oqtant.schemas.output.OqtantPlotOutput | oqtant.schemas.output.OqtantNonPlotOutput):
            The converted output values
        """

        if hasattr(output_values, "it_plot"):
            return OqtantPlotOutput(**output_values.model_dump())
        else:
            return OqtantNonPlotOutput(**output_values.model_dump())

    def write_to_file(self, *args, **kwargs) -> None:
        """Method to write the results of a submitted QuantumMatter object to a file.
        Wrapper for OqtantClient.write_job_to_file
        """
        self.client.write_job_to_file(self.result, *args, **kwargs)

    def submit_sim(self) -> None:
        """Method to submit a QuantumMatter object to be run as a simulation"""
        self.is_sim = True
        result = self.client.submit_sim(self)
        print("submitted simulation")
        self.sim = result

    def submit(self, track: bool = False, sim: bool = False) -> None:
        """Method to submit a QuantumMatter object to Oqtant to become a job and run on hardware or
        as a simulation

        Args:
            track (bool, optional): Flag to poll for job updates after submission
            sim (bool, optional): Flag to use the simulator backend instead of real hardware
        """
        if sim:
            self.submit_sim()
            return

        self.is_sim = False

        if self.job_id:
            raise exceptions.JobError(
                f"QuantumMatter object '{self.name}' was previously submitted and already has a job id.  "
                "Resubmission is not supported."
            )
        result = self.client.submit(self, track)
        self.job_id = result

    def get_sim_result(self) -> None:
        """Method to get the results of a simulator job. Alerts the user if simulation results are
        invalid due to boundary collision.
        """
        self.sim = self.client.get_sim_result(self.sim, self.image)

        output = None

        if self.image == job_schema.ImageType.IN_TRAP:
            it_output = self.sim.it_plot
            output = OqtantPlotOutput(**it_output)

        if self.image == job_schema.ImageType.TIME_OF_FLIGHT:
            tof_output = self.sim.tof_output
            output = OqtantNonPlotOutput(**tof_output)

        self.output = QuantumMatter.output_values_to_oqtant_output(output)

        self.result = self.client.convert_matter_to_job(self)
        if self.result.run is None:
            self.result.inputs[0].run = 1
            self.result.input_count = 1

        self.result.status = job_schema.JobStatus.COMPLETE
        job_done_msg = "Simulation complete."
        print(f"{job_done_msg:<20}")

        if self.sim.hit_boundary:
            print(
                "Results may be invalid after atoms reached simulation boundaries. "
                "Consider reducing barrier height or increasing ramp/evolution time."
            )

    def get_result(self, run: int | None = None) -> None:
        """Method to get the results of a hardware job

        Args:
            run (int, optional): The specific run to get
        """
        if self.is_sim:
            self.get_sim_result()
            return

        if not self.job_id:
            raise exceptions.JobError("Matter must be submitted before retrieving results")

        # use current run if one is not provided
        run = run if run else self.run
        self.result = self.client.get_job(self.job_id, run)

        # update matter input if current run is different than provided run
        if self.run != run:
            matter = self.from_input(
                name=self.name,
                input=self.result.inputs[0].values,
                note=self.result.inputs[0].notes,
                client=self.client,
            )
            self.lifetime = matter.lifetime
            self.image = matter.image
            self.time_of_flight = matter.time_of_flight
            self.rf_evap = matter.rf_evap
            self.rf_shield = matter.rf_shield
            self.barriers = matter.barriers
            self.lasers = matter.lasers
            self.note = matter.note
            self.run = run

        # clear output and update if new data exists
        self.output = None
        if self.result.status == job_schema.JobStatus.COMPLETE:
            self.output = QuantumMatter.output_values_to_oqtant_output(
                self.result.inputs[0].output.values
            )

    def corrected_rf_power(self, frequency_mhz: float, power_mw: float) -> float:
        """Method to calculate the corrected RF power based on the given frequency and power

        Args:
            frequency_mhz (float): The frequency in MHz
            power (float): The power in mW

        Returns:
            float: The corrected RF power in mW
        """
        voltage = power_mw * 5.0 / 1000.0  # payload power to attenuator voltage
        power_dbm = -26.2 - 42 * np.exp(-0.142 * frequency_mhz) - 32.76 * np.exp(-1.2 * voltage)

        # based on data taken from smallbert for power measured in dbm by a nearby pickup rf loop
        # as a function of the frequency (in MHz) and RF attenuator voltage (in volts)
        # the 'composer' turns payload powers of 0-1000 mW into voltages using a linear
        # relationship that maps 0-1000 mW to 0-5 V on the RF attenuator (5V = max power)

        return (1000.0 / 2.0e-3) * 10 ** (power_dbm / 10.0)  # dbm to mW with overall scaling

    def corrected_rf_powers(self, frequencies: list[float], powers: list[float]) -> list[float]:
        """Method to calculate the corrected RF powers based on the given lists of frequencies
        and powers

        Args:
            frequencies (list[float]): The frequencies in MHz
            powers (list[float]): The powers in mW

        Returns:
            list[float]: The corrected list of RF powers in mW
        """
        return [self.corrected_rf_power(freq, pow) for freq, pow in zip(frequencies, powers)]

    def show_rf_dynamics(self, corrected: bool = False) -> None:
        """Method to plot the dynamics of a QuantumMatter object's RF output

        Args:
            corrected (bool, optional): Flag to correct the RF power
        """
        evap = self.rf_evaporation
        rf_evap = RfEvap.from_input(evap)
        tstart = min(rf_evap.times_ms)
        evap_times = np.linspace(tstart, 0, num=int(abs(tstart) / 10), endpoint=True)
        fig, ax1 = plt.subplots()
        lns = []
        labs = []

        # plot of rf frequency vs time
        color = next(ax1._get_lines.prop_cycler)["color"]
        ax1.set_xlabel("time (ms)")
        ax1.set_ylabel("frequency (MHz)")
        ax1.set_ylim([0, 25])
        (ln1,) = plt.plot(evap_times, rf_evap.get_frequencies(evap_times), color=color)
        lns.append(ln1)
        labs.append("frequency")
        plt.plot(
            rf_evap.times_ms,
            rf_evap.get_frequencies(rf_evap.times_ms),
            ".",
            color=color,
        )
        if self.rf_shield is not None:
            plt.plot(
                [0, self.lifetime],
                [self.rf_shield.frequency] * 2,
                marker=".",
                color=color,
            )

        # plot of rf power vs time, on the same time axis as ax1
        ax2 = ax1.twinx()
        ax2.set_ylim([0, 1000])
        ax2.set_ylabel("power (mW)")
        color = next(ax1._get_lines.prop_cycler)["color"]
        (ln2,) = plt.plot(evap_times, rf_evap.get_powers(evap_times), color=color)
        lns.append(ln2)
        labs.append("power")
        plt.plot(
            rf_evap.times_ms,
            rf_evap.get_powers(rf_evap.times_ms),
            ".",
            color=color,
        )
        if self.rf_shield is not None:
            plt.plot([0, self.lifetime], [self.rf_shield.power] * 2, marker=".", color=color)
        if corrected:
            (ln3,) = plt.plot(
                evap_times,
                self.corrected_rf_powers(
                    rf_evap.get_frequencies(evap_times),
                    rf_evap.get_powers(evap_times),
                ),
                "--",
                color=color,
            )
            if self.rf_shield is not None:
                plt.plot(
                    [0, self.rf_shield.lifetime],
                    self.corrected_rf_powers(
                        [self.rf_shield.frequency] * 2,
                        [self.rf_shield.power] * 2,
                    ),
                    "--",
                    color=color,
                )
            lns.append(ln3)
            labs.append("corrected power")
        # shared setup
        ax1.legend(lns, labs, loc="upper center")
        color = next(ax1._get_lines.prop_cycler)["color"]
        plt.axvline(x=0, linestyle="dashed", color=color)
        plt.title("RF dynamic behavior")
        fig.tight_layout()  # avoid clipping right y-axis label
        plt.show()

    def get_magnetic_potential(self, positions: list[float]) -> list[float]:
        """Method to calculate the magnetic potentials for a given set of positions

        Args:
            positions (list[float]): The positions at which to calculate the potentials

        Returns:
            list[float]: List of magnetic potentials in kHz corresponding to the given positions
        """
        w = 2 * np.pi * 50  # weak axis trap frequency
        m = 87 * 1.66054e-27
        h = 6.626e-34

        # U = mf * g * ub * |B| with B = B0 + 0.5 * m * w^2 * x^2
        # for this purpose, we will set B0 = 0
        # (magnetic potential referenced to trap bottom as rf frequencies are)
        # our measured trap frequency is ~ 50 Hz

        potentials = 0.5 * m * w**2 * np.square(1e-6 * np.asarray(positions))  # in J
        potentials_khz = potentials / h / 1000.0  # in kHz
        return list(potentials_khz)

    def get_ideal_optical_potential(self, time: float, positions: list[float]) -> list[float]:
        """Method to calculate the "ideal" optical potential from constituent optical objects

        Args:
            time (float): time, in ms, for which the optical potential should be evaluated
            positions (list[float]): positions, in microns, where potential should be evaluated

        Returns:
            list[float]: list of potential energies, in kHz, at the request time and positions
        """
        potential = np.zeros_like(positions)
        if self.barriers is not None:
            for barr in self.barriers:
                potential += np.asarray(barr.get_ideal_potential(time=time, positions=positions))
        if self.landscape is not None:
            potential += np.asarray(
                self.landscape.get_ideal_potential(time=time, positions=positions)
            )
        return list(potential)

    def get_potential(
        self, time: float, positions: list[float], include_magnetic: bool = True
    ) -> list[float]:
        """Method to calculate the optical and magnetic potential at the given time for each
        position

        Args:
            time (float): The time at which to calculate the potential
            positions (list[float]): The positions at which to calculate the potential
            include_magnetic (bool, optional): Flag to include contributions from magnetic trap
        Returns:
            list[float]: List of potential energy corresponding to each request position
        """
        potential = np.asarray(
            projected.get_actual_potential(
                self.get_ideal_optical_potential, time=time, positions=positions
            )
        )
        if include_magnetic:
            potential += np.asarray(self.get_magnetic_potential(positions=positions))
        return list(potential)

    def show_potential(
        self,
        times: list[float] = [0.0],
        xlimits: list[float] = [pset.min_position - 1, pset.max_position + 1],
        ylimits: list[float] = [0.0 - 1, pset.max_energy + 1],
        include_ideal: bool = False,
        include_magnetic: bool = True,
        include_terminator: bool = False,
    ) -> None:
        """Method to plot the (optical) potential energy surface at the specified times

        Args:
            times (list[float], optional): The times for which to display the potential energy
            xlimits (list[float], optional): The plot limits for the x axis
            ylimits (list[float], optional): The plot limits for the y axis
            include_ideal (bool, optional): Flag for including target potential in plot
            include_magnetic (bool, optional): Flag to include contributions from magnetic trap
            include_terminator (bool, optional): Flag to include the position of the terminator beam
            relative to the trap
        """

        GAUSSIAN_1e2_DIAM_TO_FULL_WIDTH_HALF_MAX = 1.18
        term_radius_1e2 = pset.terminator_width
        full_width_half_max = GAUSSIAN_1e2_DIAM_TO_FULL_WIDTH_HALF_MAX * term_radius_1e2

        positions = np.arange(pset.min_position, pset.max_position + 0.1, 0.1, dtype=float)
        fig, ax = plt.subplots()

        plotted_term_already = False
        lns = []
        labs = []
        ln_term = []
        labs_term = []

        for time in times:
            color = next(ax._get_lines.prop_cycler)["color"]
            (ln,) = plt.plot(
                positions,
                self.get_potential(time, positions, include_magnetic),
                color=color,
                label=" ",
            )
            lns.append(ln)
            labs.append("t = " + str(time) + " ms")
            if include_ideal:
                potential = np.asarray(
                    self.get_ideal_optical_potential(time=time, positions=positions)
                )
                if include_magnetic:
                    potential += np.asarray(self.get_magnetic_potential(positions=positions))
                (ln2,) = plt.plot(positions, potential, "--", color=color, label=" ")
                lns.append(ln2)
                labs.append("t = " + str(time) + " ms (ideal)")

            if (
                self.lasers
                and self.lasers[0].type == job_schema.LaserType.TERMINATOR
                and not plotted_term_already
            ):
                term_center = self.lasers[0].position_um
                if include_terminator and self.lasers[0].is_on(time):
                    plt.vlines([term_center], ylimits[0], ylimits[1], "r", "--")
                    x_fwhm = [
                        term_center - full_width_half_max / 2,
                        term_center + full_width_half_max / 2,
                    ]
                    x_1e2 = [
                        term_center - term_radius_1e2,
                        term_center + term_radius_1e2,
                    ]
                    plt.fill_between(
                        x_fwhm,
                        [ylimits[0], ylimits[0]],
                        [ylimits[1], ylimits[1]],
                        alpha=0.5,
                        color="r",
                    )
                    (ln,) = plt.fill(np.NaN, np.NaN, "r", alpha=0.5, label=" ")
                    ln_term.append(ln)
                    labs_term.append("FWHM ($\\mu$m)")
                    plt.fill_between(
                        x_1e2,
                        [ylimits[0], ylimits[0]],
                        [ylimits[1], ylimits[1]],
                        alpha=0.1,
                        color="r",
                    )
                    (ln,) = plt.fill(np.NaN, np.NaN, "r", alpha=0.1, label=" ")
                    ln_term.append(ln)
                    labs_term.append("gaussian width (1/$e^2$) ($\\mu$m)")

                    plotted_term_already = True

        plt.xlabel("position (microns)", labelpad=6)
        plt.ylabel("potential energy (kHz)", labelpad=6)
        plt.xlim(xlimits)
        plt.ylim(ylimits)
        plt.legend()

        l2 = ax.legend(lns, labs, loc=2)
        if include_terminator:
            ax.legend(ln_term, labs_term, loc=1)
            plt.gca().add_artist(l2)
        plt.show()

    def show_barrier_dynamics(self) -> None:
        """Method to plot the time dynamics of every Barrier object within a QuantumMatter object"""
        fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=True, figsize=(6, 6))
        fig.suptitle("Barrier dynamics")
        ax1.set_xlim([-1, self.input.end_time_ms])
        ax1.set_ylabel("position (microns)")
        ax2.set_ylabel("height (kHz)")
        ax3.set_ylabel("width (microns)")
        ax3.set_xlabel("time (ms)")
        lns = []
        labs = []

        style = "steps-pre"
        for indx, barrier in enumerate(self.barriers):
            color = next(ax1._get_lines.prop_cycler)["color"]
            tstart = timing.decimal_to_float(min(barrier.times_ms))
            tstop = timing.decimal_to_float(max(barrier.times_ms))
            times = np.linspace(tstart, tstop, num=int((tstop - tstart) / 0.1), endpoint=True)
            barrier_times = timing.decimals_to_floats(barrier.times_ms)
            (ln,) = ax1.plot(times, barrier.get_positions(times), color=color, drawstyle=style)
            ax1.plot(barrier_times, barrier.get_positions(barrier_times), ".", color=color)
            ax2.plot(times, barrier.get_heights(times), color=color, drawstyle=style)
            ax2.plot(
                barrier_times,
                barrier.get_heights(barrier_times),
                ".",
                color=color,
            )
            ax3.plot(times, barrier.get_widths(times), color=color, drawstyle=style)
            ax3.plot(barrier_times, barrier.get_widths(barrier_times), ".", color=color)
            lns.append(ln)
            labs.append("barrier " + str(indx + 1))
        fig.legend(lns, labs)
        plt.show()

    def show_laser_pulse_timing(self, figsize=(6, 4)) -> None:
        """
        Method to plot the timing of a single terminator pulse in the experiment

        Args:
            figsize (tuple, optional) : Size of the output plot

        """

        fig, ax1 = plt.subplots(figsize=figsize)
        ax2 = ax1.twinx()
        lns = []
        labs = []

        # TODO support plotting for more than one laser, more than one pulse per laser

        if self.lasers:
            for laser in self.lasers:
                # sample on 50us time steps
                # TODO: support calculation and plotting of non-square pulses
                times = np.arange(0, timing.decimal_to_float(self.lifetime), 50e-3)
                intensities = np.zeros(len(times))
                detunings = np.zeros(len(times))

                # add all the pulse times, detunings, and intensities
                for pulse in laser.pulses:
                    interpolation = job_schema.interpolation_to_kind(pulse.interpolation)
                    f_pulse = interp1d(
                        timing.decimals_to_floats(pulse.times_ms),
                        pulse.intensities_mw_per_cm2,
                        kind=interpolation,
                        bounds_error=False,
                        fill_value=0,
                    )
                    intensities_pulse = f_pulse(times)
                    intensities += intensities_pulse
                    det_idx = np.argwhere(
                        (times >= timing.decimal_to_float(pulse.times_ms[0]))
                        & (times <= timing.decimal_to_float(pulse.times_ms[-1]))
                    )
                    detunings[det_idx] = pulse.detuning_mhz

                (ln,) = ax1.plot(times, intensities, "g")
                labs.append("intensities")
                lns.append(ln)
                (ln,) = ax2.plot(times, detunings, "b")
                lns.append(ln)
                labs.append("detunings ")

        ax1.set_xlabel("Time (ms)")
        ax1.set_ylabel("Intensity (mW/$cm^2$)", color="g")
        ax2.set_ylabel("Detuning (MHz)", color="b")

        fig.legend(lns, labs, bbox_to_anchor=(0.8, 0.3))
        fig.suptitle("Laser pulse timing during in-trap experiment")
        plt.show()

    class Config:
        validate_assignment = True
        arbitrary_types_allowed = True


class QuantumMatterFactory:
    """An abstract factory for creating instances of the QuantumMatter schema classes"""

    def __init__(self):
        self.login = notebook_login()
        self.client = None

    def get_login(self) -> Auth:
        """Method to display the authentication widget inside of a notebook, if no access token file
        is found.

        Returns:
            ipyauth.Auth: The authentication widget
        """
        access_token = None
        try:
            with open(os.path.join(os.path.expanduser("~"), ".access-token.txt")) as file:
                access_token = file.read()
        except:  # noqa: E722
            ...
        if access_token:
            self.login = OqtantLogin(access_token=access_token)
        else:
            return self.login

    def get_client(self, token: str | None = None) -> None:
        """Method to get an instance of OqtantClient and assign it to self.client

        Args:
            token (str | None, optional): Token to use when working outside of a notebook
        """
        access_token = token or self.login.access_token
        self.client = oq.get_oqtant_client(access_token)

    def search_jobs(self, *args, **kwargs) -> list[dict]:
        """Method to search for jobs.
        Wrapper for OqtantClient.search_jobs

        Returns:
            list[dict]: The jobs found for the search criteria
        """
        return self.client.search_jobs(*args, **kwargs)

    def show_queue_status(self, *args, **kwargs) -> list[dict]:
        """Method to show the current queue status of jobs submitted by the authenticated user.
        Wrapper for OqtantClient.show_queue_status

        Returns:
            list[dict]: The jobs found for the search criteria along with their queue status
        """
        return self.client.show_queue_status(*args, **kwargs)

    def show_job_limits(self) -> dict:
        """Method to show the current job limits of the authenticated user.
        Wrapper for OqtantClient.show_job_limits

        Returns:
            dict: The job limit information for the authenticated user
        """
        return self.client.show_job_limits()

    def load_matter_from_file(self, *args, **kwargs) -> QuantumMatter:
        """Method to create a QuantumMatter object using data in a file.
        Wrapper for OqtantClient.load_job_from_file

        Returns:
            QuantumMatter: A new QuantumMatter object created using the file data
        """
        job = self.client.load_job_from_file(*args, **kwargs)
        return QuantumMatter.from_oqtant_job(job, self.client)

    def load_matter_from_job_id(self, job_id: str, run: int = 1) -> QuantumMatter:
        """Method to create a QuantumMatter object using data from an existing job in the database

        Args:
            job_id (str): The id of the job to get from the database
            run (int, optional): The specific run to get

        Returns:
            QuantumMatter: A new QuantumMatter object created using the jobs data
        """
        result = self.client.get_job(job_id, run)
        if result.status == job_schema.JobStatus.COMPLETE:
            output_values = result.inputs[0].output.values
            output = QuantumMatter.output_values_to_oqtant_output(output_values)
        else:
            output = None

        matter = self.create_quantum_matter_from_input(
            name=result.name, input=result.inputs[0].values, note=result.inputs[0].notes
        )
        matter.output = output
        matter.job_id = job_id
        matter.result = result
        matter.run = run
        return matter

    def submit_list_as_batch(self, *args, **kwargs) -> str:
        """Method to submit multiple QuantumMatter objects as a single job.
        Wrapper for OqtantClient.submit_list_as_batch

        Returns:
            str: The ID of the submitted job
        """
        return self.client.submit_list_as_batch(*args, **kwargs)

    def create_quantum_matter(
        self,
        name: str | None = None,
        temperature: float | None = None,
        lifetime: float | None = None,
        image: job_schema.ImageType | None = None,
        time_of_flight: float | None = None,
        rf_evap: RfEvap | None = None,
        rf_shield: RfShield | None = None,
        barriers: list[Barrier] | None = None,
        landscape: Landscape | None = None,
        lasers: list[job_schema.Laser] | None = None,
        note: str | None = None,
    ) -> QuantumMatter:
        """Method to create a QuantumMatter object

        Args:
            name (str | None, optional): The name of the quantum matter
            temperature (float | None, optional): The quantum matter temperature
            lifetime (float | None, optional): The quantum matter lifetime
            image (bert_schemas.job.ImageType | None, optional): The quantum matter image type
            time_of_flight (float | None, optional): The quantum matter time of flight
            rf_evap (oqtant.schemas.rf.RfEvap | None, optional): The quantum matter RF evaporation
            rf_shield (oqtant.schemas.rf.RfShield | None, optional): The quantum matter RF shield
            barriers (list[oqtant.schemas.optical.Barrier] | None, optional): The quantum matter barriers
            landscape (oqtant.schemas.optical.Landscape | None, optional): The quantum matter landscape
            lasers (list[bert_schemas.job.Lasers] | None, optional): The quantum matter lasers
            note (str | None, optional): A note about the quantum matter

        Returns:
            QuantumMatter: A new QuantumMatter object
        """
        kwargs = {"client": self.client}
        for k, v in locals().items():
            if v is not None:
                kwargs[k] = v

        return QuantumMatter(**kwargs)

    def create_quantum_matter_from_input(
        self,
        name: str,
        input: job_schema.InputValues,
        note: job_schema.JobNote | None = None,
    ) -> QuantumMatter:
        """Method to create a QuantumMatter object using the input values of a job.
        Wrapper for QuantumMatter.from_input

        Args:
            name (str): The name of the quantum matter
            input (bert_schemas.job.InputValues): The input values
            note (job_schema.job.JobNote | None): The notes for the input, can be None

        Returns:
            QuantumMatter: A new QuantumMatter object created using the input data
        """
        return QuantumMatter.from_input(name, input, note, self.client)

    @staticmethod
    def create_snapshot(
        time: float = 0,
        positions: list = [-10, 10],
        potentials: list = [0, 0],
        interpolation: job_schema.InterpolationType = "LINEAR",
    ) -> Snapshot:
        """Method to create a Snapshot object

        Args:
            time (float, optional): The time in milliseconds
            positions (list, optional): A list of positions in micrometers
            potentials (list, optional): A list of potentials in kilohertz
            interpolation (bert_schemas.job.InterpolationType, optional): The type of interpolation for spatial data

        Returns:
            oqtant.schemas.optical.Snapshot: A new Snapshot object
        """
        return Snapshot(
            time_ms=time,
            positions_um=positions,
            potentials_khz=potentials,
            spatial_interpolation=interpolation,
        )

    @staticmethod
    def create_snapshot_from_input(input: job_schema.Landscape) -> Snapshot:
        """Method to create a Snapshot object using the input values of a job

        Args:
            input (bert_schemas.job.Landscape): The landscape input data

        Returns:
            oqtant.schemas.optical.Snapshot: A new Snapshot object created using the input data
        """
        return Snapshot(**input.model_dump())

    @staticmethod
    def create_landscape(
        snapshots: list[Snapshot] = [Snapshot.new(time=0), Snapshot.new(time=2)]
    ) -> Landscape:
        """Method to create a Landscape object from a list Snapshot objects

        Args:
            snapshots (list[oqtant.schemas.optical.Snapshot], optional): List of snapshots, defaults if not provided

        Returns:
            oqtant.schemas.optical.Landscape: A new Landscape object
        """
        optical_landscapes = []
        for snapshot in snapshots:
            optical_landscapes.append(  # kludge!
                job_schema.Landscape(
                    time_ms=snapshot.time_ms,
                    positions_um=snapshot.positions_um,
                    potentials_khz=snapshot.potentials_khz,
                    spatial_interpolation=snapshot.spatial_interpolation,
                )
            )
        return Landscape(landscapes=optical_landscapes)

    @staticmethod
    def create_landscape_from_input(input: job_schema.OpticalLandscape) -> Landscape:
        """Method to create a Landscape object from the input values of a job

        Args:
            input (bert_schemas.job.OpticalLandscape): The input values

        Returns:
            oqtant.schemas.optical.Landscape: A new Landscape object created using the input data
        """
        return Landscape(**input.model_dump())

    @staticmethod
    def create_barrier(
        positions: list[float] = [0.0, 0.0],
        heights: list[float] = [0.0, 0.0],
        widths: list[float] = [1.0, 1.0],
        times: list[float] = [0.0, 10.0],
        shape: job_schema.ShapeType = "GAUSSIAN",
        interpolation: job_schema.InterpolationType = "LINEAR",
    ) -> Barrier:
        """Method to create a Barrier object

        Args:
            positions (list[float], optional): The barrier positions
            heights (list[float], optional): The barrier heights
            widths (list[float], optional): The barrier widths
            times (list[float], optional): The barrier times
            shape (bert_schemas.job.ShapeType, optional): The barrier shape
            interpolation (bert_schemas.job.InterpolationType, optional): The barrier interpolation type

        Returns:
            oqtant.schemas.optical.Barrier: A new Barrier object

        Raises:
            ValueError: if data lists are not of equal length
        """
        if not (len(positions) == len(heights) == len(widths) == len(times)):
            raise ValueError("Barrier data lists must be of equal length, default minimum of 2")

        data = {
            "times_ms": times,
            "positions_um": positions,
            "heights_khz": heights,
            "widths_um": widths,
            "shape": shape,
            "interpolation": interpolation,
        }

        return Barrier(**data)

    @staticmethod
    def create_barrier_from_input(input: job_schema.Barrier) -> Barrier:
        """Method to create a Barrier object from the input values of a job

        Args:
            input (bert_schemas.job.Barrier): The input values

        Returns:
            oqtant.schemas.optical.Barrier: A new Barrier object created using the input data
        """
        return Barrier(**input.model_dump())

    @staticmethod
    def create_terminator(time_on: float, time_off: float) -> Laser:
        """Method to create terminator pulse

        Args:
            time_on (float) : time to start the pulse in ms
            time_off (float) : time to end the pulse in ms

        Returns:
            oqtant.schemas.optical.Laser: A new Laser object
        """

        pulse_data = {
            "times_ms": [time_on, time_off],
            "intensities_mw_per_cm2": [1, 1],
            "detuning_mhz": 0,
            "interpolation": job_schema.InterpolationType.OFF,
        }

        pulse = Pulse(**pulse_data)

        laser_data = {
            "type": job_schema.LaserType.TERMINATOR,
            "position_um": pset.terminator_position,
            "pulses": [pulse],
        }

        return Laser(**laser_data)

    @staticmethod
    def create_terminator_from_input(input: job_schema.Laser) -> Laser:
        """Method to create a Laser object from the input values of a job

        Args:
            input (bert_schemas.job.Laser): The input values

        Returns:
            oqtant.schemas.optical.Laser: A new Laser object created using the input data
        """
        return Laser(**input.model_dump())

    @staticmethod
    def create_rf_sequence(
        times: list = [0],
        powers: list = [0],
        frequencies: list = [0],
        interpolation: str = "LINEAR",
    ) -> RfSequence:
        """Method to create a RfSequence object

        Args:
            times (list[int], optional): The time values in milliseconds
            powers (list[list[float], optional): The power values in milliwatts
            frequencies (list[float], optional): The frequency values in megahertz
            interpolation (bert_schemas.job.InterpolationType, optional): The interpolation type to be used

        Returns:
            oqtant.schemas.rf.RfSequence: A new RfSequence object
        """
        return RfSequence(
            times_ms=times,
            powers_mw=powers,
            frequencies_mhz=frequencies,
            interpolation=interpolation,
        )

    @staticmethod
    def create_rf_sequence_from_input(input: job_schema.RfEvaporation) -> RfSequence:
        """Method to create a RfSequence object from the input values of a job

        Args:
            input (bert_schemas.job.RfEvaporation: The input values

        Returns:
            oqtant.schemas.rf.RfSequence: A new RfSequence object created using the input data
        """
        return RfSequence(**input.model_dump())

    @staticmethod
    def create_rf_evap(
        times: list = [0],
        powers: list = [0],
        frequencies: list = [0],
        interpolation: str = "LINEAR",
    ) -> RfEvap:
        """Method to create a RfEvap object

        Args:
            times (list[int], optional): The time values in milliseconds
            powers (list[list[float], optional): The power values in milliwatts
            frequencies (list[float], optional): The frequency values in megahertz
            interpolation (bert_schemas.job.InterpolationType, optional): The interpolation type to be used

        Returns:
            oqtant.schemas.rf.RfEvap: A new RfEvap object
        """
        return RfEvap.new(
            times=[t - max(times) for t in times],
            powers=powers,
            frequencies=frequencies,
            interpolation=interpolation,
        )

    @staticmethod
    def create_rf_evap_from_input(input: job_schema.RfEvaporation) -> RfEvap:
        """Method to create a RfEvap object from the input values of a job

        Args:
            input (bert_schemas.job.RfEvaporation): The input values

        Returns:
            oqtant.schemas.rf.RfEvap: A new RfEvap object created using the input data
        """
        return RfEvap.from_input(input)

    @staticmethod
    def create_rf_shield(
        power: float = 0, frequency: float = 0, lifetime: timing.EndTimeMs = 1.0
    ) -> RfShield:
        """Method to create a RfShield object

        Args:
            power (float, optional): The RfShield power
            frequency (float, optional): The RfShield frequency
            lifetime (float, optional): The RfShield lifetime

        Returns:
            oqtant.schemas.rf.RfShield: A new RfShield object
        """
        return RfShield.new(
            lifetime,
            frequency,
            power,
            interpolation="OFF",
        )

    @staticmethod
    def create_rf_shield_from_input(input: job_schema.RfEvaporation) -> RfShield:
        """Method to create a RfShield object from the input values of a job

        Args:
            input (bert_schemas.job.RfEvaporation): The input values

        Returns:
            oqtant.schemas.rf.RfShield: A new RfShield object created using the input data
        """
        return RfShield.from_input(input)
