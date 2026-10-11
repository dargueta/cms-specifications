// SPDX-License-Identifier: BSD-3-Clause
local pcug = import 'pcug.libjsonnet';

// TODO (dargueta): This feels wrong, verify field indexes against the schema.
//  An off-by-one error seems likely.
{
  base: '14.3/records/record.json',
  changes: [
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
