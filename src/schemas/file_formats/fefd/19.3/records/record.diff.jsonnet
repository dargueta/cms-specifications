// SPDX-License-Identifier: BSD-3-Clause
local base = import 'fefd/14.3/records/record.jsonnet';
local pcug = import 'pcug.libjsonnet';

// TODO (dargueta): This feels wrong, verify field indexes against the schema.
//  An off-by-one error seems likely.
base {
  __changes__: {
    district_office_code: null,
    _filler_2: pcug.filler('_filler_2', 12),
  },
}
