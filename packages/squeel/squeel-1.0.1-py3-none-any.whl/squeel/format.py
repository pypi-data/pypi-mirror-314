from enum import StrEnum
from typing import Literal
import sqlparse


class FormatStrategy(StrEnum):
    SQLPARSE = "sqlparse"
    PG_FORMAT = "pg_format"


def format_sql(
    content: bytes,
    strategy: FormatStrategy = FormatStrategy.SQLPARSE,
) -> bytes:
    match strategy:
        case FormatStrategy.SQLPARSE:
            return _sqlparse_format(content)
        case FormatStrategy.PG_FORMAT:
            return _pg_format(content)
        case _:
            raise Exception("Invalid format strategy provided")


def _sqlparse_format(
    content: bytes | str,
    keyword_case: Literal["upper", "lower", "capitalize"] = "upper",
    identifier_case: Literal["upper", "lower", "capitalize"] = "lower",
    reindent: bool = True,
    reindent_aligned: bool = False,
    indent_width: int = 4,
    wrap_after: int | None = None,
):
    optional_args = {}
    if wrap_after is not None:
        optional_args["wrap_after"] = wrap_after

    return sqlparse.format(
        content,
        keyword_case=keyword_case,
        indentifier_case=identifier_case,
        reindent=reindent,
        reindent_aligned=reindent_aligned,
        indent_width=indent_width,
        output_format="sql",
        **optional_args,
    ).strip()


def _pg_format(content: bytes):
    import subprocess

    try:
        result = subprocess.run(
            ["pg_format"],
            input=content,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if result.returncode != 0:
            print(f"Error: {result.stderr.decode()}")
            return None

        return result.stdout
    except FileNotFoundError:
        print("Error: pg_format is not installed or not in PATH.")
        return None
