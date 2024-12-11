# Squeel

Format embedded sql (squeel) in python source code files.

Uses [treesitter](https://github.com/tree-sitter/tree-sitter) to query python strings inside the python files starting with a sql comment `-- sql`. Then formats the sql matching strings with the selected formatter, by default `pg_format`, and writes them back to the files.

Uses one of [sqlparse](https://github.com/andialbrecht/sqlparse) or [pg_format](https://github.com/darold/pgFormatter) to format the SQL within the python code.

## Requirements

`pgFormatter` if using the default format strategy `pg_format`

## Install

`pip install squeel`

## Usage

See `squeel -h`

Example:

```
squeel --glob *.py --format_strategy sqlparse src
```

