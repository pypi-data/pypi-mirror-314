# Squeel

Format embedded sql (squeel) in python source code files.

Uses [treesitter](https://github.com/tree-sitter/tree-sitter) to query python strings inside the python files starting with a sql comment `-- sql`. Then formats the sql matching strings with the selected formatter, by default `pg_format`, and writes them back to the files.

Uses one of [sqlparse](https://github.com/andialbrecht/sqlparse) or [pg_format](https://github.com/darold/pgFormatter) to format the SQL within the python code.

## Warning

This is an experimental tool.

Its purpose is to change files on your system. I recommend checking your changes into git before running this tool in case it explodes. Ensure you give it the appropriate root_folder and glob patterns so it doesn't change files on your system that you don't want changed. No changes will be written to any files unless you supply the `--change` flag. The default behaviou is to dry run.

```
$ squeel .      
-- DRY RUN -- No actual changes will be made.
Found 42 files matching the glob pattern.
Would format 1 files:
test/data/test-1.py: 1 sql strings to be changed, 0 unchanged.
```

## Requirements

`pgFormatter` if using the default format strategy `pg_format`

## Install

`pip install squeel`

## Usage

See `squeel -h`

```
squeel -h
usage: squeel [-h] [--change] [--glob GLOB] [--format_strategy FORMAT_STRATEGY] root_folder

Squeel

positional arguments:
  root_folder           The root folder to look for files to format

options:
  -h, --help            show this help message and exit
  --change              Dry run
  --glob GLOB           Glob pattern
  --format_strategy FORMAT_STRATEGY
                        Format strategy, one of 'pg_format' or 'sqlparse' (default pg_format)
```

Example run:

```
squeel --glob *.py --format_strategy sqlparse --change src
```

