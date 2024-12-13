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

from enum import Enum
from math import floor, log10

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
from bert_schemas import job as job_schema
from matplotlib.ticker import FormatStrFormatter, LinearLocator
from pydantic import BaseModel

from oqtant.schemas.job import print_keys
from oqtant.util.exceptions import (
    JobPlotFitError,
    JobPlotFitMismatchError,
    JobReadError,
)


class OutputImageType(str, Enum):
    TIME_OF_FLIGHT = "TIME_OF_FLIGHT"
    IN_TRAP = "IN_TRAP"
    MOT = "MOT"
    TIME_OF_FLIGHT_FIT = "TIME_OF_FLIGHT_FIT"


class AxisType(str, Enum):
    x = "x"
    y = "y"


def in_trap_check(func):
    def wrapper(*args, **kwargs):
        if args[0].image_type == OutputImageType.IN_TRAP:
            print("** not available for In-Trap output **")
        else:
            return func(*args, **kwargs)

    return wrapper


class OqtantOutput(BaseModel):
    """A class that represents the output of a job submitted to Oqtant"""

    @property
    def image_type(self):
        if hasattr(self, "it_plot"):
            return OutputImageType.IN_TRAP
        else:
            return OutputImageType.TIME_OF_FLIGHT

    @property
    def fields(self):
        """Method to print out the output fields for an OqtantOutput"""
        return print_keys(self.model_dump())

    @property
    def atom_statistics(self):
        """Property that prints out the atom statistics of a TIME_OF_FLIGHT image job's output"""
        if not self.image_type.IN_TRAP:
            print(f"Temperature (nK): {self.temperature_nk}")
            print(f"Total atoms : {self.tof_atom_number}")
            print(f"Condensed atoms : {self.condensed_atom_number}")
            print(f"Thermal atoms : {self.thermal_atom_number}")
        else:
            print(
                "** Atom statistics only available for TIME_OF_FLIGHT imaging in a BEC job. **"
            )

    @property
    def TOF(self) -> np.ndarray | None:
        """Property that returns the shaped time of flight (TOF) image of a job's output if it exists

        Returns:
            numpy.ndarray: The reshaped pixels of the TOF image
        """
        reshaped_pixels = None
        try:
            reshaped_pixels = np.array(self.tof_image.pixels).reshape(
                self.tof_image.rows, self.tof_image.columns
            )
        except Exception:
            print("** not an TOF image **")
        return reshaped_pixels

    @property
    def IT(self) -> np.ndarray | None:
        """Property that returns the shaped in-trap (IT) image of a job's output if it exists

        Returns:
            numpy.ndarray: The reshaped pixels of the IT image
        """
        reshaped_pixels = None
        try:
            reshaped_pixels = np.array(self.it_plot.pixels).reshape(
                self.it_plot.rows, self.it_plot.columns
            )
        except Exception:
            print("** not an IT image **")
        return reshaped_pixels

    @property
    @in_trap_check
    def temperature(self):
        """Property that returns the atom temperature of a job's output

        Returns:
            int: The atom temperature of a job's output
        """
        return self.temperature_nk

    @property
    @in_trap_check
    def mot_population(self):
        """Property that returns the thermal atom count of a job's output

        Returns:
            int: The thermal atom count of a job's output
        """
        return self.thermal_atom_number

    @property
    @in_trap_check
    def thermal_population(self):
        """Property that returns the thermal atom count of a job's output

        Returns:
            int: The thermal atom count of a job's output
        """
        return self.thermal_atom_number

    @property
    @in_trap_check
    def condensed_population(self):
        """Property that returns the condensed atom count of a job's output

        Returns:
            int: The condensed atom count of a job's output
        """
        return self.condensed_atom_number

    @property
    @in_trap_check
    def total_population(self):
        """Property that returns the count of both thermal and condensed atoms of a job's output

        Returns:
            int: The count of both thermal and condensed atoms of a job's output
        """
        return self.thermal_population + self.condensed_population

    @property
    @in_trap_check
    def condensed_fraction(self):
        """Property that returns the condensed fraction of atoms for the condensed population and
        total population of a job's output

        Returns:
            float: The condensed fraction of atoms for the condensed population and the total
                population of a job's output
        """
        return np.round(self.condensed_population / self.total_population, 3)

    @property
    @in_trap_check
    def get_bimodal_fit_parameters(self):
        """Property that returns the TOF fit data for a job's output

        Returns:
            job_schemas.TofFit: The TOF fit data for a job's output
        """
        return self.tof_fit

    def get_image_data(self, image: OutputImageType | None = None) -> np.ndarray | None:
        """Method to retrieve the image data for the specified image type, if no image type is
        provided the job's imaging type will be returned

        Args:
            image (oqtant.schemas.output.OutputImageType | None, optional): The image type to retrieve

        Returns:
            numpy.ndarray: The image data for the specified image type
        """
        in_trap = job_schema.ImageType.IN_TRAP
        tof = job_schema.ImageType.TIME_OF_FLIGHT

        data, shape = None, None
        if image is None:
            # no type specified, assume user wants output image of the correct
            # type based on the image_type used in the job
            image = in_trap if self.image_type == in_trap else tof

        if image == in_trap:
            data = self.it_plot.pixels
            shape = (self.it_plot.rows, self.it_plot.columns)
        elif image == tof:
            data = self.tof_image.pixels
            shape = (self.tof_image.rows, self.tof_image.columns)
        elif image == "MOT":
            data = self.mot_fluorescence_image.pixels
            shape = (
                self.mot_fluorescence_image.rows,
                self.mot_fluorescence_image.columns,
            )
        elif image == "TIME_OF_FLIGHT_FIT":
            if self.image_type == in_trap:
                print("** no fit image available for IN_TRAP **")
                return None
            data = self.tof_fit_image.pixels
            shape = (self.tof_fit_image.rows, self.tof_fit_image.columns)

        output = None
        try:
            output = np.asarray(data).reshape(shape)
        except ValueError:
            print("Could not get image Data.")

        return output

    def get_image_pixcal(self, image: OutputImageType) -> float:
        """Method to get the pixel calibration for the provided image type

        Args:
            image (oqtant.schemas.output.OutputImageType): The image type to retrieve the pixel calibration for

        Returns:
            float: The pixel calibration for the provided image
        """

        def __parse_pixcal(image_name: str) -> float:
            try:
                return getattr(self, image_name).pixcal
            except Exception:
                raise JobReadError(
                    f"{self.job_type} job does not contain a {image} image"
                )

        if image == OutputImageType.TIME_OF_FLIGHT:
            pixcal = __parse_pixcal("tof_image")
        elif image == OutputImageType.IN_TRAP:
            pixcal = __parse_pixcal("it_plot")
        elif image == OutputImageType.MOT:
            pixcal = __parse_pixcal("mot_fluorescence_image")
        elif image == OutputImageType.TIME_OF_FLIGHT_FIT:
            pixcal = __parse_pixcal("tof_fit_image")
        else:
            # raise exception unknown image type
            image_name = (
                "tof_image" if image == OutputImageType.TIME_OF_FLIGHT else "it_plot"
            )
            pixcal = __parse_pixcal(image_name)
        return pixcal

    def get_slice(self, axis: AxisType = "x") -> list[float]:
        """Method that returns a list of data point representing a slice along the specified axis

        Args:
            axis (oqtant.schemas.output.AxisType, optional): The axis along which the take the slice

        Returns:
            list[float]: A list of data points representing the slice along the specified axis
        """
        if axis == "x":
            data = self.tof_x_slice.points
            cut_data = [point["y"] for point in data]
        else:
            data = self.tof_y_slice.points
            cut_data = [point["y"] for point in data]
        return cut_data

    @staticmethod
    def get_image_space(
        datafile: np.ndarray = np.zeros((100, 100)), centered: str = "y"
    ) -> tuple[np.meshgrid, int, int]:
        """Method to generate a numpy.meshgrid of image coordinates

        Args:
            datafile (numpy.ndarray, default): A matrix of optical density data
            centered (str, optional): The orientation of the image

        Returns:
            tuple[numpy.meshgrid, int, int]: The numpy.meshgrid of image coordinates
        """
        lx, ly = np.shape(datafile)
        x, y = np.arange(lx), np.arange(ly)

        if centered == "y":
            x = x - round(lx / 2)
            y = y - round(ly / 2)

        xy_mesh = np.meshgrid(x, y)

        return xy_mesh, lx, ly

    def fit_bimodal_data2D(
        self, xi: list[float] = None, lb: list[float] = None, ub: list[float] = None
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.float64]:
        """Method to perform a fit via a trust region reflective algorithm

        Args:
            xi (list[float] | None, optional): List of fit parameter initial guesses
            lb (list[float] | None, optional): List of fit parameter lower bounds
            ub (list[float] | None, optional): List of fit parameter upper bounds

        Returns:
            tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.float64]: The calculated fit data
        """
        xi = xi if xi else [0.25, 8, 8, 1, 4, 6, 0, 0, 0.02]
        lb = lb if lb else [0, 7, 7, 0, 2, 2, -20, -20, 0]
        ub = ub if ub else [2, 20, 20, 2, 20, 20, 20, 20, 1]

        xy_mesh, _, _ = self.get_image_space()  # TOF_data)

        (X, Y) = xy_mesh
        x = X[0]
        y = Y[:, 0]

        fit_params, cov_mat = opt.curve_fit(
            bimodal_dist_2D, xy_mesh, np.ravel(self.TOF), p0=xi, bounds=(lb, ub)
        )
        fit_residual = self.TOF - bimodal_dist_2D(xy_mesh, *fit_params).reshape(
            np.outer(x, y).shape
        )
        fit_r_squared = 1 - np.var(fit_residual) / np.var(self.TOF)

        return fit_params, cov_mat, fit_residual, fit_r_squared

    def plot_fit_results(
        self,
        fit_params: np.ndarray,
        model: str = "bimodal",
        file_name: str = None,
        plot_title: str = None,
        pix_cal: float = 1.0,
    ) -> None:
        """Method to plot the results of a fit operation

        Args:
            fit_params (numpy.ndarray): List of parameters from a fit operation
            model (str. optional): The shape(?) to use while plotting
            file_name (str | None, optional): The name of the file to write the plot to
            plot_title (str | None, optional): The title of the resulting plot result
            pix_cal (float, optional): The pixel calibration to use while generating the plot
        """

        xy_mesh, lx, ly = self.get_image_space()  # TOF_data)

        (X, Y) = xy_mesh

        if model == "bimodal":
            try:
                m = bimodal_dist_2D(xy_mesh, *fit_params)
            except TypeError as exc:
                raise JobPlotFitMismatchError() from exc
            except Exception as exc:
                raise JobPlotFitError() from exc

        elif model == "gaussian":
            try:
                m = Gaussian_dist_2D(xy_mesh, *fit_params)
            except TypeError as exc:
                raise TypeError(
                    "PLOT FIT RESULTS: mismatched parameters and model type"
                ) from exc
            except Exception as exc:
                raise JobPlotFitError() from exc
        elif model == "TF":
            try:
                m = TF_dist_2D(xy_mesh, *fit_params)
            except TypeError as exc:
                raise JobPlotFitMismatchError() from exc
            except Exception as exc:
                raise JobPlotFitError() from exc
        else:
            print(
                f"PLOT FIT RESULTS: Invalid model specified: {model}.",
                " Select 'bimodal', 'gaussian', or 'TF'",
            )
            return

        m = m.reshape(lx, ly)
        plt.figure()
        plt.imshow(
            m,
            origin="upper",
            cmap="viridis",
            extent=(
                np.min(X) * pix_cal,
                np.max(X) * pix_cal,
                np.min(Y) * pix_cal,
                np.max(Y) * pix_cal,
            ),
        )

        if plot_title is None:
            plot_title = f"job: {self.name}\nTOF fit: {model}"

        plt.title(plot_title)

        if file_name:
            self._save_plot_file(plt, file_name)
        plt.show()

    @staticmethod
    def _save_plot_file(plot: plt, file_name: str) -> None:
        """Method to save a plot to a file

        Args:
            plot (matplotlib.pyplot): Module containing the plot to save
            file_name (str): The name of the file to save
        """
        file = f"{file_name}.png"
        try:
            plot.savefig(file)
            print(f"plot saved to file: {file}")
        except (FileNotFoundError, Exception):
            print(f"failed to save plot at {file}")

    def plot_tof(
        self,
        file_name: str = None,
        figsize: tuple[int, int] = (12, 12),
        grid_on: bool = False,
    ) -> None:
        """Method to generate a 2D plot of atom OD

        Args:
            file_name (str | None, optional): The name of the file to write the plot to
            figsize (tuple[int, int], optional): The size of the figure to generate
            grid_on (bool, optional): Flag to show grid lines or not in the plot

        """
        xy_mesh, _, _ = self.get_image_space()  # TOF_data
        (X, Y) = xy_mesh

        fig2D = plt.figure(figsize=figsize)
        ax = fig2D.gca()
        plt2D = plt.imshow(
            self.TOF,
            origin="upper",
            cmap="viridis",
            extent=(
                np.min(X) * self.get_image_pixcal(OutputImageType.TIME_OF_FLIGHT),
                np.max(X) * self.get_image_pixcal(OutputImageType.TIME_OF_FLIGHT),
                np.min(Y) * self.get_image_pixcal(OutputImageType.TIME_OF_FLIGHT),
                np.max(Y) * self.get_image_pixcal(OutputImageType.TIME_OF_FLIGHT),
            ),
        )
        plt.grid(b=grid_on)
        plt.colorbar(plt2D, shrink=0.8)

        ax.set_xlabel("x position (microns)", labelpad=15, fontsize=16)
        ax.set_ylabel("y position (microns)", labelpad=15, fontsize=16)
        plt.title("time of flight optical depth", fontsize=16)

        if file_name:
            self._save_plot_file(plt, file_name)
        plt.show()

    def plot_slice(
        self, file_name: str = None, axis: AxisType = "x", grid_on: bool = False
    ) -> None:
        """Method to generate a 1D slice plot of atom OD in x or y

        Args:
            file_name (str | None, optional): The name of the file to write the plot to
            axis: (oqtant.schemas.output.AxisType, optional): The axis to use in the plot
            grid_on (bool, optional): Flag to show grid lines or not in the plot
        """
        xy_mesh, lx, ly = self.get_image_space(self.TOF)
        (X, Y) = xy_mesh

        params, *_ = self.fit_bimodal_data2D()
        fitOD = bimodal_dist_2D(xy_mesh, *params)

        Gfit_params = [params[0], params[6], params[7], params[1], params[2], params[8]]
        fitODG = Gaussian_dist_2D(xy_mesh, *Gfit_params)

        # Reshape Fit Distributions to 2D form
        fitOD2D = fitOD.reshape(lx, ly)
        fitODG2D = fitODG.reshape(lx, ly)

        # Define Central slices
        xslice = fitOD2D[int(lx / 2), :]
        yslice = fitOD2D[:, int(ly / 2)]
        xsliceG = fitODG2D[int(lx / 2), :]
        ysliceG = fitODG2D[:, int(ly / 2)]

        if axis == "x":
            xsliceD = self.TOF[int(len(X[1]) / 2), :]
            xslice = fitOD2D[int(len(X[1]) / 2), :]
            xsliceG = fitODG2D[int(len(X[1]) / 2), :]
            plt.title("x slice", fontsize=16)
            plt.plot(
                X[1] * self.get_image_pixcal(OutputImageType.TIME_OF_FLIGHT),
                xsliceD,
                "ok",
            )
            plt.plot(
                X[1] * self.get_image_pixcal(OutputImageType.TIME_OF_FLIGHT),
                xslice,
                "b",
            )
            plt.plot(
                X[1] * self.get_image_pixcal(OutputImageType.TIME_OF_FLIGHT),
                xsliceG,
                "r",
            )
        elif axis == "y":
            ysliceD = self.TOF[:, int(len(Y[1]) / 2)]
            yslice = fitOD2D[:, int(len(Y[1]) / 2)]
            ysliceG = fitODG2D[:, int(len(Y[1]) / 2)]
            plt.title("y slice", fontsize=16)
            plt.plot(
                Y[:, 1] * self.get_image_pixcal(OutputImageType.TIME_OF_FLIGHT),
                ysliceD,
                "ok",
            )
            plt.plot(
                Y[:, 1] * self.get_image_pixcal(OutputImageType.TIME_OF_FLIGHT),
                yslice,
                "b",
            )
            plt.plot(
                Y[:, 1] * self.get_image_pixcal(OutputImageType.TIME_OF_FLIGHT),
                ysliceG,
                "r",
            )
        else:
            raise ValueError("input either x or y")

        plt.grid(b=grid_on)
        plt.xlabel("x position (microns)", labelpad=15, fontsize=16)
        plt.ylabel("optical depth", labelpad=15, fontsize=16)

        if file_name:
            self._save_plot_file(plt, file_name)
        plt.show()

    def plot_it(
        self,
        file_name: str = None,
        figsize: tuple[int, int] = (12, 12),
        grid_on=False,
    ) -> None:
        """Method to plot an in-trap image output

        Args:
            file_name (str | None, optional): The name of the file to write the plot to
            figsize (tuple[int, int], optional): The size of the figure to generate
            grid_on (bool): Show grid in plot?
        """
        it_od = self.get_image_data("IN_TRAP")

        pixcal = self.get_image_pixcal(image="IN_TRAP")

        plt.figure(figsize=figsize)
        plt.title("in-trap optical depth")
        it_plot = plt.imshow(
            it_od,
            origin="upper",
            cmap="viridis",
            extent=[-256 * pixcal, 256 * pixcal, -74 * pixcal, 74 * pixcal],
        )
        plt.xlabel("x position (microns)")
        plt.ylabel("y position (microns)")
        plt.grid(visible=grid_on)
        plt.colorbar(it_plot, shrink=0.25)
        plt.show()

        if file_name:
            self._save_plot_file(plt, file_name)
        plt.show()

    # This function plots the optical depth as a 3D surface with projected density contours
    def plot_tof_3d(
        self,
        file_name: str = None,
        view_angle: int = -45,
        figsize: tuple[int, int] = (10, 10),
    ) -> None:
        """Method to generate a 3D slice plot of atom OD

        Args:
            file_name (str | None, optional): The name of the file to write the plot to
            view_angle (int, optional): Azimuthal/horizontal angle of "camera" view
            figsize (tuple[int, int], optional): The size of the figure to generate
        """

        fig3d = plt.figure(figsize=figsize)
        ax = fig3d.gca(projection="3d")

        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter("%.02f"))
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False

        # Set axis labels
        ax.set_xlabel("x position (microns)", labelpad=10)
        ax.set_ylabel("y position (microns)", labelpad=10)
        ax.set_zlabel("optical depth", labelpad=10)

        # rotate the axes and update
        ax.view_init(30, view_angle)

        if file_name:
            self._save_plot_file(plt, file_name)
        plt.show()


