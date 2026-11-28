// SPDX-License-Identifier: BSD-3-Clause
local pcug = import 'pcug.libjsonnet';

local zero_padded = {
  customProperties+: {
    serialization: {
      align: 'right',
      paddingCharacter: '0',
    },
  },
};

{
  id: 'detail',
  logicalType: 'object',
  physicalType: 'table',
  // The final field list is always the data fields followed by a single padding field
  // that fills out the rest of the record. Records extending this one should append
  // to `data_fields` and set `padding_length`, never touch `fields` directly:
  //
  //   base {
  //     data_fields+: [ ...new fields... ],
  //     padding_length:: 123,
  //   }
  properties: self.data_fields + [pcug.filler('record_padding', self.padding_length)],
  padding_length:: error 'Records extending the BQN4 detail record must set padding_length.',

  data_fields:: [
    pcug.const('record_type', 'DTL'),
    {
      name: 'Record Type',
      logicalType: 'string',
      logicalTypeOptions: {
        minLength: 5,
        maxLength: 5,
      },
      required: true,
      physicalName: 'original_record_type',
      physicalType: 'VARCHAR(5)',
    },
    pcug.beneficiary_identifier {
      description: 'This field will contain exactly what is received in the same field of the '
                   + "beneficiary's Detail record in the related BEQ Request file.",
    },
    pcug.filler('_filler_1', 9),
    pcug.date8 {
      name: "Beneficiary's Date of Birth Sent",
      physicalName: 'sent_date_of_birth',
    },
    pcug.sex_code {
      name: "Beneficiary's Sex Code Sent",
      physicalName: 'sent_sex_code',
    },
    {
      name: 'Detail Record Sequence Number',
      logicalType: 'integer',
      logicalTypeOptions: {
        format: 'u32',
        minimum: 0,
        maximum: 9999999,
      },
      required: true,
      physicalName: 'detail_record_sequence_number',
      physicalType: 'INTEGER',
      customProperties: {
        serialization: {
          length: 7,
          uniqueWithinFile: true,
        },
      },
    },
    pcug.bool_yn {
      name: 'Processed Flag',
      physicalName: 'processed_flag',
      required: true,
    },
    pcug.bool_yn {
      name: 'Beneficiary Matched Flag',
      description: |||
        * "Y": The beneficiary was matched (located) successfully.
        * "N": The beneficiary was not matched (located) successfully.
        * " " (SPACE) = Beneficiary match was not attempted due to an Invalid
          condition in the Transaction (Detail Record).
      |||,
      physicalName: 'beneficiary_matched_flag',
    },
    pcug.date8 {
      name: 'Medicare Part A Entitlement Start Date',
      physicalName: 'medicare_part_a_entitlement_start_date',
    },
    pcug.date8 {
      name: 'Medicare Part A Entitlement End Date',
      physicalName: 'medicare_part_a_entitlement_end_date',
    },
    pcug.date8 {
      name: 'Medicare Part B Entitlement Start Date',
      physicalName: 'medicare_part_b_entitlement_start_date',
    },
    pcug.date8 {
      name: 'Medicare Part B Entitlement End Date',
      physicalName: 'medicare_part_b_entitlement_end_date',
    },
    pcug.bool_10 {
      name: 'Medicaid Indicator',
      description: 'An indicator of the presence of current Medicaid coverage for the beneficiary.\n'
                   + 'The value for this field is based upon the presence of Medicaid reported '
                   + 'for the beneficiary by states in the previous calendar month via the MMA '
                   + 'State Files.',
      physicalName: 'medicaid_indicator',
    },
  ] + std.flattenArrays([
    [
      pcug.date8 {
        name: 'Part D Enrollment Effective Date or Employer Subsidy Start Date (Occurrence %d)' % i,
        physicalName: 'part_d_enrollment_effective_date_%d' % i,
      },
      pcug.date8 {
        name: 'Part D Disenrollment Date or Employer Subsidy End Date (Occurrence %d)' % i,
        physicalName: 'part_d_disenrollment_date_%d' % i,
      },
    ]
    for i in std.range(1, 10)
  ]) + [
    {
      name: 'Sending Entity',
      description: 'The Sending Entity provided on the Header Record of the BEQ Request File '
                   + 'in which the Transaction (Detail Record) was found.\n'
                   + 'The Sending Entity may be a Part D Organization.',
      logicalType: 'string',
      logicalTypeOptions: {
        minLength: 5,
        maxLength: 8,
      },
      required: true,
      physicalName: 'sending_entity',
      physicalType: 'VARCHAR(8)',
    },
    {
      name: 'File Control Number',
      description: 'The File Control Number provided by the Sending Entity on the Header '
                   + 'record of the BEQ Request File in which the Transaction (Detail Record) '
                   + 'was found.',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 9,
        minLength: 1,
      },
      required: true,
      physicalName: 'file_control_number',
      physicalType: 'VARCHAR(9)',
    },
    pcug.date8 {
      name: 'File Creation Date',
      description: 'The File Creation Date provided on the Header Record of the BEQ Request '
                   + 'File in which the Transaction (Detail Record) was found.',
      required: true,
      physicalName: 'file_creation_date',
    },
    pcug.date8 {
      name: 'Part D Eligibility Start Date',
      description: 'This field identifies the date the beneficiary became eligible for Part D '
                   + 'Benefits.',
      physicalName: 'part_d_eligibility_start_date',
    },
  ] + std.flattenArrays([
    [
      pcug.date8 {
        name: 'Deemed / Low-Income Subsidy Effective Date (Occurrence %d)' % i,
        physicalName: 'deemed_lis_effective_date_%d' % i,
      },
      pcug.date8 {
        name: 'Deemed / Low-Income Subsidy End Date (Occurrence %d)' % i,
        physicalName: 'deemed_lis_end_date_%d' % i,
      },
      {
        name: 'Co-Payment Level Identifier (Occurrence %d)' % i,
        logicalType: 'string',
        logicalTypeOptions: {
          maxLength: 1,
        },
        enum: [{ value: '1' }, { value: '2' }, { value: '3' }, { value: '4' }, { value: '5' }],
        physicalName: 'copayment_level_identifier_%d' % i,
        physicalType: 'VARCHAR(1)',
      },
      zero_padded {
        name: 'Part D Premium Subsidy Percent (Occurrence %d)' % i,
        logicalType: 'integer',
        logicalTypeOptions: {
          minimum: 0,
          maximum: 100,
        },
        enum: [
          // NOTE: 0 is not valid in later versions.
          { value: 0, label: '0%' },
          { value: 25, label: '25%' },
          { value: 50, label: '50%' },
          { value: 75, label: '75%' },
          { value: 100, label: '100%' },
        ],
        physicalName: 'part_d_premium_subsidy_percent_%d' % i,
        physicalType: 'VARCHAR(3)',
        customProperties: {
          serialization: {
            length: 3,
          },
        },
      },
    ]
    for i in std.range(1, 2)
  ]) + [
    {
      name: 'RDS / Part D Indicator (Occurrence %d)' % i,
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 1,
      },
      enum: [
        { value: 'D', label: 'Part D' },
        { value: 'R', label: 'RDS' },
      ],
      physicalName: 'rds_part_d_indicator_%d' % i,
      physicalType: 'VARCHAR(1)',
    }
    for i in std.range(1, 10)
  ] + std.flattenArrays([
    [
      pcug.date8 {
        name: 'Start Date (Occurrence %d)' % i,
        physicalName: 'start_date_%d' % i,
      },
      zero_padded {
        name: 'Number of Uncovered Months (Occurrence %d)' % i,
        logicalType: 'integer',
        logicalTypeOptions: {
          minimum: 0,
          maximum: 999,
        },
        authoritativeDefinitions: [
          { url: 'http://purl.org/dc/terms/SizeOrDuration', type: 'ontology' },
        ],
        physicalName: 'number_of_uncovered_months_%d' % i,
        customProperties: {
          serialization: {
            // TODO (dargueta): Align right and pad with "0"?
            length: 3,
          },
        },
      },
      {
        name: 'Number of Uncovered Months Status Indicator (Occurrence %d)' % i,
        logicalType: 'string',
        logicalTypeOptions: {
          maxLength: 1,
        },
        physicalName: 'number_of_uncovered_months_status_indicator_%d' % i,
      },
      zero_padded {
        name: 'Total Number of Uncovered Months Status Indicator (Occurrence %d)' % i,
        logicalType: 'integer',
        logicalTypeOptions: {
          format: 'u32',
          minimum: 0,
          maximum: 999,
        },
        physicalName: 'total_number_of_uncovered_months_%d' % i,
        physicalType: 'INTEGER',
        customProperties: {
          serialization: {
            length: 3,
          },
        },
      },
    ]
    for i in std.range(1, 20)
  ]) + [
    pcug.date8 {
      name: "Beneficiary's Retrieved Date of Birth",
      description: 'As retrieved from CMS database for matching beneficiary.',
      physicalName: 'retrieved_date_of_birth',
    },
    pcug.sex_code {
      name: "Beneficiary's Retrieved Sex Code",
      description: 'As retrieved from CMS database for matching beneficiary.',
      physicalName: 'retrieved_sex_code',
    },
  ],
}
