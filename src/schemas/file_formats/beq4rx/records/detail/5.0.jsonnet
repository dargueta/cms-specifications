// SPDX-License-Identifier: BSD-3-Clause
local pcug = import 'pcug.libjsonnet';

{
  apiVersion: '3.2.0',
  kind: 'DataContract',

  name: 'Batch Eligibility Query Detail Record',
  id: 'beq4rx_header_5_0',
  status: 'retired',
  version: '5.0',
  schema: [
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
          physicalName: 'dob',
          description: "The date of the beneficiary's birth.",
          required: true,
        },
        pcug.sex_code,
        {
          name: 'Detail Record Sequence Number',
          physicalName: 'detail_record_sequence_number',
          description: 'A unique number assigned by the Sending Entity to the Detail Record.',
          logicalType: 'integer',
          physicalType: 'VARCHAR(7)',
          required: true,
          unique: true,
          logicalTypeOptions: {
            format: 'u32',
            minimum: 0,
            maximum: 9999999,
          },
          customProperties: {
            physicalTypeOptions: {
              maxLength: 7,
            },
          },
        },
        pcug.filler('_padding', 708),
      ],
    },
  ],
}
