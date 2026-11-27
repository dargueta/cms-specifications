# SPDX-License-Identifier: BSD-3-Clause

"""Tests for dodo.py: import scanning and task generation."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

import dodo
from build_tasks.file_ops import cleanup_intermediate
from build_tasks.file_ops import link_or_copy
from build_tasks.render_tasks import run_render_jsonnet
from build_tasks.versions import VersionSpec


if TYPE_CHECKING:
    from collections.abc import Sequence

    import doit_api


# Small, fake version list so tests don't depend on the real PCUG history.
V50 = VersionSpec(major=5, minor=0)
V51 = VersionSpec(major=5, minor=1)
V52 = VersionSpec(major=5, minor=2)
V53 = VersionSpec(major=5, minor=3)
V54 = VersionSpec(major=5, minor=4)
V55 = VersionSpec(major=5, minor=5)
FAKE_VERSIONS = [V50, V51, V52, V53, V54, V55]


@pytest.fixture
def formats_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point dodo's FORMATS_BASE_DIR at an empty temporary directory."""
    path = (tmp_path / "file_formats").resolve()
    path.mkdir()
    monkeypatch.setattr(dodo, "FORMATS_BASE_DIR", path)
    return path


@pytest.fixture
def build_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point dodo's BUILD_DIR at a temporary directory."""
    path = (tmp_path / "build").resolve()
    monkeypatch.setattr(dodo, "BUILD_DIR", path)
    return path


@pytest.fixture
def fake_versions(monkeypatch: pytest.MonkeyPatch) -> list[VersionSpec]:
    """Replace the PCUG version list with `FAKE_VERSIONS`."""
    monkeypatch.setattr(dodo, "ALL_PCUG_VERSIONS", FAKE_VERSIONS)
    return FAKE_VERSIONS


def _write(path: Path, text: str = "{}") -> Path:
    """Write `text` to `path`, creating parent directories. Returns the resolved path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path.resolve()


def _make_format(
    formats_dir: Path,
    name: str,
    defined: Sequence[VersionSpec],
    removed: Sequence[VersionSpec] = (),
) -> Path:
    """Create a format directory with the given defined and removed versions."""
    root = formats_dir / name
    for version in defined:
        _write(root / "versions" / f"{version}.jsonnet", f"{{ v: '{version}' }}")
    for version in removed:
        _write(root / "versions" / f"{version}.removed", "")
    return root


def _tasks_by_name(tasks: list[doit_api.task]) -> dict[str, doit_api.task]:
    """Index a list of tasks by name, failing if any name is duplicated."""
    result = {t.name: t for t in tasks}
    assert len(result) == len(tasks), "duplicate task names"
    return result


def _run_actions(task: doit_api.task) -> None:
    """Execute a task's Python actions directly, in order."""
    for action in task.actions:
        func, args, *rest = action
        kwargs = rest[0] if rest else {}
        func(*args, **kwargs)


# ---------------------------------------------------------------------------
# _output_path


def test_output_path(build_dir: Path) -> None:
    """Output goes to BUILD_DIR/<format>/<version>.odcs.yaml."""
    assert dodo._output_path("bqn4", V51) == build_dir / "bqn4" / "5.1.odcs.yaml"


# ---------------------------------------------------------------------------
# _resolve_import


def test_resolve_import_relative_to_importer(formats_dir: Path) -> None:
    """An import is first resolved relative to the importing file's directory."""
    importer = _write(formats_dir / "fmt" / "versions" / "5.0.jsonnet")
    target = _write(formats_dir / "fmt" / "versions" / "lib.libsonnet")

    assert dodo._resolve_import(importer, "lib.libsonnet") == target


def test_resolve_import_falls_back_to_formats_base_dir(formats_dir: Path) -> None:
    """An import not found next to the importer is resolved from FORMATS_BASE_DIR."""
    importer = _write(formats_dir / "fmt" / "versions" / "5.0.jsonnet")
    target = _write(formats_dir / "fmt" / "common" / "whole_file.jsonnet")

    assert dodo._resolve_import(importer, "fmt/common/whole_file.jsonnet") == target


