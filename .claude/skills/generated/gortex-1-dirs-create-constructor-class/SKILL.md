---
name: gortex-1-dirs-create-constructor-class
description: "Work in the . +1 dirs · create_constructor_class area — 6 symbols across 2 files (76% cohesion)"
---

# . +1 dirs · create_constructor_class

6 symbols | 2 files | 76% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `src/schemas/scripts/postprocess_yaml.py`

## Key Files

| File | Symbols |
|------|---------|
| `` | replace, functools, partial |
| `src/schemas/scripts/postprocess_yaml.py` | fragment_file, yaml_loader, create_constructor_class |

## Entry Points

- `src/schemas/scripts/postprocess_yaml.py::create_constructor_class`

## How to Explore

```
get_communities with id: "community-17"
smart_context with task: "understand . +1 dirs · create_constructor_class", format: "gcx"
find_usages with id: "src/schemas/scripts/postprocess_yaml.py::create_constructor_class", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
