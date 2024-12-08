# Copyright (c) 2024 Kian-Meng Ang

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Generals Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""A console program to manipulate photos.

  website: https://github.com/kianmeng/fotolab
  changelog: https://github.com/kianmeng/fotolab/blob/master/CHANGELOG.md
  issues: https://github.com/kianmeng/fotolab/issues
"""

import argparse
import logging
import sys
from typing import Dict, Optional, Sequence

import fotolab.animate
import fotolab.auto
import fotolab.border
import fotolab.contrast
import fotolab.env
import fotolab.info
import fotolab.montage
import fotolab.resize
import fotolab.rotate
import fotolab.sharpen
import fotolab.watermark
from fotolab import __version__

log = logging.getLogger(__name__)


def setup_logging(args: argparse.Namespace) -> None:
    """Set up logging by level."""
    if args.verbose == 0:
        logging.getLogger("PIL").setLevel(logging.ERROR)

    if args.quiet:
        logging.disable(logging.NOTSET)
    else:
        conf: Dict = {
            True: {
                "level": logging.DEBUG,
                "msg": "[%(asctime)s] %(levelname)s: %(name)s: %(message)s",
            },
            False: {"level": logging.INFO, "msg": "%(message)s"},
        }

        logging.basicConfig(
            level=conf[args.debug]["level"],
            stream=sys.stdout,
            format=conf[args.debug]["msg"],
            datefmt="%Y-%m-%d %H:%M:%S",
        )


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        prog="fotolab",
        description=__doc__,
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(
            prog, max_help_position=20
        ),
    )

    parser.add_argument(
        "-o",
        "--overwrite",
        default=False,
        action="store_true",
        dest="overwrite",
        help="overwrite existing image",
    )

    parser.add_argument(
        "-op",
        "--open",
        default=False,
        action="store_true",
        dest="open",
        help="open the image using default program (default: '%(default)s')",
    )

    parser.add_argument(
        "-od",
        "--output-dir",
        dest="output_dir",
        default="output",
        help="set default output folder (default: '%(default)s')",
    )

    parser.add_argument(
        "-q",
        "--quiet",
        default=False,
        action="store_true",
        dest="quiet",
        help="suppress all logging",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        default=0,
        action="count",
        dest="verbose",
        help="show verbosity of debugging log, use -vv, -vvv for more details",
    )

    parser.add_argument(
        "-d",
        "--debug",
        default=False,
        action="store_true",
        dest="debug",
        help="show debugging log and stacktrace",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    subparsers = parser.add_subparsers(help="sub-command help")
    fotolab.animate.build_subparser(subparsers)
    fotolab.auto.build_subparser(subparsers)
    fotolab.border.build_subparser(subparsers)
    fotolab.contrast.build_subparser(subparsers)
    fotolab.info.build_subparser(subparsers)
    fotolab.resize.build_subparser(subparsers)
    fotolab.rotate.build_subparser(subparsers)
    fotolab.montage.build_subparser(subparsers)
    fotolab.sharpen.build_subparser(subparsers)
    fotolab.watermark.build_subparser(subparsers)
    fotolab.env.build_subparser(subparsers)

    return parser


def main(args: Optional[Sequence[str]] = None) -> None:
    """Run the main program flow."""
    args = args or sys.argv[1:]
    log.debug(args)

    try:
        parser = build_parser()
        if len(args) == 0:
            parser.print_help(sys.stderr)
        else:
            parsed_args = parser.parse_args(args)
            setup_logging(parsed_args)

            if hasattr(parsed_args, "func"):
                log.debug(parsed_args)
                parsed_args.func(parsed_args)
            else:
                parser.print_help(sys.stderr)

    except Exception as error:
        log.error(
            "error: %s",
            getattr(error, "message", str(error)),
            exc_info=("-d" in args or "--debug" in args),
        )

        raise SystemExit(1) from None