def test_resolve_import_prefers_importer_dir(formats_dir: Path) -> None:
    """When a file exists in both places, the one next to the importer wins."""
    importer = _write(formats_dir / "fmt" / "versions" / "5.0.jsonnet")
    local = _write(formats_dir / "fmt" / "versions" / "x.libsonnet")
    _write(formats_dir / "x.libsonnet")

    assert dodo._resolve_import(importer, "x.libsonnet") == local


def test_resolve_import_normalizes_parent_references(formats_dir: Path) -> None:
    """The returned path is absolute and has no `..` components."""
    importer = _write(formats_dir / "fmt" / "versions" / "5.0.jsonnet")
    target = _write(formats_dir / "fmt" / "common" / "base.jsonnet")

    result = dodo._resolve_import(importer, "../common/base.jsonnet")

    assert result == target
    assert result is not None
    assert result.is_absolute()
    assert ".." not in result.parts


def test_resolve_import_missing_returns_none(formats_dir: Path) -> None:
    """A path that exists in neither location resolves to None."""
    importer = _write(formats_dir / "fmt" / "versions" / "5.0.jsonnet")

    assert dodo._resolve_import(importer, "nope.libsonnet") is None


def test_resolve_import_ignores_directories(formats_dir: Path) -> None:
    """A directory with the imported name isn't a match."""
    importer = _write(formats_dir / "fmt" / "versions" / "5.0.jsonnet")
    (formats_dir / "fmt" / "versions" / "adir").mkdir()

    assert dodo._resolve_import(importer, "adir") is None


# ---------------------------------------------------------------------------
# find_jsonnet_dependencies


def test_find_dependencies_no_imports(formats_dir: Path) -> None:
    """A file with no imports has no dependencies."""
    source = _write(formats_dir / "a.jsonnet", "{ a: 1 }")

    assert dodo.find_jsonnet_dependencies(source) == []


def test_find_dependencies_both_quote_styles(formats_dir: Path) -> None:
    """Imports using single and double quotes are both detected."""
    single = _write(formats_dir / "single.libsonnet")
    double = _write(formats_dir / "double.libsonnet")
    source = _write(
        formats_dir / "a.jsonnet",
        "local s = import 'single.libsonnet';\n"
        'local d = import "double.libsonnet";\n'
        "s + d\n",
    )

    assert dodo.find_jsonnet_dependencies(source) == sorted([single, double])


def test_find_dependencies_any_whitespace_after_keyword(formats_dir: Path) -> None:
    """Any amount of whitespace, including newlines, may follow the keyword."""
    dep = _write(formats_dir / "dep.libsonnet")
    source = _write(formats_dir / "a.jsonnet", "import\n    'dep.libsonnet'")

    assert dodo.find_jsonnet_dependencies(source) == [dep]


def test_find_dependencies_is_transitive(formats_dir: Path) -> None:
    """Imports of imports are included, however deep."""
    c = _write(formats_dir / "c.libsonnet", "{}")
    b = _write(formats_dir / "b.libsonnet", "import 'c.libsonnet'")
    a = _write(formats_dir / "sub" / "a.libsonnet", "import 'b.libsonnet'")
    source = _write(formats_dir / "main.jsonnet", "import 'sub/a.libsonnet'")

    assert dodo.find_jsonnet_dependencies(source) == sorted([a, b, c])


def test_find_dependencies_resolves_each_file_relative_to_itself(
    formats_dir: Path,
) -> None:
    """A nested file's relative imports resolve against that file's directory."""
    deep = _write(formats_dir / "fmt" / "common" / "helper.libsonnet")
    middle = _write(
        formats_dir / "fmt" / "common" / "base.jsonnet", "import 'helper.libsonnet'"
    )
    source = _write(
        formats_dir / "fmt" / "versions" / "5.0.jsonnet",
        "import 'fmt/common/base.jsonnet'",
    )

    assert dodo.find_jsonnet_dependencies(source) == sorted([middle, deep])