class OqtantPlotOutput(OqtantOutput, job_schema.PlotOutput):
    ...


class OqtantNonPlotOutput(OqtantOutput, job_schema.NonPlotOutput):
    ...


def round_sig(x: float, sig: int = 2) -> float:
    """Method to round a number to a specified number of significant digits

    Args:
        x (float): The number to be rounded
        sig (int, optional): The number of significant digits

    Returns:
        float: The rounded number
    """
    return round(x, sig - int(floor(log10(abs(x)))) - 1)


def TF_dist_2D(
    xy_mesh: tuple[np.ndarray, np.ndarray],
    TFpOD: float,
    xc: float,
    yc: float,
    rx: float,
    ry: float,
    os: float,
) -> np.ndarray:
    """Method to sample a 2D Thomas-Fermi distribution with given parameters on a grid of coordinates

    Args:
        xy_mesh (tuple[numpy.ndarray, numpy.ndarray]): Matrix containing meshgrid of image coordinates
        TFpOD (float): Thomas-Fermi peak optical density
        xc (float): Cloud center along the x direction (along gravity)
        yc (float): Cloud center along the y direction
        rx (float): Thomas-Fermi radius along the x direction
        ry (float): Thomas-Fermi radius along the y direction (along gravity)
        os (float): Constant offset

    Returns:
        numpy.ndarray: a 2D array of samples from a Thomas Fermi distribution
    """

    # unpack 1D list into 2D x and y coords
    (x, y) = xy_mesh

    # Simplify Thomas-Fermi expression
    A = 1 - ((y - yc) / ry) ** 2 - ((x - xc) / rx) ** 2

    # make 2D Thomas-Fermi distribution
    OD = np.real(TFpOD * np.maximum(np.sign(A) * (np.abs(A)) ** (3 / 2), 0)) + os

    # flatten the 2D Gaussian down to 1D
    return OD.ravel()


