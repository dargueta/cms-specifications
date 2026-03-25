#!/usr/bin/env python3
# SPDX-License-Identifier: BSD-3-Clause

"""Extract a Mermaid diagram from Markdown and convert it to JSON."""

from __future__ import annotations

import json
import re
import sys
import typing
from pathlib import Path

import click


if typing.TYPE_CHECKING:
    from typing import Any
    from typing import TextIO


@click.argument("output", type=click.File("w", atomic=True), default=sys.stdout)
@click.argument(
    "source",
    type=click.Path(exists=True, dir_okay=False, path_type=Path, allow_dash=True),
)
@click.command()
def main(source: Path | None, output: TextIO) -> None:
    """Extract a Mermaid and convert it to JSON.

    This supports both Mermaid-only (.mmd) and Markdown (.md) files. As these diagrams
    are solely intended for describing a file's layout, only flowcharts are supported,
    and only with a very limited syntax.

    For a typical file with a header, zero or more detail records, and a trailer, the
    Mermaid code could look like:

    \b
    graph TD
        start                        -- is header?  --> parse_header
        parse_header[parse header]   -- is detail?  --> parse_detail
        parse_header                 -- is trailer? --> parse_trailer
        parse_detail[parse detail]   -- is detail?  --> parse_detail
        parse_detail                 -- is trailer? --> parse_trailer
        parse_trailer[parse trailer]                --> eof

    The produced JSON would look like:

    \b
    {
        "nodes": {
            "start": {"type": "start", "predefined": true},
            "end": {"type": "end", "predefined": true},
            "error": {"type": "error", "predefined": true},
            "detail": {"type": "parse"},
            "header": {"type": "parse"},
            "trailer": {"type": "parse"}
        },
        "edges": [
            {"from": "start", "to": "header", "type": "unconditional"},
            {"from": "header", "to": "detail", "type": "is_record_type"},
            {"from": "header", "to": "trailer", "type": "is_record_type"},
            {"from": "detail", "to": "detail", "type": "is_record_type"},
            {"from": "detail", "to": "trailer", "type": "is_record_type"},
            {"from": "trailer", "to": "end", "type": "unconditional"}
        ]
    }
    """  # noqa: D301
    if not source:
        mermaid_text = sys.stdin.read()
    elif source.suffix == ".mmd":
        mermaid_text = source.read_text()
    else:
        with click.open_file(source) as fd:
            try:
                mermaid_text = find_mermaid_in_markdown(typing.cast("TextIO", fd))
            except ValueError:
                sys.exit(
                    f"Couldn't find Mermaid text in (assumed) Markdown file: {source}"
                )

    try:
        result = parse_mermaid(mermaid_text)
    except ValueError as err:
        sys.exit(str(err) + "\n" + "\n".join(err.__notes__))

    json.dump(result, output, indent=2, sort_keys=True)


def find_mermaid_in_markdown(source: TextIO) -> str:
    """Extract the first fenced block of Mermaid code in the input."""
    for line in source:
        if line.strip().startswith("```mermaid"):
            break
    else:
        raise ValueError(
            "No fenced mermaid diagram exists in this file. Expected a line to start"
            " with ```mermaid somewhere."
        )

    # Found a mermaid diagram, continue until we find the end of the fence.
    result = ""
    for line in source:
        if line.strip() == "```":
            break
        if trimmed_line := line.rstrip():
            result += trimmed_line + "\n"

    return result


LINE_REGEX = r"""(?x)
(?P<left>\w+)(\[(?P<left_label>.+?)\])?
\s*
(
    -->
    | (--(\s*(?P<edge_label>.+?)\s*)-->)
)
\s*
(?P<right>\w+)(\[(?P<right_label>.+?)\])?
"""

NODE_DECLARATION_REGEX = r"^\s*(?P<name>\w+)\[(?P<label>.+?)\]$"


def parse_mermaid(text: str) -> dict[str, Any]:
    """Parse full mermaid text."""
    lines = text.splitlines()
    if not lines:
        return {}

    first_line, *remainder = lines
    if not first_line.startswith(("flowchart ", "graph ")):
        raise ValueError("Only flowcharts and graphs are supported; got {first_line!r}")

    all_nodes = {
        # Predefine some common node types.
        "start": {"type": "start", "label": "start", "predefined": True},
        "end": {"type": "end", "label": "end", "predefined": True},
        "error": {"type": "error", "label": "error", "predefined": True},
    }

    all_edges = []

    for lineno, line in enumerate(remainder, start=2):
        node_def = re.match(NODE_DECLARATION_REGEX, line.strip())
        edge_def = re.match(LINE_REGEX, line.strip(), re.VERBOSE)

        if node_def:
            name = node_def.group("name")
            label = node_def.group("label")
            if name in all_nodes:
                raise ValueError(
                    f"Duplicated node definition on line {lineno}: {line.strip()}"
                )
            all_nodes[name] = {"type": "parse", "label": label}
        elif edge_def:
            left_node_id = edge_def.group("left")
            left_node_label = edge_def.group("left_label")
            edge_label = edge_def.group("edge_label")
            right_node_id = edge_def.group("right")
            right_node_label = edge_def.group("right_label")

            if left_node_id not in all_nodes:
                all_nodes[left_node_id] = {"type": "record", "label": left_node_label}
            elif not all_nodes[left_node_id]["label"]:
                all_nodes[left_node_id]["label"] = left_node_label

            if right_node_id not in all_nodes:
                all_nodes[right_node_id] = {"type": "record", "label": right_node_label}
            elif not all_nodes[right_node_id]["label"]:
                all_nodes[right_node_id]["label"] = right_node_label

            try:
                edge_type = resolve_node_type_from_label(edge_label)
            except ValueError as err:
                err.add_note(f"On line {lineno}")
                raise

            all_edges.append(
                {"from": left_node_id, "to": right_node_id, "type": edge_type}
            )

    return {"nodes": all_nodes, "edges": all_edges}


def parse_edge(
    line: str,
) -> tuple[dict[str, str | None], str | None, dict[str, str | None]]:
    """Parse a single line definition."""
    parts = re.match(LINE_REGEX, line.strip(), re.VERBOSE)
    if not parts:
        raise ValueError("Line failed to match regex: {line.strip()!r}")

    return (
        {parts.group("left"): parts.group("left_label")},
        parts.group("edge_label"),
        {parts.group("right"): parts.group("right_label")},
    )


def resolve_node_type_from_label(label: str | None) -> str:
    """Convert a label to a standardized check slug."""
    label = (label or "").strip('" ')
    if not label:
        return "unconditional"
    if label.startswith("is ") and label.endswith("?"):
        return "is_record_type"
    raise ValueError("Can't figure out type of edge label from {label!r}.")


if __name__ == "__main__":
    main()