def test_find_dependencies_deduplicates_diamond(formats_dir: Path) -> None:
    """A file imported along several paths is listed once."""
    shared = _write(formats_dir / "shared.libsonnet")
    left = _write(formats_dir / "left.libsonnet", "import 'shared.libsonnet'")
    right = _write(formats_dir / "right.libsonnet", "import 'shared.libsonnet'")
    source = _write(
        formats_dir / "main.jsonnet",
        "(import 'left.libsonnet') + (import 'right.libsonnet')",
    )

    result = dodo.find_jsonnet_dependencies(source)

    assert result == sorted([left, right, shared])


def test_find_dependencies_handles_cycles(formats_dir: Path) -> None:
    """Import cycles terminate, and the source is never listed as its own dependency."""
    b = _write(formats_dir / "b.libsonnet", "import 'main.jsonnet'")
    source = _write(formats_dir / "main.jsonnet", "import 'b.libsonnet'")

    assert dodo.find_jsonnet_dependencies(source) == [b]


def test_find_dependencies_result_is_sorted(formats_dir: Path) -> None:
    """Dependencies are returned in sorted order regardless of import order."""
    names = ["zz.libsonnet", "aa.libsonnet", "mm.libsonnet"]
    for name in names:
        _write(formats_dir / name)
    source = _write(
        formats_dir / "main.jsonnet", "\n".join(f"import '{n}'" for n in names)
    )

    result = dodo.find_jsonnet_dependencies(source)

    assert result == sorted(result)
    assert [p.name for p in result] == sorted(names)


def test_find_dependencies_importstr_included_but_not_scanned(
    formats_dir: Path,
) -> None:
    """`importstr` targets are dependencies, but their contents aren't scanned."""
    _write(formats_dir / "hidden.libsonnet")
    data = _write(formats_dir / "data.txt", "import 'hidden.libsonnet'\n")
    source = _write(formats_dir / "main.jsonnet", "{ text: importstr 'data.txt' }")

    assert dodo.find_jsonnet_dependencies(source) == [data]


def test_find_dependencies_importbin_included_but_not_scanned(
    formats_dir: Path,
) -> None:
    """`importbin` targets are dependencies, but their contents aren't scanned."""
    _write(formats_dir / "hidden.libsonnet")
    data = _write(formats_dir / "data.bin", "import 'hidden.libsonnet'\n")
    source = _write(formats_dir / "main.jsonnet", "{ b: importbin 'data.bin' }")

    assert dodo.find_jsonnet_dependencies(source) == [data]


def test_find_dependencies_ignores_identifiers_containing_import(
    formats_dir: Path,
) -> None:
    """Words that merely end in "import" (e.g. `myimport`) aren't imports."""
    _write(formats_dir / "x.libsonnet")
    source = _write(formats_dir / "main.jsonnet", "{ myimport 'x.libsonnet' }")

    assert dodo.find_jsonnet_dependencies(source) == []


