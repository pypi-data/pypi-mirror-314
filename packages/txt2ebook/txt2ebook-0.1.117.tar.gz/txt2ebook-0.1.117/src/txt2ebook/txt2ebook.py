# pylint: disable=no-value-for-parameter
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

"""txt2ebook/tte is a cli tool to convert txt file to ebook format.

  website: https://github.com/kianmeng/txt2ebook
  changelog: https://github.com/kianmeng/txt2ebook/blob/master/CHANGELOG.md
  issues: https://github.com/kianmeng/txt2ebook/issues
"""

import argparse
import datetime
import logging
import sys
import time
from typing import Optional, Sequence

from bs4 import UnicodeDammit

from txt2ebook import __version__, print_env, setup_logger, detect_and_expect_language
from txt2ebook.exceptions import EmptyFileError
from txt2ebook.formats import (
    EBOOK_FORMATS,
    EPUB_TEMPLATES,
    PAGE_SIZES,
    create_format,
)
from txt2ebook.parser import Parser

logger = logging.getLogger(__name__)


def run(config: argparse.Namespace) -> None:
    """Set the main application logic."""
    logger.debug(config)

    if config.env:
        print_env()
    else:
        logger.info("Parsing txt file: %s", config.input_file.name)

        unicode = UnicodeDammit(config.input_file.read())
        logger.info("Detect encoding : %s", unicode.original_encoding)

        content = unicode.unicode_markup
        if not content:
            raise EmptyFileError(
                f"Empty file content in {config.input_file.name}"
            )

        config.language = detect_and_expect_language(content, config.language)
        parser = Parser(content, config)
        book = parser.parse()

        if config.test_parsing or config.debug:
            book.debug(config.verbose)

        config.format = config.format or ["epub"]
        if not config.test_parsing:
            if book.toc:
                for ebook_format in config.format:
                    writer = create_format(book, ebook_format, config)
                    writer.write()
            else:
                logger.warning("No table of content found, not exporting")


