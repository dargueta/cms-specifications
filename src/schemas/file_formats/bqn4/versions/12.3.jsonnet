// SPDX-License-Identifier: BSD-3-Clause
local detail = import 'bqn4/common/records/detail/12.3.jsonnet';
local header = import 'bqn4/common/records/header/10.3.jsonnet';  // No change
local trailer = import 'bqn4/common/records/trailer/10.3.jsonnet';  // No change
local file = import 'bqn4/common/whole_file.jsonnet';

file('12.3', header, detail, trailer)
