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
from scipy.interpolate import RectBivariateSpline, interp1d

from oqtant.simulator.three_dim import ThreeDimGrid


class WaveFunction:
    """
    'WaveFunction' Defines representation for a wavefunction
    It is sensitive to whether the system is in Time of Flight (TOF) or In Trap (IT) mode
    """

    def __init__(self, tof_nf: bool = False, tof_ff: bool = False):
        """
        Initializes a wavefuntion in Time of Flight Near Field (tof_nf) or Time of Flight Far Field (tof_ff)
        Args:
            tof_nf: Indicates if WaveFunction uses Time of Flight (TOF) Near field
            tof_ff: Indicates if WaveFunction uses TOF Far Field
        """
        self.three_d_grid = ThreeDimGrid(tof_nf=tof_nf, tof_ff=tof_ff)
        initial_psi = self.initial_psi().astype(complex)
        self.psi = self.normalize(initial_psi)

    def initial_psi(self, sigma_x: int = 1, sigma_r: int = 1) -> np.ndarray:
        """
        Defines the initial wave function of the system with
        controllable widths.

        Args:
            sigma_x (int):  width in the x direction
            sigma_r (int):  width in the r direction

        Returns:
            psi np.ndarray:  initial wave function

        """
        if sigma_x < 0 or sigma_r < 0:
            raise ValueError("Wavefunction: sigma_x and sigma_r must be non-negative")

        init_x = np.exp(-(self.three_d_grid.x**2) / (2 * sigma_x**2))
        init_r = np.exp(-(self.three_d_grid.r**2) / (2 * sigma_r**2))

        return init_x * init_r

    def normalize(self, psi: np.ndarray) -> np.ndarray:
        """
        Normalizes the wave function to the number of atoms
        Applies normalization directly to psi. This feels wonky as psi is a member of the
        Wavefunction class, however in the runge-kutta method we advance psi without saving to the
        wavefunction so we need to be able to normalize a passed in psi. We just have to assume the psi passed
        in maintains the same coordinates as the psi in the wavefunction.

        Args:
            psi (np.ndarray):  wavefunction

        Returns:
            normalized np.ndarray
        """
        if not isinstance(psi, np.ndarray):
            raise TypeError("Wavefunction: psi must be a ndarray to normalize")

        if psi.shape != self.three_d_grid.r.shape:
            raise ValueError("Cannot normalize psi as not same shape as three_d_grid.r")

        prob = self.integrate_prob_distro(psi)

        if prob == 0:
            raise ValueError("Cannot normalize a zero wave function")
        # In these units, psi is normalized to unity.  U0 is then the TF parameter N*a/aho.
        return psi * np.sqrt(1 / prob)

    def integrate_prob_distro(self, psi: np.ndarray) -> float:
        """Calculate the probability density function by integrating the square of the absolute
        value of the wavefunction.
        Args:
            psi (np.ndarray): The wavefunction
        Returns:
            float: The probability distribution
        """
        prob_distro = (
            2
            * np.pi
            * self.three_d_grid.dx
            * self.three_d_grid.dr
            * np.sum(self.three_d_grid.r * np.abs(psi) ** 2)
        )
        return prob_distro

    @property
    def density(self) -> np.ndarray:
        """
        Get the density of the wavefunction.
        Returns:
            ndarray: the density of the wave function
        """
        return np.abs(self.psi) ** 2

    @property
    def column_densities(self) -> tuple:
        """
        Returns the column densities (#/Length^2)

        Returns
            tuple : (column_zy -  the zy axes, column_zx -  the zx axes, profiles - the profiles in the x and z axes)
        """
        # column_xz
        column_zy = np.zeros((2 * self.three_d_grid.Nr, 2 * self.three_d_grid.Nr))

        profile_r = self.three_d_grid.dx * np.sum(np.abs(self.psi) ** 2, axis=1)  #

        # 1D interpolation
        profile_r_interp = interp1d(
            self.three_d_grid.r[:, 0],
            profile_r,
            fill_value=0.0,
            bounds_error=False,
            kind="cubic",
        )

        for iz in range(len(self.three_d_grid.z[0, :])):
            for iy in range(len(self.three_d_grid.y[:, 0])):
                r = np.sqrt(
                    self.three_d_grid.z[0, iz] ** 2 + self.three_d_grid.y[iy, 0] ** 2
                )
                column_zy[iz, iy] = profile_r_interp(r)

        # column zy
        # 2D interpolation
        density_interp = RectBivariateSpline(
            self.three_d_grid.r[:, 0],
            self.three_d_grid.x[0, :],
            self.density,
            kx=3,
            ky=3,
        )  # cubic spline interpolation
        column_zx = np.zeros((2 * self.three_d_grid.Nr, self.three_d_grid.Nx))

        for iz in range(len(self.three_d_grid.z[0, :])):
            for ix in range(len(self.three_d_grid.x[0, :])):
                r = np.sqrt(
                    self.three_d_grid.z[0, iz] ** 2 + self.three_d_grid.y[:, 0] ** 2
                )
                density_slice = density_interp(np.sort(r), self.three_d_grid.x[0, ix])
                column_zx[iz, ix] = self.three_d_grid.dy * np.sum(density_slice)

        #
        profile_z_zy = self.three_d_grid.dy * np.sum(column_zy, axis=1)
        profile_z_zx = self.three_d_grid.dx * np.sum(column_zx, axis=1)
        profile_x = self.three_d_grid.dz * np.sum(column_zx, axis=0)
        profiles = [profile_z_zy, profile_z_zx, profile_x]
        # check that interpolation preserved norm
        if (
            self.three_d_grid.dy * sum(profile_z_zy) > 0.95
            and self.three_d_grid.dx * sum(profile_x) > 0.95
        ):
            pass
        else:
            raise ValueError("Lost norm in interpolation")

        # the profile_x should match up with the output of the profile function.
        return column_zy, column_zx, profiles

    @property
    def density_profiles(self) -> tuple:
        """
        Returns the density profiles along the x and r axes.  #/Length
        These match the integrated column densities
        """
        profile_x = (
            2
            * np.pi
            * self.three_d_grid.dr
            * np.sum(self.three_d_grid.r * np.abs(self.psi) ** 2, axis=0)
        )
        profile_r = (
            2
            * np.pi
            * self.three_d_grid.dx
            * self.three_d_grid.r[:, 0]
            * np.sum(np.abs(self.psi) ** 2, axis=1)
        )
        return profile_x, profile_r

    @property
    def atom_number(self) -> float:
        """
        Returns atom number calculated from the current wavefunction

        Returns:
            float: number of atoms in the simulation (normalized to 1)

        """
        return (
            2
            * np.pi
            * self.three_d_grid.dx
            * self.three_d_grid.dr
            * np.sum(self.three_d_grid.r * np.abs(self.psi) ** 2)
        )

    @property
    def phase(self) -> np.ndarray:
        """
        Returns the phase of the wave function

        Returns:
            ndarray: the phase of the wavefunction (cylindrical coordinates, sim units)

        """
        return np.angle(self.psi)

    @property
    def flow(self) -> tuple:
        """
        Returns the superfluid velocities in X and R directions in two 2D arrays

        Returns:
            tuple: (flow_r - flow in R direction, flow_x - flow in X direction). Simulator units.

        """
        diff_r = (
            2
            * self.three_d_grid.dr
            * np.gradient(self.phase, self.three_d_grid.dr, axis=0, edge_order=1)
        )  # axis 0 for r
        diff_x = (
            2
            * self.three_d_grid.dz
            * np.gradient(self.phase, self.three_d_grid.dz, axis=1, edge_order=1)
        )  # axis 1 for x

        # dealing with 'jumps' from negative pi to pi.  Essentially enforcing that diff_i resides between -pi and pi
        diff_r[diff_r > np.pi] -= 2 * np.pi
        diff_r[diff_r < -np.pi] += 2 * np.pi
        diff_x[diff_x > np.pi] -= 2 * np.pi
        diff_x[diff_x < -np.pi] += 2 * np.pi

        flow_r = 2 * np.pi * diff_r / (2 * self.three_d_grid.dr)
        flow_x = 2 * np.pi * diff_x / (2 * self.three_d_grid.dx)

        return flow_r, flow_x

    @property
    def current(self) -> np.ndarray:
        """
        Returns the total current along the X-direction, 1D array

        Returns:
            ndarray : current in the X direction (simulator units)

        """
        _, flow_x = self.flow  # v_z(r,x)
        current_x = (
            2
            * np.pi
            * self.three_d_grid.dr
            * np.sum(self.three_d_grid.r * flow_x * self.density, axis=0)
        )  # j_z(z):  A 1D array of current along the x-direction.
        return current_x

    @property
    def com_position(self) -> float:
        """
        Returns the center of mass coordinates of the cloud in X direction
        The center of mass cannot be displaced in the radial direction by assumption
        Returns 1 scalar, useful for diagnostics

        Returns:
            float : the center of mass in the X direction

        """
        com_x = (
            2
            * np.pi
            * self.three_d_grid.dx
            * self.three_d_grid.dr
            * np.sum(self.three_d_grid.x * self.three_d_grid.r * np.abs(self.psi) ** 2)
        )

        return com_x

    @property
    def widths(self) -> tuple:
        """
        Returns the widths of the condensate (\\Delta r and \\Delta x) in radial and x directions

        Returns
            tuple: (Delta r, Delta x) simulation units.



        """
        square_width_x = (
            2
            * np.pi
            * self.three_d_grid.dr
            * self.three_d_grid.dx
            * np.sum(
                self.three_d_grid.r * self.three_d_grid.x**2 * np.abs(self.psi) ** 2
            )
        )
        square_width_r = (
            2
            * np.pi
            * self.three_d_grid.dr
            * self.three_d_grid.dx
            * np.sum(self.three_d_grid.r**3 * np.abs(self.psi) ** 2)
        )
        com_x = self.com_position

        return np.sqrt(square_width_x - com_x**2), np.sqrt(square_width_r)
