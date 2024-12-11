import argparse

from squeel.format_files import format_files


def squeel():
    parser = argparse.ArgumentParser(description="Squeel")
    parser.add_argument(
        "root_folder", help="The root folder to look for files to format"
    )
    parser.add_argument("--glob", type=str, help="Glob pattern")
    parser.add_argument(
        "--format_strategy",
        type=str,
        help="Format strategy, one of 'pg_format' or 'sqlparse' (default pg_format)",
    )
    args = parser.parse_args()

    glob = args.glob or "*.py"
    format_strategy = args.format_strategy or "pg_format"

    format_files(args.root_folder, glob, format_strategy)
