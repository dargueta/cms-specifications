# SPDX-License-Identifier: BSD-3-Clause

"""Task actions and doit task generators for rendering and postprocessing."""

from __future__ import annotations

import json
import subprocess
import sys
from typing import TYPE_CHECKING

import doit_api
import more_itertools as mi
import ruamel.yaml

from .constants import COMMON_INCLUDE_DIR
from .constants import FORMATS_BASE_DIR
from .constants import SCHEMAS_SOURCE_DIR


if TYPE_CHECKING:
    from collections.abc import Iterable
    from pathlib import Path


def construct_pythonpath() -> str:
    """Construct a PYTHONPATH to pass to subprocess invocations of Python."""
    return ":".join((*sys.path, str(SCHEMAS_SOURCE_DIR)))


def run_render_template(
    source: Path, output: Path, include_dirs: Iterable[Path] = ()
) -> None:
    """Render the template file at `source` into `output`."""
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-m",
            "scripts.render_templates",
            *mi.flatten(["-I", str(d)] for d in include_dirs),
            "-o",
            str(output),
            str(source),
        ],
        check=True,
        env={"PYTHONPATH": construct_pythonpath()},
    )


def run_postprocess_yaml(
    source: Path, output: Path, include_dirs: Iterable[Path] = ()
) -> None:
    """Resolve all custom YAML constructors and write into a JSON file."""
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(  # noqa: S603
        [
            sys.executable,
            "-m",
            "scripts.postprocess_yaml",
            "--json",
            *mi.flatten(["-I", str(d)] for d in include_dirs),
            "-o",
            str(output),
            str(source),
        ],
        check=True,
        env={"PYTHONPATH": construct_pythonpath()},
    )


def run_json_to_yaml(json_path: Path, yaml_path: Path) -> None:
    """Convert JSON to YAML."""
    yaml = ruamel.yaml.YAML(typ="safe")
    # Set arrays to be indented two spaces underneath the keys they're mapped to. It
    # drives me crazy otherwise.
    yaml.indent(offset=2)

    with json_path.open() as jfd:
        data = json.load(jfd)

    yaml_path.parent.mkdir(parents=True, exist_ok=True)
    with yaml_path.open("w") as yfd:
        yaml.dump(data, yfd)


def generate_yaml_postprocess_tasks(  # noqa: PLR0913
    yaml_source: Path,
    build_dir: Path,
    extra_file_deps: Iterable[Path] = (),
    output_stem: str | None = None,
    *,
    version: str,
    record_type: str,
) -> list[doit_api.task]:
    """Return tasks to postprocess a YAML file to JSON, then back to clean YAML."""
    stem = output_stem or yaml_source.stem
    json_path = build_dir / (stem + ".json")
    yaml_path = build_dir / (stem + ".yaml")

    return [
        doit_api.task(
            name=f"{version}:{record_type}:postprocess",
            actions=[
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
            file_dep=[str(yaml_source), *extra_file_deps],
            targets=[str(json_path)],
        ),
        doit_api.task(
            name=f"{version}:{record_type}:yaml",
            actions=[(run_json_to_yaml, [json_path, yaml_path])],
            file_dep=[str(json_path)],
            targets=[str(yaml_path)],
        ),
    ]


def render_template_task(
    source_file: Path,
    output_path: Path,
    extra_file_deps: Iterable[Path] = (),
    *,
    version: str,
    record_type: str,
) -> doit_api.task:
    """Return a task for rendering a template."""
    return doit_api.task(
        name=f"{version}:{record_type}:render",
        actions=[
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
        file_dep=[str(source_file), *extra_file_deps],
        targets=[str(output_path)],
    )
