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

"""Env subcommand."""

import argparse
import logging
import sys

import cjkwrap
import regex as re
from bs4 import UnicodeDammit

from txt2ebook import detect_and_expect_language
from txt2ebook.exceptions import EmptyFileError
from txt2ebook.formats.txt import TxtWriter
from txt2ebook.parser import Parser
from txt2ebook.zh_utils import zh_halfwidth_to_fullwidth

logger = logging.getLogger(__name__)


def build_subparser(subparsers) -> None:
    """Build the subparser."""
    massage_parser = subparsers.add_parser(
        "massage", help="massage the source txt file"
    )

    massage_parser.add_argument(
        "input_file",
        nargs=None if sys.stdin.isatty() else "?",  # type: ignore
        type=argparse.FileType("rb"),
        default=None if sys.stdin.isatty() else sys.stdin,
        help="source text filename",
        metavar="TXT_FILENAME",
    )

    massage_parser.add_argument(
        "output_file",
        nargs="?",
        default=None,
        help="converted ebook filename (default: 'TXT_FILENAME.txt')",
        metavar="EBOOK_FILENAME",
    )

    massage_parser.add_argument(
        "-sp",
        "--split-volume-and-chapter",
        default=False,
        action="store_true",
        dest="split_volume_and_chapter",
        help=(
            "split volume or chapter into separate file and "
            "ignore the --overwrite option"
        ),
    )

    massage_parser.add_argument(
        "-ow",
        "--overwrite",
        default=False,
        action="store_true",
        dest="overwrite",
        help="overwrite massaged TXT_FILENAME",
    )

    massage_parser.add_argument(
        "-rd",
        "--regex-delete",
        dest="re_delete",
        default=[],
        action="append",
        help="regex to delete word or phrase (default: '%(default)s')",
        metavar="REGEX",
    )

    massage_parser.add_argument(
        "-rr",
        "--regex-replace",
        dest="re_replace",
        nargs=2,
        default=[],
        action="append",
        help="regex to search and replace (default: '%(default)s')",
        metavar="REGEX",
    )

    massage_parser.add_argument(
        "-rl",
        "--regex-delete-line",
        dest="re_delete_line",
        default=[],
        action="append",
        help="regex to delete whole line (default: '%(default)s')",
        metavar="REGEX",
    )

    massage_parser.add_argument(
        "-w",
        "--width",
        dest="width",
        type=int,
        default=None,
        help="width for line wrapping",
        metavar="WIDTH",
    )

    massage_parser.add_argument(
        "-ss",
        "--sort-volume-and-chapter",
        default=False,
        action="store_true",
        dest="sort_volume_and_chapter",
        help="short volume and chapter",
    )

    massage_parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> None:
    """Run massage subcommand.

    Args:
        args (argparse.Namespace): args.from command line arguments

    Returns:
        None
    """
    massaged_txt = massage_txt(args)
    args.language = detect_and_expect_language(massaged_txt, args.language)
    args.with_toc = False
    parser = Parser(massaged_txt, args)
    book = parser.parse()

    if args.debug:
        book.debug(args.verbose)

    writer = TxtWriter(book, args)
    writer.write()


def massage_txt(args: argparse.Namespace) -> str:
    """Massage the text file."""
    logger.info("Parsing txt file: %s", args.input_file.name)

    unicode = UnicodeDammit(args.input_file.read())
    logger.info("Detect encoding : %s", unicode.original_encoding)

    content = unicode.unicode_markup
    if not content:
        raise EmptyFileError(
            f"Empty file content in {args.input_file.name}"
        )

    content = to_unix_newline(content)

    if args.fullwidth and args.language in ("zh-cn", "zh-tw"):
        logger.info("Convert halfwidth ASCII characters to fullwidth")
        content = zh_halfwidth_to_fullwidth(content)

    if args.re_delete:
        content = do_delete_regex(args, content)

    if args.re_replace:
        content = do_replace_regex(args, content)

    if args.re_delete_line:
        content = do_delete_line_regex(args, content)

    if args.width:
        content = do_wrapping(args, content)

    return content


def to_unix_newline(content: str) -> str:
    """Convert all other line ends to Unix line end.

    Args:
        content(str): The formatted book content.

    Returns:
        str: The formatted book content.
    """
    return content.replace("\r\n", "\n").replace("\r", "\n")


def do_delete_regex(args, content: str) -> str:
    """Remove words/phrases based on regex.

    Args:
        content(str): The formatted book content.

    Returns:
        str: The formatted book content.
    """
    for delete_regex in args.re_delete:
        content = re.sub(
            re.compile(rf"{delete_regex}", re.MULTILINE), "", content
        )
    return content


def do_replace_regex(args, content: str) -> str:
    """Replace words/phrases based on regex.

    Args:
        content(str): The formatted book content.

    Returns:
        str: The formatted book content.
    """
    regex = args.re_replace
    if isinstance(regex, list):
        for search, replace in regex:
            content = re.sub(
                re.compile(rf"{search}", re.MULTILINE),
                rf"{replace}",
                content,
            )

    return content


def do_delete_line_regex(args, content: str) -> str:
    """Delete whole line based on regex.

    Args:
        content(str): The formatted book content.

    Returns:
        str: The formatted book content.
    """
    for delete_line_regex in args.re_delete_line:
        content = re.sub(
            re.compile(rf"^.*{delete_line_regex}.*$", re.MULTILINE),
            "",
            content,
        )
    return content


def do_wrapping(args, content: str) -> str:
    """Wrap or fill CJK text.

    Args:
        content (str): The formatted book content.

    Returns:
        str: The formatted book content.
    """
    logger.info("Wrapping paragraph to width: %s", args.width)

    paragraphs = []
    # We don't remove empty line and keep all formatting as it.
    for paragraph in content.split("\n"):
        paragraph = paragraph.strip()

        lines = cjkwrap.wrap(paragraph, width=args.width)
        paragraph = "\n".join(lines)
        paragraphs.append(paragraph)

    wrapped_content = "\n".join(paragraphs)
    return wrapped_content
