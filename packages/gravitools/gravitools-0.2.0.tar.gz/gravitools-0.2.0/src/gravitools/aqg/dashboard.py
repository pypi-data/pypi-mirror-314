"""
AQG dashboard based on PyQt6 and pyqtgraph

Usage:
    pip install gravitools[dashboard]
    gt-aqg-dash --help
"""

import argparse
from functools import partial
import logging
from math import sqrt
from pathlib import Path
import signal
import subprocess
import sys
import traceback

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSpinBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)
import numpy as np
import pyqtgraph as pg
from pyqtgraph.parametertree import Parameter, ParameterTree
import yaml

from gravitools.aqg import process_aqg_raw_dataset, read_aqg_dataset
from gravitools.aqg.utils import AQG_SENSITIVITY
from gravitools.config import read_config
from gravitools.utils import STANDARD_HEIGHT

logger = logging.getLogger(__name__)

COLORS = [  # matplotlib palette
    "#1f77b4",  # blue
    "#ff7f0e",  # orange
    "#2ca02c",  # green
    "#d62728",  # red
    "#9467bd",  # purple
    "#8c564b",  # brown
    "#e377c2",  # pink
    "#7f7f7f",  # gray
    "#bcbd22",  # olive
    "#17becf",  # cyan
]
TEMPERATURES = [
    "external",
    "laser",
    "sensor_head",
    "tiltmeter",
    "vacuum_chamber",
]
TILTS = "x_tilt", "y_tilt"
POLLING_INTERVAL = 10  # seconds


def error_dialog(parent, exc_type, exc_value, exc_traceback):
    tb = "\n".join(traceback.format_tb(exc_traceback))
    text = f"<pre>{tb}\n{exc_type.__name__}: {exc_value}</pre>"
    QMessageBox.critical(parent, "Exception", text)


def ro_param(key, value):
    if isinstance(value, list):
        value = "\n".join(value)
    return Parameter.create(name=key, type="str", value=value, readonly=True)


def set_timeseries_data(plot, series):
    # Convert nanosecond timestamps to second
    plot.setData(series.index.astype("int64") * 1e-9, series.values)


def path_or_none(path):
    return Path(path) if path else None


class QFileSelector(QWidget):
    def __init__(self, parent=None, path=None, hint=None, filter=None):
        super().__init__(parent)
        self.hint = hint
        self.filter = filter
        self.line_edit = QLineEdit(str(path or ""))
        self.button = QPushButton(text="\u2026")  # ellipsis
        self.button.setFixedSize(25, self.line_edit.sizeHint().height())
        self.button.clicked.connect(self.on_browse)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def on_browse(self, button_state):
        directory = self.path.parent if self.path else Path.home()
        path, _ = QFileDialog.getOpenFileName(
            self, self.hint, str(directory), filter=self.filter
        )
        if path:
            self.line_edit.setText(path)

    @property
    def path(self):
        return path_or_none(self.line_edit.text())


class PreferencesDialog(QDialog):
    def __init__(self, *args, preferences=None, **kwargs):
        super().__init__(*args, **kwargs)
        preferences = preferences or {}

        self.setWindowTitle("Preferences")
        self.layout = QFormLayout()
        self.setLayout(self.layout)

        self.config_path = QFileSelector(
            path=preferences.get("config_path") or "",
            hint="Select processing configuration YAML file",
            filter="YAML (*.yml)",
        )
        self.layout.addRow(QLabel("Config file"), self.config_path)

        self.auto_reload = QCheckBox()
        self.auto_reload.setChecked(preferences.get("auto_reload", True))
        self.layout.addRow(QLabel("Auto-reload"), self.auto_reload)

        self.reload_interval = QSpinBox()
        self.reload_interval.setValue(preferences.get("reload_interval", 10))
        self.reload_interval.setMinimum(1)
        self.reload_interval.setMaximum(60)
        self.reload_interval.setSuffix(" s")
        self.layout.addRow(QLabel("Refresh interval"), self.reload_interval)

        self.height = QDoubleSpinBox()
        self.height.setValue(preferences.get("height", 0))
        self.height.setMinimum(0)
        self.height.setMaximum(2)
        self.height.setSingleStep(0.01)
        self.height.setSuffix(" m")
        self.layout.addRow(QLabel("Transfer height"), self.height)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        self.layout.addWidget(button_box)

    @property
    def preferences(self):
        return {
            "config_path": self.config_path.path,
            "auto_reload": self.auto_reload.isChecked(),
            "reload_interval": self.reload_interval.value(),
            "height": self.height.value(),
        }


