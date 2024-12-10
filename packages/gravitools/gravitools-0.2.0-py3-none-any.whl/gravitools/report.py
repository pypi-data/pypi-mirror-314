"""Base functionality for PDF data reports"""

from __future__ import annotations

from contextlib import contextmanager
import datetime
import logging
from pathlib import Path
from tempfile import TemporaryDirectory

from PIL import Image
from fpdf import FPDF
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


# pylint: disable=too-many-instance-attributes
class PDF(FPDF):
    """PDF document customized for data reports

    Extends the methods of fpdf.FPDF with common report methods and default
    settings.

    Args:
        logo: Path to a logo image to include in the page header.
    """

    def __init__(self, *, logo: str = None, **kwargs):
        # Set units to millimeters so that all dimensions are consistent
        super().__init__(unit="mm", **kwargs)
        self.set_margins(left=25, top=12)

        # Additional parameters
        self.title_font_size = 16
        self.section_font_size = 14
        self.subsection_font_size = 12
        self.text_font_size = 10
        self.line_spacing = 1.3
        self.header_font_size = 8
        self.footer_font_size = self.header_font_size
        self.logo = logo
        self.logo_height = 12
        self.header_height = self.logo_height
        self.footer_height = self.b_margin

        # PDF metadata
        self.subject = ""

        self.alias_nb_pages()

        self.set_font("Helvetica")
        self.set_text_font()

        # Start first page
        self.add_page()

    @property
    def line_height(self) -> float:
        """Calculated text line height"""
        return self.line_spacing * self.font_size

    def set_text_font(self):
        """Set default font size"""
        self.set_font("Helvetica", size=self.text_font_size)

    def header(self):
        """Create header section on current page"""
        self.set_font("Helvetica", size=self.header_font_size)
        if self.logo:
            self.image(self.logo, self.l_margin, self.t_margin, h=self.logo_height)
        self.cell(0, 2 * self.font_size, "", ln=1)
        self.cell(0, self.font_size, f"{datetime.datetime.now().date()}", align="R")
        self.horizontal_rule(self.t_margin + self.header_height)
        self.set_y(self.t_margin + self.header_height)
        self.ln(h=5)
        self.set_text_font()

    def footer(self):
        """Create footer section on current page"""
        self.horizontal_rule(-self.footer_height)
        self.set_y(-self.footer_height)
        self.set_font("Helvetica", size=self.footer_font_size)
        self.ln(0.2 * self.line_height)
        self.cell(50, self.line_height, "Data report", align="L")
        self.cell(
            self.epw - 100,
            self.line_height,
            f"{self.subject}" if self.subject else "",
            align="C",
        )
        self.cell(50, self.line_height, f"Page {self.page_no()} of {{nb}}", align="R")

    def horizontal_rule(self, y: float):
        """Create a horizontal divider line"""
        if y < 0:
            y = self.h + y
        self.line(self.l_margin, y, self.l_margin + self.epw, y)

    def section(self, text: str, add_page: bool = True):
        """Create a section header"""
        if add_page:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_font("Helvetica", style="B", size=self.section_font_size)
        self.cell(0, self.line_height, text, align="L", ln=1)
        self.ln(0.5 * self.line_height)
        self.set_text_font()

    def subsection(self, text: str, add_page: bool = False):
        """Create a sub-section header"""
        if add_page:
            self.add_page()
        self.set_x(self.l_margin)
        self.set_font("Helvetica", style="B", size=self.subsection_font_size)
        self.cell(0, self.line_height, text, align="L", ln=1)
        self.set_text_font()

    def make_title(self, title: str, super_title: str = None):
        """Create the report title

        Args:
            title:
                The report title text.
            super_title:
                A smaller title above the main title, intended to state the
                report type.
        """
        if super_title:
            self.set_font("Helvetica", size=0.9 * self.title_font_size)
            self.cell(0, self.line_height, super_title, align="L", ln=1)

        self.set_font("Helvetica", style="B", size=self.title_font_size)
        self.cell(0, self.line_height, title, align="L", ln=1)
        self.ln(0.5 * self.line_height)
        self.set_text_font()

        # PDF metadata
        self.set_title(f"{super_title}: {title}" if super_title else title)
        self.set_subject(title)

    def insert_mpl_plot(self):
        """Insert the current Matplotlib plot"""
        dpi = plt.gcf().dpi
        with TemporaryDirectory() as tmp:
            plot_path = Path(tmp) / "plot.png"
            plt.savefig(plot_path, dpi=dpi, bbox_inches="tight")

            with Image.open(plot_path) as img:
                width_px, height_px = img.size

            # Scale image to real size
            # FPDF.k is the scaling factor to convert to point (pt) units.
            # See fpdf.utils.get_scale_factor
            scale = (72 / dpi) / self.k
            width_mm = int(scale * width_px)
            height_mm = int(scale * height_px)
            self.image(plot_path, w=width_mm, h=height_mm)


