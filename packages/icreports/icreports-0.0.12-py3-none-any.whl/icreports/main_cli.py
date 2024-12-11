import os
import logging
import argparse
from pathlib import Path

from icreports.rendering import render_book

logger = logging.getLogger(__name__)


def render_book_cli(cli_args):

    source_dir = cli_args.source_dir.resolve()
    config_path = cli_args.config.resolve()
    if not config_path.exists():
        config_path = source_dir / "_config.yml"

    render_book(source_dir, cli_args.build_dir.resolve(), config_path, cli_args.rebuild)


def main_cli():

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)

    book_parser = subparsers.add_parser("book")
    book_parser.add_argument(
        "--source_dir",
        type=Path,
        default=Path(os.getcwd()),
        help="Path to the document sources",
    )
    book_parser.add_argument(
        "--config",
        type=Path,
        default=Path(os.getcwd()) / "_config.yml",
        help="Path to document config",
    )
    book_parser.add_argument(
        "--build_dir",
        type=Path,
        default=Path(os.getcwd()) / "_build",
        help="Path for build output",
    )
    book_parser.add_argument(
        "--rebuild",
        type=bool,
        default=True,
        help="If true do a clean rebuild of the book",
    )
    book_parser.set_defaults(func=render_book_cli)
    args = parser.parse_args()

    logging.basicConfig(encoding="utf-8", level=logging.INFO)

    args.func(args)


if __name__ == "__main__":

    main_cli()
