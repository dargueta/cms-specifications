---
name: gortex-1-dirs-from-dict
description: "Work in the . +1 dirs · from_dict area — 4 symbols across 2 files (100% cohesion)"
---

# . +1 dirs · from_dict

4 symbols | 2 files | 100% cohesion

## When to Use

Use this skill when working on files in:
- `external-call::dep:cattrs.preconf.json`
- `src/schemas/scripts/schemas.py`

## Key Files

| File | Symbols |
|------|---------|
| `external-call::dep:cattrs.preconf.json` | cattrs.preconf.json |
| `src/schemas/scripts/schemas.py` | Table, from_dict, dct |

## Entry Points

- `src/schemas/scripts/schemas.py::Table.from_dict`

## How to Explore

```
get_communities with id: "community-18"
smart_context with task: "understand . +1 dirs · from_dict", format: "gcx"
find_usages with id: "src/schemas/scripts/schemas.py::Table.from_dict", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
