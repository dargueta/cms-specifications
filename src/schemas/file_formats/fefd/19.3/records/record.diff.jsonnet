// SPDX-License-Identifier: BSD-3-Clause
local base = import 'fefd/14.3/records/record.jsonnet';
local filler = import 'filler.jsonnet';

// TODO (dargueta): This feels wrong, verify field indexes against the schema.
//  An off-by-one error seems likely.
base {
  __changes__: {
    district_office_code: null,
    _filler_2: filler('_filler_2', 12),
  },
}
