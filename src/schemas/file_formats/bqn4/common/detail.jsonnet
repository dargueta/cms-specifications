// SPDX-License-Identifier: BSD-3-Clause
local beneficiary_identifier = import 'beneficiary_identifier.jsonnet';
local bool_10 = import 'bool_10.jsonnet';
local bool_yn = import 'bool_yn.jsonnet';
local const = import 'const.jsonnet';
local date8 = import 'date8.jsonnet';
local filler = import 'filler.jsonnet';
local sex_code = import 'sex_code.jsonnet';

local zero_padded = {
  __metadata__: {
    serialization: {
      align: 'right',
      padding_character: '0',
    },
  },
};

{
  '$schema': 'https://datapackage.org/profiles/2.0/tableschema.json',
  fieldsMatch: ['subset'],
  fields: [
    const('record_type', 'DTL'),
    {
      name: 'original_record_type',
      title: 'Record Type',
      type: 'string',
      constraints: {
        maxLength: 5,
        required: true,
      },
    },
    beneficiary_identifier {
      description: 'This field will contain exactly what is received in the same field of the '
                   + "beneficiary's Detail record in the related BEQ Request file.",
    },
    filler('_filler_1', 9),
    date8 {
      name: 'sent_date_of_birth',
      title: "Beneficiary's Date of Birth Sent",
    },
    sex_code {
      name: 'sent_sex_code',
      title: "Beneficiary's Sex Code Sent",
    },
    {
      name: 'detail_record_sequence_number',
      title: 'Detail Record Sequence Number',
      type: 'integer',
      constraints: {
        minLength: 1,
        maxLength: 7,
        minimum: 0,
        maximum: 9999999,
        required: true,
        unique: true,
      },
    },
    bool_yn {
      name: 'processed_flag',
      title: 'Processed Flag',
      constraints+: {
        required: true,
      },
    },
    bool_yn {
      name: 'beneficiary_matched_flag',
      title: 'Beneficiary Matched Flag',
      description: |||
        * "Y": The beneficiary was matched (located) successfully.
        * "N": The beneficiary was not matched (located) successfully.
        * " " (SPACE) = Beneficiary match was not attempted due to an Invalid
          condition in the Transaction (Detail Record).
      |||,
    },
    date8 {
      name: 'medicare_part_a_entitlement_start_date',
      title: 'Medicare Part A Entitlement Start Date',
    },
    date8 {
      name: 'medicare_part_a_entitlement_end_date',
      title: 'Medicare Part A Entitlement End Date',
    },
    date8 {
      name: 'medicare_part_b_entitlement_start_date',
      title: 'Medicare Part B Entitlement Start Date',
    },
    date8 {
      name: 'medicare_part_b_entitlement_end_date',
      title: 'Medicare Part B Entitlement End Date',
    },
    bool_10 {
      name: 'medicaid_indicator',
      title: 'Medicaid Indicator',
      description: 'An indicator of the presence of current Medicaid coverage for the beneficiary.\n'
                   + 'The value for this field is based upon the presence of Medicaid reported '
                   + 'for the beneficiary by states in the previous calendar month via the MMA '
                   + 'State Files.',
    },
  ] + std.flattenArrays([
    [
      date8 {
        name: 'part_d_enrollment_effective_date_%d' % i,
        title: 'Part D Enrollment Effective Date or Employer Subsidy Start Date (Occurrence %d)' % i,
      },
      date8 {
        name: 'part_d_disenrollment_date_%d' % i,
        title: 'Part D Disenrollment Date or Employer Subsidy End Date (Occurrence %d)' % i,
      },
    ]
    for i in std.range(1, 10)
  ]) + [
    {
      name: 'sending_entity',
      title: 'Sending Entity',
      description: 'The Sending Entity provided on the Header Record of the BEQ Request File '
                   + 'in which the Transaction (Detail Record) was found.\n'
                   + 'The Sending Entity may be a Part D Organization.',
      type: 'string',
      constraints: {
        minLength: 5,
        maxLength: 8,
        required: true,
      },
    },
    {
      name: 'file_control_number',
      title: 'File Control Number',
      description: 'The File Control Number provided by the Sending Entity on the Header '
                   + 'record of the BEQ Request File in which the Transaction (Detail Record) '
                   + 'was found.',
      type: 'string',
      constraints: {
        maxLength: 9,
        minLength: 1,
        required: true,
      },
    },
    date8 {
      name: 'file_creation_date',
      title: 'File Creation Date',
      description: 'The File Creation Date provided on the Header Record of the BEQ Request '
                   + 'File in which the Transaction (Detail Record) was found.',
      constraints+: {
        required: true,
      },
    },
    date8 {
      name: 'part_d_eligibility_start_date',
      title: 'Part D Eligibility Start Date',
      description: 'This field identifies the date the beneficiary became eligible for Part D '
                   + 'Benefits.',
    },
  ] + std.flattenArrays([
    [
      date8 {
        name: 'deemed_lis_effective_date_%d' % i,
        title: 'Deemed / Low-Income Subsidy Effective Date (Occurrence %d)' % i,
      },
      date8 {
        name: 'deemed_lis_end_date_%d' % i,
        title: 'Deemed / Low-Income Subsidy End Date (Occurrence %d)' % i,
      },
      {
        name: 'copayment_level_identifier_%d' % i,
        title: 'Co-Payment Level Identifier (Occurrence %d)' % i,
        type: 'string',
        constraints: {
          enum: ['1', '2', '3', '4', '5'],
          maxLength: 1,
        },
      },
      zero_padded {
        name: 'part_d_premium_subsidy_percent_%d' % i,
        title: 'Part D Premium Subsidy Percent (Occurrence %d)' % i,
        type: 'integer',
        constraints: {
          minimum: 0,
          maximum: 100,
          enum: [
            // NOTE: 0 is not valid in later versions.
            0,
            25,
            50,
            75,
            100,
          ],
          maxLength: 3,
        },
      },
    ]
    for i in std.range(1, 2)
  ]) + [
    {
      name: 'rds_part_d_indicator_%d' % i,
      title: 'RDS / Part D Indicator (Occurrence %d)' % i,
      type: 'string',
      categories: [
        { value: 'D', label: 'Part D' },
        { value: 'R', label: 'RDS' },
      ],
      constraints: {
        maxLength: 1,
      },
    }
    for i in std.range(1, 10)
  ] + std.flattenArrays([
    [
      date8 {
        name: 'start_date_%d' % i,
        title: 'Start Date (Occurrence %d)' % i,
      },
      zero_padded {
        name: 'number_of_uncovered_months_%d' % i,
        title: 'Number of Uncovered Months (Occurrence %d)' % i,
        type: 'integer',
        rdfType: 'http://purl.org/dc/terms/SizeOrDuration',
        constraints: {
          minimum: 0,
          maximum: 999,
          maxLength: 3,
        },
      },
      {
        name: 'number_of_uncovered_months_status_indicator_%d' % i,
        title: 'Number of Uncovered Months Status Indicator (Occurrence %d)' % i,
        type: 'string',
        constraints: {
          maxLength: 1,
        },
      },
      zero_padded {
        name: 'total_number_of_uncovered_months_%d' % i,
        title: 'Total Number of Uncovered Months Status Indicator (Occurrence %d)' % i,
        type: 'integer',
        constraints: {
          minimum: 0,
          maximum: 999,
          maxLength: 3,
        },
      },
    ]
    for i in std.range(1, 20)
  ]) + [
    date8 {
      name: 'retrieved_date_of_birth',
      title: "Beneficiary's Retrieved Date of Birth",
      description: 'As retrieved from CMS database for matching beneficiary.',
    },
    sex_code {
      name: 'retrieved_sex_code',
      title: "Beneficiary's Retrieved Sex Code",
      description: 'As retrieved from CMS database for matching beneficiary.',
    },
  ],
}
