---
name: gortex-2-dirs-main
description: "Work in the . +2 dirs · main area — 9 symbols across 3 files (73% cohesion)"
---

# . +2 dirs · main

9 symbols | 3 files | 73% cohesion

## When to Use

Use this skill when working on files in:
- `external-call::dep:ruamel.yaml`
- `src/build_tasks/render_tasks.py`
- `src/schemas/scripts/postprocess_yaml.py`

## Key Files

| File | Symbols |
|------|---------|
| `external-call::dep:ruamel.yaml` | ruamel.yaml |
| `src/build_tasks/render_tasks.py` | yaml_path, json_path, run_json_to_yaml |
| `src/schemas/scripts/postprocess_yaml.py` | include_dirs, main, as_json, output, file |

## Entry Points

- `src/build_tasks/render_tasks.py::run_json_to_yaml`
- `src/schemas/scripts/postprocess_yaml.py::main`

## Connected Communities

- **. +1 dirs · main** (2 cross-edges)
- **. +1 dirs · create_constructor_class** (1 cross-edges)

## How to Explore

```
get_communities with id: "community-10"
smart_context with task: "understand . +2 dirs · main", format: "gcx"
find_usages with id: "src/build_tasks/render_tasks.py::run_json_to_yaml", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
