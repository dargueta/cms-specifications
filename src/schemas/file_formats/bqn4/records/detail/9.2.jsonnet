// SPDX-License-Identifier: BSD-3-Clause

local base = import 'bqn4/records/detail/9.1.jsonnet';
local pcug = import 'pcug.libjsonnet';


base {
  data_fields+: [
    {
      name: 'Mailing Address Line %d' % i,
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 40,
      },
      physicalName: 'mailing_address_line_%d' % i,
    }
    for i in std.range(1, 6)
  ] + [
    {
      name: 'Mailing Address City',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 40,
      },
      physicalName: 'mailing_address_city',
      authoritativeDefinitions: [{ url: 'https://schema.org/City', logicalType: 'ontology' }],
    },
    {
      name: 'Mailing Address Postal State Code',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 2,
      },
      physicalName: 'mailing_address_state',
      authoritativeDefinitions: [{ url: 'https://schema.org/State', logicalType: 'ontology' }],
    },
    {
      name: 'Mailing Address ZIP Code',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 9,
      },
      physicalName: 'mailing_address_zip_code',
    },
    pcug.date8 {
      name: 'Mailing Address Start Date',
      physicalName: 'mailing_address_start_date',
    },
    {
      name: 'Residence Address Line 1',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 60,
      },
      physicalName: 'residence_address_line_1',
    },
    {
      name: 'Residence Address City',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 40,
      },
      physicalName: 'residence_address_city',
      authoritativeDefinitions: [{ url: 'https://schema.org/City', logicalType: 'ontology' }],
    },
    {
      name: 'Residence Address Postal State Code',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 2,
      },
      physicalName: 'residence_address_state',
      authoritativeDefinitions: [{ url: 'https://schema.org/State', logicalType: 'ontology' }],
    },
    {
      name: 'Residence Address ZIP Code',
      logicalType: 'string',
      logicalTypeOptions: {
        maxLength: 9,
      },
      physicalName: 'residence_address_zip_code',
    },
    pcug.date8 {
      name: 'Residence Address Start Date',
      physicalName: 'residence_address_start_date',
    },
  ],
  padding_length:: 325,
}
