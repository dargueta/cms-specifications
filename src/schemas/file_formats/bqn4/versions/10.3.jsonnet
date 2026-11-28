// SPDX-License-Identifier: BSD-3-Clause
local detail = import 'bqn4/common/records/detail/10.3.jsonnet';
local header = import 'bqn4/common/records/header/10.3.jsonnet';
local trailer = import 'bqn4/common/records/trailer/10.3.jsonnet';
local file = import 'bqn4/common/whole_file.jsonnet';

file('10.3', header, detail, trailer)
