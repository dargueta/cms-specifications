// SPDX-License-Identifier: BSD-3-Clause
local pcug = import 'pcug.libjsonnet';

{
  apiVersion: '3.2.0',
  kind: 'DataContract',

  name: 'Batch Eligibility Query',
  id: '6e67c8db-2ea5-4901-b8b7-991376a72415',
  version: '5.0',
  schema: [
    {
      id: 'header',
      name: 'header',
      logicalType: 'object',
      physicalType: 'table',
      properties: [
        pcug.const('record_type', 'MMABEQRH'),
        {
          name: 'Sending Entity',
          description: |||
            Critical Field: This field provides CMS with the identification of the entity that is sending the BEQ Request File. The value for this field is provided to CMS and used in connection with CMS electronic routing and mailbox functions. The value in this field should agree with the corresponding value in the Trailer Record.
          |||,
          logicalType: 'string',
          logicalTypeOptions: {
            maxLength: 8,
            minLength: 5,
          },
          required: true,
          physicalName: 'sending_entity',
          physicalType: 'VARCHAR(8)',
          authoritativeDefinitions: [
            { url: 'https://schema.org/Organization', type: 'ontology' },
          ],
        },
        pcug.date8 {
          name: 'File Creation Date',
          description: |||
            The date that the Sending Entity created the BEQ Request File.
            This value should agree with the corresponding value in the Trailer Record. CMS returns this information to the Sending Entity on all Detail Records of a BEQ Response File.
          |||,
          required: true,
          physicalName: 'file_creation_date',
        },
        {
          name: 'File Control Number',
          description: |||
            The specific Control Number assigned by the Sending Entity to the BEQ Request File.
            CMS returns this information to the Sending Entity on all Detail Records of a BEQ Response File. This value should agree with the corresponding value in the Trailer Record.
          |||,
          logicalType: 'string',
          logicalTypeOptions: {
            maxLength: 9,
            minLength: 1,
          },
          required: true,
          physicalName: 'file_control_number',
          physicalType: 'VARCHAR(9)',
        },
        pcug.filler('_filler_1', 717),
      ],
      customProperties: {
        serialization: {
          length: 750,
        },
      },
    },
    {
      id: 'detail',
      logicalType: 'object',
      physicalType: 'table',
      properties: [
        pcug.const('record_type', 'DTL01'),
        pcug.beneficiary_identifier,
        pcug.filler('_filler_1', 9),
        pcug.date8 {
          name: 'DOB',
          description: "The date of the beneficiary's birth.",
          physicalName: 'date_of_birth',
          required: true,
        },
        pcug.sex_code,
        {
          name: 'Detail Record Sequence Number',
          description: 'A unique number assigned by the Sending Entity to the Detail Record.',
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
        pcug.filler('_padding', 708),
      ],
      customProperties: {
        serialization: {
          length: 750,
        },
      },
    },
    {
      id: 'trailer',
      name: 'trailer',
      logicalType: 'object',
      physicalType: 'table',
      properties: [
        pcug.const('record_type', 'MMABEQRT'),
        {
          name: 'Sending Entity (CMS)',
          description: |||
            This field provides CMS with the identification of the entity that is sending the BEQ Request File. The value for this field is provided to CMS and used in connection with CMS electronic routing and mailbox functions. The value in this field should agree with the corresponding value in the Header Record.
          |||,
          logicalType: 'string',
          logicalTypeOptions: {
            maxLength: 8,
            minLength: 5,
          },
          physicalName: 'sending_entity',
          physicalType: 'VARCHAR(8)',
          required: true,
          authoritativeDefinitions: [
            { url: 'https://schema.org/Organization', type: 'ontology' },
          ],
        },
        pcug.date8 {
          name: 'File Creation Date',
          physicalName: 'file_creation_date',
          description: |||
            The date when the Sending Entity created the BEQ Request File.
            This value should agree with the corresponding value in the Header Record. CMS will pass this information back to the Sending Entity on all Detail Records of a BEQ Response File.
          |||,
          required: true,
        },
        {
          name: 'File Control Number',
          description: |||
            The specific Control Number assigned by the Sending Entity to the BEQ Request File.
            CMS will return this information to the Sending Entity on all Detail Records of a BEQ Response File. This value should agree with the corresponding value in the Header Record.
          |||,
          logicalType: 'string',
          logicalTypeOptions: {
            maxLength: 9,
            minLength: 1,
          },
          physicalName: 'file_control_number',
          physicalType: 'VARCHAR(9)',
          required: true,
        },
        {
          name: 'Record Count',
          description: 'The total number of Detail Records supplied on the BEQ Request File.',
          logicalType: 'integer',
          logicalTypeOptions: {
            format: 'u32',
            minimum: 1,
            maximum: 9999999,
          },
          required: true,
          physicalName: 'record_count',
          physicalType: 'INTEGER',
          customProperties: {
            serialization: {
              length: 7,
              align: 'right',
              paddingCharacter: '0',
            },
          },
        },
        pcug.filler('_filler_1', 710),
      ],
      customProperties: {
        serialization: {
          length: 750,
        },
      },
    },
  ],
}
