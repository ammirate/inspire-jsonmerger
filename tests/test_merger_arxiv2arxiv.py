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


def test_merging_schema_field():
    root = {'$schema': 'http://inspire-nightly.cern.ch/schemas/records/hep.json'}
    head = {'$schema': 'http://qa.inspirehep.net/schemas/records/hep.json'}
    update = {'$schema': 'http://inspirehep.net/schemas/records/hep.json'}

    expected_merged = {'$schema': 'http://qa.inspirehep.net/schemas/records/hep.json'}
    expected_conflict = [['SET_FIELD', ['$schema'], 'http://inspirehep.net/schemas/records/hep.json']]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_collections_field():
    root = {'_collections': ['Literature']}
    head = {'_collections': ['Literature', 'Conference']}
    update = {'_collections': ['Literature', 'Paper']}

    expected_merged = head
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_desy_bookkeeping_field():
    root = {
        "_desy_bookkeeping": [
            {
                "date": "2014-07-31",
                "expert": "B",
                "status": "abs"
            }, {
                "date": "2014-08-06",
                "expert": "B",
                "status": "printed"
            }, {
                "date": "2015-01-02",
                "status": "final"
            }
        ]
    }
    head = {
        "_desy_bookkeeping": [
            {
                "date": "2014-07-31",
                "expert": "B",
                "status": "printed2"
            }, {
                "date": "2014-08-06",
                "expert": "B",
                "status": "printed"
            }, {
                "date": "2015-01-02",
                "expert": "B",
                "status": "final"
            }
        ]
    }
    update = {
        "_desy_bookkeeping": [
            {
                "date": "2014-07-31",
                "status": "abs"
            }, {
                "date": "2014-08-06",
                "expert": "B",
                "status": "printed"
            }, {
                "date": "2015-01-03",
                "status": "final"
            }
        ]
    }

    expected_merged = {
        "_desy_bookkeeping": [
            {
                "date": "2014-07-31",
                "status": "printed2"
            }, {
                "date": "2014-08-06",
                "expert": "B",
                "status": "printed"
            }, {
                "date": "2015-01-02",
                "expert": "B",
                "status": "final"
            }

        ]
    }
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_export_to_field():
    root = {}
    head = {}
    update = {}

    expected_merged = {}
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_fft_field():
    root = {}
    head = {}
    update = {}

    expected_merged = {}
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


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
def test_merging_document_type():
    root = {'document_type': ['thesis']}
    head = {'document_type': ['paper']}
    update = {'document_type': ['article']}

    expected_merged = update  # since the list rule is 'Keep update'

    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_document_type_head_equals_to_root():
    root = {'document_type': ['thesis']}
    head = {'document_type': ['thesis']}
    update = {'document_type': ['article']}

    expected_merged = update
    # No expected conflict, since update is legally overwriting an old info
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_document_type_head_equals_to_root():
    root = {'document_type': ['thesis']}
    head = {'document_type': ['article']}
    update = {'document_type': ['thesis']}

    expected_merged = update

    # No expected conflict, since update is legally overwriting an old info
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_dois_field():
    root = {
        'dois': [
            {
                'material': 'preprint',
                'value': '10.1023/A:1026654312961'
            }
        ]
    }
    head = {
        'dois': [
            {
                'material': 'preprint',
                'source': 'nowhere',
                'value': '10.1023/A:1026654312961'
            }
        ]
    }
    update = {
        'dois': [
            {
                'material': 'publication',
                'value': '10.1023/A:1026654312961'
            }
        ]
    }

    expected_merged = {
        'dois': [
            {
                'material': 'publication',
                'source': 'nowhere',
                'value': '10.1023/A:1026654312961'
            }
        ]
    }
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_editions_field():
    root = {'editions': ['edition1']}
    head = {'editions': ['editionA']}
    update = {'editions': ['edition2']}

    expected_merged = {'editions': ['editionA', 'edition2']}
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_energy_ranges_field():
    root = {'energy_ranges': [1, 100]}
    head = {'energy_ranges': [1, 399, 401]}
    update = {'energy_ranges': [1, 400]}

    expected_merged = update  # just update the record with newcoming info
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_external_system_identifiers_field():
    root = {
        'external_system_identifiers': [
            {
                'schema': 'DESY',
                'value': 'DA14-kp45b'
            }, {
                'schema': 'OSTI',
                'value': 1156543
            }
        ]
    }  # record: 1308464
    head = {
        'external_system_identifiers': [
            {
                'schema': 'DESY',
                'value': 'DA14-kp45bAAA'
            }, {
                'schema': 'OSTII',
                'value': 1156543
            }
        ]
    }
    update = {
        'external_system_identifiers': [
            {
                'schema': 'DESY',
                'value': 'DA14-kp45bBBB'
            }, {
                'schema': 'OSTI',
                'value': 115654323
            }
        ]
    }

    expected_merged = update
    # since `DESY` has been curated, we don't want to lose it
    # so it appears in the conflicts
    expected_conflict = [
                            [
                                'SET_FIELD',
                                ['external_system_identifiers', 0, 'value'],
                                'DA14-kp45bAAA'
                            ]
                        ]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_funding_info_field():

    root = {'funding_info':
            [
                {
                    'grant_number': '317089',
                    'project_number': 'FP7-PEOPLE-2012-ITN'
                }
            ]}  # derived from record: 1508011
    head = {'funding_info':
            [
                {
                    'agency': 'GATIS, Gauge Theory as an Integrable System foo',
                    'grant_number': '317089',
                    'project_number': 'FP7-PEOPLE-2012-ITN'
                }
            ]}
    update = {'funding_info':
              [
                  {
                      'agency': 'GATIS, Gauge Theory as foo Integrable System',
                      'grant_number': '317089',
                      'project_number': 'FP7-PEOPLE-2013-ITN'
                  }
              ]}

    expected_merged = head
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_imprints_field():
    root = {'imprints': [
        {
            'date': '2017',
            'place': 'Oxford',
            'publisher': 'Oxford Univ. Press'
        }
    ]}  # record: 1593157
    head = {'imprints': [
        {
            'date': '2017',
            'place': 'Oxford',
            'publisher': 'Oxford University'
        }
    ]}
    update = {'imprints': [
        {
            'date': '2018',
            'place': 'Oxford',
            'publisher': 'Oxford Univ. foo bar'
        }
    ]}

    expected_merged = update
    # here, normally I would expect a conflict, but since the strategy relies
    # on the `publisher` field, for the merger they are two different objects
    # so the head is directly removed, loosing eventually curated info
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_inspire_categories_field():
    root = {'inspire_categories': [
        {
            'source': 'INSPIRE',
            'term':   'Theory-HEP'
        }
    ]}  # record: 1515398
    head = {'inspire_categories': [
        {
            'source': 'INSPIRE',
            'term':   'Theory-HEP'
        }, {
            'source': 'INSPIRE',
            'term': 'General Physic'
        }
    ]}
    update = {'inspire_categories': [
        {
            'source': 'arXiv',
            'term':   'cond-mat.dis-nn'
        }, {
            'source': 'arXiv',
            'term': 'hep-th'
        }
    ]}

    expected_merged = {'inspire_categories': [
        {
            'source': 'arXiv',
            'term':   'cond-mat.dis-nn'
        }, {
            'source': 'arXiv',
            'term': 'hep-th'
        }, {
            'source': 'INSPIRE',
            'term':   'Theory-HEP'
        }, {
            'source': 'INSPIRE',
            'term':   'General Physic'
        },
    ]}
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_isbns_field():
    root = {'isbns': [
        {
            'medium': 'Online',
            'value': '978-94-6239-243-4'
        }, {
            'medium': 'Print',
            'value':  '978-94-6239-242-7'
        }
    ]}
    # record: 1597991
    head = {'isbns': [
        {
            'medium': 'Online',
            'value': '978-94-6239-243-4'
        }, {
            'medium': 'Print',
            'value':  '978-94-6239-242-7'
        }
    ]}
    update = {'isbns': [
        {
            'medium': 'Online',
            'value': '978-94-6239-243-4'
        }, {
            'medium': 'Print',
            'value':  '978-94-6239-242-7'
        }
    ]}

    expected_merged = update
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_keywords_field():
    root = {'keywords': [
        {
            'schema': 'INSPIRE',
            'value': 'colliding beams'
        }
    ]}  # record: 1518997
    head = {'keywords': [
        {
            'schema': 'INSPIRE',
            'value': 'colliding super beams'
        }, {
            'schema': 'INSPIRE',
            'value':  'scattering'
        }
    ]}
    update = {'keywords': [
        {
            'schema': 'INSPIRE',
            'value': 'mass: lower limit'
        }
    ]}

    expected_merged = {'keywords': [
        {
            'schema': 'INSPIRE',
            'value':  'mass: lower limit'
        }, {
            'schema': 'INSPIRE',
            'value':  'colliding super beams'
        }, {
            'schema': 'INSPIRE',
            'value':  'scattering'
        }
    ]}
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_languages_field():
    root = {}
    # not sure if this is a significant case
    head = {'languages': ['it', 'fr']}
    update = {'languages': ['sp']}

    expected_merged = update
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_legacy_creation_date_field():
    root = {}  # record: 1124236
    head = {'legacy_creation_date': '2012-07-30'}
    update = {}

    expected_merged = head
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_license_field():
    root = {'license': [
        {
            'imposing': 'Elsevier',
            'url': 'http://creativecommons.org/licenses/by/4.0/',
            'license': 'elsevier foo bar'
        }
    ]}
    head = {'license': [
        {
            'imposing': 'Elsevier',
            'url': 'http://creativecommons.org/licenses/by/4.0/',
            'license': 'elsevier foo bar'
        },
        {
            'imposing': 'arXiv',
            'url':      'http://creativecommons.org/licenses/by/4.0/',
            'license':  'arxiv foo bar'
        }
    ]}
    update = {'license': [
        {
            'imposing': 'Elsevier',
            'url': 'http://creativecommons.org/licenses/by/4.0/',
            'license': 'elsevier foo bar updated!'
        }
    ]}

    expected_merged = {'license': [
        {
            'imposing': 'Elsevier',
            'url': 'http://creativecommons.org/licenses/by/4.0/',
            'license': 'elsevier foo bar updated!'
        },
        {
            'imposing': 'arXiv',
            'url':      'http://creativecommons.org/licenses/by/4.0/',
            'license':  'arxiv foo bar'
        }
    ]}
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_new_record_field():
    root = {}  # record: 37545
    head = {'new_record': {'$ref': 'd361769'}}
    update = {}

    expected_merged = head
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_new_record_field_filled_root():
    root = {}  # record: 37545
    head = {'new_record': {'$ref': 'd361769'}}
    update = {}

    expected_merged = head
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_number_of_pages_field():
    root = {'number_of_pages': 109}  # record: 1512524
    head = {'number_of_pages': 108}
    update = {'number_of_pages': 110}

    expected_merged = update
    expected_conflict = [['SET_FIELD', ['number_of_pages'], 108]]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


