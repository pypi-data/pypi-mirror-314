from collections import OrderedDict
import datetime as dt
import logging
from math import sqrt

from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt

from . import dataset
from ..report import Report, plot
from .dataset import AQGDataset

logger = logging.getLogger(__name__)


# TODO: Remove this
def removesuffix(text, suffix):
    return text[: -len(suffix) + 1]


class AQGDatasetReport(Report):
    """PDF report for an AQG dataset

    Args:
        dataset:
            Processed AQG dataset.
        **kwargs:
            Additional parameters to [Report][gravitools.report.Report].
    """

    def __init__(self, dataset: AQGDataset, **kwargs: dict):
        super().__init__(**kwargs)
        self.dataset = dataset
        # gravity signal at pillar height h=0, resampled to 10s intervals
        self.g = self.dataset.g(h=0.0)
        # TODO: min_count is arbitrary
        self.g_1h_means = self.g.resample("1h", min_count=0.1)
        self.g_mean = self.dataset.mean()
        self.g_syst_err = self.dataset.syst_uncertainty
        # TODO: This should be in AQGDataset
        self.g_total_err = sqrt(self.g_syst_err**2 + self.g_mean.error**2)
        self.g0 = self.g.y0
        self.duration = self.dataset.duration.round("1s")

    def body(self):
        """Define the content structure"""
        self.title(self.dataset.name, super_title="AQG dataset report")
        self.info_section()
        self.results_section()
        self.corrections()
        self.temperatures()
        self.other()

    def info_values(self):
        """ """
        is_outlier = self.dataset.get("is_outlier")
        t0, t1 = is_outlier.index[[0, -1]]
        description = self.dataset.metadata["description"]
        return OrderedDict(
            {
                "Timespan": f"{t0:%F %H:%M} .. {t1:%F %H:%M} UTC",
                "Duration": f"{self.duration}",
                "Location": self.dataset.metadata["location_name"],
                "Coordinate": (
                    f"{self.dataset.metadata['latitude']}, "
                    + f"{self.dataset.metadata['longitude']}, "
                    + f"{self.dataset.metadata['altitude']}"
                ),
                "Point": self.dataset.point,
                "Meter": self.dataset.meter,
                "Software AQG": self.dataset.metadata["software"],
                "gravitools version": self.dataset.metadata["processing_software"],
                "Drops": f"{len(is_outlier):,d}",
                "Outliers": f"{is_outlier.sum():,d} ({is_outlier.mean():.1%})",
                "Reference height": self.dataset.metadata["reference_height"],
                "Instrument orientation": str(self.dataset.metadata["orientation"])
                + " from North",
                "VGG": str(self.dataset.vgg),
                "Pressure admittance": self.dataset.metadata["pressure_admittance"],
                "Systematic correction": (
                    f"{self.dataset.metadata['dg_syst']} (constant)"
                ),
                "Measurement description": description,
                "Processing documenation": "\n".join(self.dataset.metadata["log"]),
                "Comment": self.dataset.comment,
            }
        )

    def info_section(self):
        """ """
        with self.table(widths=[50, 0], aligns=["R", "L"]):
            for param, value in self.info_values().items():
                self.row(param, value)

        with self.table(widths=[50, 45, 0], aligns=["R", "L", "L"]):
            self.row(
                "Mean gravity",
                f"{self.g_mean.transfer(1.25).value:,.1f} nm/s²",
                "h = 1.25 m",
            )
            self.row(
                "",
                f"{self.g_mean.transfer(self.dataset.h).value:,.1f} nm/s²",
                f"h = {self.dataset.h} m",
            )
            self.row("", f"{self.g_mean.transfer(0).value:,.1f} nm/s²", "h = 0 m")
            self.row("Statistical uncertainty", f"{self.g_mean.error:,.1f} nm/s²", "")
            self.row("Systematic uncertainty", f"{self.g_syst_err:,.1f} nm/s²", "")
            self.row("Total uncertainty", f"{self.g_total_err:,.1f} nm/s²", "")

        self.means_1h()

    @plot
    def means_1h(self):
        """ """
        self.subsection("1 hour interval means")
        # TODO: Log messages could go into Report.subsection
        logger.info("Plot 1h means")
        self.g_1h_means.plot(fmt="o", y0=self.g0)

    def results_section(self):
        """ """
        self.section("Results")
        self.adev()
        self.means_10s()
        self.full_signal()

    @plot
    def adev(self):
        """ """
        self.subsection("Allan deviation")
        logger.info("Plot Allan deviation")
        self.dataset.plot_adev()

    def means_10s(self):
        """ """
        self.subsection("10s interval means")
        logger.info("Plot 10s means")
        if self.duration <= dt.timedelta(days=1):
            # Shorter than 1 day
            with self.plot_context():
                self.g.plot(
                    fmt="o", y0=float(self.g_mean), markersize=2, errorbars=False
                )
                plt.ylabel("$g$ - $g_{mean}$ [nm/s²]")
        else:
            # Longer than 1 day
            for chunk, period in self.g.chunks("1D"):
                with self.plot_context():
                    chunk.plot(
                        ".", y0=float(self.g_mean), markersize=2, errorbars=False
                    )
                    plt.xlim(period.start_time, period.end_time.round("1ms"))
                    plt.ylabel("$g$ - $g_{mean}$ [nm/s²]")
                    plt.title(str(period), loc="left")
                    plt.gca().xaxis.set_major_formatter(DateFormatter("%H:%M"))

    def full_signal(self):
        """ """
        self.subsection("Full signal")
        logger.info("Plot full signal")
        full_g = self.dataset.full_g(incl_outliers=True)
        out = full_g.mask(~self.dataset.get("is_outlier"))
        freq = "1D"
        y0 = self.g_mean.value
        if self.duration <= dt.timedelta(days=1):
            # Shorter than 1 day
            with self.plot_context():
                full_g.plot("-", y0=y0, linewidth=0.5, label="__nolabel__")
                out.plot("r", y0=y0, label="outlier")
                plt.legend(loc="upper right")
                plt.ylabel("$g$ - $g_{mean}$ [nm/s²]")
        else:
            # Longer than 1 day
            for (ch1, per), (ch2, _) in zip(full_g.chunks(freq), out.chunks(freq)):
                with self.plot_context():
                    ch1.plot("-", y0=y0, linewidth=0.5, label="__nolabel__")
                    ch2.plot("r", y0=y0, label="outlier")
                    plt.xlim(per.start_time, per.end_time.round("1ms"))
                    plt.ylabel("$g$ - $g_{mean}$ [nm/s²]")
                    plt.title(str(per))
                    plt.legend(loc="upper right")
                    plt.gca().xaxis.set_major_formatter(DateFormatter("%H:%M"))

    def corrections(self):
        """ """
        self.section("Corrections")
        self.earth_tides()
        self.pressure()
        self.polar_motion()
        self.tilt()
        self.tilt_angles()
        self.ocean_loading()

    @plot
    def earth_tides(self):
        """ """
        self.subsection("Earth tide")
        logger.info("Plot earth tide correction")
        dg = self.dataset.get("dg_earth_tide")
        plt.plot(dg)
        plt.ylabel(r"$\Delta$g [nm/s²]")

    def ocean_loading(self):
        """ """
        self.subsection("Ocean loading")

        col = "dg_ocean_loading"
        if col not in self.dataset.columns:
            self.text("No ocean loading correction")
            return
        logger.info("Plot ocean loading correction")
        dg = self.dataset.get(col)
        if all(dg == dg.iloc[0]):
            self.text(f"{dg.iloc[0]} nm/s²  (constant)")
        else:
            with self.plot_context():
                plt.plot(dg)
                plt.ylabel(r"$\Delta$g [nm/s²]")

    @plot
    def pressure(self):
        """ """
        self.subsection("Atmospheric pressure")
        logger.info("Plot pressure correction")
        admittance = self.dataset.metadata["pressure_admittance"]
        self.text(f"Admittance factor: {admittance}")
        dg = self.dataset.get("dg_pressure")
        plt.plot(dg)
        plt.ylabel(r"$\Delta$g [nm/s²]")

    @plot
    def polar_motion(self):
        """ """
        self.subsection("Polar motion")
        logger.info("Plot polar motion correction")
        dg = self.dataset.get("dg_polar")
        plt.plot(dg)
        plt.ylabel(r"$\Delta$g [nm/s²]")

    @plot
    def tilt(self):
        """ """
        self.subsection("Instrument tilt")
        logger.info("Plot tilt correction")
        dg = self.dataset.get("dg_tilt")
        plt.plot(dg)
        plt.ylabel(r"$\Delta$g [nm/s²]")

    def tilt_angles(self):
        """tilt angles"""
        with self.plot_context():
            fig, axs = plt.subplots(nrows=2, sharex=True)
            # Convert tilt from rad to mrad
            axs[0].plot(self.dataset.get("x_tilt").dropna() * 1000, label="X tilt")
            axs[0].set_ylabel("Y tilt [mrad]")
            axs[0].legend(loc="upper left")
            axs[1].plot(self.dataset.get("y_tilt").dropna() * 1000, label="Y tilt")
            axs[1].set_ylabel("Y tilt [mrad]")
            axs[1].legend(loc="upper left")

    def temperatures(self):
        """ """
        self.section("Temperatures")
        logger.info("Plot temperatures")
        self.plot_temperatures()

    def plot_temperatures(self):
        with self.plot_context():
            columns = self.dataset.temperature_columns
            fig, axs = plt.subplots(nrows=len(columns), sharex=True, figsize=[6.8, 10])
            for ax, col in zip(axs, columns):
                heading = (
                    removesuffix(col, "_temperatures").replace("_", " ").capitalize()
                )
                ax.plot(self.dataset.get(col).dropna(), label=heading)
                ax.set_ylabel("T [°C]")
                ax.legend(loc="upper left")

    def other(self):
        """ """
        self.section("Other")
        self.atom_number()

    @plot
    def atom_number(self):
        """ """
        # TODO: Do not do this distinction
        if "atoms_number" in self.dataset.ds:
            logger.info("Plot atom number")
            atoms = self.dataset.get("atoms_number")
            p = plt.plot(atoms, alpha=0.2)
            plt.plot(atoms.resample("1min").mean(), color=p[0].get_color())
            plt.title("Atom number", loc="left")
        else:
            self.text("No atom number data available.")


if dataset.default_report is None:
    dataset.default_report = AQGDatasetReport
