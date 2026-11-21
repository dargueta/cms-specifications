// SPDX-License-Identifier: BSD-3-Clause
local pcug = import 'pcug.libjsonnet';

function(filler_size) {
  id: 'trailer',
  name: 'trailer',
  logicalType: 'object',
  physicalName: 'trailer',
  physicalType: 'table',
  properties: [
    pcug.const('record_type', 'CMSBEQRT'),
    pcug.const('sending_entity', 'MBD     ') {
      name: 'Sending Entity',
      authoritativeDefinitions: [
        { url: 'https://schema.org/Organization', type: 'ontology' },
      ],
    },
    pcug.date8 {
      name: 'File Creation Date',
      physicalName: 'file_creation_date',
      required: true,
    },
    {
      name: 'File Control Number',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 9,
        minLength: 1,
      },
      required: true,
      physicalName: 'file_control_number',
      physicalType: 'VARCHAR(9)',
    },
    {
      name: 'Record Count',
      logicalType: 'integer',
      logicalTypeOptions: {
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
          padding_character: '0',
        },
      },
    },
    pcug.filler('record_padding', filler_size),
  ],
}