@pytest.mark.xfail()
def test_merging_persistent_identifiers_field():
    root = {'persistent_identifiers': [
        {'schema': 'HDL',
            'source': 'EDP Sciences',
            'value': '10.1051/epjconf/201713506006'}
    ]}  # record: 1517880
    head = {'persistent_identifiers': [
        {
            'material': 'paper',
            'schema': 'HDL',
            'source': 'EDP Sciences',
            'value': '10.1051/epjconf/201713506006'
        }
    ]}
    update = {'persistent_identifiers': [
        {
            'material': 'paper',
            'schema': 'HDL foo',
            'source': 'EDP Sciences bar',
            'value': '10.1051/epjconf/201713506006'
        }
    ]}

    expected_merged = head
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_preprint_date_field():
    root = {'preprint_date': '2015-05-02'}  # record: 1375944
    head = {'preprint_date': '2015-05-03'}
    update = {'preprint_date': '2015-05-04'}

    expected_merged = head
    expected_conflict = [['SET_FIELD', ['preprint_date'], '2015-05-04']]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_public_notes_field():
    root = {}  # 1598270
    head = {'public_notes': [
        {'source': 'arXiv', 'value': '50 pages, 32 figures'}]
    }
    update = {'public_notes': [
        {'source': 'arXiv', 'value': '51 pages, 33 figures'},
        {'source': 'Elsevier', 'value': '51 pages, 33 figures'}],
    }

    expected_merged = update
    expected_conflict = [['SET_FIELD',
                          ['public_notes', 0, 'value'],
                          '50 pages, 32 figures']
                         ]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


