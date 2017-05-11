# -*- coding: utf-8 -*-
#
# This file is part of INSPIRE.
# Copyright (C) 2017 CERN.
#
# INSPIRE is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# INSPIRE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with INSPIRE. If not, see <http://www.gnu.org/licenses/>.
#
# In applying this license, CERN does not waive the privileges and immunities
# granted to it by virtue of its status as an Intergovernmental Organization
# or submit itself to any jurisdiction.

from __future__ import absolute_import, division, print_function

import json

import pytest

from json_merger.merger import Merger
from json_merger.config import DictMergerOps, UnifierOps
from json_merger.errors import MergeError

from modules.merger_config_arxiv2arxiv import (
    COMPARATORS,
    LIST_MERGE_OPS,
    FIELD_MERGE_OPS
)


def json_merger_arxiv_to_arxiv(root, head, update):
    merger = Merger(
        root, head, update,
        DictMergerOps.FALLBACK_KEEP_UPDATE,  # Most common operation
        UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
        comparators=COMPARATORS,
        list_merge_ops=LIST_MERGE_OPS,
        list_dict_ops=FIELD_MERGE_OPS
    )
    conflicts = None
    try:
        merger.merge()
    except MergeError as e:
        conflicts = [json.loads(c.to_json()) for c in e.content]
    merged = merger.merged_root

    return merged, conflicts


@pytest.mark.parametrize('scenario', ['arxiv2arxiv'])
def test_complete_merge(update_fixture_loader, scenario):
    root, head, update = update_fixture_loader.load_test(scenario)

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    expected_merged = {}
    expected_conflict = []

    import pdb; pdb.set_trace()
    assert merged == expected_merged
    assert conflict == expected_conflict
