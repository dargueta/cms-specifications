// SPDX-License-Identifier: BSD-3-Clause

local base = import 'bqn4/common/records/detail/5.1.jsonnet';
local pcug = import 'pcug.libjsonnet';


base {
  data_fields+: [
    pcug.bool_10 {
      name: 'End Stage Renal Disease Indicator',
      physicalName: 'esrd_indicator',
    },
    {
      name: 'PBP Number',
      description: 'Associated with contract number in Field 88, positions 717 - 721.',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 3,
      },
      physicalName: 'part_c_pbp_number',
    },
    pcug.plan_type_code {
      name: 'Plan Type Code',
      description: 'Associated with PBP number in Field 95, positions 746 - 748',
      physicalName: 'part_c_plan_type_code',
    },
    pcug.bool_yn {
      name: 'EGHP Indicator',
      description: 'Associated with PBP number in Field 95, positions 746 - 748',
      physicalName: 'part_c_eghp_indicator',
    },
    {
      name: 'PBP Number',
      description: 'Associated with contract number in Field 91, positions 731 - 735',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 3,
      },
      physicalName: 'part_c_d_pbp_number',
    },
    pcug.plan_type_code {
      name: 'Plan Type Code',
      physicalName: 'part_c_d_plan_type_code',
      description: 'Associated with contract number in Field 91, positions 731 - 735',
    },
    pcug.bool_yn {
      name: 'EGHP Indicator',
      description: 'Associated with contract number in Field 91, positions 731 - 735',
      physicalName: 'part_c_d_eghp_indicator',
    },
  ],
  padding_length:: 743,
}
