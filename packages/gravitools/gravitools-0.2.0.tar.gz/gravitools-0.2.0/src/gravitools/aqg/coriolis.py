from __future__ import annotations

from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def fit_model(theta, amplitude, phase, offset):
    return np.cos(theta / 180 * np.pi + phase) * amplitude + offset


@dataclass
class CoriolisAnalysis:
    """Results summary of an AQG Coriolis measurement"""

    orientations: list[float]
    g_values: list[float]
    g_err_values: list[float]
    g_true: float
    amplitude: float
    amplitude_uncert: float
    phase: float
    phase_uncert: float
    name: str

    def __str__(self):
        return f"{self.amplitude:.0f}({self.amplitude_uncert:.0f}) nm/s²"

    def plot(self, ax=None, fmt=".", label=None, **plot_args):
        """Plot data with fit model"""
        ax = ax or plt.gca()
        ax.set_xlabel("Sensor orientation [deg]")
        ax.set_ylabel(r"$\Delta g$ [nm/s²]")
        ax.set_xticks([0, 90, 180, 270, 360])
        ax.margins(x=0)
        # Input data
        p = ax.errorbar(
            self.orientations,
            self.g_values - self.g_true,
            self.g_err_values,
            fmt=fmt,
            label=label or f"{self.name}: {self}",
            **plot_args,
        )
        # Fit model
        theta = np.linspace(-20, 380, 100)
        parameters = self.amplitude, self.phase, 0
        ax.plot(
            theta,
            fit_model(theta, *parameters),
            color=p[0].get_color(),
        )


def perform_coriolis_analysis(datasets, name=None):
    """Perform Coriolis analysis on a list of datasets

    Args:
        datasets (list[AQGDataset]):
            Processed AQG datasets.
        name (str):
            Identifier.

    Returns (CoriolisAnalysis):
        Analysis results.
    """
    orientations = [dataset.metadata["orientation"] for dataset in datasets]
    g_values = []
    g_err_values = []
    for dataset in datasets:
        g = dataset.mean()
        g_values.append(g.value)
        g_err_values.append(g.error)
    g_true = np.mean(g_values)
    starting_parameters = 100, 0, 0
    (amplitude, phase, offset), cov = curve_fit(
        fit_model,
        orientations,
        g_values - g_true,
        sigma=g_err_values,
        p0=starting_parameters,
    )
    amplitude_uncert, phase_uncert, _ = np.sqrt(np.diag(cov))
    return CoriolisAnalysis(
        orientations=orientations,
        g_values=g_values,
        g_err_values=g_err_values,
        g_true=g_true + offset,
        amplitude=amplitude,
        amplitude_uncert=amplitude_uncert,
        phase=phase,
        phase_uncert=phase_uncert,
        name=name or str(datasets[0].time_span[0].date()),
    )
