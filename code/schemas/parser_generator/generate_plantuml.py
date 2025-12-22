#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause

import argparse
import csv
import io
import re
import sys


ID_REGEX = r"^[a-zA-Z_]\w*$"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("layout_csv", default=sys.stdin)
    parser.add_argument("plantuml_file", default=sys.stdout)
    args = parser.parse_args()

    if not args.layout_csv or args.layout_csv == "-":
        source_fd = sys.stdin
    else:
        source_fd = open(args.layout_csv, "r")

    result = io.StringIO("@startuml\n")

    with source_fd:
        reader = csv.DictReader(source_fd)
        for line_num, record in enumerate(reader, start=2):
            try:
                validate_record(line_num, record)
            except ValueError as err:
                print(str(err), file=sys.stderr)
                sys.exit(1)

            if record["action"]:
                result.write("{from} --> {to} : {action}\n".format_map(record))
            else:
                result.write("{from} --> {to}\n".format_map(record))

    result.write("@enduml\n")

    if not args.plantuml_file or args.plantuml_file == "-":
        print(result.getvalue())
    else:
        with open(args.plantuml_file, "w") as fd:
            fd.write(result.getvalue())


def validate_record(line_num: int, record: dict[str, str]) -> None:
    if not re.match(ID_REGEX, record["from"]):
        raise ValueError(
            f"Syntax error on line {line_num}: `from` state is not an"
            f" identifier; must match regex: {ID_REGEX}\n"
        )

    if not re.match(ID_REGEX, record["end"]):
        raise ValueError(
            f"Syntax error on line {line_num}: `from` state is not an"
            f" identifier; must match regex: {ID_REGEX}\n"
        )

    if record["action"] and not record["action"].startswith(
        ("ASSERT", "CHECK", "PARSE")
    ):
        raise ValueError(
            f"Syntax error on line {line_num}: `action` must start with"
            " one of 'ASSERT', 'CHECK', 'PARSE'\n"
        )


if __name__ == "__main__":
    main()
