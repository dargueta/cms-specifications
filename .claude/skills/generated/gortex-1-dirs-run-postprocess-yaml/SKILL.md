---
name: gortex-1-dirs-run-postprocess-yaml
description: "Work in the . +1 dirs · run_postprocess_yaml area — 12 symbols across 2 files (82% cohesion)"
---

# . +1 dirs · run_postprocess_yaml

12 symbols | 2 files | 82% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/build_tasks/render_tasks.py`

## Key Files

| File | Symbols |
|------|---------|
| `` | getenv, os, subprocess, run |
| `src/build_tasks/render_tasks.py` | include_dirs, run_render_template, source, output, source, ... |

## Entry Points

- `src/build_tasks/render_tasks.py::run_postprocess_yaml`
- `src/build_tasks/render_tasks.py::run_render_template`

## Connected Communities

- **build_tasks +1 dirs** (3 cross-edges)

## How to Explore

```
get_communities with id: "community-28"
smart_context with task: "understand . +1 dirs · run_postprocess_yaml", format: "gcx"
find_usages with id: "src/build_tasks/render_tasks.py::run_postprocess_yaml", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