def plot(func):
    """Decorator marking report class methods as plots"""

    def make_plot(self, *args, **kwargs):
        with self.plot_context():
            func(self, *args, **kwargs)

    return make_plot


class Report:
    """Abstract base class for data reports

    Args:
        author:
            Report author.
    """

    def __init__(
        self,
        *,
        author: str = None,
        logo: str | Path = None,
        date: datetime.datetime = None,
    ):
        self.date = date or datetime.datetime.utcnow()
        self.pdf = PDF(logo=logo)
        if author:
            self.pdf.set_author(author)

        # Temporaty table parameters
        self._col_widths = None
        self._col_aligns = None

        # Default Matplotlib style settings
        self.rc_params = {
            "font.size": 8,
            "figure.dpi": 200,
            "figure.figsize": (6.8, 3),
            "grid.color": "#d0d0d0",
            "axes.grid": True,
            "axes.titlelocation": "left",
            "axes.xmargin": 0.02,
            "lines.markersize": 4,
            "date.autoformatter.month": "%b\n%Y",
            "date.autoformatter.day": "%-d %b",
            "date.autoformatter.hour": "%H:%M\n%-d %b",
            "date.autoformatter.minute": "%H:%M",
        }

        # Report was fully created
        self._is_done = False

    def body(self) -> None:
        """Create report contents"""
        # Placeholder method
        raise NotImplementedError

    def make(self) -> None:
        """Build the entire report"""
        if self._is_done:
            # Do not build twice
            return
        logger.info("Make report")
        self.body()
        self._is_done = True

    def save(self, path: str | Path) -> None:
        """Create report and save to file

        Args:
            path:
                Output path.
        """
        self.make()
        logger.info("Save report to %s", path)
        self.pdf.output(path)

    def title(self, title: str, super_title: str = None) -> None:
        """Create the title"""
        self.pdf.make_title(title, super_title=super_title)

    def section(self, heading: str) -> None:
        """Create a new section"""
        self.pdf.section(heading)

    def subsection(self, heading: str) -> None:
        """Create a new sub-section"""
        self.pdf.subsection(heading)

    def text(self, text: str) -> None:
        """Write a simple line of text"""
        self.pdf.cell(0, self.pdf.line_height, text)
        self.pdf.ln()

    @contextmanager
    def plot_context(self):
        """Context manager to insert a Matplotlib figure"""
        with plt.rc_context(self.rc_params):
            plt.figure()
            yield
            self.pdf.insert_mpl_plot()
            plt.close()

    @contextmanager
    def table(self, widths: list[float] = None, aligns: list[str] = None) -> None:
        """Context manager to create a table

        Args:
            widths:
                Column widths.
            aligns:
                Column alignments.
        """
        self._col_widths = widths
        self._col_aligns = aligns
        yield
        self._col_widths = None
        self._col_aligns = None

    def row(self, *cell_texts):
        """Create a table row"""
        prev_y = self.pdf.y
        max_cell_height = self.pdf.line_height
        for text, width, align in zip(cell_texts, self._col_widths, self._col_aligns):
            self.pdf.set_xy(self.pdf.x, prev_y)
            self.pdf.multi_cell(width, self.pdf.line_height, text, align=align)
            cell_height = self.pdf.y - prev_y
            max_cell_height = max(max_cell_height, cell_height)
        self.pdf.set_y(prev_y + max_cell_height)
