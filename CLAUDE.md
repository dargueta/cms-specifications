# Project: CMS File Processing

A collection of datapackage.org schemas and Python scripts to generate code for processing files sent by CMS to Medicare Advantage payors.

## Context

You pride yourself on your ability to 1) write strict, thorough tests; B) write documentation useful for both developers and moderately technical end users.

Your coworker will have to write many complex YAML files by hand, many of them highly similar or identical. You want to help this coworker avoid writing more than necessary, while not making the code that accomplishes this too difficult to read or maintain.

## Ground Rules

* NEVER create code paths in production code that are only executed during testing.
* Text must be UTF-8, strongly preferring ASCII. Anything outside the Unicode Basic Multilingual Plane is forbidden.
* If a Python library for a file format exists, use that to generate files instead of string concatenation. Use `csv` for generating CSVs, `json` for generating JSON, `ruamel.yaml` for YAML, etc.
* Avoid writing code when a third-party library provides the needed functionality. For Python, you can freely use any libraries listed in @src/requirements.txt.

## Other Notes

Code must be cross-platform and run on Windows, Mac, or Linux. If something can't be made cross-platform (e.g. Windows machines won't have `make`), then a similar parallel feature should be made available.

<!-- gortex:communities:start -->
<!-- gortex:skills:start -->
## Community Skills

| Area | Description | Skill |
|------|-------------|-------|
| 2 Dirs Tasks For Source File | 25 symbols | `/gortex-2-dirs-tasks-for-source-file` |
| 1 Dirs Parse Build Rules | 21 symbols | `/gortex-1-dirs-parse-build-rules` |
| 1 Dirs Deep To Dict | 18 symbols | `/gortex-1-dirs-deep-to-dict` |
| 1 Dirs Render Single File | 18 symbols | `/gortex-1-dirs-render-single-file` |
| 1 Dirs Link Or Copy File | 17 symbols | `/gortex-1-dirs-link-or-copy-file` |
| Build Tasks 1 Dirs | 14 symbols | `/gortex-build-tasks-1-dirs` |
| 1 Dirs Run Postprocess Yaml | 12 symbols | `/gortex-1-dirs-run-postprocess-yaml` |
| 1 Dirs Tasks For Identical Versions | 10 symbols | `/gortex-1-dirs-tasks-for-identical-versions` |
| Schemas Scripts Deep To Dict | 10 symbols | `/gortex-schemas-scripts-deep-to-dict` |
| 2 Dirs Main | 9 symbols | `/gortex-2-dirs-main` |
| 1 Dirs Create Constructor Class | 6 symbols | `/gortex-1-dirs-create-constructor-class` |
| 1 Dirs Main | 6 symbols | `/gortex-1-dirs-main` |
| Click | 6 symbols | `/gortex-click` |
| Schemas Scripts From Yaml | 4 symbols | `/gortex-schemas-scripts-from-yaml` |
| 1 Dirs From Dict | 4 symbols | `/gortex-1-dirs-from-dict` |
| Jinja2 | 3 symbols | `/gortex-jinja2` |
| Attrs | 3 symbols | `/gortex-attrs` |
<!-- gortex:skills:end -->

<!-- gortex:communities:end -->