@pytest.mark.xfail()
def test_merging_publication_info_field():
    # TODO: test more
    root = {'publication_info': [
        {
            'artid': '948-979',
            'journal_title': 'Adv.Theor.Math.Phys.',
            'journal_volume': '12',
            'year': '2008'
        }
    ]}  # record 697133
    head = {'publication_info': [
        {
            'artid': '948-979',
            'curated_relation': True,
            'journal_issue': 'foo',
            'journal_title': 'Adv.Theor.Math.Phys.',
            'journal_volume': '12',
            'year': '2008'
        }
    ]}
    update = {'publication_info': [
        {
            'artid': '948-979',
            'curated_relation': False,
            'journal_title': 'Adv.Theor.Math.Phys.',
            'journal_volume': '12',
            'year': '2008'
        }, {
            'journal_title': 'foor bar',
            'journal_volume': '12',
            'year': '2016'
        }
    ]}

    expected_merged = {'publication_info': [
        {
            'artid': '948-979',
            'curated_relation': False,
            'journal_issue': 'foo',  # added from head changes
            'journal_title': 'Adv.Theor.Math.Phys.',
            'journal_volume': '12',
            'year': '2008'
        }, {
            'journal_title': 'foor bar',
            'journal_volume': '12',
            'year': '2016'
        }
    ]}
    expected_conflict = [['SET_FIELD',
                          ['publication_info', 0, 'curated_relation'],
                          True]]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_publication_type_field():
    root = {'publication_type': ['introductory']}
    head = {'publication_type': ['introductory', 'lectures']}
    update = {'publication_type': ['lectures', 'review']}

    expected_merged = update
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_refereed_field():
    root = {}
    head = {'refereed': True}
    update = {'refereed': False}

    expected_merged = update
    expected_conflict = [['SET_FIELD', ['refereed'], True]]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


