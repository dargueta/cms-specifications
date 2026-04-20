# CMS Technical Specifications and Code Generation

This repository consists of two major parts:

* An archive of technical documentation made publicly available by US Centers for Medicare and Medicaid Services ("CMS") [on their website](https://www.cms.gov/), and
* Language-agnostic [schemas](https://datapackage.org/standard/table-schema/) and tools to generate parsers, SQL DDL, and more.

It's intended for software engineers looking to implement, for example, file parsing for CMS' plan communications (BEQR, MONMEMD, and the like). I include historical versions because only the latest version of the PCUG specification is available on their site ([here](https://www.cms.gov/data-research/cms-information-technology/access-cms-data-application/mapd-plan-communication-user-guide)). Previous releases are *not* easy to find, especially as you go farther back in time.

**I am in no way affiliated with neither CMS nor the US government, nor has any entity of the US government endorsed this project.** All I want is to reduce the burden on healthcare companies working with the US government to provide medical care for those who need it most.

Instead of links I've included the actual files here because I hate dead links, and, quite frankly, I don't trust [DOGE](https://doge.gov/) to not break everything.

## System Requirements

Python 3.12 or higher is required for building all the schema references. I strongly recommend using a virtual environment so you can install the required dependencies without affecting your system.

## Licensing

* Except as noted, all files in the `us_federal_government_docs` directory are works of the U.S. Federal Government. Under 17 U.S.C. §105 these are public domain. *I did not create these, nor do I claim any rights on these files or their contents.*
* Anything else is governed by the [3-Clause BSD License](https://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_(%22BSD_License_2.0%22,_%22Revised_BSD_License%22,_%22New_BSD_License%22,_or_%22Modified_BSD_License%22)). For details, see the `LICENSE` and `LICENSE_EXCEPTION` files.

## Contributing

See the contributing guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md).
