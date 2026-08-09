---
name: gortex-1-dirs-link-or-copy-file
description: "Work in the . +1 dirs · _link_or_copy_file area — 17 symbols across 2 files (100% cohesion)"
---

# . +1 dirs · _link_or_copy_file

17 symbols | 2 files | 100% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/build_tasks/file_ops.py`

## Key Files

| File | Symbols |
|------|---------|
| `` | copytree, suppress, contextlib, shutil, copyfile, ... |
| `src/build_tasks/file_ops.py` | link, children, parent, link_or_copy, link, ... |

## Entry Points

- `src/build_tasks/file_ops.py::link_or_copy`
- `src/build_tasks/file_ops.py::cleanup_intermediate`
- `src/build_tasks/file_ops.py::_link_or_copy_file`
- `src/build_tasks/file_ops.py::_link_or_copy_directory`

## How to Explore

```
get_communities with id: "community-21"
smart_context with task: "understand . +1 dirs · _link_or_copy_file", format: "gcx"
find_usages with id: "src/build_tasks/file_ops.py::link_or_copy", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