@pytest.mark.xfail()
def test_merging_references_field():
    root = {}
    head = {}
    update = {}

    expected_merged = {}
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_report_numbers_field():
    root = {'report_number': [
                {
                    'source': 'arXiv',
                    'value': 'arXiv:1705.01099'
                }
            ]}  # record: 1598022
    head = {'report_number': [
                {
                    'hidden': True,
                    'source': 'arXiv',
                    'value': 'arXiv:1705.01099'
                }, {
                    'source': 'foo bar',
                    'value': 'foo:123456'
                }
            ]}
    update = {'report_number': [
                {
                    'hidden': False,
                    'source': 'arXiv',
                    'value': 'arXiv:1705.01099'
                }
            ]}

    expected_merged = update
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_self_field():
    root = {}
    head = {'$ref': 'url foo'}
    update = {}

    expected_merged = head
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_special_collections_field():
    root = {'special_collections': ['CDF-INTERNAL-NOTE', 'CDF-NOTE']}
    head = {'special_collections': ['CDF-INTERNAL-NOTE']}
    update = {'special_collections': []}

    expected_merged = head
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_succeeding_entry_field():
    root = {'succeeding_entry': {
                    'isbn': 'ERN-EP-2016-305',
                    'relationship_code': 'w1510564'
                }
            }  # record: 1503270
    head = {'succeeding_entry': {
                    'isbn': 'ERN-EP-2016-305',
                    'record': {'$ref': 'something'},
                    'relationship_code': 'w1510564'
                }
            }
    update = {'something': 'else'}

    expected_merged = {
        'something': 'else',
        'succeeding_entry': {
                    'isbn': 'ERN-EP-2016-305',
                    'record': {'$ref': 'something'},
                    'relationship_code': 'w1510564'
                }
            }
    # updates tries to remove info but we keep the head
    expected_conflict = [['REMOVE_FIELD', ['succeeding_entry'], None]]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_texkeys_field():
    root = {'texkeys': ['Kotwal:2016']}
    head = {'texkeys': ['Kotwal:2016', 'Kotwalfoo:2017']}
    update = {}

    expected_merged = head
    expected_conflict = [['REMOVE_FIELD', ['texkeys'], None]]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict

