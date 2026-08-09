---
name: gortex-build-tasks-1-dirs
description: "Work in the build_tasks +1 dirs area — 14 symbols across 3 files (68% cohesion)"
---

# build_tasks +1 dirs

14 symbols | 3 files | 68% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/build_tasks/__init__.py`
- `src/build_tasks/format_tasks.py`

## Key Files

| File | Symbols |
|------|---------|
| `` | re, values, extend, match |
| `src/build_tasks/__init__.py` | generate_all_tasks, build_dir |
| `src/build_tasks/format_tasks.py` | tasks_for_file_builds, target_root, output_root, dep_map, build_dir, ... |

## Entry Points

- `src/build_tasks/format_tasks.py::tasks_for_file_builds`
- `src/build_tasks/format_tasks.py::generate_tasks_for_format`
- `src/build_tasks/__init__.py::generate_all_tasks`

## Connected Communities

- **. +2 dirs · tasks_for_source_file** (4 cross-edges)
- **. +1 dirs · parse_build_rules** (3 cross-edges)
- **. +1 dirs · tasks_for_identical_versions** (1 cross-edges)

## How to Explore

```
get_communities with id: "community-11"
smart_context with task: "understand build_tasks +1 dirs", format: "gcx"
find_usages with id: "src/build_tasks/format_tasks.py::tasks_for_file_builds", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
