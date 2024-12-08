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

"""Watermark subcommand."""

import argparse
import logging
import math

from PIL import Image, ImageColor, ImageDraw, ImageFont

from fotolab import save_image
from fotolab.info import camera_metadata

log = logging.getLogger(__name__)

FONT_SIZE_ASPECT_RATIO = 12 / 600
FONT_PADDING_ASPECT_RATIO = 15 / 600
FONT_OUTLINE_WIDTH_ASPECT_RATIO = 2 / 600
POSITIONS = ["top-left", "top-right", "bottom-left", "bottom-right"]


def build_subparser(subparsers) -> None:
    """Build the subparser."""
    watermark_parser = subparsers.add_parser(
        "watermark", help="watermark an image"
    )

    watermark_parser.set_defaults(func=run)

    watermark_parser.add_argument(
        dest="image_filenames",
        help="set the image filenames",
        nargs="+",
        type=str,
        default=None,
        metavar="IMAGE_FILENAMES",
    )

    watermark_parser.add_argument(
        "-t",
        "--text",
        dest="text",
        help="set the watermark text (default: '%(default)s')",
        type=str,
        default="kianmeng.org",
        metavar="WATERMARK_TEXT",
    )

    watermark_parser.add_argument(
        "-p",
        "--position",
        dest="position",
        choices=POSITIONS,
        help="set position of the watermark text (default: '%(default)s')",
        default="bottom-left",
    )

    watermark_parser.add_argument(
        "-pd",
        "--padding",
        dest="padding",
        type=int,
        default=15,
        help=(
            "set the padding of the watermark text relative to the image "
            "(default: '%(default)s')"
        ),
        metavar="PADDING",
    )

    watermark_parser.add_argument(
        "-fs",
        "--font-size",
        dest="font_size",
        type=int,
        default=12,
        help="set the font size of watermark text (default: '%(default)s')",
        metavar="FONT_SIZE",
    )

    watermark_parser.add_argument(
        "-fc",
        "--font-color",
        dest="font_color",
        type=str,
        default="white",
        help="set the font color of watermark text (default: '%(default)s')",
        metavar="FONT_COLOR",
    )

    watermark_parser.add_argument(
        "-ow",
        "--outline-width",
        dest="outline_width",
        type=int,
        default=2,
        help=(
            "set the outline width of the watermark text "
            "(default: '%(default)s')"
        ),
        metavar="OUTLINE_WIDTH",
    )

    watermark_parser.add_argument(
        "-oc",
        "--outline-color",
        dest="outline_color",
        type=str,
        default="black",
        help=(
            "set the outline color of the watermark text "
            "(default: '%(default)s')"
        ),
        metavar="OUTLINE_COLOR",
    )

    watermark_parser.add_argument(
        "--camera",
        default=False,
        action="store_true",
        dest="camera",
        help="use camera metadata as watermark",
    )

    watermark_parser.add_argument(
        "-l",
        "--lowercase",
        default=True,
        action=argparse.BooleanOptionalAction,
        dest="lowercase",
        help="lowercase the watermark text",
    )


def run(args: argparse.Namespace) -> None:
    """Run watermark subcommand.

    Args:
        args (argparse.Namespace): Config from command line arguments

    Returns:
        None
    """
    log.debug(args)

    for image_filename in args.image_filenames:
        watermarked_image = watermark_image(image_filename, args)
        save_image(args, watermarked_image, image_filename, "watermark")


def watermark_image(image_filename, args):
    """Watermark the image."""
    original_image = Image.open(image_filename)
    watermarked_image = original_image.copy()

    draw = ImageDraw.Draw(watermarked_image)

    font = ImageFont.load_default(calc_font_size(original_image, args))
    log.debug("default font: %s", " ".join(font.getname()))

    text = args.text
    if args.camera and camera_metadata(image_filename):
        text = camera_metadata(image_filename)

    if args.lowercase:
        text = text.lower()

    (left, top, right, bottom) = draw.textbbox(xy=(0, 0), text=text, font=font)
    text_width = right - left
    text_height = bottom - top
    (position_x, position_y) = calc_position(
        watermarked_image,
        text_width,
        text_height,
        args.position,
        calc_padding(original_image, args),
    )

    draw.text(
        (position_x, position_y),
        text,
        font=font,
        fill=(*ImageColor.getrgb(args.font_color), 128),
        stroke_width=calc_font_outline_width(original_image, args),
        stroke_fill=(*ImageColor.getrgb(args.outline_color), 128),
    )
    return watermarked_image


def calc_font_size(image, args) -> int:
    """Calculate the font size based on the width of the image."""
    width, _height = image.size
    new_font_size = args.font_size
    if width > 600:
        new_font_size = math.floor(FONT_SIZE_ASPECT_RATIO * width)

    log.debug("new font size: %d", new_font_size)
    return new_font_size


def calc_font_outline_width(image, args) -> int:
    """Calculate the font padding based on the width of the image."""
    width, _height = image.size
    new_font_outline_width = args.outline_width
    if width > 600:
        new_font_outline_width = math.floor(
            FONT_OUTLINE_WIDTH_ASPECT_RATIO * width
        )

    log.debug("new font outline width: %d", new_font_outline_width)
    return new_font_outline_width


def calc_padding(image, args) -> int:
    """Calculate the font padding based on the width of the image."""
    width, _height = image.size
    new_padding = args.padding
    if width > 600:
        new_padding = math.floor(FONT_PADDING_ASPECT_RATIO * width)

    log.debug("new padding: %d", new_padding)
    return new_padding


def calc_position(image, text_width, text_height, position, padding) -> tuple:
    """Calculate the boundary coordinates of the watermark text."""
    (position_x, position_y) = (0, 0)

    if position == "top-left":
        position_x = 0 + padding
        position_y = 0 + padding
    elif position == "top-right":
        position_x = image.width - text_width - padding
        position_y = 0 + padding
    elif position == "bottom-left":
        position_x = 0 + padding
        position_y = image.height - text_height - padding
    elif position == "bottom-right":
        position_x = image.width - text_width - padding
        position_y = image.height - text_height - padding

    return (position_x, position_y)
