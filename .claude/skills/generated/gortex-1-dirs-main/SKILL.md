---
name: gortex-1-dirs-main
description: "Work in the . +1 dirs · main area — 6 symbols across 2 files (82% cohesion)"
---

# . +1 dirs · main

6 symbols | 2 files | 82% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/schemas/scripts/minijson.py`

## Key Files

| File | Symbols |
|------|---------|
| `` | json, load, dump |
| `src/schemas/scripts/minijson.py` | output, source, main |

## Entry Points

- `src/schemas/scripts/minijson.py::main`

## How to Explore

```
get_communities with id: "community-25"
smart_context with task: "understand . +1 dirs · main", format: "gcx"
find_usages with id: "src/schemas/scripts/minijson.py::main", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
