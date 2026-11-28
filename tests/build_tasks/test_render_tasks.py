# SPDX-License-Identifier: BSD-3-Clause

"""Tests for build_tasks.render_tasks."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest
from ruamel.yaml import YAML

from build_tasks.render_tasks import run_render_jsonnet


if TYPE_CHECKING:
    from pathlib import Path


def _load_yaml(path: Path) -> object:
    """Parse a YAML file with the safe loader."""
    return YAML(typ="safe", pure=True).load(path.read_text(encoding="utf-8"))


def test_output_is_yaml_equal_to_jsonnet_value(tmp_path: Path) -> None:
    """The YAML output must parse back to exactly the value the Jsonnet evaluates to."""
    source = tmp_path / "in.jsonnet"
    source.write_text(
        "{ name: 'x', count: 1 + 2, items: [1, 'two', null, true], nested: { a: {} } }",
        encoding="utf-8",
    )
    output = tmp_path / "out.odcs.yaml"

    run_render_jsonnet(source=source, output=output)

    assert _load_yaml(output) == {
        "name": "x",
        "count": 3,
        "items": [1, "two", None, True],
        "nested": {"a": {}},
    }


def test_output_uses_block_style(tmp_path: Path) -> None:
    """Non-empty mappings and sequences must be written in block style, not flow style."""
    source = tmp_path / "in.jsonnet"
    source.write_text("{ outer: { inner: [1, 2] } }", encoding="utf-8")
    output = tmp_path / "out.odcs.yaml"

    run_render_jsonnet(source=source, output=output)

    assert output.read_text(encoding="utf-8") == "outer:\n  inner:\n  - 1\n  - 2\n"


def test_output_key_order_matches_jsonnet_output(tmp_path: Path) -> None:
    """Keys must appear in the order Jsonnet emits them (sorted), not reordered again."""
    source = tmp_path / "in.jsonnet"
    source.write_text("{ zeta: 1, alpha: 2, mid: 3 }", encoding="utf-8")
    output = tmp_path / "out.odcs.yaml"

    run_render_jsonnet(source=source, output=output)

    keys = [line.split(":")[0] for line in output.read_text("utf-8").splitlines()]
    assert keys == ["alpha", "mid", "zeta"]


def test_non_ascii_text_round_trips(tmp_path: Path) -> None:
    """Non-ASCII characters in the Basic Multilingual Plane must survive rendering."""
    source = tmp_path / "in.jsonnet"
    source.write_text("{ text: 'Señor — café' }", encoding="utf-8")
    output = tmp_path / "out.odcs.yaml"

    run_render_jsonnet(source=source, output=output)

    assert _load_yaml(output) == {"text": "Señor — café"}


def test_creates_missing_parent_directories(tmp_path: Path) -> None:
    """The output's parent directories must be created if they don't exist."""
    source = tmp_path / "in.jsonnet"
    source.write_text("{ a: 1 }", encoding="utf-8")
    output = tmp_path / "does" / "not" / "exist" / "out.odcs.yaml"

    run_render_jsonnet(source=source, output=output)

    assert _load_yaml(output) == {"a": 1}


def test_include_dirs_are_searched_for_imports(tmp_path: Path) -> None:
    """Imports that aren't next to the source must be found in `include_dirs`."""
    lib_dir = tmp_path / "lib"
    (lib_dir / "pkg").mkdir(parents=True)
    (lib_dir / "pkg" / "common.libsonnet").write_text("{ shared: 42 }", "utf-8")
    source = tmp_path / "src" / "in.jsonnet"
    source.parent.mkdir()
    source.write_text("(import 'pkg/common.libsonnet') + { own: 1 }", "utf-8")
    output = tmp_path / "out.odcs.yaml"

    run_render_jsonnet(source=source, output=output, include_dirs=[lib_dir])

    assert _load_yaml(output) == {"own": 1, "shared": 42}


def test_import_without_include_dirs_fails(tmp_path: Path) -> None:
    """Without `include_dirs`, an import that only exists in a library dir must fail."""
    lib_dir = tmp_path / "lib"
    lib_dir.mkdir()
    (lib_dir / "common.libsonnet").write_text("{}", "utf-8")
    source = tmp_path / "src" / "in.jsonnet"
    source.parent.mkdir()
    source.write_text("import 'common.libsonnet'", "utf-8")

    with pytest.raises(RuntimeError, match=r"common\.libsonnet"):
        run_render_jsonnet(source=source, output=tmp_path / "out.odcs.yaml")


def test_invalid_jsonnet_raises_and_writes_nothing(tmp_path: Path) -> None:
    """A Jsonnet error must propagate and must not leave a partial output file."""
    source = tmp_path / "in.jsonnet"
    source.write_text("{ a: error 'boom' }", encoding="utf-8")
    output = tmp_path / "out.odcs.yaml"

    with pytest.raises(RuntimeError, match="boom"):
        run_render_jsonnet(source=source, output=output)

    assert not output.exists()


def test_rerender_overwrites_existing_output(tmp_path: Path) -> None:
    """Rendering again must completely replace the previous output."""
    source = tmp_path / "in.jsonnet"
    output = tmp_path / "out.odcs.yaml"
    source.write_text("{ a: 1, b: [1, 2, 3, 4, 5, 6, 7, 8] }", encoding="utf-8")
    run_render_jsonnet(source=source, output=output)

    source.write_text("{ c: 3 }", encoding="utf-8")
    run_render_jsonnet(source=source, output=output)

    assert output.read_text(encoding="utf-8") == "c: 3\n"


def test_rerender_updates_hard_links_to_output(tmp_path: Path) -> None:
    """Re-rendering must write in place so hard links to the output see the new data.

    Inherited versions are hard links to their ancestor's output, so replacing the
    file (instead of rewriting it) would leave them stale.
    """
    source = tmp_path / "in.jsonnet"
    output = tmp_path / "out.odcs.yaml"
    link = tmp_path / "link.odcs.yaml"
    source.write_text("{ v: 1 }", encoding="utf-8")
    run_render_jsonnet(source=source, output=output)
    try:
        os.link(output, link)
    except OSError:  # pragma: no cover (filesystem-dependent)
        pytest.skip("Filesystem doesn't support hard links")

    source.write_text("{ v: 2 }", encoding="utf-8")
    run_render_jsonnet(source=source, output=output)

    assert _load_yaml(link) == {"v": 2}
