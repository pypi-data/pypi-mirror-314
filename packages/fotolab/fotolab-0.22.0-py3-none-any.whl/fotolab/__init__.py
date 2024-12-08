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

"""A console program that manipulate images."""

import logging
import os
import subprocess
import sys
from pathlib import Path

__version__ = "0.22.0"

log = logging.getLogger(__name__)


def save_image(args, new_image, output_filename, subcommand):
    """Save image after image operation.

    Args:
        args (argparse.Namespace): Config from command line arguments
        new_image(PIL.Image.Image): Modified image
        subcommand(str): Subcommand used to call this function

    Returns:
        None
    """
    image_file = Path(output_filename)

    if args.overwrite:
        new_filename = image_file.with_name(image_file.name)
    else:
        new_filename = Path(
            args.output_dir,
            image_file.with_name(f"{subcommand}_{image_file.name}"),
        )
        new_filename.parent.mkdir(parents=True, exist_ok=True)

    log.info("%s image: %s", subcommand, new_filename.resolve())
    new_image.save(new_filename)

    if args.open:
        _open_image(new_filename)


def _open_image(filename):
    """Open generated image using default program."""
    if sys.platform == "linux":
        subprocess.call(["xdg-open", filename])
    elif sys.platform == "darwin":
        subprocess.call(["open", filename])
    elif sys.platform == "windows":
        os.startfile(filename)

    log.info("open image: %s", filename.resolve())
