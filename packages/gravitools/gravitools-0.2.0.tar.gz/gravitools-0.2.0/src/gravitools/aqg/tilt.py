"""
Functions for processing an AQG tilt offset calibration measurement
"""

from __future__ import annotations

from dataclasses import dataclass
import pathlib
import zipfile

import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np
import pandas as pd
import scipy.optimize

from ..corrections import effective_tilt
from .dataset import AQGDataset
from .rawdata import process_aqg_raw_dataset

RAD_TO_MILLIRAD = 1e3
RAD_TO_MICRORAD = 1e6
TILT_FOR_1_UGAL = 45.18e-6  # in radian


def draw_circle(x: float, y: float, radius: float, ax=None, n=100, **kwargs):
    """Draw a circle in a Matplotlib graph"""
    ax = ax or plt.gca()
    phi = np.linspace(0, 2 * np.pi, n)
    return ax.plot(x + radius * np.cos(phi), y + radius * np.sin(phi), **kwargs)


def plot_tilt_offset(
    x: float,
    y: float,
    origin: tuple(float, float) = (0, 0),
    *,
    circle: bool = True,
    ax=None,
    **kwargs: dict,
) -> None:
    """Draw tilt offset position on a Matplotlib graph

    Args:
        x:
            Tilt offset in X axis.
        y:
            Tilt offset in Y axis.
        origin:
            Plot origin coordinate.
        circle:
            Draw a circle around the position indicating a 10 nm/s² uncertainty.
        ax:
            Axis on which to draw the plot.
        **kwargs:
            Arguments to pass on to `matplotlib.pyplot.scatter()`.
    """
    if ax is None:
        ax = plt.gca()
        ax.axis("equal")
        ax.set_xlabel("X tilt offset [µrad]")
        ax.set_ylabel("Y tilt offset [µrad]")
    offset = np.array((x, y))
    origin = np.array(origin)
    position = (offset - origin) * RAD_TO_MICRORAD
    graph = ax.scatter(*position[np.newaxis].T, linestyle="", **kwargs)
    if circle:
        draw_circle(
            *position,
            radius=TILT_FOR_1_UGAL * RAD_TO_MICRORAD,
            ax=ax,
            color=graph.get_facecolor(),
        )


@dataclass
class TiltOffset:
    """AQG tilt offset fit result"""

    x: float
    y: float
    g: float = 0
    u_x: float = 0
    u_y: float = 0
    u_g: float = 0

    def __str__(self) -> str:
        return (
            f"x = {self.x * RAD_TO_MICRORAD:.1f} ± {self.u_x * RAD_TO_MICRORAD:.1f} "
            "µrad, "
            f"y = {self.y * RAD_TO_MICRORAD:.1f} ± {self.u_y * RAD_TO_MICRORAD:.1f} "
            "µrad"
        )

    def __iter__(self) -> tuple[float, float]:
        return iter((self.x, self.y))

    def plot(self, **kwargs):
        """Plot as a 2D tilt graph with a circle for 1 µGal"""
        return plot_tilt_offset(*self, **kwargs)


def fit_model(
    tilt_xy: np.ndarray, offset_x: np.ndarray, offset_y: np.ndarray, g_true: np.ndarray
) -> np.ndarray:
    """Model used to fit tilt calibration measurements

    See also [tilt_correction()][gravitools.corrections.tilt_correction].

    Args:
        tilt_xy:
            2D array of X and Y tilt angles, in radian.
        offset_x:
            Tilt offset in X direction, in radian.
        offset_y:
            Tilt offset in X direction, in radian.
        g_true:
            Gravity value at verticality, in nm/s².

    Returns:
        Absolute gravity value reduced due to instrument tilt.
    """
    tilt_x, tilt_y = tilt_xy
    return g_true * np.cos(effective_tilt(tilt_x - offset_x, tilt_y - offset_y))


