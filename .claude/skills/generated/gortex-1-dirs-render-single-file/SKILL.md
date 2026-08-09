---
name: gortex-1-dirs-render-single-file
description: "Work in the . +1 dirs · render_single_file area — 18 symbols across 3 files (100% cohesion)"
---

# . +1 dirs · render_single_file

18 symbols | 3 files | 100% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `external-call::stdlib:jinja2`
- `src/schemas/scripts/render_templates.py`

## Key Files

| File | Symbols |
|------|---------|
| `` | sys, relative_to, pathlib, exit, Path, ... |
| `external-call::stdlib:jinja2` | jinja2 |
| `src/schemas/scripts/render_templates.py` | file, environment, definitions, include, output, ... |

## Entry Points

- `src/schemas/scripts/render_templates.py::main`
- `src/schemas/scripts/render_templates.py::render_single_file`

## How to Explore

```
get_communities with id: "community-29"
smart_context with task: "understand . +1 dirs · render_single_file", format: "gcx"
find_usages with id: "src/schemas/scripts/render_templates.py::main", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
