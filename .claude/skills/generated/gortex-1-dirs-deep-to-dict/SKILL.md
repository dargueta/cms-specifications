---
name: gortex-1-dirs-deep-to-dict
description: "Work in the . +1 dirs · deep_to_dict area — 18 symbols across 4 files (95% cohesion)"
---

# . +1 dirs · deep_to_dict

18 symbols | 4 files | 95% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `external-call::stdlib:deep_chainmap`
- `src/schemas/scripts/_common.py`
- `src/schemas/scripts/postprocess_yaml.py`

## Key Files

| File | Symbols |
|------|---------|
| `` | pop |
| `external-call::stdlib:deep_chainmap` | deep_chainmap |
| `src/schemas/scripts/_common.py` | deep_merge_dicts, dicts, item, deep_to_dict, deep_to_dict, ... |
| `src/schemas/scripts/postprocess_yaml.py` | node, fragment, _cls, construct_item, constructor, ... |

## Entry Points

- `src/schemas/scripts/_common.py::deep_to_dict_L42`
- `src/schemas/scripts/postprocess_yaml.py::construct_item`
- `src/schemas/scripts/postprocess_yaml.py::Const.from_yaml`
- `src/schemas/scripts/_common.py::deep_merge_dicts`

## Connected Communities

- **. +1 dirs · parse_build_rules** (1 cross-edges)

## How to Explore

```
get_communities with id: "community-15"
smart_context with task: "understand . +1 dirs · deep_to_dict", format: "gcx"
find_usages with id: "src/schemas/scripts/_common.py::deep_to_dict_L42", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
