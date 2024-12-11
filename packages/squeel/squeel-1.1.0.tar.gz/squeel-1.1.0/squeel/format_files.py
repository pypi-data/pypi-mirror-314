from pathlib import Path
from dataclasses import dataclass
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

from squeel.format import FormatStrategy, format_sql
from squeel.utils import find_current_line_whitespace

PY_LANGUAGE = Language(tspython.language())
CAPTURE_PATTERN = "python_sql_string"

parser = Parser(PY_LANGUAGE)
query = PY_LANGUAGE.query(
    r"""
    (
      string
         (string_start) @_s_start (#match? @_s_start "[\"\'][\"\'][\"\']")
         (string_content) @python_sql_string
            (#match? @python_sql_string "^\\s+--\\s+[sS][qQ][lL]")
         (string_end) @_s_end (#match? @_s_end "[\"\'][\"\'][\"\']")
    )
    """
)


@dataclass
class FormattedChunk:
    start_byte: int
    end_byte: int
    formatted_bytes: bytes
    indent: bytes


@dataclass
class FileCaptures:
    file: str
    formatted: int
    unchanged: int


def format_files(
    dir: str,
    pattern: str,
    format_strategy: FormatStrategy,
    dry_run: bool = True,
    encoding: str | None = None,
):
    total_files = 0
    files_formatted: list[FileCaptures] = []
    for file in Path(dir).rglob(pattern):
        with open(file, "r+b", encoding=encoding) as f:
            total_files += 1
            content = f.read()
            tree = parser.parse(content)

            caps = query.captures(tree.root_node)
            if CAPTURE_PATTERN not in caps:
                continue

            formatted_chunks: list[FormattedChunk] = []
            file_captures: int = 0
            unchanged: int = 0

            for c in caps[CAPTURE_PATTERN]:
                raw_bytes = content[c.start_byte : c.end_byte]
                formatted_bytes = format_sql(
                    content[c.start_byte : c.end_byte],
                    strategy=FormatStrategy.PG_FORMAT,
                )

                if raw_bytes == formatted_bytes:
                    unchanged += 1
                    continue

                indent = find_current_line_whitespace(content, c.start_byte)
                formatted_chunks.append(
                    FormattedChunk(
                        c.start_byte,
                        c.end_byte,
                        format_sql(
                            content[c.start_byte : c.end_byte],
                            strategy=format_strategy,
                        ),
                        indent,
                    )
                )
                file_captures += 1

            if not file_captures:
                continue

            if not dry_run:
                for i in range(len(formatted_chunks)):
                    chunk = formatted_chunks[-i]
                    end = content[chunk.end_byte :]

                    content = content[: chunk.start_byte]

                    lines = chunk.formatted_bytes.splitlines()

                    content = content + lines[0]  # the -- sql comment line

                    for line in lines[1:]:
                        content = content + b"\n" + indent + b"    " + line

                    content = content + b"\n" + end

            f.seek(0)
            f.write(content)
            f.truncate()

            files_formatted.append(FileCaptures(str(file), file_captures, unchanged))

    if not total_files:
        print("No files were found matching the glob pattern.")
        return

    print(f"Found {total_files} files matching the glob pattern.")

    if not files_formatted:
        print("No changes was made, files up to date!")
        return

    print(f"{"Would format" if dry_run else "Formatted"} {len(files_formatted)} files:")

    for file_report in files_formatted:
        print(
            f"{file_report.file}: {file_report.formatted} sql strings {"to be " if dry_run else ""}changed, {file_report.unchanged} unchanged."
        )