def perform_tilt_offset_fit(
    tilt_x: np.ndarray, tilt_y: np.ndarray, g: np.ndarray, g_err: np.ndarray
) -> TiltOffset:
    """Fit tilt offset values from set of calibration datapoints

    Args:
        tilt_x:
            Instrument tilt in X direction, in radian.
        tilt_y:
            Instrument tilt in Y direction, in radian.
        g:
            Measured absolute gravity, in nm/s².
        g_err:
            Standard uncertainty of measured gravity, in nm/s².

    Returns:
        Tilt offset fit results.
    """
    start_parameters = np.mean(tilt_x), np.mean(tilt_y), np.max(g)
    popt, pcov = scipy.optimize.curve_fit(
        fit_model, (tilt_x, tilt_y), g, sigma=g_err, p0=start_parameters
    )
    perr = np.sqrt(np.diag(pcov))
    return TiltOffset(*popt, *perr)


@dataclass(repr=False)
class AQGTiltAnalysis:
    """Summary of an AQG tilt offset analysis"""

    datapoints: pd.DataFrame
    result: TiltOffset
    name: str = None
    datasets: list[AQGDataset] = None

    @classmethod
    def fit(cls, datapoints, datasets=None, name=None):
        """Fit the tilt offset from a list of data points"""
        result = perform_tilt_offset_fit(
            datapoints.tilt_x,
            datapoints.tilt_y,
            datapoints.g,
            datapoints.g_err,
        )
        datapoints["tilt"] = effective_tilt(
            datapoints.tilt_x - result.x, datapoints.tilt_y - result.y
        )
        datapoints["g_fit"] = fit_model(
            datapoints[["tilt_x", "tilt_y"]].values.T,
            result.x,
            result.y,
            result.g,
        )
        datapoints["dg_residual"] = datapoints.g - datapoints.g_fit
        return cls(datapoints, result=result, datasets=datasets, name=name)

    def __post_init__(self):
        if self.datasets and not self.name:
            # Take date of first dataset
            self.name = str(self.datasets[0].time_span[0].date())

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self) -> str:
        return f"{self.result} ({self.name})"

    def plot_tilt_offset(self, label: str = None, **kwargs: dict) -> None:
        """Plot tilt offset result"""
        self.result.plot(label=label or self.name, **kwargs)

    def plot_tilt_distribution(self, ax=None) -> None:
        """Plot 2D distribution of tilt angles"""
        ax = ax or plt.gca()

        # Draw center and 1 mrad circle
        attrs = dict(color="grey", linewidth=1, linestyle=":")
        position = np.array(tuple(self.result)) * RAD_TO_MICRORAD
        ax.axvline(position[0], **attrs)
        ax.axhline(position[1], **attrs)
        draw_circle(*position, radius=1000, **attrs)

        # Draw data points
        tilt_x = RAD_TO_MICRORAD * self.datapoints.tilt_x
        tilt_y = RAD_TO_MICRORAD * self.datapoints.tilt_y
        dg = self.datapoints.dg_residual
        dg_max = dg.abs().max()
        ax.scatter(
            tilt_x,
            tilt_y,
            c=dg,
            cmap=plt.get_cmap("coolwarm"),
            vmin=-dg_max,
            vmax=dg_max,
        )

        # Draw numbers and residuals
        for nr, row in self.datapoints.iterrows():
            ax.text(
                RAD_TO_MICRORAD * row.tilt_x,
                RAD_TO_MICRORAD * row.tilt_y,
                f"{nr:d}: {row.dg_residual:+.0f}",
                transform=mtransforms.offset_copy(
                    ax.transData, x=0, y=0.1, units="inches", fig=plt.gcf()
                ),
                ha="center",
            )

        # Plot configurations
        ax.axes.set_aspect("equal")
        ax.set_xlabel("Tilt X [µrad]")
        ax.set_ylabel("Tilt Y [µrad]")
        ax.set_title("Fit residuals [nm/s²]")
        ax.margins(x=0.1, y=0.1)

    def plot_residuals(self, ax=None) -> None:
        """Plot residuals against effective angle"""
        ax = ax or plt.gca()
        # Zero line
        ax.axhline(0, color="grey", linewidth=0.7)
        # Data points
        ax.errorbar(
            self.datapoints.tilt * RAD_TO_MICRORAD,
            self.datapoints.dg_residual,
            self.datapoints.g_err,
            fmt=".",
            capsize=2,
            linewidth=1,
            label=self.name,
        )
        ax.set_xlabel("Effective tilt angle [µrad]")
        ax.set_ylabel(r"Fit residual $\Delta g$ [nm/s²]")
        ax.set_xlim(0, self.datapoints.tilt.max() * 1.1 * RAD_TO_MICRORAD)

    def plot_datasets(self, indices: list[int] = None, ylim=None) -> None:
        """Plot individual measurements"""
        if self.datasets is None:
            raise ValueError("Datasets are unavailable")

        indices = indices or self.datapoints.index
        fig, axs = plt.subplots(nrows=len(indices), figsize=(10, len(indices)))
        fig.subplots_adjust(hspace=1)
        for idx, ax in zip(indices, axs):
            dataset = self.datasets[idx]

            ax.set_title(f"[#{idx:02d}] {dataset.name}", loc="left")

            outliers = dataset.get("is_outlier")
            g = dataset.get("g")
            dg = g - g[~outliers].mean()
            ax.plot(dg[~outliers], ".", markersize=2, label="Ok")
            ax.plot(dg[outliers], "r.", markersize=2, label="Outlier")
            # 1-sigma bounds
            dg_std = dg[~outliers].std()
            for y in [dg_std, -dg_std]:
                ax.axhline(y, color="k", linewidth=1, linestyle="--")

            ax.margins(x=0.01, y=0.3)
            if ylim:
                ax.set_ylim(*ylim)
            ax.set_ylabel(r"$\Delta g$ [nm/s²]")

        axs[0].legend(loc=1, markerscale=5, ncol=2, frameon=False)


