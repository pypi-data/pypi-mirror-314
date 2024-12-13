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

import json

import matplotlib.pyplot as plt
import numpy as np
from bert_schemas import job as job_schema
from bert_schemas import projected
from bert_schemas.projected import (
    BarrierHeights,
    BarrierPositions,
    BarrierTimes,
    BarrierWidths,
    ProjectedEnergies,
    ProjectedPositions,
)
from bert_schemas.projected import Settings as ProjectionSettings
from bert_schemas.timing import TimeMs, decimal_to_float

pset = ProjectionSettings()

# Module containing methods and classes for abstractions of quasi-1D "painted" light Oqtant object

# "ideal" optical potentials are those specified by the user using included objects
# "actual" optical potentials include implementation and hardware realities
# such as objects being projected as a sum of gaussians on a pre-defined position grid
# with dynamic weights recalculated on a periodic basis


class Snapshot(job_schema.Landscape):
    """A class that represents a painted optical landscape/potential at a single
    point in (manipulation stage) time
    """

    @classmethod
    def new(
        cls,
        time: TimeMs = 0.0,
        positions: ProjectedPositions = [-10, 10],
        potentials: ProjectedEnergies = [0, 0],
        interpolation: job_schema.InterpolationType = "LINEAR",
    ) -> Snapshot:
        """Method to create a new Snapshot object

        Args:
            time (float, optional): Time associated with the snapshot
            positions (list, optional): Position list for the snapshot
            potentials (list, optional): Potential energies corresponding to the list of positions
            interpolation (bert_schemas.job.InterpolationType, optional): How to connect the object's
                (positions, potentials) data in space.

        Returns:
            Snapshot: a new Snapshot object
        """
        return cls(
            time_ms=time,
            positions_um=positions,
            potentials_khz=potentials,
            spatial_interpolation=interpolation,
        )

    @classmethod
    def from_input(cls, landscape: job_schema.Landscape) -> Snapshot:
        """Method to create a Snapshot object from an existing jobs input

        Args:
            landscape (bert_schemas.job.Landscape): The input values

        Returns:
            Snapshot: A new Snapshot object created using the input data
        """
        return cls(**landscape.model_dump())

    def show_potential(
        self,
        xlimits: list[float] = [pset.min_position - 1, pset.max_position + 1],
        ylimits: list[float] = [-1.0, pset.max_energy + 1],
        include_ideal: bool = False,
    ) -> None:
        """Method to plot the potential energy as a function of position for a Landscape
        object at the given times

        Args:
            xlimits (list[float], optional): Plot limits for x axis
            ylimits (list[float], optional): Plot limits for y axis
            include_ideal (bool, optional): Flag for including target potential in plot
        """

        positions = np.arange(pset.min_position, pset.max_position + 0.1, 0.1, dtype=float)

        _, ax = plt.subplots()
        color = next(ax._get_lines.prop_cycler)["color"]
        (ln,) = plt.plot(positions, self.get_potential(positions=positions), color=color)
        if include_ideal:
            (ln2,) = plt.plot(
                positions,
                self.get_ideal_potential(positions=positions),
                "--",
                color=color,
            )
            plt.plot(self.positions_um, self.potentials_khz, ".", color=color)
            lns = [ln, ln2]
            labs = ["actual", "ideal"]
            ax.legend(lns, labs, loc=0)
        plt.xlabel("position (microns)", labelpad=6)
        plt.ylabel("potential energy (kHz)", labelpad=6)
        plt.title("Snapshot potential energy profile")
        plt.xlim(xlimits)
        plt.ylim(ylimits)
        plt.show()


