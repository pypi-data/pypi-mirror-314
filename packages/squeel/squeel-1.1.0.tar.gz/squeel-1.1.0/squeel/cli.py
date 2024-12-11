import argparse

from squeel.format_files import format_files


def squeel():
    parser = argparse.ArgumentParser(description="Squeel")
    parser.add_argument(
        "root_folder", help="The root folder to look for files to format"
    )
    parser.add_argument("--change", help="Dry run", action="store_true", default=False)
    parser.add_argument("--glob", type=str, help="Glob pattern")
    parser.add_argument(
        "--format_strategy",
        type=str,
        help="Format strategy, one of 'pg_format' or 'sqlparse' (default pg_format)",
    )
    args = parser.parse_args()

    glob = args.glob or "*.py"
    dry_run = not args.change
    format_strategy = args.format_strategy or "pg_format"

    if dry_run:
        print("-- DRY RUN -- No actual changes will be made.")

    format_files(args.root_folder, glob, format_strategy, dry_run)