def calculate_tilt_dataset_means(datasets: list[AQGDataset]) -> pd.DataFrame:
    """Calculate mean values of an AQG tilt offset calibration dataset"""

    def process(dataset):
        is_outlier = dataset.get("is_outlier")
        # Get corrected gravity signal without tilt correction. Corrections
        # were subtracted, so *add* here.
        g = dataset.full_g(incl_outliers=False).y + dataset.get("dg_tilt")[~is_outlier]
        g_err = g.resample("10s").mean().sem()
        return dict(
            name=dataset.name,
            tilt_x=dataset.get("x_tilt")[~is_outlier].mean(),
            tilt_y=dataset.get("y_tilt")[~is_outlier].mean(),
            g=g.mean(),
            g_err=g_err,
            valid_drops=dataset.num_drops - dataset.num_outliers,
            total_drops=dataset.num_drops,
        )

    return pd.DataFrame(map(process, datasets))


def analyze_aqg_tilt_calibration(
    rawdata_paths: list[str | pathlib.Path | zipfile.Path],
    config: dict = None,
    name: str = None,
) -> AQGTiltAnalysis:
    """Perform an AQG tilt offset calibration from a list of rawdata files

    Args:
        rawdata_paths:
            List of file paths to AQG raw datasets
        config:
            Processing configuration parameters.
        name:
            Identifier name for this calibration measurement. If unspecified,
            the date of the first dataset is chosen.

    Returns:
        Summary of this analysis results
    """
    # Process all datasets normally
    datasets = [process_aqg_raw_dataset(path, config=config) for path in rawdata_paths]
    # Calculate dataset means, excl. tilt correction
    datapoints = calculate_tilt_dataset_means(datasets)
    return AQGTiltAnalysis.fit(datapoints=datapoints, name=name, datasets=datasets)


def plot_tilt_analyses(
    tilt_analyses: list[AQGTiltAnalysis],
    origin: tuple[float, float] = None,
    **kwargs: dict,
) -> None:
    """Plot multiple tilt analyis results"""
    for tilt_analysis in tilt_analyses:
        if origin is None:
            origin = tuple(tilt_analysis.result)
        tilt_analysis.plot_tilt_offset(origin=origin, **kwargs)