def Gaussian_dist_2D(
    xy_mesh: tuple[np.ndarray, np.ndarray],
    GpOD: float,
    xc: float,
    yc: float,
    sigx: float,
    sigy: float,
    os: float,
) -> np.ndarray:
    """Method to sample a 2D Gaussian distribution with given parameters on a grid of coordinates

    Args:
        xy_mesh (tuple[numpy.ndarray, numpy.ndarray]): Matrix containing meshgrid of image coordinates
        GpOD (float): Gaussian peak optical density
        xc (float): Cloud center along the x direction (along gravity)
        yc (float): Could center along the y direction
        sigx (float): Gaussian spread along the x direction
        sigy (float): Gaussian spread along the y direction (along gravity)
        os (float): Constant offset

    Returns:
        numpy.ndarray: a 2D array of samples from a Gaussian distribution
    """

    (x, y) = xy_mesh

    OD = (
        GpOD * np.exp(-0.5 * ((y - yc) / sigy) ** 2 - 0.5 * ((x - xc) / sigx) ** 2) + os
    )
    return OD.ravel()


def bimodal_dist_2D(
    xy_mesh: tuple[np.ndarray, np.ndarray],
    GpOD: float,
    sigx: float,
    sigy: float,
    TFpOD: float,
    rx: float,
    ry: float,
    xc: float,
    yc: float,
    os: float,
):
    """Method to sample a bimodal (Thomas-Fermi + Gaussian) distribution with given parameters on a grid of coordinates

    Args:
        xy_mesh (tuple[numpy.ndarray, numpy.ndarray]): Matrix containing meshgrid of image coordinates
        GpOD (float): Gaussian peak optical density
        sigx (float): Gaussian spread along the x direction
        sigy (float): Gaussian spread along the y direction (along gravity)
        TFpOD (float): Thomas-Fermi peak optical density
        rx (float): Thomas-Fermi radius along the x direction
        ry (float): Thomas-Fermi radius along the y direction (along gravity)
        xc (float): Cloud center along the x direction (along gravity)
        yc (float): Cloud center along the y direction
        os (float): Constant offset

    Returns:
        numpy.ndarray: a 2D array of samples from a bimodal (Thomas-Fermi + Gaussian) distribution
    """

    return Gaussian_dist_2D(xy_mesh, GpOD, xc, yc, sigx, sigy, os) + TF_dist_2D(
        xy_mesh, TFpOD, xc, yc, rx, ry, os
    )