def build_parser(
    args: Optional[Sequence[str]] = None,
) -> argparse.ArgumentParser:
    """Generate the argument parser."""
    args = args or []

    parser = argparse.ArgumentParser(
        prog="txt2ebook",
        add_help=False,
        description=__doc__,
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(
            prog, max_help_position=6
        ),
    )

    epub = parser.add_argument_group("--format epub")
    pdf = parser.add_argument_group("--format pdf")
    txt = parser.add_argument_group("--format txt")
    tex = parser.add_argument_group("--format tex")
    zhlang = parser.add_argument_group("--language zh-cn / --language zh-tw")

    if "--env" not in args:
        parser.add_argument(
            "input_file",
            nargs=None if sys.stdin.isatty() else "?",  # type: ignore
            type=argparse.FileType("rb"),
            default=None if sys.stdin.isatty() else sys.stdin,
            help="source text filename",
            metavar="TXT_FILENAME",
        )

        parser.add_argument(
            "output_file",
            nargs="?",
            default=None,
            help="converted ebook filename (default: 'TXT_FILENAME.epub')",
            metavar="EBOOK_FILENAME",
        )

    parser.add_argument(
        "-of",
        "--output-folder",
        dest="output_folder",
        default="output",
        help="set default output folder (default: '%(default)s')",
    )

    parser.add_argument(
        "-p",
        "--purge",
        default=False,
        action="store_true",
        dest="purge",
        help=(
            "remove converted ebooks specified by --output-folder option "
            "(default: '%(default)s')"
        ),
    )

    parser.add_argument(
        "-f",
        "--format",
        dest="format",
        choices=EBOOK_FORMATS,
        action="append",
        help="ebook format (default: 'epub')",
    )

    parser.add_argument(
        "-ik",
        "--index-keyword",
        dest="index_keyword",
        action="append",
        default=[],
        help="keyword to index (default: '%(default)s')",
    )

    parser.add_argument(
        "-t",
        "--title",
        dest="title",
        default=None,
        help="title of the ebook (default: '%(default)s')",
        metavar="TITLE",
    )

    parser.add_argument(
        "-l",
        "--language",
        dest="language",
        default=None,
        help="language of the ebook (default: '%(default)s')",
        metavar="LANGUAGE",
    )

    parser.add_argument(
        "-a",
        "--author",
        dest="author",
        default=[],
        action="append",
        help="author of the ebook (default: '%(default)s')",
        metavar="AUTHOR",
    )

    parser.add_argument(
        "-tr",
        "--translator",
        dest="translator",
        default=[],
        action="append",
        help="translator of the ebook (default: '%(default)s')",
        metavar="TRANSLATOR",
    )

    epub.add_argument(
        "-c",
        "--cover",
        dest="cover",
        default=None,
        help="cover of the ebook",
        metavar="IMAGE_FILENAME",
    )

    txt.add_argument(
        "-w",
        "--width",
        dest="width",
        type=int,
        default=None,
        help="width for line wrapping",
        metavar="WIDTH",
    )

    parser.add_argument(
        "-ff",
        "--filename-format",
        dest="filename_format",
        type=int,
        default=None,
        help=(
            "the output filename format "
            "(default: TXT_FILENAME [EBOOK_FILENAME])\n"
            "1 - title_authors.EBOOK_EXTENSION\n"
            "2 - authors_title.EBOOK_EXTENSION"
        ),
        metavar="FILENAME_FORMAT",
    )

    parser.add_argument(
        "-ps",
        "--paragraph_separator",
        dest="paragraph_separator",
        type=lambda value: value.encode("utf-8").decode("unicode_escape"),
        default="\n\n",
        help="paragraph separator (default: %(default)r)",
        metavar="SEPARATOR",
    )

    pdf.add_argument(
        "-pz",
        "--page-size",
        dest="page_size",
        default="a5",
        choices=PAGE_SIZES,
        help="page size of the ebook (default: '%(default)s')",
        metavar="PAGE_SIZE",
    )

    parser.add_argument(
        "-rd",
        "--regex-delete",
        dest="re_delete",
        default=[],
        action="append",
        help="regex to delete word or phrase (default: '%(default)s')",
        metavar="REGEX",
    )

    parser.add_argument(
        "-rvc",
        "--regex-volume-chapter",
        dest="re_volume_chapter",
        default=[],
        action="append",
        help=(
            "regex to parse volume and chapter header "
            "(default: by LANGUAGE)"
        ),
        metavar="REGEX",
    )

    parser.add_argument(
        "-rv",
        "--regex-volume",
        dest="re_volume",
        default=[],
        action="append",
        help="regex to parse volume header (default: by LANGUAGE)",
        metavar="REGEX",
    )

    parser.add_argument(
        "-rc",
        "--regex-chapter",
        dest="re_chapter",
        default=[],
        action="append",
        help="regex to parse chapter header (default: by LANGUAGE)",
        metavar="REGEX",
    )

    parser.add_argument(
        "-rt",
        "--regex-title",
        dest="re_title",
        default=[],
        action="append",
        help="regex to parse title of the book (default: by LANGUAGE)",
        metavar="REGEX",
    )

    parser.add_argument(
        "-ra",
        "--regex-author",
        dest="re_author",
        default=[],
        action="append",
        help="regex to parse author of the book (default: by LANGUAGE)",
        metavar="REGEX",
    )

    parser.add_argument(
        "-rl",
        "--regex-delete-line",
        dest="re_delete_line",
        default=[],
        action="append",
        help="regex to delete whole line (default: '%(default)s')",
        metavar="REGEX",
    )

    parser.add_argument(
        "-rr",
        "--regex-replace",
        dest="re_replace",
        nargs=2,
        default=[],
        action="append",
        help="regex to search and replace (default: '%(default)s')",
        metavar="REGEX",
    )

    tex.add_argument(
        "-ct",
        "--clean-tex",
        default=False,
        action="store_true",
        dest="clean_tex",
        help="purge artifacts generated by TeX (default: '%(default)s')",
    )

    epub.add_argument(
        "-et",
        "--epub-template",
        default="clean",
        choices=EPUB_TEMPLATES,
        dest="epub_template",
        help="CSS template for epub ebook (default: '%(default)s')",
    )

    epub.add_argument(
        "-vp",
        "--volume-page",
        default=False,
        action="store_true",
        dest="volume_page",
        help="generate each volume as separate page",
    )

    parser.add_argument(
        "-tp",
        "--test-parsing",
        default=False,
        action="store_true",
        dest="test_parsing",
        help="test parsing for volume/chapter header",
    )

    txt.add_argument(
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

    parser.add_argument(
        "-ss",
        "--sort-volume-and-chapter",
        default=False,
        action="store_true",
        dest="sort_volume_and_chapter",
        help="short volume and chapter",
    )

    txt.add_argument(
        "-toc",
        "--table-of-content",
        default=False,
        action="store_true",
        dest="with_toc",
        help="add table of content",
    )

    zhlang.add_argument(
        "-hn",
        "--header-number",
        default=False,
        action="store_true",
        dest="header_number",
        help="convert section header from words to numbers",
    )

    zhlang.add_argument(
        "-fw",
        "--fullwidth",
        default=False,
        action="store_true",
        dest="fullwidth",
        help="convert ASCII character from halfwidth to fullwidth",
    )

    parser.add_argument(
        "-rw",
        "--raise-on-warning",
        default=False,
        action="store_true",
        dest="raise_on_warning",
        help="raise exception and stop parsing upon warning",
    )

    parser.add_argument(
        "-ow",
        "--overwrite",
        default=False,
        action="store_true",
        dest="overwrite",
        help="overwrite massaged TXT_FILENAME",
    )

    parser.add_argument(
        "-op",
        "--open",
        default=False,
        action="store_true",
        dest="open",
        help="open the generated file using default program",
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
        "-y",
        "--yes",
        default=False,
        action="store_true",
        dest="yes",
        help="yes to prompt",
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
        "--env",
        default=False,
        action="store_true",
        dest="env",
        help="print environments information for bug reporting",
    )

    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="show this help message and exit",
    )

    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    return parser


def main(args: Optional[Sequence[str]] = None):
    """Set the main entrypoint of the CLI script."""
    args = args or sys.argv[1:]
    config = argparse.Namespace()

    try:
        parser = build_parser(args)
        config = parser.parse_args(args)
        logger.debug(config)

        setup_logger(config)

        start_time = time.time()
        run(config)
        end_time = time.time()
        elapsed_time = end_time - start_time
        timedelta = datetime.timedelta(seconds=elapsed_time)
        logger.info("Time taken: %s", timedelta)

    except Exception as error:
        logger.error(
            getattr(error, "message", str(error)),
            exc_info=("-d" in args or "--debug" in args),
        )
        raise SystemExit(1) from None
