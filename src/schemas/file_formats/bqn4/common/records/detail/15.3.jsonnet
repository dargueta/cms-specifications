// SPDX-License-Identifier: BSD-3-Clause

local base = import 'bqn4/common/records/detail/12.3.jsonnet';
local pcug = import 'pcug.libjsonnet';


base {
  data_fields+: [
    pcug.date8 {
      name: 'Medicare Part A Entitlement Start Date 2',
      physicalName: 'medicare_part_a_entitlement_start_date_2',
    },
    pcug.date8 {
      name: 'Medicare Part A Entitlement End Date 2',
      physicalName: 'medicare_part_a_entitlement_end_date_2',
    },
    pcug.date8 {
      name: 'Medicare Part B Entitlement Start Date 2',
      physicalName: 'medicare_part_b_entitlement_start_date_2',
    },
    pcug.date8 {
      name: 'Medicare Part B Entitlement End Date 2',
      physicalName: 'medicare_part_b_entitlement_end_date_2',
    },
  ],
  padding_length:: 234,
}
