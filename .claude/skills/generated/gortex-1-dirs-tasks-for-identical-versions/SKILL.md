---
name: gortex-1-dirs-tasks-for-identical-versions
description: "Work in the . +1 dirs · tasks_for_identical_versions area — 10 symbols across 2 files (80% cohesion)"
---

# . +1 dirs · tasks_for_identical_versions

10 symbols | 2 files | 80% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/build_tasks/format_tasks.py`

## Key Files

| File | Symbols |
|------|---------|
| `` | keys, update, join |
| `src/build_tasks/format_tasks.py` | format_build_root, child_versions, already_handled, format_name, output_root, ... |

## Entry Points

- `src/build_tasks/format_tasks.py::tasks_for_identical_versions`

## Connected Communities

- **. +2 dirs · tasks_for_source_file** (1 cross-edges)

## How to Explore

```
get_communities with id: "community-9"
smart_context with task: "understand . +1 dirs · tasks_for_identical_versions", format: "gcx"
find_usages with id: "src/build_tasks/format_tasks.py::tasks_for_identical_versions", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
