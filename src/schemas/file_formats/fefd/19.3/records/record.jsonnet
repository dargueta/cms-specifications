// SPDX-License-Identifier: BSD-3-Clause
local base = import '14.3/records/record.jsonnet';
local pcug = import 'pcug.libjsonnet';

// TODO (dargueta): This feels wrong, verify field indexes against the schema.
//  An off-by-one error seems likely.
base {
  __patch__+: [
    {
      selector: '$.fields[?(@.name == "district_office_code")]',
      new_value: null,  // Delete
    },
    {
      selector: '$.fields[?(@.name == "_filler_2")]',
      new_value: pcug.filler('_filler_2', 12),
    },
  ],
}
