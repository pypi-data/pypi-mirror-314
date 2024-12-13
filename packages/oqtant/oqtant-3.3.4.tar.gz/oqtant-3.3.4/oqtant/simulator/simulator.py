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

import math
from dataclasses import dataclass
from logging import getLogger
from typing import Final

import matplotlib.pyplot as plt
import numpy as np
from bert_schemas.job import Image, LineChart
from matplotlib.animation import FuncAnimation
from scipy import interpolate
from scipy.interpolate import RectBivariateSpline

from oqtant.simulator.qm_potential import QMPotential
from oqtant.simulator.wave_function import WaveFunction
from oqtant.util.exceptions import SimValueError

logger = getLogger(__name__)


@dataclass
class TimeSpan:
    start: float
    end: float


class Simulator:
    """
    'Simulator' Defines methods for evolution and plotting of the system described by the Oqtant simulator.
    The Oqtant simulator is constantly in evolution and the inteface should not be relied upon for use external to
    the Oqtant API.
    """

    number_of_atoms: Final[int] = 1e4
    # this is specific to interactions between Rubidium - 87 atoms
    scattering_length: Final[float] = 0.0034117
    interaction_strength: Final[float] = (
        4.0 * np.pi * number_of_atoms * scattering_length
    )
    EXPERIMENT_IT_TOF_OD_RATIO: Final[int] = 0.04057

    def __init__(self, potential: QMPotential):
        """
        Creates Three Wavefunctions:
        - One is In-Trap (IT)
        - One is Time of Flight Far Field (tof_ff)
        - One is Time of Flight Near Field (tof_nf)

        Args:
        potential: Defined with QMPotential object.
        """
        # No need for TOF version of self.qm_potential as it's switched off in this mode.
        self.qm_potential = potential
        self.wavefunction = WaveFunction()
        self.wavefunction_tof_nf = WaveFunction(tof_nf=True)
        self.wavefunction_tof_ff = WaveFunction(tof_ff=True)

        self.times: list | None = None
        self.psi_history = []  # None
        self.time_step = 0.5e-3
        self.sampling_rate = 100

        # use near-field grid for up to 10ms
        self.max_NF_time = 6 * self.qm_potential.oqt_time_to_sim

        # tof_nf mode uses larger grids and turns off the trap
        self.tof_nf = False

        # tof_ff uses even larger grids and turns off the trap
        self.tof_ff = False

        self.ground = False  # ground state mode. evolves in imaginary time
        self.clip = True  # clip:  should we restrict the maximum energy in the problem for stability purposes?
        self.last_it_time_idx = 0
        self.hit_boundary = False

    def set_ground_state(self) -> None:
        """
        This function evolves the condensate with ground = True.
        It is done at negative times before the barriers are switched on.
        2.5 simulation units of time is sufficient to settle down to the ground state.

        Returns:
            None

        """

        self.wavefunction.psi = self.wavefunction.initial_psi(
            sigma_r=1 / np.sqrt(self.qm_potential.w0r)
        )
        self.times = []
        self.psi_history = []
        self.ground = True  # we are in ground state mode
        self.run_rk4(TimeSpan(-2.5, -0.01))
        self.times = [0]  # reset times
        self.psi_history = [
            self.wavefunction.psi
        ]  # reset psi_history to begin from the ground state.

    def run_evolution(self) -> None:
        """
        Run the simulation in In-Trap (IT) mode. This function evolves the condensate with ground = False.
        It is done at positive times during the "experiment" stage (t=0).
        Optical potentials may be applied during this stage.
        It runs for the lifetime of the quantum_matter object
        It starts from the end result of running get_ground_state

        Returns:
            None

        """
        if self.times is None:
            raise ValueError("Ground State not set")
        self.ground = False  # we are no longer in the ground state mode

        # start from the end result of running get_ground_state
        # load the ground state found in set_ground_state
        self.wavefunction.psi = self.psi_history[0]
        if (
            self.qm_potential.lifetime > 0
        ):  # if lifetime is greater than zero, then we must evolve the wave function.
            self.psi_history = []  # clear psi_history
            self.times = []  # clear times
            self.run_rk4(TimeSpan(0, self.qm_potential.lifetime), stage_name="in-trap ")
        self.last_it_time_idx = len(self.times) - 1

    def run_TOF(self) -> None:
        """
        This function runs the TOF evolution and turns on/off the far field grid as needed

        Returns:
            None

        """

        self.run_TOF_nearField()
        # run in far field mode if user specifies long TOF
        if self.qm_potential.time_of_flight > self.max_NF_time:
            self.run_TOF_farField()

    def run_TOF_nearField(self) -> None:  # TOF mode
        """
        This function evolves the condensate with ground = False, with no trapping potentials or optical potentials.
        It runs for up to 6ms of the quantum_matter object, beginning with the result wavefunction of run_evolution
        It uses the near field TOF grid: self.wavefunction_tof_nf.three_d_grid is created with argument NF = True

        Returns:
            None

        """
        # we are now in "TOF mode".  Functions will use the TOF grids.
        self.tof_nf = True
        self.tof_ff = False  # we are not yet in far field mode.

        # load the final state from the IT evolution and interpolate it onto the near-field grids.
        # basically this loads wavefunction_tof
        self.wavefunction_tof_nf.psi = self.convert_intrap_to_nearfield(
            self.psi_history[-1]
        )

        # check if we need to go limit time in near-field mode.
        if self.qm_potential.time_of_flight > self.max_NF_time:
            end_nf_time = self.max_NF_time
        else:
            end_nf_time = self.qm_potential.time_of_flight

        # evolve using the near-field grids.
        self.run_rk4(
            TimeSpan(
                self.qm_potential.lifetime,
                self.qm_potential.lifetime + end_nf_time,
            ),
            stage_name="near field TOF ",
        )

    def run_TOF_farField(self) -> None:  # TOF mode
        """
        This function evolves the condensate with ground = False, with no trapping potentials or optical potentials.
        It runs for the remaining time of flight of the quantum_matter object, beginning with the result wavefunction
        of run_TOF_nearField at 6ms.
        It uses the far field TOF grid: self.wavefunction_tof_ff.three_d_grid is created with argument FF = True

        Returns:
            None

        """

        self.tof_nf = False  # we are no longer in near field mode.
        self.tof_ff = True  # we are now in far field mode.

        # load the final state from the NF evolution and interpolate it onto the three_d_grid_TOF grids.
        # basically this loads wavefunction_tof
        self.wavefunction_tof_ff.psi = self.convert_nearfield_to_farfield(
            self.psi_history[-1]
        )

        # evolve using far-field grids.
        self.run_rk4(
            TimeSpan(
                self.qm_potential.lifetime + self.max_NF_time,
                self.qm_potential.lifetime + self.qm_potential.time_of_flight,
            ),
            stage_name="far field TOF ",
        )

        return

    def convert_intrap_to_nearfield(self, psi: np.ndarray) -> np.ndarray:
        """
        Performs interpolation of wave function between IT and TOF grids
        For handoff between evolve IT and in TOF modes.

        Args:
            psi (ndarray):  a wave function of the IT grid (self.wavefunction.three_d_grid)
        Returns:
            ndarray:  psi interpolated onto the TOF nearfield grid (self.wavefunction_tof_nf.three_d_grid)
        """

        # construct an interpolation function for psi from the IT grid.  separate out into real and imag parts.
        ip_real = RectBivariateSpline(
            self.wavefunction.three_d_grid.r[:, 0],
            self.wavefunction.three_d_grid.x[0, :],
            np.real(psi),
            kx=3,
            ky=3,
        )  # cubic spline interpolation
        ip_imag = RectBivariateSpline(
            self.wavefunction.three_d_grid.r[:, 0],
            self.wavefunction.three_d_grid.x[0, :],
            np.imag(psi),
            kx=3,
            ky=3,
        )  # cubic spline interpolation

        # interpolate psi onto TOF grid
        psi_tof_nf = ip_real(
            self.wavefunction_tof_nf.three_d_grid.r[:, 0],
            self.wavefunction_tof_nf.three_d_grid.x[0, :],
        ) + 1j * ip_imag(
            self.wavefunction_tof_nf.three_d_grid.r[:, 0],
            self.wavefunction_tof_nf.three_d_grid.x[0, :],
        )

        return psi_tof_nf

    def convert_nearfield_to_farfield(self, psi_tof_nf: np.ndarray) -> np.ndarray:
        """
        Interpolation of wave function between NF and FF grids
        For handoff between evolve NF and in FF modes.

        Args:
            psi_tof_nf (ndarray):  a wave function of the NF grid (self.wavefunction_tof_nf.three_d_grid)
        Returns:
            ndarray:  psi interpolated onto the TOF grid (self.wavefunction_tof_ff.three_d_grid)
        """

        # construct an interpolation function for psi from the IT grid.  separate out into real and imag parts.
        ip_real = RectBivariateSpline(
            self.wavefunction_tof_nf.three_d_grid.r[:, 0],
            self.wavefunction_tof_nf.three_d_grid.x[0, :],
            np.real(psi_tof_nf),
            kx=3,
            ky=3,
        )  # cubic spline interpolation
        ip_imag = RectBivariateSpline(
            self.wavefunction_tof_nf.three_d_grid.r[:, 0],
            self.wavefunction_tof_nf.three_d_grid.x[0, :],
            np.imag(psi_tof_nf),
            kx=3,
            ky=3,
        )  # cubic spline interpolation

        # interpolate psi onto TOF grid
        psi_tof_ff = ip_real(
            self.wavefunction_tof_ff.three_d_grid.r[:, 0],
            self.wavefunction_tof_ff.three_d_grid.x[0, :],
        ) + 1j * ip_imag(
            self.wavefunction_tof_ff.three_d_grid.r[:, 0],
            self.wavefunction_tof_ff.three_d_grid.x[0, :],
        )

        return psi_tof_ff

    def get_laplacian(self, y: np.ndarray) -> np.ndarray:
        """
        Implementation of the second derivatives in x and r including forward, central, and backward formulas
        to second order accuracy

        Args:
            y (ndarray): function for which we calculate the laplacian

        Returns:
            ndarray: The laplacian of the function

        """
        if self.tof_nf:
            dr, dx = (
                self.wavefunction_tof_nf.three_d_grid.dr,
                self.wavefunction_tof_nf.three_d_grid.dx,
            )
        elif self.tof_ff:
            dr, dx = (
                self.wavefunction_tof_ff.three_d_grid.dr,
                self.wavefunction_tof_ff.three_d_grid.dx,
            )
        else:
            dr, dx = (
                self.wavefunction.three_d_grid.dr,
                self.wavefunction.three_d_grid.dx,
            )

        # First derivative.
        dydr = np.gradient(y, axis=0, edge_order=2) / dr
        dydr[0, :] = 0  # Enforce Neumann boundary condition

        #         # Central difference
        d2ydr2 = (np.roll(y, -1, axis=0) - 2 * y + np.roll(y, 1, axis=0)) / dr**2
        d2ydx2 = (np.roll(y, -1, axis=1) - 2 * y + np.roll(y, 1, axis=1)) / dx**2

        #         # Forward difference at start of array
        d2ydr2[0, :] = (2 * y[0, :] - 5 * y[1, :] + 4 * y[2, :] - y[3, :]) / dr**2
        d2ydx2[:, 0] = (2 * y[:, 0] - 5 * y[:, 1] + 4 * y[:, 2] - y[:, 3]) / dx**2

        #         # Backward difference at end of array
        d2ydr2[-1, :] = (
            -y[-4, :] + 4 * y[-3, :] - 5 * y[-2, :] + 2 * y[-1, :]
        ) / dr**2
        d2ydx2[:, -1] = (
            -y[:, -4] + 4 * y[:, -3] - 5 * y[:, -2] + 2 * y[:, -1]
        ) / dx**2

        if self.tof_nf:  # trying to avoid having to make new r grids
            # Laplacian in cylindrical coordinates with axial symmetry
            return (
                (1.0 / self.wavefunction_tof_nf.three_d_grid.r) * dydr + d2ydr2 + d2ydx2
            )

        elif self.tof_ff:
            return (
                (1.0 / self.wavefunction_tof_ff.three_d_grid.r) * dydr + d2ydr2 + d2ydx2
            )
        else:
            return (1.0 / self.wavefunction.three_d_grid.r) * dydr + d2ydr2 + d2ydx2

    def get_gpe(self, psi: np.ndarray) -> np.ndarray:
        """
        Implementation of the Gross-Pitaevskii Equation w/Neumann boundary conditions at r = 0
        and Dirichlet at large x and r.
        If self.tof_nf or self.tof_ff == True, the external potential is ignored.

        Args:
            psi (ndarray): the current timestep wavefunction

        Returns:
            ndarray: wavefunction calculated by the Gross-Pitaevskii Equation

        """
        # Enforce Neumann boundary condition
        psi[1, :] = psi[0, :]

        laplacian = self.get_laplacian(psi)

        # if we are not in TOF mode we are then in in-trap mode
        if self.tof_nf | self.tof_ff:
            return (0.5 * 1j) * laplacian - 1j * (
                self.interaction_strength * np.abs(psi) ** 2
            ) * psi
        else:
            return (0.5 * 1j) * laplacian - 1j * (
                self.qm_potential.potential
                + self.interaction_strength * np.abs(psi) ** 2
            ) * psi

    def run_rk4(self, time_span: TimeSpan, stage_name: str = "") -> None:
        """
        Implementation of the Runge-Kutta 4th order method to evolve in time.
        Depends on if the simulation is in IT mode, tof_nf or tof_ff mode.

        Args:
            time_span (TimeSpan):  a list of times (in milliseconds)
            stage_name (str): name for the evolving stage. default = ""
        Returns:
            None
        """
        # TODO: Refactor: ALB-6346
        if self.tof_nf:  # toggle between IT and TOF grids
            three_d_grid = self.wavefunction_tof_nf.three_d_grid
            wavefunction = self.wavefunction_tof_nf
        elif self.tof_ff:
            three_d_grid = self.wavefunction_tof_ff.three_d_grid
            wavefunction = self.wavefunction_tof_ff
        else:
            three_d_grid = self.wavefunction.three_d_grid
            wavefunction = self.wavefunction

        n = int(
            (time_span.end - time_span.start) / self.time_step
        )  # number of sub-intervals to evaluate rk4 on.
        t = np.linspace(
            time_span.start, time_span.end, n + 1
        )  # list of all time sub-intervals

        f = np.zeros(
            (three_d_grid.Nr, three_d_grid.Nx),
            dtype=complex,
        )  # stored wave function at each time

        # Set the initial wave function
        f = wavefunction.psi

        dt = self.time_step

        # if ground = True, we evolve in imaginary time
        if self.ground:
            dt = -dt * 1j

        oqt_times_us = t * QMPotential.sim_time_to_oqt / QMPotential.msec

        for i in range(n):
            # If in IT mode, we update the potential every 100 microseconds
            if not (self.tof_nf | self.tof_ff) and i == 0:
                self.qm_potential.update_potential(t[i], self.clip)

            if (
                not (self.tof_nf | self.tof_ff)
                and i > 0
                and (
                    oqt_times_us[i] % 100 < oqt_times_us[i - 1] % 100
                    and self.ground is False
                )
            ):
                self.qm_potential.update_potential(t[i], self.clip)

            psi = wavefunction.psi

            f1 = self.get_gpe(psi)
            f2 = self.get_gpe(psi + f1 * dt / 2)
            f3 = self.get_gpe(psi + f2 * dt / 2)
            f4 = self.get_gpe(psi + f3 * dt)

            f = f + dt * (f1 + 2.0 * f2 + 2.0 * f3 + f4) / 6.0

            # Dirichlet boundary conditions at asymptotes of simulation
            f[-1, :] = 0
            f[:, 0] = 0
            f[:, -1] = 0

            # Enforce Neumann boundary condition
            f[1, :] = f[0, :]

            wavefunction.psi = f
            wavefunction.psi = wavefunction.normalize(
                wavefunction.psi
            )  # Enforce normalization
            f = wavefunction.psi

            if i % self.sampling_rate == 0:
                self.psi_history.append(f)
                self.times.append(t[i])

                if not self.hit_boundary:
                    self.is_wavefunction_at_boundary(
                        f
                    )  # check if the condensate is hitting the simulation boundary.

                if not self.ground and len(self.times) > 1:
                    oqt_time = self.times[-1] * self.qm_potential.sim_time_to_oqt
                    total_time = (
                        self.qm_potential.lifetime + self.qm_potential.time_of_flight
                    ) * self.qm_potential.sim_time_to_oqt
                    print(
                        f"simulating: {stage_name:s} {oqt_time:.3f} of {total_time:.3f}ms         ",
                        end="\r",
                    )

    def is_wavefunction_at_boundary(self, psi: np.ndarray) -> None:
        """
        Warn user if the condensate is hitting the edge of the simulation.

        Args:
            psi (ndarray): the wave function
        """
        left_x = np.abs(psi[:, 1]) ** 2  # entire left boundary
        right_x = np.abs(psi[:, -2]) ** 2  # entire right boundary
        top_r = np.abs(psi[-2, :]) ** 2  # entire top boundary in radial direction
        tol = 1e-3
        if self.tof_nf:
            tol = 1e-5
        elif self.tof_ff:
            # TODO: Get with victor to see if value too wide; ticket: ALB-6344
            tol = 1e-7

        if any(i > tol for i in left_x):
            print(
                "Condensate hit left boundary at time:  ",
                self.times[-1] * self.qm_potential.sim_time_to_oqt,
            )
            self.hit_boundary = True
        if any(i > tol for i in right_x):
            print(
                "Condensate hit right boundary at time:  ",
                self.times[-1] * self.qm_potential.sim_time_to_oqt,
            )
            self.hit_boundary = True
        if any(i > tol for i in top_r):  # are any of the densities larger than tol?
            print(
                "Condensate hit top boundary at time:  ",
                self.times[-1] * self.qm_potential.sim_time_to_oqt,
            )
            self.hit_boundary = True

    @property
    def it_plot(self) -> dict:
        """
        Generate a simulation analog to an in-trap image from the Oqtant hardware.

        Returns:
            dict: data for generating an Image object(pixels, pixcal, rows, columns)
        """

        wavefunction = self.which_wavefunction_mode(self.times[-1])
        wavefunction.psi = self.psi_history[-1]  # we display the final result only

        # get the Y-integrated column denisty from wavefunction number / simulation area
        _, density_pixels, _ = wavefunction.column_densities

        density_pixels = (
            density_pixels.flatten()
            * wavefunction.three_d_grid.dx
            * wavefunction.three_d_grid.dz
        )

        # get conversion from simulation length to um
        pixcal = QMPotential.sim_length_to_oqt

        a_pixel_area = (
            pixcal**2 * wavefunction.three_d_grid.dz * wavefunction.three_d_grid.dx
        )  # * (pixcal) ** 2  # um2

        it_exp_pixcal = 0.344  # um

        # resonant cross section, D2 line, pi polarized light
        # REF: https://steck.us/alkalidata/rubidium87numbers.1.6.pdf
        sigma = 1.938e-1  # um2

        # convert density (atoms/length^2) to OD using the sim grid size and cross-section
        od_pixels = density_pixels * sigma * self.number_of_atoms / a_pixel_area

        # apply experimental imaging scaling to OD image
        # this is the average ratio between the number of atoms in experimental IT images vs TOF images
        # for heartbeat jobs due to inefficiencies in detection (i.e. magnetic field during imaging)
        # this necessarily destroys the atom number information in simulator generated OD images

        od_pixels *= self.EXPERIMENT_IT_TOF_OD_RATIO

        # half the length of the simulation grid axes, in um
        lx_half = (wavefunction.three_d_grid.Lx / 2) * pixcal
        ly_half = wavefunction.three_d_grid.Lr * pixcal

        # grids for building simulation interpolation function (um)
        sim_grid_col = np.linspace(-lx_half, lx_half, wavefunction.three_d_grid.Nx)
        sim_grid_row = np.linspace(-ly_half, ly_half, wavefunction.three_d_grid.Nr * 2)

        # build interpolation function for sim data
        f = interpolate.RegularGridInterpolator(
            (sim_grid_row, sim_grid_col),
            od_pixels.reshape(
                (wavefunction.three_d_grid.Nr * 2, wavefunction.three_d_grid.Nx)
            ),
        )

        # grids for sampling simulation in experiment resolution (um)
        exp_grid_col = np.arange(-lx_half, lx_half, it_exp_pixcal)
        exp_grid_row = np.arange(-ly_half, ly_half, it_exp_pixcal)

        exp_meshgrid_row, exp_meshgrid_col = np.meshgrid(exp_grid_row, exp_grid_col)

        points = np.array([exp_meshgrid_row.flatten(), exp_meshgrid_col.flatten()]).T

        # sample the interpolation function and reshape the output
        interpolated_sim = f(points).reshape(len(exp_grid_col), len(exp_grid_row))

        # how many pixels to pad the image?
        add_zeros_rows = math.ceil((148 - len(exp_grid_row)) / 2)
        add_zeros_cols = math.ceil((512 - len(exp_grid_col)) / 2)

        # pad the image to match IT_PLOT size
        padded_interp_sim = np.pad(
            interpolated_sim,
            [
                [add_zeros_cols, 512 - len(exp_grid_col) - add_zeros_cols],
                [add_zeros_rows, 148 - len(exp_grid_row) - add_zeros_rows],
            ],
        ).T

        # prepare values to be returned
        columns = len(padded_interp_sim[0])
        rows = len(padded_interp_sim)
        pixels_pad_interp_sim = list(padded_interp_sim.flatten())

        return {
            "it_plot": {
                "pixels": pixels_pad_interp_sim,
                "rows": rows,
                "columns": columns,
                "pixcal": it_exp_pixcal,
            }
        }

    @property
    def tof_output(self) -> dict:
        """
        Generate an simulation analog to a TOF image from the Oqtant hardware.

        Returns:
            dict: data for generating an Image object(pixels, pixcal, rows, columns)
        """

        # TODO refactor See; ALB-6345

        wavefunction = self.which_wavefunction_mode(self.times[-1])

        # generate and fit tof image with output class TF_dist_2D
        tof_exp_pixcal = 4.4  # um

        # get the Y-integrated column denisty from wavefunction number / simulation area
        _, density_pixels, _ = wavefunction.column_densities

        density_pixels = (
            density_pixels * wavefunction.three_d_grid.dx * wavefunction.three_d_grid.dz
        )

        # get conversion from simulation length to um
        pixcal = QMPotential.sim_length_to_oqt

        a_pixel_area = (
            pixcal**2 * wavefunction.three_d_grid.dz * wavefunction.three_d_grid.dx
        )  # um2

        # This sigma is sued for mF=2 -> mF=3; polarized light absorption cross-section
        # Ref: https://steck.us/alkalidata/rubidium87numbers.1.6.pdf
        sigma = 2.907e-1  # um2

        # convert density (atoms/length^2) to OD using the sim grid size and cross-section
        od_pixels = density_pixels * sigma * self.number_of_atoms / a_pixel_area

        int(len(od_pixels) / 2)
        int(len(od_pixels[0]) / 2)

        # half the length of the simulation grid axes, in um
        lx_half = (wavefunction.three_d_grid.Lx / 2) * pixcal
        lz_half = wavefunction.three_d_grid.Lr * pixcal

        # grids for building simulation interpolation function (um)
        sim_grid_col = np.linspace(-lx_half, lx_half, wavefunction.three_d_grid.Nx)
        sim_grid_row = np.linspace(-lz_half, lz_half, wavefunction.three_d_grid.Nr * 2)

        # build interpolation function for sim data
        f = interpolate.RegularGridInterpolator(
            (sim_grid_row, sim_grid_col),
            od_pixels,
            bounds_error=False,
            fill_value=0,
        )

        exp_grid_col = np.arange(
            -50 * tof_exp_pixcal, 50 * tof_exp_pixcal, tof_exp_pixcal
        )
        exp_grid_row = np.arange(
            -50 * tof_exp_pixcal, 50 * tof_exp_pixcal, tof_exp_pixcal
        )

        exp_meshgrid_row, exp_meshgrid_col = np.meshgrid(exp_grid_row, exp_grid_col)

        points = np.array([exp_meshgrid_row.flatten(), exp_meshgrid_col.flatten()]).T

        # sample the interpolation function and reshape the output
        interpolated_sim = f(points).reshape(len(exp_grid_col), len(exp_grid_row))

        # how many pixels to pad the image?
        add_zeros_rows = math.ceil((100 - len(exp_grid_row)) / 2)
        add_zeros_cols = math.ceil((100 - len(exp_grid_col)) / 2)

        # pad the image to match IT_PLOT size
        padded_interp_sim = np.pad(
            interpolated_sim,
            [
                [add_zeros_cols, 100 - len(exp_grid_col) - add_zeros_cols],
                [add_zeros_rows, 100 - len(exp_grid_row) - add_zeros_rows],
            ],
        ).T

        # prepare values to be returned
        columns = len(padded_interp_sim[0])
        rows = len(padded_interp_sim)
        pixels_interp_sim = list(padded_interp_sim.flatten())

        tof_image = Image(
            pixels=pixels_interp_sim,
            rows=rows,
            columns=columns,
            pixcal=tof_exp_pixcal,
        )

        x_points = padded_interp_sim[50]
        y_points = np.array(padded_interp_sim).T[50]

        d = []

        for i in range(100):
            d.append({"x": x_points[i], "y": y_points[i]})

        tof_x_slice = LineChart(points=d)
        tof_y_slice = LineChart(points=d)

        dummy_img = Image(
            pixels=[0 for i in range(100 * 100)], rows=2, columns=2, pixcal=1
        )

        dummy_fit = {
            "gaussian_od": 0,
            "gaussian_sigma_x": 0,
            "gaussian_sigma_y": 0,
            "tf_od": 0,
            "tf_x": 0,
            "tf_y": 0,
            "x_0": 0,
            "y_0": 0,
            "offset": 0,
        }

        output_dict = {
            "tof_image": tof_image,
            "tof_x_slice": tof_x_slice,
            "tof_y_slice": tof_y_slice,
            "mot_fluorescence_image": dummy_img,
            "tof_fit_image": dummy_img,
            "tof_fit": dummy_fit,
            "total_mot_atom_number": 0,
            "tof_atom_number": 0,
            "thermal_atom_number": 0,
            "condensed_atom_number": self.number_of_atoms,
            "temperature_nk": 0,
        }

        return output_dict

    def is_time_intrap(self, time: float) -> bool:
        """
        Checks if the time is when the condensate is still in trap.

        Args:
            time (float):   time in simulation units.
        Returns:
            Bool:  True means the system is in IT mode at that time.  False means it is not (it is in TOF mode).
        """
        test = time < self.qm_potential.lifetime
        if self.qm_potential.lifetime == 0.0:  # <-------------
            test = True  # edge case for lifetime = 0

        return test

    def is_time_near_field(self, time: float) -> bool:
        """
        Checks if the time is when the condensate is in near-field part of TOF.

        Args:
            time (float):   time in simulation (!) units.
        Returns:
            Bool:  True means the system is in NF of TOF mode at that time.
        """

        return (
            self.max_NF_time + self.qm_potential.lifetime
            > time
            >= self.qm_potential.lifetime
        )

    def is_time_far_field(self, time: float) -> bool:
        """
        Checks if the time is when the condensate is in far-field part of TOF.

        Args:
            time (float):   time in simulation (!) units.
        Returns:
            Bool:  True means the system is in FF of TOF mode at that time.
        """

        return time >= self.qm_potential.lifetime + self.max_NF_time

    def which_wavefunction_mode(self, time: float) -> WaveFunction:
        """
        Checks which mode the time corresponds to and returns the correct wavefunction class.

        Args:
            time (float):   time in simulation (!) units.
        Returns:
            WaveFunction:  instance of the wavefunction class in the correct mode
        """
        # checks which mode the simulator is in at that time.
        if self.is_time_intrap(time):
            wavefunction = self.wavefunction
            # update the potential to correct value in trap.
            self.qm_potential.update_potential(time)

        elif self.is_time_near_field(time):
            wavefunction = self.wavefunction_tof_nf

        elif self.is_time_far_field(time):
            wavefunction = self.wavefunction_tof_ff

        else:
            print("No wavefunction found for the requested timestep")
            raise ValueError("No wavefunction found for the requested timestep")

        return wavefunction

    def show_final_result(self) -> None:
        """
        Plot the density at the end of the simulation in cylindrical coordinates.
        Useful coordinates for diagonising issues but not to be returned to the user.
        """

        wavefunction = self.which_wavefunction_mode(self.times[-1])
        wavefunction.psi = self.psi_history[-1]  # we display the final result only

        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        density = (
            wavefunction.density / QMPotential.sim_length_to_oqt**3
        )  # atoms / micron^3
        ax.plot_surface(
            self.qm_potential.sim_length_to_oqt * wavefunction.three_d_grid.r,
            self.qm_potential.sim_length_to_oqt * wavefunction.three_d_grid.x,
            density,
            cmap="viridis",
        )
        plt.title("Density (Atoms/$\\mu$m$^3$) at final time")
        ax.set_xlabel("$R$-Position ($\\mu$m)")
        ax.set_ylabel("$X$-Position ($\\mu$m)")

    def convert_timesteps(self, timesteps: list) -> np.ndarray:
        """
        Convert a list of arbitrary times (in oqtant units) to a list of simulator timestep indices.
        Simulation must already have been evaluated.

        Args:
            timesteps (list): list of times in oqtant units

        Returns:
            ndarray : array of simulator timestep indexes (not the values of the timesteps)

        """

        if self.times is None:
            raise SimValueError("times not set")

        np.ceil(QMPotential.sim_time_to_oqt * self.qm_potential.lifetime)
        np.ceil(
            QMPotential.sim_time_to_oqt
            * (self.qm_potential.lifetime + self.max_NF_time)
        )

        time_end_oqt = np.ceil(
            QMPotential.sim_time_to_oqt
            * (self.qm_potential.time_of_flight + self.qm_potential.lifetime)
        )
        last_timestep_idx = self.times[-1]

        np_timesteps = np.array(timesteps, dtype=float)
        # convert input time in msec to simulation units
        np_timesteps *= QMPotential.oqt_time_to_sim

        # if the user has requested the end time of the simulation exactly, adjust this to the last saved timestep

        for i in range(len(timesteps)):
            oqt_time = timesteps[i]
            if oqt_time == time_end_oqt:
                np_timesteps[i] = last_timestep_idx

        if (
            np.max(np_timesteps) > self.times[-1]
            or np.min(np_timesteps) < self.times[0]
        ):
            raise SimValueError("timesteps outside of job window")

        if np.min(np_timesteps) < 0:
            raise SimValueError("timesteps must be positive")

        return np_timesteps

    def get_grids(self, time_ms: float) -> tuple:
        """
        Returns the x-grid in microns at a user specified time.

        Args:
            time_ms (float):  time (in milliseconds)
        Returns:
            tuple (dx, Lx, x_1d) : the simulation resolution, length in x-direction, and length array in x-direction
        """
        [sim_time] = self.convert_timesteps([time_ms])

        i = np.searchsorted(self.times, sim_time, side="left", sorter=None)

        wavefunction = self.which_wavefunction_mode(self.times[i])
        wavefunction.psi = self.psi_history[i]  # load a snapshot of psi

        oqt_length = self.qm_potential.sim_length_to_oqt
        Lx = wavefunction.three_d_grid.Lx * oqt_length
        x_1d = wavefunction.three_d_grid.x_1d * oqt_length
        dx = wavefunction.three_d_grid.dx * oqt_length

        return dx, Lx, x_1d

    def get_times(self):
        """
        Returns the an array of  times in oqtant units

        Returns:
            array times : the timesteps in oqtant units (milliseconds)
        """
        times = np.array(self.times) * self.qm_potential.sim_time_to_oqt

        return times

    def get_column_densities(self, time_ms: float) -> tuple:
        """
        Returns the column densities and slices of the condensate in cartesian coordinates
        for an arbitrary time.
        In correct coordinates to be returned to the user.

        Args:
            time_ms (float):  time (in milliseconds)
        Returns:
            tuple (column_zy, column_zx, slice_y, slice_x) : the column densitites and slices at the desired time
        """
        [sim_time] = self.convert_timesteps([time_ms])

        i = np.searchsorted(self.times, sim_time, side="left", sorter=None)

        wavefunction = self.which_wavefunction_mode(self.times[i])
        wavefunction.psi = self.psi_history[i]  # load a snapshot of psi

        # load the column densities
        (
            column_zy,
            column_zx,
            profiles,
        ) = wavefunction.column_densities

        column_zy *= self.number_of_atoms
        column_zx *= self.number_of_atoms

        slice_x = column_zx[int(wavefunction.three_d_grid.Nr - 1), :]
        slice_y = column_zy[int(wavefunction.three_d_grid.Nr - 1), :]

        return column_zy, column_zx, slice_y, slice_x

    def show_density_cylindrical(self, times_ms: list, figsize=(15, 7)) -> None:
        """
        Plots the density profile of the condensate in cylindrical coordinates
        for an input array of times.
        Useful coordinates for diagonising issues but not to be returned to the user.

        Args:
            times_ms (list):  a list of times (in milliseconds/oqtant units)
            figsize (tuple): size of output figure. default = (15,7)
        Returns:
            None
        """
        # convert into simulation times
        converted_timesteps = self.convert_timesteps(times_ms)

        # convert to simulation indices for the nearest timestep, loop over timesteps
        for time in converted_timesteps:
            i = np.searchsorted(self.times, time, side="left", sorter=None)

            wavefunction = self.which_wavefunction_mode(self.times[i])
            fig = plt.figure(figsize=figsize)

            # Add first subplot in a plot with two rows and 2 columns.
            ax1 = fig.add_subplot(111)
            wavefunction.psi = self.psi_history[i]
            density = (
                wavefunction.density
                * self.number_of_atoms
                / QMPotential.sim_length_to_oqt**3
            )  # atoms / micron^3
            img1 = ax1.imshow(
                np.concatenate(
                    (np.flip(density, axis=0), density)
                ),  # mirror the condensate over the z-axis
                extent=[
                    wavefunction.three_d_grid.x[0, 0]
                    * self.qm_potential.sim_length_to_oqt,
                    wavefunction.three_d_grid.x[0, -1]
                    * self.qm_potential.sim_length_to_oqt,
                    -wavefunction.three_d_grid.r[-1, 0]
                    * self.qm_potential.sim_length_to_oqt,
                    wavefunction.three_d_grid.r[-1, 0]
                    * self.qm_potential.sim_length_to_oqt,
                ],
                aspect="auto",
                cmap="viridis",
            )
            oqt_time = self.times[i] * self.qm_potential.sim_time_to_oqt
            plt.title("Density (Atoms/$\\mu$m$^3$) at t = %.2f ms" % oqt_time)
            ax1.set_xlabel("$X$-Position ($\\mu$m)")
            ax1.set_ylabel("$R$-Position ($\\mu$m)")
            fig.colorbar(img1, ax=ax1, orientation="vertical")

    def show_column_densities(
        self, times_ms: list, slices: bool = True, figsize=(15, 7)
    ):
        """
        Plots the column densities and slices of the condensate in cartesian coordinates
        for an input array of times.
        In correct coordinates to be returned to the user.

        Args:
            times_ms (list):  a list of times (in milliseconds)
            slices (bool): plot or not to plot slices
            figsize (tuple): size of output figure. default = (15,7)
        Returns:
            None
        """
        converted_timesteps = self.convert_timesteps(times_ms)

        for time in converted_timesteps:

            i = np.searchsorted(self.times, time, side="left", sorter=None)
            wavefunction = self.which_wavefunction_mode(self.times[i])

            wavefunction.psi = self.psi_history[i]  # load a snapshot of psi

            # load the column densities
            (
                column_zy,
                column_zx,
                profiles,
            ) = wavefunction.column_densities
            slice_x_2 = column_zx[int(wavefunction.three_d_grid.Nr - 1), :]
            slice_z = column_zy[int(wavefunction.three_d_grid.Nr - 1), :]
            slice_z_zy, slice_z_zx, slice_x = profiles

            fig = plt.figure(figsize=figsize)

            # column densities
            # Add first subplot in a plot with two rows and 2 columns.
            ax1 = fig.add_subplot(221)
            im1 = ax1.imshow(
                self.number_of_atoms
                * column_zy
                / QMPotential.sim_length_to_oqt**2,  # atoms / micron^2,
                extent=[
                    -wavefunction.three_d_grid.Lr * self.qm_potential.sim_length_to_oqt,
                    wavefunction.three_d_grid.Lr * self.qm_potential.sim_length_to_oqt,
                    -wavefunction.three_d_grid.Lr * self.qm_potential.sim_length_to_oqt,
                    wavefunction.three_d_grid.Lr * self.qm_potential.sim_length_to_oqt,
                ],
                aspect="auto",
                cmap="viridis",
            )
            oqt_time = self.times[i] * self.qm_potential.sim_time_to_oqt
            plt.title("Column densities at t = %.2f ms" % oqt_time)
            plt.xlabel("$Y$-Position ($\\mu$m)")
            plt.ylabel("$Z$-Position ($\\mu$m)")
            cbar1 = fig.colorbar(im1, ax=ax1, orientation="vertical")
            cbar1.ax.set_ylabel("Density (Atoms/$\\mu$m$^2$)")

            ax2 = fig.add_subplot(222)
            im2 = ax2.imshow(
                self.number_of_atoms
                * column_zx
                / QMPotential.sim_length_to_oqt**2,  # atoms / micron^2,
                extent=[
                    -self.qm_potential.sim_length_to_oqt
                    * wavefunction.three_d_grid.Lx
                    / 2,
                    self.qm_potential.sim_length_to_oqt
                    * wavefunction.three_d_grid.Lx
                    / 2,
                    -self.qm_potential.sim_length_to_oqt * wavefunction.three_d_grid.Lr,
                    self.qm_potential.sim_length_to_oqt * wavefunction.three_d_grid.Lr,
                ],
                aspect="auto",
                cmap="viridis",
            )
            plt.xlabel("$X$-Position ($\\mu$m)")
            plt.ylabel("$Z$-Position ($\\mu$m)")
            cbar2 = fig.colorbar(im2, ax=ax2, orientation="vertical")
            cbar2.ax.set_ylabel("Density (Atoms/$\\mu$m$^2$)")

            # slices
            if slices:
                ax3 = fig.add_subplot(223)
                pos1 = ax1.get_position()
                pos3 = ax3.get_position()

                ax3.plot(
                    wavefunction.three_d_grid.z[0, :]
                    * self.qm_potential.sim_length_to_oqt,
                    self.number_of_atoms
                    * slice_z
                    / QMPotential.sim_length_to_oqt,  # atoms / micron
                )
                plt.title("Slices at t = %.2f ms" % oqt_time)
                ax3.set_xlabel("$Z$-Position ($\\mu$m)")
                ax3.set_ylabel("Density (Atoms/$\\mu$m)")
                ax3.set_position([pos1.x0, pos3.y0 * 0.5, pos1.width, pos3.height])

                #
                ax4 = fig.add_subplot(224)
                pos2 = ax2.get_position()
                pos4 = ax4.get_position()

                ax4.plot(
                    wavefunction.three_d_grid.x[0, :]
                    * self.qm_potential.sim_length_to_oqt,
                    self.number_of_atoms
                    * slice_x_2
                    / QMPotential.sim_length_to_oqt,  # atoms / micron,
                )
                ax4.set_xlabel("$X$-Position ($\\mu$m)")
                ax4.set_ylabel("Density (Atoms/$\\mu$m)")
                ax4.set_position([pos2.x0, pos4.y0 * 0.5, pos2.width, pos4.height])

            plt.show()

    def show_phase(self, times_ms: list, figsize=(10, 7)) -> None:
        """
        Plot the phase for a given list of timesteps
        This can only be displayed in cylindrical coordinates.
        It is a helpful tool still for the user.  The aspect ratio is still a bit weird.

        Args:
            times_ms (list): List of times to display
            figsize (tuple): size of output figure. default = (10,7)
        Returns:
            None
        """
        converted_timesteps = self.convert_timesteps(times_ms)

        for time in converted_timesteps:
            # convert to simulation indices for the nearest timestep, loop over timesteps
            i = np.searchsorted(self.times, time, side="left", sorter=None)

            wavefunction = self.which_wavefunction_mode(self.times[i])

            wavefunction.psi = self.psi_history[i]

            plt.figure(figsize=figsize)
            plt.imshow(
                np.concatenate(
                    (np.flip(wavefunction.phase, axis=0), wavefunction.phase)
                ),  # needs to be flipped to plot x on x axis and r on y axis.
                extent=[
                    wavefunction.three_d_grid.x[0, 0]
                    * self.qm_potential.sim_length_to_oqt,
                    wavefunction.three_d_grid.x[0, -1]
                    * self.qm_potential.sim_length_to_oqt,
                    -wavefunction.three_d_grid.r[-1, 0]
                    * self.qm_potential.sim_length_to_oqt,
                    wavefunction.three_d_grid.r[-1, 0]
                    * self.qm_potential.sim_length_to_oqt,
                ],
                aspect="auto",
                cmap="RdYlBu",
            )
            plt.colorbar(label="Phase (Radians)")
            plt.clim(-np.pi, np.pi)
            oqt_time = self.times[i] * self.qm_potential.sim_time_to_oqt
            plt.title("Phase at t = %.2f ms" % oqt_time)
            plt.xlabel("$X$-Position ($\\mu$m)")
            plt.ylabel("$R$-Position ($\\mu$m)")
            plt.show()

    def show_current(self, times_ms: list, figsize=(10, 7)) -> None:
        """
        Plot the flow for a given list of timesteps
        two separate subplots

        Args:
            times_ms (list): List of times (ms) at which to display current
            figsize (tuple): size of output figure. default = (10,7)

        Returns:
            None
        """
        converted_timesteps = self.convert_timesteps(times_ms)

        for time in converted_timesteps:
            i = np.searchsorted(self.times, time, side="left", sorter=None)

            wavefunction = self.which_wavefunction_mode(self.times[i])
            wavefunction.psi = self.psi_history[i]

            plt.figure(1, figsize=figsize)
            plt.plot(
                wavefunction.three_d_grid.x_1d * self.qm_potential.sim_length_to_oqt,
                self.number_of_atoms
                * wavefunction.current
                / self.qm_potential.sim_time_to_oqt,
            )
            oqt_time = self.times[i] * self.qm_potential.sim_time_to_oqt
            plt.title("Current at t = %.2f ms" % oqt_time)
            plt.xlabel("$X$-Position ($\\mu$m)")
            plt.ylabel("Atom Current (# of Atoms / msec)")
            plt.show()

    def animate_current(
        self, frame_interval: int = 1, y_limit=number_of_atoms
    ) -> FuncAnimation:
        """
        Animates the density profiles and change in potentials over time.  This is an integrated profile along
        the x-direction and is different from a single slice.
        Args:
            frame_interval (int): number of frames to skip each interval, determines smoothness. default =1
            current_bound (float):  adjustable bound on the y-axis in the case that the current exceeds the default.
        Returns:
            FuncAnimation: an animation of the profile along the x-direction.
        """
        fig, ax1 = plt.subplots(1, 1)

        self.wavefunction.psi = self.psi_history[0]

        (line1,) = ax1.plot([], [], lw=2, color="b", label="Atom Current - X")
        line = [line1]

        ax1.set_ylim(-y_limit, y_limit)
        ax1.set_xlim(
            -QMPotential.sim_length_to_oqt * self.wavefunction.three_d_grid.Lx / 2,
            QMPotential.sim_length_to_oqt * self.wavefunction.three_d_grid.Lx / 2,
        )

        ax1.grid()
        ax1.legend(loc="upper right")
        ax1.set_xlabel("$X$ ($\\mu$m)")
        ax1.set_ylabel("Atom Current (# of Atoms / msec)")
        fig.suptitle("t = 0 ms", x=0.5, y=0.85)

        fig.tight_layout()
        plt.close()

        def init_animation():
            """Callable for matplotlib used for initializing animation"""

            line[0].set_data([], [])
            return line

        def update(frame):
            """Callable for matplotlib used for updating the wf through the animation."""
            self.qm_potential.update_potential(self.times[frame])
            self.wavefunction.psi = self.psi_history[frame]

            current = (
                self.number_of_atoms
                * self.wavefunction.current
                / self.qm_potential.sim_time_to_oqt
            )

            x1 = (
                self.wavefunction.three_d_grid.x[0]
                * self.qm_potential.sim_length_to_oqt
            )
            y1 = current

            oqt_time = self.times[frame] * self.qm_potential.sim_time_to_oqt
            fig.suptitle("t = %.2f ms" % oqt_time, x=0.5, y=0.85)

            line[0].set_data(x1, y1)
            return (line,)

        anim = FuncAnimation(
            fig,
            update,
            init_func=init_animation,
            frames=range(0, self.last_it_time_idx, frame_interval),
            interval=50 + 100 * frame_interval,
            blit=False,
        )

        return anim

    def animate_phase(
        self, frame_interval: int = 1, show_potential: bool = True, figsize=(8, 3)
    ):
        """
        Animate the change in phase

        Args:
            frame_interval (int): number of frames to skip each interval, determines smoothness. default =1
            show_potential (bool): whether or not to show the potential on the animation. default = True
            figsize (tuple): size of the output figure. default = (8,3)

        Returns:
            FuncAnimation: an animation of the profile along the x-direction.
        """
        fig, ax = plt.subplots(figsize=figsize)

        self.qm_potential.update_potential(self.times[0])
        self.wavefunction.psi = self.psi_history[0]

        phase = self.wavefunction.phase

        extent = [
            self.wavefunction.three_d_grid.x[0, 0]
            * self.qm_potential.sim_length_to_oqt,
            self.wavefunction.three_d_grid.x[0, -1]
            * self.qm_potential.sim_length_to_oqt,
            -self.wavefunction.three_d_grid.r[-1, 0]
            * self.qm_potential.sim_length_to_oqt,
            self.wavefunction.three_d_grid.r[-1, 0]
            * self.qm_potential.sim_length_to_oqt,
        ]
        im = ax.imshow(
            np.concatenate((np.flip(phase, axis=0), phase)),
            extent=extent,
            vmin=-np.pi,
            vmax=np.pi,
            cmap="RdYlBu",
        )

        if show_potential:
            cont1 = ax.contour(
                self.wavefunction.three_d_grid.x_1d
                * self.qm_potential.sim_length_to_oqt,
                np.concatenate(
                    (
                        -np.flip(self.wavefunction.three_d_grid.r_1d, axis=0),
                        self.wavefunction.three_d_grid.r_1d,
                    )
                )
                * self.qm_potential.sim_length_to_oqt,
                self.qm_potential.potential_to_cartesian_oqt_units(),
                colors="white",
            )

        ax.set_xlabel("X (um)")
        ax.set_ylabel("R (um)")
        fig.suptitle("t = 0 ms", x=0.5, y=0.85)
        plt.colorbar(im, ax=ax, label="Phase (Radians)")
        plt.close()

        def update(frame):
            if show_potential:
                nonlocal cont1
                for c in cont1.collections:
                    c.remove()
            self.qm_potential.update_potential(self.times[frame])
            self.wavefunction.psi = self.psi_history[frame]
            phase = self.wavefunction.phase
            im.set_array(np.concatenate((np.flip(phase, axis=0), phase)))
            oqt_time = self.times[frame] * self.qm_potential.sim_time_to_oqt
            fig.suptitle("t = %.2f ms" % oqt_time, x=0.5, y=0.85)
            cont1 = ax.contour(
                self.wavefunction.three_d_grid.x_1d
                * self.qm_potential.sim_length_to_oqt,
                np.concatenate(
                    (
                        -np.flip(self.wavefunction.three_d_grid.r_1d, axis=0),
                        self.wavefunction.three_d_grid.r_1d,
                    )
                )
                * self.qm_potential.sim_length_to_oqt,
                self.qm_potential.potential_to_cartesian_oqt_units(),
                colors="white",
            )

            if show_potential:
                return im, cont1
            return im

        anim = FuncAnimation(
            fig,
            update,
            frames=range(0, self.last_it_time_idx, frame_interval),
            interval=50 + 100 * frame_interval,
            blit=False,
        )

        return anim

    def animate_density(self, frame_interval=1, figsize=(8, 3), show_potential=True):
        """
        Animates the change in density and potential over time

        Args:
            frame_interval (int): number of frames to skip each interval, determines smoothness. default = 1
            show_potential (bool): whether or not to show the potential on the animation. default = True
            figsize (tuple): size of the output figure. default = (8,3)

        Returns:
            FuncAnimation: an animation of the profile along the x-direction.

        """
        fig, ax = plt.subplots(figsize=(figsize))

        wavefunction = self.wavefunction

        _, density, _ = wavefunction.column_densities

        extent = [
            wavefunction.three_d_grid.x[0, 0] * self.qm_potential.sim_length_to_oqt,
            wavefunction.three_d_grid.x[0, -1] * self.qm_potential.sim_length_to_oqt,
            -wavefunction.three_d_grid.y[-1, 0] * self.qm_potential.sim_length_to_oqt,
            wavefunction.three_d_grid.y[-1, 0] * self.qm_potential.sim_length_to_oqt,
        ]

        # vmin and vmax normalize the colorbar, making the cloud more visible
        im = ax.imshow(
            self.number_of_atoms
            * density
            / QMPotential.sim_length_to_oqt**2,  # atoms / micron^2,
            extent=extent,
            cmap="viridis",
        )  # normalize in here with vmin and vmax
        if show_potential:
            cont1 = ax.contour(
                wavefunction.three_d_grid.x_1d * self.qm_potential.sim_length_to_oqt,
                np.concatenate(
                    (
                        -np.flip(wavefunction.three_d_grid.r_1d, axis=0),
                        wavefunction.three_d_grid.r_1d,
                    )
                )
                * self.qm_potential.sim_length_to_oqt,
                self.qm_potential.potential_to_cartesian_oqt_units(),
                colors="white",
            )

        ax.set_xlabel("X (um)")
        ax.set_ylabel("Y (um)")
        fig.suptitle("t = 0 ms", x=0.5, y=0.85)

        plt.colorbar(im, ax=ax, label="Density (Atoms/$\\mu$m$^2$)")
        plt.close()

        def update(frame):
            self.qm_potential.update_potential(self.times[frame])
            wavefunction.psi = self.psi_history[frame]
            _, density, _ = wavefunction.column_densities
            im.set_array(
                self.number_of_atoms * density / QMPotential.sim_length_to_oqt**2
            )  # atoms / micron^2)
            oqt_time = self.times[frame] * self.qm_potential.sim_time_to_oqt
            fig.suptitle("t = %.2f ms" % oqt_time, x=0.5, y=0.85)
            if show_potential:
                nonlocal cont1
                for c in cont1.collections:
                    c.remove()
                cont1 = ax.contour(
                    wavefunction.three_d_grid.x_1d
                    * self.qm_potential.sim_length_to_oqt,
                    np.concatenate(
                        (
                            -np.flip(wavefunction.three_d_grid.r_1d, axis=0),
                            wavefunction.three_d_grid.r_1d,
                        )
                    )
                    * self.qm_potential.sim_length_to_oqt,
                    self.qm_potential.potential_to_cartesian_oqt_units(),
                    colors="white",
                )

            if show_potential:
                return im, cont1  # , cont2, cont3, cont4
            else:
                return im

        anim = FuncAnimation(
            fig,
            update,
            frames=range(0, self.last_it_time_idx, frame_interval),
            interval=50 + 100 * frame_interval,
            blit=False,
        )

        return anim

    def animate_profiles(
        self,
        frame_interval=1,
        y_limit=number_of_atoms / (QMPotential.sim_length_to_oqt * 5),
    ):
        """
        Animates the density profiles and change in potentials over time.  This is an integrated profile along
        the x-direction and is different from a single slice(!).

        Args:
            frame_interval (int): number of frames to skip each interval, determines smoothness. default = 1
            y_axis (float):  optional arguement to adjust the y-axis in the event that the density is to large.

        Returns:
            FuncAnimation: an animation of the profile along the x-direction.

        """
        fig, ax1 = plt.subplots(1, 1)

        self.wavefunction.psi = self.psi_history[0]

        profile_x, _ = self.wavefunction.density_profiles

        (line1,) = ax1.plot([], [], lw=2, color="b", label="Density Profile - X")
        line = [line1]

        ax1.set_ylim(0, y_limit)
        ax1.set_xlim(
            -QMPotential.sim_length_to_oqt * self.wavefunction.three_d_grid.Lx / 2,
            QMPotential.sim_length_to_oqt * self.wavefunction.three_d_grid.Lx / 2,
        )

        ax1.grid()
        ax1.legend(loc="upper right")
        ax1.set_xlabel("X (um)")
        ax1.set_ylabel("Density (Atoms/$\\mu$m$^2$)")
        fig.suptitle("t = 0 ms", x=0.5, y=0.85)

        fig.tight_layout()
        plt.close()

        def init_animation():
            """Callable for matplotlib used for initializing animation"""
            line[0].set_data([], [])
            return line

        def update(frame):
            """Callable for matplotlib used for updating the wf through the animation."""
            self.qm_potential.update_potential(self.times[frame])
            self.wavefunction.psi = self.psi_history[frame]

            profile_x, _ = self.wavefunction.density_profiles

            oqt_time = self.times[frame] * self.qm_potential.sim_time_to_oqt
            fig.suptitle("t = %.2f ms" % oqt_time, x=0.5, y=0.85)

            x1 = (
                self.wavefunction.three_d_grid.x[0]
                * self.qm_potential.sim_length_to_oqt
            )

            y1 = self.number_of_atoms * profile_x / QMPotential.sim_length_to_oqt

            line[0].set_data(x1, y1)
            return (line,)

        anim = FuncAnimation(
            fig,
            update,
            init_func=init_animation,
            frames=range(0, self.last_it_time_idx, frame_interval),
            interval=50 + 100 * frame_interval,
            blit=False,
        )

        return anim
