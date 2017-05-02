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

from json_merger.merger import Merger
from json_merger.config import DictMergerOps, UnifierOps
from json_merger.errors import MergeError

from merger_config_arxiv2arxiv import COMPARATORS, LIST_MERGE_OPS


def json_merger_arxiv_to_arxiv_head(root, head, update):
    merger = Merger(
        root, head, update,
        DictMergerOps.FALLBACK_KEEP_HEAD,
        UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
        comparators=COMPARATORS,
        list_merge_ops=LIST_MERGE_OPS
    )
    conflicts = None
    try:
        merger.merge()
    except MergeError as e:
        conflicts = [json.loads(c.to_json()) for c in e.content]
    merged = merger.merged_root

    return merged, conflicts


def json_merger_arxiv_to_arxiv_update(root, head, update):
    merger = Merger(
        root, head, update,
        DictMergerOps.FALLBACK_KEEP_HEAD,
        UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
        comparators=COMPARATORS,
        list_merge_ops=LIST_MERGE_OPS
    )
    conflicts = None
    try:
        merger.merge()
    except MergeError as e:
        conflicts = [json.loads(c.to_json()) for c in e.content]
    merged = merger.merged_root

    return merged, conflicts


def test_merging_schema_field():
    root = {'$schema': 'http://inspire-nightly.cern.ch/schemas/records/hep.json'}
    head = {'$schema': 'http://qa.inspirehep.net/schemas/records/hep.json'}
    update = {'$schema': 'http://inspirehep.net/schemas/records/hep.json'}

    expected_merged = {'$schema': 'http://qa.inspirehep.net/schemas/records/hep.json'}
    expected_conflict = [['SET_FIELD', ['$schema'], 'http://inspirehep.net/schemas/records/hep.json']]

    merged, conflict = json_merger_arxiv_to_arxiv_head(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


# te

# def test_merging_collections_field():
#     root = {'_collections': ['bar']}
#     head = {'_collections': ['bar', 'foo']}
#     update = {'_collections': ['baz', 'spam']}
#
#     expected_merged = {'_collections': ['bar', 'foo']}
#     expected_conflict = None
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_desy_bookkeeping_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_export_to_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_fft_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_files_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_private_notes_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_abstracts_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_accelerator_experiments_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_acquisition_source_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_arxiv_eprints_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_authors_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_affiliations_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_alternative_names_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_credit_roles_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_curated_relation_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_emails_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_full_name_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_ids_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_inspire_roles_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_raw_affiliations_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_record_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_signature_block_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_uuid_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_book_series_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_citeable_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_collaborations_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_control_number_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_copyright_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_core_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_corporate_author_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_deleted_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_deleted_records_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_document_type_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_dois_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_editions_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_energy_ranges_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_external_system_identifiers_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_funding_info_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_imprints_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_inspire_categories_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_isbns_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_keywords_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_languages_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_legacy_creation_date_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_license_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_new_record_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_number_of_pages_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_persistent_identifiers_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_preprint_date_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_public_notes_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_publication_info_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_publication_type_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_refereed_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_references_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_report_numbers_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_self_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_special_collections_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_succeeding_entry_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_texkeys_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_thesis_info_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_title_translations_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_titles_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_urls_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#
#
# def test_merging_wirthdrawn_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = {}
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
