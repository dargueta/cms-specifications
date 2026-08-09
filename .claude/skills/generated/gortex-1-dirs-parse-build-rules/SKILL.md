---
name: gortex-1-dirs-parse-build-rules
description: "Work in the . +1 dirs · parse_build_rules area — 21 symbols across 5 files (82% cohesion)"
---

# . +1 dirs · parse_build_rules

21 symbols | 5 files | 82% cohesion

## When to Use

Use this skill when working on files in:
- ``
- `external-call::dep:more_itertools.always_iterable`
- `external-call::stdlib:more_itertools`
- `src/build_tasks/build_rules.py`
- `src/build_tasks/versions.py`

## Key Files

| File | Symbols |
|------|---------|
| `` | items, get, strip, setdefault |
| `external-call::dep:more_itertools.always_iterable` | more_itertools.always_iterable |
| `external-call::stdlib:more_itertools` | more_itertools |
| `src/build_tasks/build_rules.py` | source_root, parse_build_rules, config_path, ParsedBuildRules |
| `src/build_tasks/versions.py` | __str__, constraints, versions_matching, other_version, VersionSpec, ... |

## Entry Points

- `src/build_tasks/build_rules.py::parse_build_rules`
- `src/build_tasks/versions.py::VersionConstraint.from_spec_string`
- `src/build_tasks/versions.py::versions_matching`
- `src/build_tasks/versions.py::VersionSpec.from_string`
- `src/build_tasks/versions.py::VersionConstraint.check`

## Connected Communities

- **. +2 dirs · tasks_for_source_file** (2 cross-edges)
- **. +1 dirs · tasks_for_identical_versions** (1 cross-edges)
- **build_tasks +1 dirs** (1 cross-edges)
- **. +2 dirs · main** (1 cross-edges)

## How to Explore

```
get_communities with id: "community-13"
smart_context with task: "understand . +1 dirs · parse_build_rules", format: "gcx"
find_usages with id: "src/build_tasks/build_rules.py::parse_build_rules", format: "gcx"
```

_`format: "gcx"` returns the [GCX1 compact wire format](../../docs/wire-format.md) — round-trippable, ~27% fewer tokens than JSON. Drop it for JSON output; agents using `@gortex/wire` or the Go `github.com/gortexhq/gcx-go` package decode either._
