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

"""Animate subcommand."""

import argparse
import logging
from pathlib import Path

from PIL import Image

from fotolab import _open_image

log = logging.getLogger(__name__)


def build_subparser(subparsers) -> None:
    """Build the subparser."""
    animate_parser = subparsers.add_parser("animate", help="animate an image")

    animate_parser.set_defaults(func=run)

    animate_parser.add_argument(
        dest="image_filenames",
        help="set the image filenames",
        nargs="+",
        type=str,
        default=None,
        metavar="IMAGE_FILENAMES",
    )

    animate_parser.add_argument(
        "-f",
        "--format",
        dest="format",
        type=str,
        choices=["gif", "webp"],
        default="gif",
        help="set the image format (default: '%(default)s')",
        metavar="FORMAT",
    )

    animate_parser.add_argument(
        "-d",
        "--duration",
        dest="duration",
        type=int,
        default=2500,
        help="set the duration in milliseconds (default: '%(default)s')",
        metavar="DURATION",
    )

    animate_parser.add_argument(
        "-l",
        "--loop",
        dest="loop",
        type=int,
        default=0,
        help="set the loop cycle (default: '%(default)s')",
        metavar="LOOP",
    )


def run(args: argparse.Namespace) -> None:
    """Run animate subcommand.

    Args:
        config (argparse.Namespace): Config from command line arguments

    Returns:
        None
    """
    log.debug(args)

    first_image = args.image_filenames[0]
    animated_image = Image.open(first_image)

    append_images = []
    for image_filename in args.image_filenames[1:]:
        append_images.append(Image.open(image_filename))

    image_file = Path(first_image)
    new_filename = Path(
        args.output_dir,
        image_file.with_name(f"animate_{image_file.stem}.{args.format}"),
    )
    new_filename.parent.mkdir(parents=True, exist_ok=True)

    log.info("animate image: %s", new_filename)

    animated_image.save(
        new_filename,
        format=args.format,
        append_images=append_images,
        save_all=True,
        duration=args.duration,
        loop=args.loop,
        optimize=True,
    )

    if args.open:
        _open_image(new_filename)
