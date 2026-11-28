// SPDX-License-Identifier: BSD-3-Clause
local pcug = import 'pcug.libjsonnet';

function(filler_size) {
  id: 'header',
  name: 'header',
  logicalType: 'object',
  physicalType: 'table',
  properties: [
    pcug.const('record_type', 'CMSBEQRH'),
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
    pcug.filler('record_padding', filler_size),
  ],
}
