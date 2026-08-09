---
name: gortex-schemas-scripts-from-yaml
description: "Work in the schemas/scripts · from_yaml area — 4 symbols across 1 files (100% cohesion)"
---

# schemas/scripts · from_yaml

4 symbols | 1 files | 100% cohesion

## When to Use

Use this skill when working on files in:
- `src/schemas/scripts/postprocess_yaml.py`

## Key Files

| File | Symbols |
|------|---------|
| `src/schemas/scripts/postprocess_yaml.py` | from_yaml, Filler, node, constructor |

## Entry Points

- `src/schemas/scripts/postprocess_yaml.py::Filler.from_yaml`

## How to Explore

```
get_communities with id: "community-16"
smart_context with task: "understand schemas/scripts · from_yaml", format: "gcx"
find_usages with id: "src/schemas/scripts/postprocess_yaml.py::Filler.from_yaml", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