@pytest.mark.xfail()
def test_merging_thesis_info_field():
    root = {'thesis_info':
                {
                    'date': '2017',
                    'defense_date': '2017',
                     'degree_type': 'PhD',
                    'institutions': [
                        {
                            'curated_relation': False,
                            'name': 'Columbia U.',
                            'record': {'$ref': 'foo-link'}
                        }
                    ]
                }
            }  # record: 1597507
    head = {'thesis_info': {
                    'date': '2017',
                    'defense_date': '2017',
                     'degree_type': 'PhD',
                    'institutions': [
                        {
                            'curated_relation': True,
                            'name': 'Columbia University',
                            'record': {'$ref': 'foo-link'}
                        }
                    ]
                }
            }
    update = {'thesis_info': {
                    'date': '2017',
                    'defense_date': '2017',
                     'degree_type': 'PhD',
                    'institutions': [
                        {
                            'curated_relation': False,
                            'name': 'Second university of foo bar',
                            'record': {'$ref': 'foo-link2'}
                        }, {
                            'curated_relation': False,
                            'name': 'Columbia U.',
                            'record': {'$ref': 'foo-link'}
                        },
                    ]
                }
             }

    expected_merged = head
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_title_translations_field():
    root = {'title_translations': [
        {
            'source': 'submitter',
            'title': 'ANTARES: An observatory at the seabed '
                     'to the confines of the Universe'
        }  # record: 1519935
    ]}
    head = {'title_translations': [
        {
            'language': 'en',
            'source': 'submitter',
            'subtitle': 'this subtitle has been added by a curator',
            'title': 'ANTARES: An observatory at the seabed '
                     'to the confines of the Universe'
        }
    ]}
    update = {'title_translations': [
        {
            'source': 'submitter',
            'title': 'ANTARES: An observatory at the seabed '
                     'to the confines of the Universe'
        }, {
            'language': 'it',
            'source': 'submitter',
            'title': 'ANTARES: Un osservatorio foo bar'
        }
    ]}

    expected_merged = head
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_titles_field():
    root = {'titles': [
        {
            'language': '',
            'source': 'submitter',
            'title':  'ANTARES: An observatory at the seabed '
                      'to the confines of the Universe'
        }  # record: 1519935
    ]}
    head = {'titles': [
        {
            'language': '',
            'source':   'submitter',
            'subtitle': 'this subtitle has been added by a curator',
            'title':    'ANTARES: An observatory at the seabed '
                        'to the confines of the Universe'
        }
    ]}
    update = {'titles': [
        {
            'language': 'it',
            'source':   'submitter',
            'title':    'ANTARES: Un osservatorio foo bar'
        }, {
            'language': '',
            'source':   'submitter',
            'title':    'ANTARES: An observatory at the seabed '
                        'to the confines of the Universe'
        }
    ]}

    expected_merged = {'titles': [
        {
            'language': 'it',
            'source':   'submitter',
            'title':    'ANTARES: Un osservatorio foo bar'
        }, {
            'language': '',
            'source':   'submitter',
            'subtitle': 'this subtitle has been added by a curator',
            'title':    'ANTARES: An observatory at the seabed '
                        'to the confines of the Universe'
        }
    ]}
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_urls_field():
    root = {'urls': [
        {'description': 'descr 1', 'value': 'a'}
    ]}
    head = {'urls': [
        {'description': 'descr 1', 'value': 'a'},
        {'description': 'descr 2', 'value': 'b'},

    ]}
    update = {}

    expected_merged = head
    expected_conflict = [['REMOVE_FIELD', ['urls'], None]]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_wirthdrawn_field():
    root = {}
    head = {'withdrawn': True}
    update = {'withdrawn': False}

    expected_merged = update
    expected_conflict = [['SET_FIELD', ['withdrawn'], True]]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict
