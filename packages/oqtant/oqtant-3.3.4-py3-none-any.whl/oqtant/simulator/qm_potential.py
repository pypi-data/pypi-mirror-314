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

import numpy as np
from bert_schemas import job as job_schema

from oqtant.simulator.three_dim import ThreeDimGrid
from bert_schemas.timing import decimal_to_float


class QMPotential:
    """
    'QMPotential' represents the quantum matter object potential (combination of magnetic trap/snapshot/barriers)
    in simulation units. Contains a 2D array of the potential energy in the simulation at a given time.
    """

    # natural units of Oqtant
    weak_trap_freq = 2 * np.pi * 50  # weak axis trap frequency
    m = 87 * 1.66054e-27  # rb87 mass
    h = 6.626e-34  # planck's constant
    msec = 1e-3
    microns = 1e-6
    khz = 1e3
    hbar = h / 2 / np.pi  # hbar

    # natural units of the simulation (in SI) #CHECKED
    sim_time_unit = 1 / weak_trap_freq  # 3.18 milliseconds = 1 simulation time
    sim_length_unit = np.sqrt(
        hbar / m / weak_trap_freq
    )  # 1.52 microns = 1 simulation length
    sim_energy_unit = hbar * weak_trap_freq

    # convert simulation units to Oqtant units # Checked
    sim_length_to_oqt = (
        sim_length_unit / microns
    )  # convert a simulation length to microns.  1.524 microns
    sim_time_to_oqt = (
        sim_time_unit / msec
    )  # convert a simulation time to microseconds.  3.183 mseconds
    oqt_time_to_sim = 1 / sim_time_to_oqt

    w0x = 1.0  # 50hz; trap angular frequency; set natural units
    w0r = 8.0  # 400hz; trap angular frequency

    def __init__(self, quantum_matter):
        self.quantum_matter = quantum_matter
        self.three_d_grid = ThreeDimGrid()
        self.potential = None

    # convert units of quantum matter object to simulation relevant quantities
    @property
    def lifetime(self) -> float:
        """Returns the lifetime of the simulation in simulation time units."""
        return (
            decimal_to_float(self.quantum_matter.lifetime) * QMPotential.msec / QMPotential.sim_time_unit
        )

    @property
    def time_of_flight(self) -> float:
        """If image type is in trap returns zero. Else calculate and return time of flight in the units of the sim"""
        if self.quantum_matter.image == job_schema.ImageType.IN_TRAP:
            return 0.0

        return (
            decimal_to_float(self.quantum_matter.time_of_flight)
            * QMPotential.msec
            / QMPotential.sim_time_unit
        )

    def update_potential(self, time: np.ndarray, clip: bool = False) -> None:
        """
        Function to query the potential at a specific simulation time (sim units), from the Oqtant
        quantum matter object. Potential is updated with the magnetic trap

        Updates property self.potential

        Args:
            time (np.ndarray[float]):  time (in simulation units)
            clip (boolean): whether to clip

        Returns:
            None
        """
        if time > self.lifetime + self.time_of_flight:
            raise ValueError(
                "Potential update requested outside time bounds of the simulation"
            )

        # time: sim -> msec # Checked
        time *= QMPotential.sim_time_unit / QMPotential.msec

        # potential in x-direction (in kHz)
        potential_1d_x = np.array(
            self.quantum_matter.get_potential(
                time,
                self.three_d_grid.x_1d
                * QMPotential.sim_length_unit
                / QMPotential.microns,
            )
        )

        # potential in z-direction (in sim. units) # Checked
        potential_1d_x *= QMPotential.h * QMPotential.khz / QMPotential.sim_energy_unit

        # potential in r-direction (in sim. units) # Checked
        potential_1d_r = 0.5 * QMPotential.w0r**2 * self.three_d_grid.r_1d**2

        # meshgrid in r and x directions (simulation units)
        pot_x, pot_r = np.meshgrid(potential_1d_x, potential_1d_r)

        # total potential: simulation units
        if clip:
            self.potential = np.clip(
                pot_x + pot_r, 0.0, 400.0
            )  # clip energies above 20 khz.  can be raised...

        else:
            self.potential = pot_x + pot_r

    def potential_to_cartesian_oqt_units(self) -> np.ndarray:
        """
        Convert the potential object self.potential to cartesian coordinates and oqtant units (microns, kHz).

        Returns:
            array: the converted potential in cartesian coordinates and oqtant units
        """

        # convert potential to oqtant units from sim energy units
        potential_khz = (
            self.potential
            * QMPotential.sim_energy_unit
            / (QMPotential.h * QMPotential.khz)
        )

        return np.concatenate((np.flip(potential_khz, axis=0), potential_khz))