# (potentially) dynamic landscape made up of snapshots
class Landscape(job_schema.OpticalLandscape):
    """Class that represents a dynamic painted-potential optical landscape constructed
    from individual (instantaneous time) Snapshots
    """

    @classmethod
    def new(
        cls,
        snapshots: list[Snapshot] = [
            Snapshot.new(time=0),
            Snapshot.new(time=2),
        ],
    ) -> Landscape:
        """Method to create a new Landscape object

        Args:
            snapshots (list[Snapshot], optional): A list of Snapshot objects

        Returns:
            Landscape: A new Landscape object
        """
        optical_landscapes = []
        for snapshot in snapshots:
            optical_landscapes.append(
                job_schema.Landscape(
                    time_ms=snapshot.time_ms,
                    positions_um=snapshot.positions_um,
                    potentials_khz=snapshot.potentials_khz,
                    spatial_interpolation=snapshot.spatial_interpolation,
                )
            )
        return cls(landscapes=optical_landscapes)

    @classmethod
    def from_input(cls, landscape: job_schema.OpticalLandscape) -> Landscape:
        """Method to create a Landscape object from an existing jobs input

        Args:
            landscape (job_schema.OpticalLandscape): The input values

        Returns:
            Landscape: A new Landscape object
        """
        return cls(**json.loads(landscape.model_dump_json()))

    # extract Snapshot abstract objects from backend data structure
    @property
    def snapshots(self) -> list[Snapshot]:
        """Property to get a list of Snapshot objects associated to a Landscape object

        Returns:
            list[Snapshot]: List of Snapshot objects
        """
        return [Snapshot(**landscape.model_dump()) for landscape in self.landscapes]

    def show_potential(
        self,
        times: list = [0.0],
        xlimits: list = [pset.min_position - 1, pset.max_position + 1],
        ylimits: list = [-1.0, pset.max_energy + 1],
        include_ideal: bool = False,
    ):
        """Method to plot the potential energy as a function of position for a Landscape object at the given times

        Args:
            times (list[float], optional): Times, in ms, at which to evaluate and plot the potential
            xlimits (list[float], optional): Plot limits for x axis
            ylimits (list[float], optional): Plot limits for y axis
            include_ideal (bool, optional): Flag for including target potential in plot
        """
        positions = np.arange(pset.min_position, pset.max_position + 0.1, 0.1, dtype=float)

        fig, ax = plt.subplots()
        lns = []
        labs = []
        for time in times:
            potentials = self.get_potential(time, positions)
            color = next(ax._get_lines.prop_cycler)["color"]
            (ln,) = plt.plot(positions, potentials, color=color)
            lns.append(ln)
            labs.append("t = " + str(time) + " ms")
            if include_ideal:
                potentials_ideal = self.get_ideal_potential(time=time, positions=positions)
                (ln,) = plt.plot(positions, potentials_ideal, "--", color=color)
                lns.append(ln)
                labs.append("t = " + str(time) + " ms (ideal)")

        plt.xlabel("position (microns)", labelpad=6)
        plt.ylabel("potential energy (kHz)", labelpad=6)
        plt.title("Landscape potential energy profile")
        plt.xlim(xlimits)
        plt.ylim(ylimits)
        ax.legend(lns, labs, loc=0)
        plt.show()


