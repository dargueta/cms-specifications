// SPDX-License-Identifier: BSD-3-Clause

local base = import 'bqn4/common/records/detail/10.0.jsonnet';
local pcug = import 'pcug.libjsonnet';


base {
  data_fields+: [
    pcug.enrollment_source_type_code {
      name: 'Current Enrollment Source Type Code',
      description: 'Associated with PBP number in Field 95, positions 746 - 748.',
      physicalName: 'current_enrollment_source_type_code_95',
    },
    pcug.enrollment_source_type_code {
      name: 'Current Enrollment Source Type Code',
      description: 'Associated with PBP number in Field 98, positions 752 - 754.',
      physicalName: 'current_enrollment_source_type_code_98',
    },
    {
      name: 'Prior Part C/D Contract Number',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 5,
      },
      physicalName: 'prior_part_c_d_contract_number',
    },
    pcug.date8 {
      name: 'Prior Part C/D Enrollment Start Date',
      description: 'Associated with PBP Number in Field 162, positions 1520-1522.',
      physicalName: 'prior_part_c_d_enrollment_start_date',
    },
    pcug.date8 {
      name: 'Prior Part C/D Disenrollment Date',
      description: 'Associated with PBP Number in Field 162, positions 1520-1522.',
      physicalName: 'prior_part_c_d_enrollment_disenrollment_date',
    },
    pcug.bool_yn {
      name: 'Prior Part D Indicator',
      description: 'Associated with PBP Number in Field 162, positions 1520-1522.',
      physicalName: 'prior_part_d_indicator',
    },
    {
      name: 'Prior PBP Number',
      description: 'Associated with Contract Number in Field 158, positions 1498-1502.',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 3,
      },
      physicalName: 'prior_pbp_number',
    },
    pcug.plan_type_code {
      name: 'Prior Plan Type Code',
      physicalName: 'prior_plan_type_code',
    },
    pcug.bool_yn {
      name: 'Prior EGHP Indicator',
      description: 'Associated with PBP Number in Field 162, positions 1520-1522.',
      physicalName: 'prior_eghp_indicator',
    },
    pcug.enrollment_source_type_code {
      name: 'Prior Enrollment Source Type Code',
      description: 'Associated with PBP Number in positions 1520-1522.',
      physicalName: 'prior_enrollment_source_type_code',
    },
    {
      name: 'Prior Part C Contract Number',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 5,
      },
      physicalName: 'prior_part_c_contract_number',
    },
    pcug.date8 {
      name: 'Prior Part C Enrollment Start Date',
      description: 'Associated with PBP Number in Field 170, positions 1549-1551.',
      physicalName: 'prior_part_c_enrollment_start_date',
    },
    pcug.date8 {
      name: 'Prior Part C Disenrollment Date',
      description: 'Associated with PBP Number in Field 170, positions 1549-1551.',
      physicalName: 'prior_part_c_enrollment_disenrollment_date',
    },
    pcug.bool_yn {
      name: 'Prior Part D Indicator',
      description: 'Associated with PBP Number in Field 170, positions 1549-1551.',
      physicalName: 'prior_part_d_indicator',
    },
    {
      name: 'Prior PBP Number',
      description: 'Associated with Contract Number in Field 166, positions 1527-1531.',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 3,
      },
      physicalName: 'prior_pbp_number',
    },
    pcug.plan_type_code {
      name: 'Prior Plan Type Code',
      description: 'Associated with PBP Number in Field 170, positions 1549-1551.',
      physicalName: 'prior_plan_type_code',
    },
    pcug.bool_yn {
      name: 'Prior EGHP Indicator',
      description: 'Associated with PBP Number in Field 170, positions 1549-1551.',
      physicalName: 'prior_eghp_indicator',
    },
    pcug.enrollment_source_type_code {
      name: 'Prior Enrollment Source Type Code',
      description: 'Associated with PBP Number in Field 170, positions 1549-1551.',
      physicalName: 'prior_enrollment_source_type_code',
    },
  ],
  padding_length:: 455,
}
