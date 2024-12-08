# Copyright (C) 2021,2022,2023,2024 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""md subcommand."""

import argparse
import logging
import sys

from txt2ebook.subcommands.parse import run as parse_txt
from txt2ebook.formats.typ import TypWriter
from txt2ebook.formats import PAGE_SIZES


logger = logging.getLogger(__name__)


def build_subparser(subparsers) -> None:
    """Build the subparser."""
    typ_parser = subparsers.add_parser(
        "typ", help="generate ebook in Typst format"
    )

    typ_parser.set_defaults(func=run)

    typ_parser.add_argument(
        "input_file",
        nargs=None if sys.stdin.isatty() else "?",  # type: ignore
        type=argparse.FileType("rb"),
        default=None if sys.stdin.isatty() else sys.stdin,
        help="source text filename",
        metavar="TXT_FILENAME",
    )

    typ_parser.add_argument(
        "output_file",
        nargs="?",
        default=None,
        help="converted ebook filename (default: 'TXT_FILENAME.typ')",
        metavar="EBOOK_FILENAME",
    )

    typ_parser.add_argument(
        "-pz",
        "--page-size",
        dest="page_size",
        default="a5",
        choices=PAGE_SIZES,
        help="page size of the ebook (default: '%(default)s')",
        metavar="PAGE_SIZE",
    )

    typ_parser.add_argument(
        "--toc",
        default=False,
        action=argparse.BooleanOptionalAction,
        dest="with_toc",
        help="add table of content",
    )

    typ_parser.add_argument(
        "-ik",
        "--index-keyword",
        dest="index_keyword",
        action="append",
        default=[],
        help="keyword to index (default: '%(default)s')",
    )

    typ_parser.add_argument(
        "-op",
        "--open",
        default=False,
        action="store_true",
        dest="open",
        help="open the generated file using default program",
    )


def run(args: argparse.Namespace) -> None:
    """Run typ subcommand.

    Args:
        config (argparse.Namespace): Config from command line arguments

    Returns:
        None
    """
    book = parse_txt(args)
    writer = TypWriter(book, args)
    writer.write()