def test_find_dependencies_unresolvable_import_warns_and_skips(
    formats_dir: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """An import that can't be found logs a warning and is left out of the result."""
    real = _write(formats_dir / "real.libsonnet")
    source = _write(
        formats_dir / "main.jsonnet",
        "// import 'commented_out.libsonnet'\nimport 'real.libsonnet'",
    )

    with caplog.at_level(logging.WARNING, logger=dodo.LOG.name):
        result = dodo.find_jsonnet_dependencies(source)

    assert result == [real]
    assert "commented_out.libsonnet" in caplog.text


def test_find_dependencies_accepts_relative_source_path(
    formats_dir: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A relative source path works and is still excluded from its own dependencies."""
    dep = _write(formats_dir / "dep.libsonnet")
    _write(
        formats_dir / "main.jsonnet", "import 'dep.libsonnet' + import 'main.jsonnet'"
    )
    monkeypatch.chdir(formats_dir)

    assert dodo.find_jsonnet_dependencies(Path("main.jsonnet")) == [dep]


# ---------------------------------------------------------------------------
# create_jsonnet_render_task


def test_render_task_fields(formats_dir: Path, build_dir: Path) -> None:
    """The render task has the right name, deps, target, action, and clean flag."""
    dep = _write(formats_dir / "fmt" / "common" / "whole_file.jsonnet")
    source = _write(
        formats_dir / "fmt" / "versions" / "5.0.jsonnet",
        "import 'fmt/common/whole_file.jsonnet'",
    )
    target = build_dir / "fmt" / "5.0.odcs.yaml"

    task = dodo.create_jsonnet_render_task(
        format_name="fmt", pcug_version=V50, source_file=source, target_file=target
    )

    assert task.name == "5.0"
    assert task.file_dep == [source, dep]
    assert task.targets == [target]
    assert task.clean is True
    assert task.actions == [
        (
            run_render_jsonnet,
            [],
            {"source": source, "output": target, "include_dirs": [formats_dir]},
        )
    ]


def test_render_task_action_produces_yaml(formats_dir: Path, build_dir: Path) -> None:
    """Running the render task's action writes the rendered YAML to the target."""
    _write(formats_dir / "fmt" / "common" / "base.libsonnet", "{ from_base: true }")
    source = _write(
        formats_dir / "fmt" / "versions" / "5.0.jsonnet",
        "(import 'fmt/common/base.libsonnet') + { version: '5.0' }",
    )
    target = build_dir / "fmt" / "5.0.odcs.yaml"
    task = dodo.create_jsonnet_render_task("fmt", V50, source, target)

    _run_actions(task)

    assert target.read_text(encoding="utf-8") == "from_base: true\nversion: '5.0'\n"


# ---------------------------------------------------------------------------
# create_copy_rendered_file_task


def test_clone_task_fields(build_dir: Path) -> None:
    """The clone task has the right name, deps, target, actions, and clean flag."""
    source = build_dir / "fmt" / "5.0.odcs.yaml"
    target = build_dir / "fmt" / "5.1.odcs.yaml"

    task = dodo.create_copy_rendered_file_task(
        format_name="fmt",
        ancestor_version=V50,
        this_version=V51,
        rendered_source_file=source,
        target_file=target,
    )

    assert task.name == "5.1:_clone"
    assert task.file_dep == [source]
    assert task.targets == [target]
    assert task.clean is True
    assert task.uptodate is None
    assert task.actions == [
        (cleanup_intermediate, [target]),
        (link_or_copy, [source, [target]]),
    ]


def test_clone_task_doc_names_both_versions(build_dir: Path) -> None:
    """The clone task's description names both the ancestor and the new version."""
    task = dodo.create_copy_rendered_file_task(
        "fmt", V50, V53, build_dir / "a.yaml", build_dir / "b.yaml"
    )

    assert task.doc == "Clone fmt v5.0 to v5.3"


def test_clone_task_creates_target(build_dir: Path) -> None:
    """Running the clone task creates a target with the ancestor's contents."""
    source = _write(build_dir / "fmt" / "5.0.odcs.yaml", "a: 1\n")
    target = build_dir / "fmt" / "5.1.odcs.yaml"
    task = dodo.create_copy_rendered_file_task("fmt", V50, V51, source, target)

    _run_actions(task)

    assert target.read_text(encoding="utf-8") == "a: 1\n"


def test_clone_task_replaces_stale_copy(build_dir: Path) -> None:
    """A stale, unlinked target is replaced, not silently kept."""
    source = _write(build_dir / "fmt" / "5.0.odcs.yaml", "new: 2\n")
    target = _write(build_dir / "fmt" / "5.1.odcs.yaml", "stale: 1\n")
    task = dodo.create_copy_rendered_file_task("fmt", V50, V51, source, target)

    _run_actions(task)

    assert target.read_text(encoding="utf-8") == "new: 2\n"


# ---------------------------------------------------------------------------
# create_tasks_for_pcug_file_format


@pytest.mark.usefixtures("build_dir", "fake_versions")
def test_format_without_versions_dir_yields_nothing(
    formats_dir: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """A format with no versions/ directory produces no tasks and logs a warning."""
    root = formats_dir / "fmt"
    _write(root / "records" / "detail" / "5.0.jsonnet")

    with caplog.at_level(logging.WARNING, logger=dodo.LOG.name):
        tasks = list(dodo.create_tasks_for_pcug_file_format(root))

    assert tasks == []
    assert "no versions/ directory" in caplog.text


@pytest.mark.usefixtures("build_dir", "fake_versions")
def test_empty_versions_dir_yields_nothing(formats_dir: Path) -> None:
    """A versions/ directory with no Jsonnet files produces no tasks."""
    root = formats_dir / "fmt"
    (root / "versions").mkdir(parents=True)

    assert list(dodo.create_tasks_for_pcug_file_format(root)) == []


@pytest.mark.usefixtures("fake_versions")
def test_explicit_and_inherited_versions(formats_dir: Path, build_dir: Path) -> None:
    """Defined versions render; later undefined versions clone the last defined one."""
    root = _make_format(formats_dir, "fmt", defined=[V51, V53])
    out = build_dir / "fmt"

    tasks = _tasks_by_name(list(dodo.create_tasks_for_pcug_file_format(root)))

    # 5.0 comes before any definition, so it's unsupported.
    assert set(tasks) == {"5.1", "5.2:_clone", "5.3", "5.4:_clone", "5.5:_clone"}

    assert tasks["5.1"].file_dep == [(root / "versions" / "5.1.jsonnet").resolve()]
    assert tasks["5.1"].targets == [out / "5.1.odcs.yaml"]
    assert tasks["5.3"].targets == [out / "5.3.odcs.yaml"]

    assert tasks["5.2:_clone"].file_dep == [out / "5.1.odcs.yaml"]
    assert tasks["5.2:_clone"].targets == [out / "5.2.odcs.yaml"]
    assert tasks["5.4:_clone"].file_dep == [out / "5.3.odcs.yaml"]
    assert tasks["5.5:_clone"].file_dep == [out / "5.3.odcs.yaml"]


@pytest.mark.usefixtures("build_dir", "fake_versions")
def test_clones_always_point_at_rendered_file(formats_dir: Path) -> None:
    """Every clone depends on a rendered target, never on another clone's target."""
    root = _make_format(formats_dir, "fmt", defined=[V50])

    tasks = list(dodo.create_tasks_for_pcug_file_format(root))

    rendered = {t.targets[0] for t in tasks if not t.name.endswith(":_clone")}
    for task in tasks:
        if task.name.endswith(":_clone"):
            assert task.file_dep[0] in rendered


@pytest.mark.usefixtures("fake_versions")
def test_removed_sentinel_stops_inheritance(formats_dir: Path, build_dir: Path) -> None:
    """A .removed sentinel stops inheritance until the next defined version."""
    root = _make_format(formats_dir, "fmt", defined=[V50, V54], removed=[V52])

    tasks = _tasks_by_name(list(dodo.create_tasks_for_pcug_file_format(root)))

    assert set(tasks) == {"5.0", "5.1:_clone", "5.4", "5.5:_clone"}
    assert tasks["5.5:_clone"].file_dep == [build_dir / "fmt" / "5.4.odcs.yaml"]


@pytest.mark.usefixtures("build_dir", "fake_versions")
def test_removed_sentinel_through_last_version(formats_dir: Path) -> None:
    """With no later definition, nothing after a .removed sentinel is generated."""
    root = _make_format(formats_dir, "fmt", defined=[V50], removed=[V51])

    tasks = _tasks_by_name(list(dodo.create_tasks_for_pcug_file_format(root)))

    assert set(tasks) == {"5.0"}


@pytest.mark.usefixtures("build_dir", "fake_versions")
def test_removed_sentinel_before_any_definition(formats_dir: Path) -> None:
    """A .removed sentinel before the first definition has no effect on later ones."""
    root = _make_format(formats_dir, "fmt", defined=[V53], removed=[V51])

    tasks = _tasks_by_name(list(dodo.create_tasks_for_pcug_file_format(root)))

    assert set(tasks) == {"5.3", "5.4:_clone", "5.5:_clone"}


@pytest.mark.usefixtures("build_dir", "fake_versions")
def test_definition_wins_over_sentinel_for_same_version(formats_dir: Path) -> None:
    """If a version has both a .jsonnet file and a .removed file, it is rendered."""
    root = _make_format(formats_dir, "fmt", defined=[V50, V52], removed=[V52])

    tasks = _tasks_by_name(list(dodo.create_tasks_for_pcug_file_format(root)))

    assert set(tasks) == {
        "5.0",
        "5.1:_clone",
        "5.2",
        "5.3:_clone",
        "5.4:_clone",
        "5.5:_clone",
    }


@pytest.mark.usefixtures("build_dir", "fake_versions")
def test_other_files_in_versions_dir_are_ignored(formats_dir: Path) -> None:
    """Files that aren't <version>.jsonnet or <version>.removed don't create tasks."""
    root = _make_format(formats_dir, "fmt", defined=[V55])
    _write(root / "versions" / "README.md", "hi")
    _write(root / "versions" / "9.9.jsonnet")  # Not a known PCUG version.
    _write(root / "versions" / "helpers.libsonnet")

    tasks = _tasks_by_name(list(dodo.create_tasks_for_pcug_file_format(root)))

    assert set(tasks) == {"5.5"}


@pytest.mark.usefixtures("build_dir", "fake_versions")
def test_render_tasks_include_transitive_imports(formats_dir: Path) -> None:
    """Each render task's file_dep includes every file its version imports."""
    root = formats_dir / "fmt"
    header = _write(root / "common" / "records" / "header" / "5.0.jsonnet")
    whole = _write(root / "common" / "whole_file.jsonnet")
    source = _write(
        root / "versions" / "5.0.jsonnet",
        "local h = import 'fmt/common/records/header/5.0.jsonnet';\n"
        "local f = import 'fmt/common/whole_file.jsonnet';\n"
        "f('5.0', h)\n",
    )

    tasks = _tasks_by_name(list(dodo.create_tasks_for_pcug_file_format(root)))

    assert tasks["5.0"].file_dep == [source, header, whole]


@pytest.mark.usefixtures("build_dir", "fake_versions")
def test_all_tasks_clean_their_targets(formats_dir: Path) -> None:
    """Every generated task removes its target on `doit clean`."""
    root = _make_format(formats_dir, "fmt", defined=[V50, V53], removed=[V55])

    tasks = list(dodo.create_tasks_for_pcug_file_format(root))

    assert tasks
    assert all(t.clean is True for t in tasks)


@pytest.mark.usefixtures("fake_versions")
def test_running_all_tasks_produces_expected_outputs(
    formats_dir: Path, build_dir: Path
) -> None:
    """Running every task in order renders defined versions and clones the rest."""
    root = _make_format(formats_dir, "fmt", defined=[V51, V53], removed=[V55])

    for task in dodo.create_tasks_for_pcug_file_format(root):
        _run_actions(task)

    out = build_dir / "fmt"
    assert sorted(p.name for p in out.iterdir()) == [
        "5.1.odcs.yaml",
        "5.2.odcs.yaml",
        "5.3.odcs.yaml",
        "5.4.odcs.yaml",
    ]
    assert (out / "5.2.odcs.yaml").read_text("utf-8") == "v: '5.1'\n"
    assert (out / "5.4.odcs.yaml").read_text("utf-8") == "v: '5.3'\n"
