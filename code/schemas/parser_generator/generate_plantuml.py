#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause

import argparse
import csv
import io
import pathlib


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("layout_csv", type=pathlib.Path)
    parser.add_argument("plantuml_file", type=pathlib.Path)
    args = parser.parse_args()

    output = io.StringIO("@startuml")

    with args.layout_csv.open() as fd:
        reader = csv.DictReader(fd)
        for record in reader:
            if record["action"]:
                output.write("{from} --> {to} : {action}\n".format_map(record))
            else:
                output.write("{from} --> {to}\n".format_map(record))

    output.write("@enduml")
    args.plantuml_file.write_text(output.getvalue())


if __name__ == "__main__":
    main()
