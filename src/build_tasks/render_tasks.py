# SPDX-License-Identifier: BSD-3-Clause

"""Task actions and doit task generators for rendering and postprocessing."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from typing import TYPE_CHECKING

import ruamel.yaml

from .constants import COMMON_INCLUDE_DIR
from .constants import FORMATS_BASE_DIR


if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path
    from typing import Any


def run_render_template(
    source: Path, output: Path, include_dirs: Iterable[Path] = ()
) -> None:
    """Render the Liquid template file at `source` into `output`."""
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "scripts.render_templates"]
    for d in include_dirs:
        cmd.extend(["-I", str(d)])

    subprocess.run([*cmd, "-o", str(output), str(source)], check=True)  # noqa: S603


def run_postprocess_yaml(
    source: Path, output: Path, include_dirs: Iterable[Path] = ()
) -> None:
    """Resolve all custom YAML constructors and write into a JSON file."""
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [sys.executable, "-m", "scripts.postprocess_yaml", "--json"]
    for d in include_dirs:
        cmd.extend(["-I", str(d)])
    cmd.extend(["-o", str(output), str(source)])
    subprocess.run(cmd, check=True)  # noqa: S603


def run_json_to_yaml(json_path: Path, yaml_path: Path) -> None:
    """Convert JSON to YAML."""
    yaml = ruamel.yaml.YAML(typ="safe")
    # Set arrays to be indented two spaces underneath the keys they're mapped to. It
    # drives me crazy otherwise.
    yaml.indent(offset=2)

    with json_path.open() as jfd:
        data = json.load(jfd)
    with yaml_path.open("w") as yfd:
        yaml.dump(data, yfd)


def _path_to_slug(p: Path, build_dir: Path) -> str:
    return str(p.relative_to(build_dir)).replace(os.sep, "_").replace(".", "_")


def yaml_postprocess_tasks(
    yaml_source: Path,
    build_dir: Path,
    extra_file_deps: Iterable[Path] = (),
    output_stem: str | None = None,
    *,
    output_root: Path,
) -> list[dict[str, Any]]:
    """Return task dicts to postprocess a YAML file to JSON, then back to clean YAML."""
    stem = output_stem or yaml_source.stem
    json_path = build_dir / (stem + ".json")
    yaml_path = build_dir / (stem + ".yaml")

    return [
        {
            "name": _path_to_slug(json_path, output_root),
            "actions": [
                (
                    run_postprocess_yaml,
                    [],
                    {
                        "source": yaml_source,
                        "output": json_path,
                        "include_dirs": [COMMON_INCLUDE_DIR],
                    },
                ),
            ],
            "file_dep": [str(yaml_source)] + [str(p) for p in (extra_file_deps or [])],
            "targets": [str(json_path)],
        },
        {
            "name": _path_to_slug(yaml_path, output_root),
            "actions": [(run_json_to_yaml, [json_path, yaml_path])],
            "file_dep": [str(json_path)],
            "targets": [str(yaml_path)],
        },
    ]


def render_template_task(
    source_file: Path,
    output_path: Path,
    extra_file_deps: Iterable[Path] = (),
    *,
    output_root: Path,
) -> dict[str, Any]:
    """Return a task dict for rendering a .liquid template."""
    return {
        "name": _path_to_slug(output_path, output_root),
        "actions": [
            (
                run_render_template,
                [],
                {
                    "source": source_file,
                    "output": output_path,
                    "include_dirs": [FORMATS_BASE_DIR],
                },
            ),
        ],
        "file_dep": [str(source_file)] + [str(p) for p in (extra_file_deps or [])],
        "targets": [str(output_path)],
    }
