// SPDX-License-Identifier: BSD-3-Clause

local detail_record = import 'bqn4/common/records/detail/base.jsonnet';
local pcug = import 'pcug.libjsonnet';


detail_record {
  data_fields+: [
    {
      name: 'Last Name',
      description: "The beneficiary's last name.",
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 40,
      },
      physicalName: 'last_name',
      physicalType: 'VARCHAR(40)',
    },
    {
      name: 'First Name',
      description: "The beneficiary's first name.",
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 30,
      },
      physicalName: 'first_name',
      physicalType: 'VARCHAR(30)',
    },
    {
      name: 'Middle Initial',
      description: "The beneficiary's middle initial.",
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 1,
      },
      physicalName: 'middle_initial',
      physicalType: 'VARCHAR(1)',
    },
    {
      name: 'Current State Code',
      logicalType: 'string',
      logicalTypeOptions: {
        minLength: 2,
        maxLength: 2,
      },
      physicalName: 'current_state_code',
      physicalType: 'VARCHAR(2)',
    },
    {
      name: 'Current County Code',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 3,
      },
      physicalName: 'current_county_code',
      physicalType: 'VARCHAR(3)',
    },
    pcug.date8 {
      name: 'Date of Death',
      physicalName: 'date_of_death',
    },
    {
      name: 'Part C/D Contract Number',
      description: 'If available.',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 5,
      },
      physicalName: 'part_c_d_contract_number',
      physicalType: 'VARCHAR(5)',
    },
    pcug.date8 {
      name: 'Part C/D Enrollment Start Date',
      physicalName: 'part_c_d_enrollment_start_date',
    },
    pcug.bool_yn {
      name: 'Part D Indicator',
      physicalName: 'part_d_indicator',
    },
    {
      name: 'Part C Contract Number',
      description: 'If available.',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 5,
      },
      physicalName: 'part_c_contract_number',
      physicalType: 'VARCHAR(5)',
    },
    pcug.date8 {
      name: 'Part C Enrollment Start Date',
      physicalName: 'part_c_enrollment_start_date',
    },
    pcug.bool_yn {
      name: 'Part C Indicator',
      description: 'The v5.0 documentation implies, but does not state, that this should never be true.',
      physicalName: 'part_c_indicator',
    },
  ],
  padding_length:: 6,
}
