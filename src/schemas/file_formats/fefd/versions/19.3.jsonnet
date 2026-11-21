// SPDX-License-Identifier: BSD-3-Clause
local base = import 'fefd/versions/14.3.jsonnet';
local pcug = import 'pcug.libjsonnet';

// TODO (dargueta): This feels wrong, verify field indexes against the schema.
//  An off-by-one error seems likely.
base {
  __patch__+: [
    {
      selector: '$.version',
      new_value: '19.3',
    },
    {
      selector: '$.schema[0].properties[?(@.physicalName == "district_office_code")]',
      new_value: null,  // Delete
    },
    {
      selector: '$.schema[0].properties[?(@.physicalName == "_filler_2")]',
      new_value: pcug.filler('_filler_2', 12),
    },
  ],
}
