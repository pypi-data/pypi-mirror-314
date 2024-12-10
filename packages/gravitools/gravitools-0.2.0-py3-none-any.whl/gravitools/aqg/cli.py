from argparse import ArgumentParser
import logging
from pathlib import Path

import yaml

from ..corrections import update_eop_data
from .rawdata import process_aqg_raw_dataset

logger = logging.getLogger(__name__)


def main(args=None):
    parser = ArgumentParser(description="AQG raw data processing")
    parser.add_argument("--outputdir", "-o", default=".", help="Data output directory")
    parser.add_argument("--config", "-c", default="", help="Path to configuration file")
    parser.add_argument(
        "--overwrite",
        "-f",
        action="store_true",
        help="Allow overwriting output files",
    )
    parser.add_argument(
        "--query-eop", "-q", action="store_true", help="Download EOP data from iers.org"
    )
    parser.add_argument(
        "--pdf", action="store_true", help="Create a PDF data report for each dataset"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        default=0,
        action="count",
        help="Level of output verbosity",
    )
    parser.add_argument("datapaths", nargs="+", help="Paths to input data")

    args = parser.parse_args(args)
    outputdir = Path(args.outputdir)
    if not outputdir.is_dir():
        raise NotADirectoryError(outputdir)

    loglevel = logging.WARNING - 10 * args.verbose
    logging.basicConfig(level=loglevel, format="[{levelname[0]}] {message}", style="{")
    for name in "matplotlib", "PIL", "fpdf":
        logging.getLogger(name).setLevel(logging.WARNING)

    config = {}
    if args.config:
        logging.info(f"Read configuration: {args.config}")
        with open(args.config, encoding="utf-8") as f:
            config = yaml.load(f.read(), Loader=yaml.CLoader)

    if args.query_eop:
        update_eop_data()

    for path in args.datapaths:
        path = Path(path)
        name = path.stem
        nc_path = outputdir / f"{name}.nc"
        if nc_path.exists() and not args.overwrite:
            logging.warning(f"Skipping {path.name} because {nc_path} exists already.")
            continue

        dataset = process_aqg_raw_dataset(path, config=config, name=name)
        dataset.to_nc(nc_path)
        if args.pdf:
            dataset.save_report(outputdir / f"{name}.pdf")
