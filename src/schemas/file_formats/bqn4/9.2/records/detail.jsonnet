// SPDX-License-Identifier: BSD-3-Clause

local base = import 'bqn4/9.1/records/detail.jsonnet';
local date8 = import 'date8.jsonnet';


base {
  data_fields+: [
    {
      name: 'mailing_address_line_%d' % i,
      title: 'Mailing Address Line %d' % i,
      type: 'string',
      constraints: {
        maxLength: 40,
      },
    }
    for i in std.range(1, 6)
  ] + [
    {
      name: 'mailing_address_city',
      title: 'Mailing Address City',
      type: 'string',
      rdfType: 'https://schema.org/City',
      constraints: {
        maxLength: 40,
      },
    },
    {
      name: 'mailing_address_state',
      title: 'Mailing Address Postal State Code',
      type: 'string',
      rdfType: 'https://schema.org/State',
      constraints: {
        maxLength: 2,
      },
    },
    {
      name: 'mailing_address_zip_code',
      title: 'Mailing Address ZIP Code',
      type: 'string',
      constraints: {
        maxLength: 9,
      },
    },
    date8 {
      name: 'mailing_address_start_date',
      title: 'Mailing Address Start Date',
    },
    {
      name: 'residence_address_line_1',
      title: 'Residence Address Line 1',
      type: 'string',
      constraints: {
        maxLength: 60,
      },
    },
    {
      name: 'residence_address_city',
      title: 'Residence Address City',
      type: 'string',
      rdfType: 'https://schema.org/City',
      constraints: {
        maxLength: 40,
      },
    },
    {
      name: 'residence_address_state',
      title: 'Residence Address Postal State Code',
      type: 'string',
      rdfType: 'https://schema.org/State',
      constraints: {
        maxLength: 2,
      },
    },
    {
      name: 'residence_address_zip_code',
      title: 'Residence Address ZIP Code',
      type: 'string',
      constraints: {
        maxLength: 9,
      },
    },
    date8 {
      name: 'residence_address_start_date',
      title: 'Residence Address Start Date',
    },
  ],
  padding_length:: 325,
}
