# Copyright (C) 2024 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""Border subcommand."""

import argparse
import logging

from PIL import Image, ImageColor, ImageOps

from fotolab import save_image

log = logging.getLogger(__name__)


def build_subparser(subparsers) -> None:
    """Build the subparser."""
    border_parser = subparsers.add_parser("border", help="add border to image")

    border_parser.set_defaults(func=run)

    border_parser.add_argument(
        dest="image_filenames",
        help="set the image filenames",
        nargs="+",
        type=str,
        default=None,
        metavar="IMAGE_FILENAMES",
    )

    border_parser.add_argument(
        "-c",
        "--color",
        dest="color",
        type=str,
        default="black",
        help="set the color of border (default: '%(default)s')",
        metavar="COLOR",
    )

    border_parser.add_argument(
        "-w",
        "--width",
        dest="width",
        type=str,
        default=10,
        help="set the width of border (default: '%(default)s')",
        metavar="WIDTH",
    )

    border_parser.add_argument(
        "-wt",
        "--width-top",
        dest="width_top",
        type=str,
        default=0,
        help="set the width of top border (default: '%(default)s')",
        metavar="WIDTH",
    )

    border_parser.add_argument(
        "-wr",
        "--width-right",
        dest="width_right",
        type=str,
        default=0,
        help="set the width of right border (default: '%(default)s')",
        metavar="WIDTH",
    )

    border_parser.add_argument(
        "-wb",
        "--width-bottom",
        dest="width_bottom",
        type=str,
        default=0,
        help="set the width of bottom border (default: '%(default)s')",
        metavar="WIDTH",
    )

    border_parser.add_argument(
        "-wl",
        "--width-left",
        dest="width_left",
        type=str,
        default=0,
        help="set the width of left border (default: '%(default)s')",
        metavar="WIDTH",
    )


def run(args: argparse.Namespace) -> None:
    """Run border subcommand.

    Args:
        config (argparse.Namespace): Config from command line arguments

    Returns:
        None
    """
    log.debug(args)

    for image_filename in args.image_filenames:
        original_image = Image.open(image_filename)

        if (
            args.width_left
            or args.width_top
            or args.width_right
            or args.width_bottom
        ):
            border = (
                int(args.width_left),
                int(args.width_top),
                int(args.width_right),
                int(args.width_bottom),
            )
        else:
            border = args.width

        bordered_image = ImageOps.expand(
            original_image,
            border=border,
            fill=ImageColor.getrgb(args.color),
        )

        save_image(args, bordered_image, image_filename, "watermark")
