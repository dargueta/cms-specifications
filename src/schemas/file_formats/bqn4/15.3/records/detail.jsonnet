// SPDX-License-Identifier: BSD-3-Clause

local base = import 'bqn4/12.3/records/detail.jsonnet';
local date8 = import 'date8.jsonnet';


base {
  data_fields+: [
    date8 {
      name: 'medicare_part_a_entitlement_start_date_2',
      title: 'Medicare Part A Entitlement Start Date 2',
    },
    date8 {
      name: 'medicare_part_a_entitlement_end_date_2',
      title: 'Medicare Part A Entitlement End Date 2',
    },
    date8 {
      name: 'medicare_part_b_entitlement_start_date_2',
      title: 'Medicare Part B Entitlement Start Date 2',
    },
    date8 {
      name: 'medicare_part_b_entitlement_end_date_2',
      title: 'Medicare Part B Entitlement End Date 2',
    },
  ],
  padding_length:: 234,
}
