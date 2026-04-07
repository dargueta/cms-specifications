"""Extract a Mermaid flowchart from a Markdown file."""

from __future__ import annotations

import itertools
import sys
import textwrap
import typing

import click


if typing.TYPE_CHECKING:
    from typing import TextIO


@click.argument("output_file", type=click.File("w", atomic=True), default=sys.stdout)
@click.argument("source_file", type=click.File("r"), default=sys.stdin)
@click.command
def main(source_file: TextIO, output_file: TextIO) -> None:
    """Extract a Mermaid diagram from a Markdown file."""
    for line in source_file:
        if line.strip().startswith("```mermaid"):
            diagram_text = process_mermaid(source_file)
            break
    else:
        sys.exit("No fenced Mermaid diagram found. Is this a Markdown file?")

    if not diagram_text:
        sys.exit("The file doesn't contain a Mermaid diagram, or it's empty.")

    # We do this weird little thing to ensure that the diagram file ends with a single
    # trailing newline, and any leading blank lines are ignored.
    output_file.write(diagram_text.strip() + "\n")


def process_mermaid(source_file: TextIO) -> str:
    """Dedent and clean up a fenced Mermaid diagram and write it to the output.

    This expects the opening fence line to have been consumed. When this returns, the
    closing fence line (if any) will have been consumed.
    """
    # Consume lines until EOF or the closing fence is found. In theory, we should crash
    # if there's no closing fence, but... eh.
    diagram_lines = itertools.takewhile((lambda ln: ln.strip() != "```"), source_file)

    # This does two things:
    #   * Strips trailing whitespace on a line so that "blah  \n" is normalized to
    #     "blah\n".
    #   * Converts tabs to spaces. This is necessary because `textwrap.dedent()` doesn't
    #     treat tabs and spaces equally. A tab is 4 spaces.
    diagram_text = "\n".join(
        ln.rstrip(ln).replace("\t", "    ") for ln in diagram_lines
    )
    return textwrap.dedent(diagram_text)


if __name__ == "__main__":
    main()
