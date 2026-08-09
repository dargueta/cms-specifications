---
name: gortex-2-dirs-tasks-for-source-file
description: "Work in the . +2 dirs · tasks_for_source_file area — 25 symbols across 6 files (80% cohesion)"
---

# . +2 dirs · tasks_for_source_file

25 symbols | 6 files | 80% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `external-call::dep:build_tasks.constants.FORMAT_SOURCE_DIRS_BY_NAME`
- `external-call::dep:build_tasks.format_tasks.generate_tasks_for_format`
- `src/build_tasks/format_tasks.py`
- `src/build_tasks/render_tasks.py`
- `src/dodo.py`

## Key Files

| File | Symbols |
|------|---------|
| `` | Path, append, pathlib.Path |
| `external-call::dep:build_tasks.constants.FORMAT_SOURCE_DIRS_BY_NAME` | build_tasks.constants.FORMAT_SOURCE_DIRS_BY_NAME |
| `external-call::dep:build_tasks.format_tasks.generate_tasks_for_format` | build_tasks.format_tasks.generate_tasks_for_format |
| `src/build_tasks/format_tasks.py` | extra_file_deps, output_root, source_file, tasks_for_source_file, version_build_dir |
| `src/build_tasks/render_tasks.py` | render_template_task, output_path, build_dir, p, source_file, ... |
| `src/dodo.py` | task_build |

## Entry Points

- `src/dodo.py::task_build`
- `src/build_tasks/format_tasks.py::tasks_for_source_file`
- `src/build_tasks/render_tasks.py::yaml_postprocess_tasks`
- `src/build_tasks/render_tasks.py::render_template_task`

## Connected Communities

- **. +1 dirs · parse_build_rules** (2 cross-edges)
- **build_tasks +1 dirs** (1 cross-edges)
- **. +1 dirs · create_constructor_class** (1 cross-edges)

## How to Explore

```
get_communities with id: "community-12"
smart_context with task: "understand . +2 dirs · tasks_for_source_file", format: "gcx"
find_usages with id: "src/dodo.py::task_build", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