class Barrier(job_schema.Barrier):
    """Class that represents a painted optical barrier."""

    @classmethod
    def new(
        cls,
        positions: BarrierPositions = [0.0, 0.0],
        heights: BarrierHeights = [0.0, 0.0],
        widths: BarrierWidths = [1.0, 1.0],
        times: BarrierTimes = [0.0, 10.0],
        shape: job_schema.ShapeType = job_schema.ShapeType.GAUSSIAN,
        interpolation: job_schema.InterpolationType = job_schema.InterpolationType.LINEAR,
    ) -> Barrier:
        """Method to create a new Barrier object

        Args:
            positions (list[float], optional): Positions for the barrier
            heights (list[float], optional): Heights for the barrier
            widths (list[float], optional): Widths for the barrier
            times (list[float], optional): Times for the barrier
            shape (bert_schemas.job.ShapeType, optional): Shape of the barrier
            interpolation (bert_schemas.job.InterpolationType, optional): Interpolation type of the barrier

        Returns:
            Barrier: A new Barrier object

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

        return cls(**data)

    @classmethod
    def from_input(cls, barrier: job_schema.Barrier) -> Barrier:
        """Method to create a Barrier object using the input values of a job

        Args:
            barrier (job_schema.Barrier): The input values

        Returns:
            Barrier: A new Barrier object created using the input data
        """
        return cls(**barrier.model_dump())

    def show_dynamics(self) -> None:
        """Method to plot the position, width and height of a Barrier object over time"""
        tstart = min(self.times_ms)
        tstop = max(self.times_ms)
        times = np.linspace(
            decimal_to_float(tstart),
            decimal_to_float(tstop),
            num = int((tstop - tstart) / pset.update_period),
            endpoint=True,
        )
        fig, ax1 = plt.subplots()

        # plot position and width vs time
        style = "steps-pre"
        color = next(ax1._get_lines.prop_cycler)["color"]
        ax1.set_xlabel("time (ms)")
        ax1.set_ylabel("position or width (microns)")
        ax1.set_xlim([-1, self.times_ms[-1] + 1])
        ax1.set_ylim([pset.min_position - 1, pset.max_position + 1])
        (ln1,) = plt.plot(times, self.get_positions(times), color=color, drawstyle=style)
        plt.plot(
            self.times_ms,
            self.get_positions(self.times_ms),
            ".",
            color=color,
        )
        color = next(ax1._get_lines.prop_cycler)["color"]
        (ln2,) = plt.plot(times, self.get_widths(times), color=color, drawstyle=style)
        plt.plot(self.times_ms, self.get_widths(self.times_ms), ".", color=color)

        # plot height on the same time axis
        ax2 = ax1.twinx()
        ax2.set_ylabel("height (kHz)")
        ax2.set_ylim([0, 100])
        color = next(ax1._get_lines.prop_cycler)["color"]
        (ln3,) = plt.plot(times, self.get_heights(times), color=color, drawstyle=style)
        plt.plot(self.times_ms, self.get_heights(self.times_ms), ".", color=color)

        # shared setup
        color = next(ax1._get_lines.prop_cycler)["color"]
        ax1.legend([ln1, ln2, ln3], ["position", "width", "height"], loc="upper left")
        plt.title("Barrier dynamics")
        fig.tight_layout()
        plt.show()

    def show_potential(
        self,
        times: list[float] = [0.0],
        xlimits: list[float] = [pset.min_position - 1, pset.max_position + 1],
        ylimits: list[float] = [-1.0, pset.max_energy + 1],
        include_ideal: bool = False,
    ) -> None:
        """Method to plot the potential energy as a function of position for a Barrier object

        Args:
            times (list[float], optional): The times, in ms, at which the potential is evaluated
            xlimits (list[float], optional): Plot limits for x axis
            ylimits (list[float], optional): Plot limits for y axis
            include_ideal (bool, optional): Flag for including target potential in plot
        """

        positions = np.arange(np.floor(min(xlimits)), np.ceil(max(xlimits)) + 1, 0.1)

        fig, ax1 = plt.subplots()
        ax = plt.gca()
        lns = []
        labs = []
        for time in times:
            color = next(ax._get_lines.prop_cycler)["color"]
            potential = self.get_potential(time=time, positions=positions)
            (ln,) = plt.plot(positions, potential, color=color)
            lns.append(ln)
            labs.append("t = " + str(time) + " ms")
            if include_ideal:
                potentials_ideal = self.get_ideal_potential(time=time, positions=positions)
                (ln,) = plt.plot(positions, potentials_ideal, "--", color=color)
                lns.append(ln)
                labs.append("t = " + str(time) + "ms (ideal)")

        plt.xlabel("position (microns)", labelpad=6)
        plt.ylabel("potential energy (kHz)", labelpad=6)
        plt.xlim(xlimits)
        plt.ylim(ylimits)
        ax1.legend(lns, labs, loc=0)
        plt.show()


class Pulse(job_schema.Pulse):
    """Class that represents a terminator laser pulse"""

    @classmethod
    def new(
        cls,
        times_ms: list[TimeMs],
        intensities_mw_per_cm2: list[float] = [1, 1],
        detuning_mhz: float = 0,
        interpolation: job_schema.InterpolationType = job_schema.InterpolationType.OFF,
    ) -> Pulse:
        """Method to create a new terminator laser pulse

        Args:
            times_ms (list) : [turn on time, turn off time]
            intensities_mw_per_cm2 (list[float]) : intensities in mw per cm^2, default = [1,1]
            detuning_mhz (float) : laser frequency detuning from resonance, default = 0
            interpolation (job_schema.InterpolationType) : interpolation in time for intensity,
                default = job_schema.InterpolationType.OFF
        Returns:
            Pulse: A new Pulse object

        Raises:
            ValueError: #TODO check that no values are specified for fields which are not supported yet
        """

        print(times_ms, intensities_mw_per_cm2)

        data = {
            "times_ms": times_ms,
            "intensities_mw_per_cm2": intensities_mw_per_cm2,
            "detuning_mhz": detuning_mhz,
            "interpolation": interpolation,
        }

        return cls(**data)

    @classmethod
    def from_input(cls, pulse: job_schema.Pulse) -> Pulse:
        """Method to create a Pulse object using the input values of a job

        Args:
            pulse (job_schema.Pulse): The input values

        Returns:
            Pulse: A new Pulse object created using the input data
        """
        return cls(**pulse.model_dump())


class Laser(job_schema.Laser):
    """Class that represents a terminator laser with a single pulse."""

    @classmethod
    def new(
        cls,
        pulses: list[Pulse],
        type: job_schema.LaserType = "TERMINATOR",
        position_um: float = pset.terminator_position,
    ) -> Laser:
        """Method to create a new Laser

        Args:
            pulses (list[Pulse]) : a list of laser pulse objects
            type (job_schema.LaseType) : laser type by task/experiment, default = "TERMINATOR"
            position_um (float) : position along the X axis in microns, default = 0 #TODO put real beam center here

        Returns:
            Barrier: A new Barrier object

        Raises:
            OqtantError: #TODO check that there is only one pulse
        """

        data = {"type": type, "position_um": position_um, "pulses": pulses}

        return cls(**data)

    @classmethod
    def from_input(cls, laser: job_schema.Laser) -> Laser:
        """Method to create a Laser object using the input values of a job

        Args:
            laser (job_schema.Laser): The input values

        Returns:
            Laser: A new Laser object created using the input data
        """
        return cls(**laser.model_dump())

    def is_on(self, time_ms: float) -> bool:
        for pulse in self.pulses:
            if (time_ms >= decimal_to_float(pulse.times_ms[0])) & (
                time_ms <= decimal_to_float(pulse.times_ms[-1])
            ):
                return True
        return False
