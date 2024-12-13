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

from dataclasses import dataclass

import numpy as np


@dataclass
class ThreeDimGrid:
    """
    'ThreeDimGrid' Defines a two dimensional grid space in cylindrical coordinates with axial symmetry.
    Nx and Nr are the number of points in the x and r directions
    Lx and Lr are the lenghts of the x and z dimensions
    tof_nf toggles the near field grids
    tof_ff toggles the far field grids
    """

    Nx: int
    Nr: int
    Lx: int
    Lr: int
    dr: int
    dz: int
    dy: int

    def __init__(self, tof_nf: bool = False, tof_ff: bool = False):
        # parameters for 3D space
        if tof_nf and tof_ff:
            raise ValueError("tof_nf and tof_ff cannot both be True")
        if tof_nf:
            self.Nx = 500
            self.Nr = 300
            self.Lx = 50
            self.Lr = 30
        elif tof_ff:
            self.Nx = 500
            self.Nr = 500
            self.Lx = 70
            self.Lr = 50
        else:
            self.Nx = 400
            self.Nr = 40
            self.Lx = 40
            self.Lr = 4

        self.dx = self.Lx / self.Nx
        self.dr = self.Lr / self.Nr

        # defining cylindrical grids using np.meshgrid
        self.x_1d, self.r_1d = np.linspace(
            -self.Lx / 2, self.Lx / 2, self.Nx
        ), np.linspace(self.dr / 2, self.Lr - self.dr / 2, self.Nr)

        self.x, self.r = np.meshgrid(self.x_1d, self.r_1d)

        # defining the equivalent cartesian grids for constructing the column densities
        self.z, self.y = np.meshgrid(
            np.linspace(-self.Lr + self.dr / 2, self.Lr - self.dr / 2, 2 * self.Nr),
            np.linspace(-self.Lr + self.dr / 2, self.Lr - self.dr / 2, 2 * self.Nr),
        )
        self.dz, self.dy = self.dr, self.dr
