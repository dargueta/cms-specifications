// SPDX-License-Identifier: BSD-3-Clause
local detail = import 'bqn4/common/records/detail/5.1.jsonnet';
local header = import 'bqn4/common/records/header/5.0.jsonnet';  // No change from 5.0
local trailer = import 'bqn4/common/records/trailer/5.0.jsonnet';  // No change from 5.0
local file = import 'bqn4/common/whole_file.jsonnet';

file('5.1', header, detail, trailer)