class MainWindow(QMainWindow):
    def __init__(self, *, height=None, config_path=None):
        super().__init__()
        self.data_path = None
        self.preferences = {
            "height": height or 0,
            "config_path": path_or_none(config_path),
            "auto_reload": True,
            "reload_interval": POLLING_INTERVAL,
        }
        self.dataset = None
        self.timer = None
        self._range_change = False

        self.setWindowTitle("AQG Dashboard")
        self.resize(1800, 950)
        self.showMaximized()

        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        for label, shortcut, callback in [
            ("Open raw dataset folder...", "ctrl+f", self.on_open_raw_folder),
            ("Open raw dataset archive...", "ctrl+a", self.on_open_raw_archive),
            ("Open processed dataset...", "ctrl+d", self.on_open_processed_dataset),
            ("Save report...", "ctrl+p", self.on_save_report),
            ("Save protocol...", "ctrl+s", self.on_save_protocol),
            ("Preferences...", "ctrl+k", self.on_open_preferences),
        ]:
            button = QAction(label, self)
            button.setShortcut(QKeySequence(shortcut))
            button.triggered.connect(callback)
            file_menu.addAction(button)

        self.graphs = pg.GraphicsLayoutWidget()
        self.graphs.setBackground(None)  # transparent
        self.graphs.scene().sigMouseClicked.connect(self.on_mouse_clicked)
        self.paramtree = ParameterTree(showHeader=False)

        # Protocol elements
        self.tripod_height_before = QLineEdit()
        self.tripod_height_after = QLineEdit()
        self.tripod_pads_used = QLineEdit()
        self.sensor_cover_used = QCheckBox("Sensor head cover used")
        self.log = QPlainTextEdit(font=QFont("monospace"))
        self.time_warmup = QLineEdit()
        self.outdoor_measurement = QCheckBox("Outdoor measurement")
        self.dispenser_voltage = QLineEdit()
        self.atom_collection_problematic = QCheckBox("Problems with atom collection")
        self.collimator_sucessful = QCheckBox("Collimator calibration successful")
        self.collimator_repeated = QCheckBox(
            "Collimator calibration repeated after measurement"
        )
        self.tiltmeter_calibration_done = QCheckBox(
            "Accompanying tiltmeter calibration realized"
        )
        self.environmental_conditions = QLineEdit()
        self.operators = QLineEdit()

        # Protocol form
        protocol_form = QFormLayout()
        protocol_form.addRow(QLabel("Operators"), self.operators)
        protocol_form.addRow(QLabel("Duration of system warm-up"), self.time_warmup)
        protocol_form.addRow(None, self.outdoor_measurement)
        protocol_form.addRow(None, self.sensor_cover_used)
        protocol_form.addRow(
            QLabel("Number of tripod (rubber) pads used"), self.tripod_pads_used
        )
        protocol_form.addRow(QLabel("Dispenser voltage"), self.dispenser_voltage)
        protocol_form.addRow(QLabel("Tripod height before"), self.tripod_height_before)
        protocol_form.addRow(
            QLabel("Tripod height afterwards"), self.tripod_height_after
        )
        protocol_form.addRow(None, self.collimator_sucessful)
        protocol_form.addRow(None, self.collimator_repeated)
        protocol_form.addRow(None, self.atom_collection_problematic)
        protocol_form.addRow(
            QLabel("Environmental conditons (wind, precipitation, vibrations, etc.)"),
            self.environmental_conditions,
        )
        protocol_form.addRow(None, self.tiltmeter_calibration_done)
        protocol_form_widget = QWidget()
        protocol_form_widget.setLayout(protocol_form)

        # Protocol layout
        protocol_layout = QVBoxLayout()
        protocol_layout.addWidget(
            QLabel("Measurement protocol", font=QFont("sans", pointSize=14))
        )
        protocol_layout.addWidget(protocol_form_widget)
        protocol_layout.addWidget(QLabel("Journal"))
        protocol_layout.addWidget(self.log)
        self.protocol = QWidget()
        self.protocol.setLayout(protocol_layout)

        # Dashboard
        self.dash_label = QLabel("g = ...", font=QFont("monospace", pointSize=20))
        self.dash_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dashboard_layout = QVBoxLayout()
        dashboard_layout.setContentsMargins(0, 0, 0, 0)
        dashboard_layout.addWidget(self.dash_label)
        dashboard_layout.addWidget(self.graphs)
        dashboard = QWidget()
        dashboard.setLayout(dashboard_layout)

        # Splitter layout
        self.splitter = QSplitter()
        self.splitter.addWidget(self.paramtree)
        self.splitter.addWidget(dashboard)
        self.splitter.addWidget(self.protocol)
        self.splitter.setSizes([300, 800, 300])
        self.setCentralWidget(self.splitter)

        # Splitter toggle shortcut
        shortcut = QShortcut(QKeySequence("ctrl+i"), self)
        shortcut.activated.connect(self.on_toggle_paramtree)
        self._splitter_position, *_ = self.splitter.sizes()

        pen = pg.mkPen(color=COLORS[0])

        # Gravity
        self.plot1 = self.graphs.addPlot(
            colspan=2, axisItems={"bottom": pg.DateAxisItem()}
        )
        self.gravity = self.plot1.plot([], [], pen=pen)
        self.outliers = self.plot1.plot(
            [],
            [],
            pen=None,
            symbolPen=None,
            symbolBrush="r",
            symbolSize=4,
        )
        self.plot1.setLabel("left", "&Delta;g [nm/s²]")
        self.plot1.setLabel("bottom", "UTC")

        # Allan deviation
        self.plot2 = self.graphs.addPlot()
        self.plot2.setLogMode(True, True)
        self.adev = self.plot2.plot([], [], pen=pen)
        tau = np.array([10, 1e4])
        sensitivity = AQG_SENSITIVITY / np.sqrt(tau)
        self.plot2.plot(tau, sensitivity, pen=pg.mkPen(color="k", style=Qt.DashLine))
        self.plot2.setLabel("left", "Allan deviation &sigma; [nm/s²]")
        self.plot2.setLabel("bottom", "&tau; [s]")

        self.graphs.nextRow()

        # Atom number
        self.plot3 = self.graphs.addPlot(axisItems={"bottom": pg.DateAxisItem()})
        self.atoms = self.plot3.plot([], [], pen=pen)
        self.plot3.setLabel("left", "Atom number")

        # Tilt angles
        self.plot4 = self.graphs.addPlot(axisItems={"bottom": pg.DateAxisItem()})
        self.plot4.addLegend()
        self.plot4.setLabel("left", "Tilt angle [µrad]")
        self.tilts = [
            self.plot4.plot([], [], pen=pg.mkPen(color=color), name=name[0].upper())
            for color, name in zip(COLORS, TILTS)
        ]

        # Temperatures
        self.plot5 = self.graphs.addPlot(axisItems={"bottom": pg.DateAxisItem()})
        self.plot5.addLegend()
        self.plot5.setLabel("left", "Temperature [°C]")
        self.temperatures = [
            self.plot5.plot(
                [],
                [],
                pen=pg.mkPen(color=color),
                name=name.replace("_", " ").capitalize(),
            )
            for color, name in zip(COLORS, TEMPERATURES)
        ]

        # Link plot axes
        self.linked_plots = self.plot1, self.plot3, self.plot4, self.plot5
        for plot in self.linked_plots:
            plot.getViewBox().sigXRangeChanged.connect(
                partial(self.on_range_changed, plot)
            )

        for plot in (self.plot2, *self.linked_plots):
            plot.showGrid(x=True, y=True, alpha=0.3)
            plot.showAxes(True)
            plot.getViewBox().setBackgroundColor("w")

    def on_range_changed(self, plot, viewbox, view_range):
        if self._range_change:
            # Prevent recursive range change
            return
        try:
            self._range_change = True
            for other_plot in self.linked_plots:
                if other_plot is not plot:
                    other_plot.setXRange(*view_range, padding=0)
        finally:
            self._range_change = False

    def on_mouse_clicked(self, event):
        if event.double():
            self.auto_range()

    def auto_range(self):
        self.plot2.enableAutoRange()
        # The other plots are linked
        self.plot1.enableAutoRange()

    def on_open_raw_folder(self, button_state):
        directory = self.data_path.parent if self.data_path else Path.home()
        path = QFileDialog.getExistingDirectory(
            self, "Open AQG raw data folder", str(directory), QFileDialog.ShowDirsOnly
        )
        if not path:
            return
        self.open(path)
        self.auto_range()

    def on_open_raw_archive(self, button_state):
        directory = self.data_path.parent if self.data_path else Path.home()
        path, _ = QFileDialog.getOpenFileName(
            self, "Open AQG raw data archive", str(directory), filter="ZIP (*.zip)"
        )
        if not path:
            return
        self.open(path)
        self.auto_range()

    def on_open_processed_dataset(self, button_state):
        directory = self.data_path.parent if self.data_path else Path.home()
        path, _ = QFileDialog.getOpenFileName(
            self, "Open AQG processed dataset", str(directory), filter="NETCDF (*.nc)"
        )
        if not path:
            return
        self.open(path)
        self.auto_range()

    def on_save_report(self, button_state):
        if not self.dataset:
            return
        directory = self.data_path.parent if self.data_path else Path.home()
        # By default, this will ask for overwrite confirmation
        path, _ = QFileDialog.getSaveFileName(
            self, "Save AQG data report", str(directory), filter="PDF (*.pdf)"
        )
        if not path:
            return
        self.dataset.save_report(path)
        subprocess.call(("xdg-open", path))

    def on_save_protocol(self, button_state):
        directory = self.data_path.parent if self.data_path else Path.home()
        # By default, this will ask for overwrite confirmation
        path, _ = QFileDialog.getSaveFileName(
            self, "Save AQG measurement protocol", str(directory), filter="YAML (*.yml)"
        )
        if not path:
            return
        protocol = {
            "Operators": self.operators.text(),
            "Duration of system start-up / warm-up": self.time_warmup.text(),
            "Measurement outdoors": self.outdoor_measurement.isChecked(),
            "Tripod pads used": self.tripod_pads_used.text(),
            "Sensor cover used": self.sensor_cover_used.isChecked(),
            "Dispenser voltage": self.dispenser_voltage.text(),
            "Problems with atom collection": (
                self.atom_collection_problematic.isChecked()
            ),
            "Tripod height before measurement": self.tripod_height_before.text(),
            "Tripod height after measurement": self.tripod_height_after.text(),
            "Collimator calibration successful": self.collimator_sucessful.isChecked(),
            "Collimator calibration repeated after measurement": (
                self.collimator_repeated.isChecked()
            ),
            "Tiltmeter calibration realized": (
                self.tiltmeter_calibration_done.isChecked()
            ),
            "Environmental conditions (wind, precipitation, vibrations, etc.)": (
                self.environmental_conditions.text()
            ),
            "log": self.log.toPlainText(),
        }
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(protocol, f)

    def on_open_preferences(self, button_state):
        dialog = PreferencesDialog(self, preferences=self.preferences)
        if not dialog.exec():
            return
        logger.debug("Preferences changed")
        self.preferences.update(dialog.preferences)
        self.update()

    def on_toggle_paramtree(self):
        position, *_ = self.splitter.sizes()
        if position >= 80:
            # Collapse
            self.splitter.moveSplitter(0, 1)
            self._splitter_position = position
        else:
            # Expand to previous size
            self.splitter.moveSplitter(self._splitter_position, 1)

    def open(self, path):
        logger.info(f"Open {path}")

        path = Path(path)
        if path.suffix.lower() == ".nc":
            self.dataset = read_aqg_dataset(path)
        else:
            config_path = self.preferences.get("config_path")
            config = read_config(config_path) if config_path else {}
            self.dataset = process_aqg_raw_dataset(path, config=config)
        # Set data_path afterwards to keep old value, if reading dataset fails
        self.data_path = path

        self.setWindowTitle(f"AQG Dashboard - {self.data_path.name}")
        # Gravity
        g_mean = self.dataset.mean(h=None)
        height = self.preferences.get("height")
        self.dash_label.setText(f"g = {g_mean.transfer(height)}")
        delta_g = self.dataset.get("g") - float(g_mean)
        is_outlier = self.dataset.get("is_outlier")
        outliers = delta_g[is_outlier]
        set_timeseries_data(self.gravity, delta_g)
        set_timeseries_data(self.outliers, outliers)

        # Allan deviation
        adev = self.dataset.adev()
        self.adev.setData(adev.index.values, adev.values)

        # Atom number
        atoms = self.dataset.get("atoms_number").resample("10s").mean()
        set_timeseries_data(self.atoms, atoms)

        # Tilts
        for plot, name in zip(self.tilts, TILTS):
            # Convert rad to µrad
            set_timeseries_data(plot, self.dataset.get(name) * 1e6)

        # Temperatures
        for plot, name in zip(self.temperatures, TEMPERATURES):
            timeseries = (
                self.dataset.get(name + "_temperature").resample("10s").mean().dropna()
            )
            set_timeseries_data(plot, timeseries)

        total_uncertainty = sqrt(g_mean.error**2 + self.dataset.syst_uncertainty)

        results = [
            ro_param("Total drops", self.dataset.num_drops),
            ro_param(
                "Outliers",
                f"{self.dataset.num_outliers:,d} "
                + f"({self.dataset.num_outliers/self.dataset.num_drops:.1%})",
            ),
            ro_param("Gravity @ 1.25 m", g_mean.transfer(1.25).only_value),
            ro_param(f"Gravity @ {g_mean.height} m", g_mean.only_value),
            ro_param("Gravity @ 0 m", g_mean.transfer(0).only_value),
            # ro_param("syst. uncertainty", self.dataset.metadata["syst_uncertainty"]),
            ro_param("Systematic uncertainty", self.dataset.syst_uncertainty),
            ro_param("Statistical uncertainty", f"{g_mean.error:.1f} nm/s²"),
            ro_param("Total uncertainty", f"{total_uncertainty:.1f} nm/s²"),
        ]

        t0, t1 = self.dataset.get("is_outlier").index[[0, -1]]

        metadata_measurement = [
            # ro_param(key, value) for key, value in self.dataset.metadata.items()
            ro_param("Timespan", f"{t0:%F %H:%M} .. {t1:%F %H:%M} UTC"),
            ro_param("Duration", self.dataset.duration.round("1s")),
            ro_param("Location", self.dataset.metadata["location_name"]),
            ro_param(
                "Coordinates",
                f"{self.dataset.metadata['latitude']}, "
                + f"{self.dataset.metadata['longitude']}, "
                + f"{self.dataset.metadata['altitude']}",
            ),
            ro_param("Setname", self.dataset.metadata["name"]),
            ro_param("Point", self.dataset.point),
            ro_param(
                "Description (from AQG GUI)", self.dataset.metadata["description"]
            ),
            ro_param("Vertical gravity gradient", self.dataset.metadata["vgg"]),
            ro_param(
                "Pressure admittance", self.dataset.metadata["pressure_admittance"]
            ),
            ro_param("Name of tidal model", self.dataset.metadata["tide_model_name"]),
            ro_param("Comment (from config file)", self.dataset.comment),
        ]
        metadata_device = [
            ro_param("Meter", self.dataset.metadata["meter"]),
            ro_param("Software version", self.dataset.metadata["software"]),
            ro_param("Reference height", self.dataset.metadata["reference_height"]),
            ro_param("Tripod height", self.dataset.metadata["tripod_base_height"]),
            ro_param(
                "Factory height",
                self.dataset.metadata["instrument_factory_height"],
            ),
            ro_param("Sensor orientation [to North]", self.dataset.orientation),
            ro_param("Systematic instrument bias", self.dataset.metadata["dg_syst"]),
            ro_param(
                "Tiltmeter offset (x,y)",
                f"({self.dataset.metadata['tilt_offset_x']}, "
                + f"{self.dataset.metadata['tilt_offset_y']})",
            ),
        ]
        metadata_processing = [
            ro_param(
                "gravitools version", self.dataset.metadata["processing_software"]
            ),
            ro_param("Processing log", self.dataset.metadata["log"]),
        ]
        params = Parameter.create(
            name="params",
            type="group",
            children=[
                Parameter.create(name="Results", type="group", children=results),
                Parameter.create(
                    name="Measurement", type="group", children=metadata_measurement
                ),
                Parameter.create(
                    name="Instrument", type="group", children=metadata_device
                ),
                Parameter.create(
                    name="Processing", type="group", children=metadata_processing
                ),
            ],
        )
        self.paramtree.setParameters(params, showTop=False)

        if not self.timer and not self.data_path.name.endswith(".zip"):
            self.timer = QTimer()
            self.timer.setInterval(
                1000 * self.preferences.get("reload_interval", POLLING_INTERVAL)
            )
            self.timer.timeout.connect(self.update)
            self.timer.start()

    def update(self):
        if not self.data_path:
            return
        self.open(self.data_path)


def handle_sigint(*args):
    QApplication.quit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--height", type=float, default=STANDARD_HEIGHT)
    parser.add_argument("--config")
    parser.add_argument("path", nargs="?")
    args = parser.parse_args()

    logging.basicConfig(
        format="{asctime} [{levelname}] ({name}) {message}",
        style="{",
        datefmt="%T",
        level=logging.DEBUG,
    )
    for name in "fpdf", "matplotlib", "PIL":
        logging.getLogger(name).setLevel(logging.WARNING)

    signal.signal(signal.SIGINT, handle_sigint)

    app = QApplication([])
    win = MainWindow(height=args.height, config_path=args.config)
    win.show()

    def handle_exception(exc_type, exc_value, exc_traceback):
        error_dialog(win, exc_type, exc_value, exc_traceback)
        logger.error(
            f"{exc_type.__name__}: {exc_value}",
            exc_info=(exc_type, exc_value, exc_traceback),
        )

    sys.excepthook = handle_exception

    # Trigger event loop regularly to catch keyboard interrupts
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    if args.path:
        win.open(args.path)
        win.auto_range()

    app.exec()


if __name__ == "__main__":
    main()
