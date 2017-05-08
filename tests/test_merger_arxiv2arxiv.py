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
    root = {'$schema': 'http://inspire-nightly.cern.ch/schemas/records/hep.json'}  # record_id: 1308464
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
        '_desy_bookkeeping': [
            {
                'date': '2014-07-31',
                'expert': 'B',
                'status': 'abs'
            }, {
                'date': '2014-08-06',
                'expert': 'B',
                'status': 'printed'
            }, {
                'date': '2015-01-02',
                'status': 'final'
            }
        ]
    }
    # record_id: 1308464
    head = {
        '_desy_bookkeeping': [
            {
                'date': '2014-07-31',
                'expert': 'B',
                'status': 'printed2'
            }, {
                'date': '2014-08-06',
                'expert': 'B',
                'status': 'printed'
            }, {
                'date': '2015-01-02',
                'expert': 'B',
                'status': 'final'
            }
        ]
    }
    update = {
        '_desy_bookkeeping': [
            {
                'date': '2014-07-31',
                'status': 'abs'
            }, {
                'date': '2014-08-06',
                'expert': 'B',
                'status': 'printed'
            }, {
                'date': '2015-01-03',
                'status': 'final'
            }
        ]
    }

    expected_merged = {
        '_desy_bookkeeping': [
            {
                'date': '2014-07-31',
                'status': 'printed2'
            }, {
                'date': '2014-08-06',
                'expert': 'B',
                'status': 'printed'
            }, {
                'date': '2015-01-02',
                'expert': 'B',
                'status': 'final'
            }

        ]
    }
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_export_to_field():
    root = {
        '_export_to': {
            'CDS': False,
            'HAL': False
        }
    }
    # record_id: 432169 & 717606
    head = {
        '_export_to': {
            'CDS': True,
            'HAL': False
        }
    }
    update = {
        '_export_to': {
            'CDS': False,
            'HAL': False
        }
    }

    expected_merged = head
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_fft_field():
    root = {
        '_fft': [
            {
                'creation_datetime': '2014-07-28T23:15:16',
                'description': 'Fulltext',
                'filename': 'fermilab-thesis-2014-17',
                'format': '.pdf',
                'path': '/opt/cds-invenio/var/data/files/g95/1902084/content.pdf;1',
                'type': 'Main',
                'version': 1
            }
        ]
    }
    # record_id: 1308464
    head = {
        '_fft': [
            {
                'creation_datetime': '2014-07-28T23:15:16',
                'description': 'Fulltext',
                'filename': 'fermilab-thesis-2014-18',
                'format': '.pdf',
                'path': '/opt/cds-invenio/var/data/files/g95/1902084/content.pdf;1',
                'type': 'Main',
                'version': 1
            }
        ]
    }
    update = {
        '_fft': [
            {
                'creation_datetime': '2014-07-28T23:15:16',
                'description': 'Fulltext',
                'filename': 'fermilab-thesis-2014-19',
                'format': '.pdf',
                'path': '/opt/cds-invenio/var/data/files/g95/1902084/content.pdf;1',
                'type': 'Main',
                'version': 1
            }
        ]
    }

    expected_merged = head
    expected_conflict = [['SET_FIELD', ['_fft', 0, 'filename'], 'fermilab-thesis-2014-19']]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_files_field():
    root = {
        '_files': [
            {
                'bucket': 'foo',
                'checksum': 'bar',
                'key': 'baz',
                'previewer': 'spam',
                'size': 'egg',
                'type': 'eggs',
                'version_id': 'version'
            }
        ]
    }
    # record_id: not found 9/05/2017
    head = {
        '_files': [
            {
                'bucket': 'foo1',
                'checksum': 'bar',
                'key': 'baz',
                'previewer': 'spam',
                'size': 'egg',
                'type': 'eggs',
                'version_id': 'version'
            }
        ]
    }
    update = {
        '_files': [
            {
                'bucket': 'foo2',
                'checksum': 'bar',
                'key': 'baz',
                'previewer': 'spam',
                'size': 'egg',
                'type': 'eggs',
                'version_id': 'version'
            }, {
                'bucket': 'foo2',
                'checksum': 'bar',
                'key': 'baz',
                'previewer': 'spam',
                'size': 'egg',
                'type': 'eggs',
                'version_id': 'second version'
            }
        ]
    }

    expected_merged = update
    expected_conflict = [['SET_FIELD', ['_files', 0, 'bucket'], 'foo1']]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_private_notes_field():
    root = {
        '_private_notes': [
            {
                'source': 'SPIRES-HIDDEN',
                'value': 'Update from APS OAI Harvest'
            }
        ]
    }
    # record_id: 905854
    head = {
        '_private_notes': [
            {
                'source': 'SPIRES-HIDDEN',
                'value': 'Update from APS OAI Harvest foo'
            }
        ]
    }
    update = {
        '_private_notes': [
            {
                'source': 'SPIRES-HIDDEN',
                'value': 'Update from APS OAI Harvest bar'
            }, {
                'source': 'SPIRES',
                'value': 'Added by ..HEP.ADD.TO.HEP from APS OAI Harvest'
            }
        ]
    }

    expected_merged = {
        '_private_notes': [
            {
                'source': 'SPIRES-HIDDEN',
                'value': 'Update from APS OAI Harvest foo'
            }
        ]
    }
    expected_conflict = [['SET_FIELD', ['_private_notes', 0, 'value'], 'Update from APS OAI Harvest bar']]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_abstracts_field():
    root = {
        'abstracts': [
            {
                'value': 'We investigate the structure of a proto-neutron star with '
                         'trapped neutrinos by us ing quantum hadrodynamics.',
                'source': 'arxiv'
            }
        ]
    }
    # record_id: 905854
    head = {
        'abstracts': [
            {
                'value': 'We investigate the structure of a proto-neutron star with '
                         'trapped neutrinos by us ing quantum hadrodynamics. bar',
                'source': 'arxiv'
            }
        ]
    }
    update = {
        'abstracts': [
            {
                'value': 'We investigate the structure of a proto-neutron star with '
                         'trapped neutrinos by us ing quantum hadrodynamics. foo',
                'source': 'arxiv'
            }
        ]
    }

    expected_merged = update
    expected_conflict = [
        [
            'SET_FIELD',
            ['abstracts', 0, 'value'],
            'We investigate the structure of a proto-neutron star with '
            'trapped neutrinos by us ing quantum hadrodynamics. bar'
        ]
    ]
    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_accelerator_experiments_field():
    root = {
        'accelerator_experiments': [
            {
                'curated_relation': True,
                'experiment': 'FNAL-E-0830',
                'facet_experiment': [
                    ['FNAL-E-0830']
                ],
                'recid': 1110316,
                'record': {
                    '$ref': 'http://newlabs.inspirehep.net/api/experiments/1110316'
                }
            }
        ],
    }
    # record_id: 982117
    head = {
        'accelerator_experiments': [
            {
                'curated_relation': True,
                'experiment': 'FNAL-E-08302',
                'facet_experiment': [
                    ['FNAL-E-0830']
                ],
                'recid': 1110316,
                'record': {
                    '$ref': 'http://newlabs.inspirehep.net/api/experiments/1110316'
                }
            }, {
                'curated_relation': True,
                'experiment': 'FNAL-E-08301',
                'facet_experiment': [
                    ['FNAL-E-0831']
                ],
                'recid': 1110317,
                'record': {
                    '$ref': 'http://newlabs.inspirehep.net/api/experiments/1110317'
                }
            }
        ],
    }
    update = {
        'accelerator_experiments': [
            {
                'curated_relation': True,
                'experiment': 'FNAL-E-08301',
                'facet_experiment': [
                    ['FNAL-E-0830']
                ],
                'recid': 1110316,
                'record': {
                    '$ref': 'http://newlabs.inspirehep.net/api/experiments/1110316'
                }
            }
        ],
    }

    expected_merged = head
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_acquisition_source_field():
    root = {
        'acquisition_source': {
            'method': 'batchuploade',
            'source': 'ejl'
        }
    }
    # record_id: 1517095
    head = {
        'acquisition_source': {
            'method': 'batchuploadeR',
            'source': 'ejl'
        }
    }
    update = {
        'acquisition_source': {
            'method': 'batchuploader',
            'source': 'ejl'
        }
    }

    expected_merged = head
    expected_conflict = [['SET_FIELD', ['acquisition_source', 'method'], 'batchuploader']]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_arxiv_eprints_field():
    root = {
        'arxiv_eprints': [
            {
                'categories': [
                    'nucl-th',
                    'astro-ph'
                ],
                'value': 'astro-physics'
            }
        ]
    }
    # record id: There are not examples of this kind of
    # field in Inspire. We created some examples with
    # the real date inside inspire.
    head = {
        'arxiv_eprints': [
            {
                'categories': [
                    'nucl-th',
                    'astro-ph'
                ],
                'value': 'astro-physics'
            }
        ]
    }
    update = {
        'arxiv_eprints': [
            {
                'categories': [
                    'nucl-th',
                    'math'
                ],
                'value': 'astro-physics'
            }, {
                'categories': [
                    'gr-qc'
                ],
                'value': 'General Relativity'
            }
        ]
    }

    expected_merged = {
        'arxiv_eprints': [
            {
                'categories': [
                    'nucl-th',
                    'math'
                ],
                'value': 'astro-physics'
            }, {
                'categories': [
                    'gr-qc'
                ],
                'value': 'General Relativity'
            }
        ]
    }
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


# def test_merging_authors_field():
#     root = {"authors": [
#         {
#         "affiliations": [
#           {
#             "recid": 902867,
#             "record": {
#               "$ref": "http://newlabs.inspirehep.net/api/institutions/902867"
#             },
#             "value": "Illinois U., Urbana"
#           }
#         ],
#         "curated_relation": True,
#         "full_name": "Matera, Keith",
#         "ids": [
#           {
#             "schema": "INSPIRE ID",
#             "value": "INSPIRE-00264905"
#           }
#         ],
#         "name_suggest": {
#           "input": [
#             "K Matera",
#             "Keith Matera",
#             "Matera",
#             "Matera K",
#             "Matera Keith",
#             "Matera, K",
#             "Matera, Keith"
#           ],
#           "output": "Matera, Keith",
#           "payload": {
#             "bai": None
#           }
#         },
#         "name_variations": [
#           "K Matera",
#           "Keith Matera",
#           "Matera",
#           "Matera K",
#           "Matera Keith",
#           "Matera, K",
#           "Matera, Keith"
#         ],
#         "recid": 1051922,
#         "record": {
#           "$ref": "http://newlabs.inspirehep.net/api/authors/1051922"
#         },
#         "uuid": "110ff8b8-f73e-4959-8fbf-fe16d62d83c2"
#         },
#         {
#         "affiliations": [
#           {
#             "recid": 902867,
#             "record": {
#               "$ref": "http://newlabs.inspirehep.net/api/institutions/902867"
#             },
#             "value": "Illinois U., Urbana"
#           }
#         ],
#         "full_name": "Pitts, Kevin T.",
#         "inspire_roles": [
#           "supervisor"
#         ],
#         "name_suggest": {
#           "input": [
#             "K Pitts",
#             "K T Pitts",
#             "Kevin Pitts",
#             "Kevin T Pitts",
#             "Pitts",
#             "Pitts K",
#             "Pitts K T",
#             "Pitts Kevin",
#             "Pitts Kevin T",
#             "Pitts T",
#             "Pitts, K",
#             "Pitts, K T",
#             "Pitts, Kevin",
#             "Pitts, Kevin T",
#             "Pitts, T",
#             "T Pitts"
#           ],
#           "output": "Pitts, Kevin T.",
#           "payload": {
#             "bai": None
#           }
#         },
#         "name_variations": [
#           "K Pitts",
#           "K T Pitts",
#           "Kevin Pitts",
#           "Kevin T Pitts",
#           "Pitts",
#           "Pitts K",
#           "Pitts K T",
#           "Pitts Kevin",
#           "Pitts Kevin T",
#           "Pitts T",
#           "Pitts, K",
#           "Pitts, K T",
#           "Pitts, Kevin",
#           "Pitts, Kevin T",
#           "Pitts, T",
#           "T Pitts"
#         ],
#         "uuid": "800ba182-b01a-4fbb-896b-3afc3896f5de"
#         }
#         ]}
#     #1308464
#     head = {"authors": [
#         {
#         "affiliations": [
#           {
#             "recid": 902867,
#             "record": {
#               "$ref": "http://newlabs.inspirehep.net/api/institutions/902867"
#             },
#             "value": "Illinois University of Urbana"
#           }
#         ],
#         "curated_relation": True,
#         "full_name": "Matera, Keith",
#         "ids": [
#           {
#             "schema": "INSPIRE ID",
#             "value": "INSPIRE-00264905"
#           }
#         ],
#         "name_suggest": {
#           "input": [
#             "K Matera",
#             "Keith Matera",
#             "Matera",
#             "Matera K",
#             "Matera Keith",
#             "Matera, K",
#             "Matera, Keith"
#           ],
#           "output": "Matera, Keith",
#           "payload": {
#             "bai": None
#           }
#         },
#         "name_variations": [
#           "K Matera",
#           "Keith Matera",
#           "Matera",
#           "Matera K",
#           "Matera Keith",
#           "Matera, K",
#           "Matera, Keith"
#         ],
#         "recid": 1051922,
#         "record": {
#           "$ref": "http://newlabs.inspirehep.net/api/authors/1051922"
#         },
#         "uuid": "110ff8b8-f73e-4959-8fbf-fe16d62d83c2"
#         },
#         {
#         "affiliations": [
#           {
#             "recid": 902867,
#             "record": {
#               "$ref": "http://newlabs.inspirehep.net/api/institutions/902867"
#             },
#             "value": "Illinois U., Urbana"
#           }
#         ],
#         "full_name": "Pitts, Kevin T.",
#         "inspire_roles": [
#           "supervisor"
#         ],
#         "name_suggest": {
#           "input": [
#             "K Pitts",
#             "K T Pitts",
#             "Kevin Pitts",
#             "Kevin T Pitts",
#             "Pitts",
#             "Pitts K",
#             "Pitts K T",
#             "Pitts Kevin",
#             "Pitts Kevin T",
#             "Pitts T",
#             "Pitts, K",
#             "Pitts, K T",
#             "Pitts, Kevin",
#             "Pitts, Kevin T",
#             "Pitts, T",
#             "T Pitts"
#           ],
#           "output": "Pitts, Kevin T.",
#           "payload": {
#             "bai": None
#           }
#         },
#         "name_variations": [
#           "K Pitts",
#           "K T Pitts",
#           "Kevin Pitts",
#           "Kevin T Pitts",
#           "Pitts",
#           "Pitts K",
#           "Pitts K T",
#           "Pitts Kevin",
#           "Pitts Kevin T",
#           "Pitts T",
#           "Pitts, K",
#           "Pitts, K T",
#           "Pitts, Kevin",
#           "Pitts, Kevin T",
#           "Pitts, T",
#           "T Pitts"
#         ],
#         "uuid": "800ba182-b01a-4fbb-896b-3afc3896f5de"
#         }
#     ]}
#     update = {"authors": [
#         {
#         "affiliations": [
#           {
#             "recid": 902867,
#             "record": {
#               "$ref": "http://newlabs.inspirehep.net/api/institutions/902867"
#             },
#             "value": "Illinois University Urbana"
#           }
#         ],
#         "curated_relation": True,
#         "full_name": "Matera, Keith",
#         "ids": [
#           {
#             "schema": "INSPIRE ID",
#             "value": "INSPIRE-00264905"
#           }
#         ],
#         "name_suggest": {
#           "input": [
#             "K Matera",
#             "Keith Matera",
#             "Matera",
#             "Matera K",
#             "Matera Keith",
#             "Matera, K",
#             "Matera, Keith"
#           ],
#           "output": "Matera, Keith",
#           "payload": {
#             "bai": None
#           }
#         },
#         "name_variations": [
#           "K Matera",
#           "Keith Matera",
#           "Matera",
#           "Matera K",
#           "Matera Keith",
#           "Matera, K",
#           "Matera, Keith"
#         ],
#         "recid": 1051922,
#         "record": {
#           "$ref": "http://newlabs.inspirehep.net/api/authors/1051922"
#         },
#         "uuid": "110ff8b8-f73e-4959-8fbf-fe16d62d83c2"
#         },
#         {
#         "affiliations": [
#           {
#             "recid": 902867,
#             "record": {
#               "$ref": "http://newlabs.inspirehep.net/api/institutions/902867"
#             },
#             "value": "Illinois U., Urbana"
#           }
#         ],
#         "full_name": "Pitts, Kevin T.",
#         "inspire_roles": [
#           "supervisor"
#         ],
#         "name_suggest": {
#           "input": [
#             "K Pitts",
#             "K T Pitts",
#             "Kevin Pitts",
#             "Kevin T Pitts",
#             "Pitts",
#             "Pitts K",
#             "Pitts K T",
#             "Pitts Kevin",
#             "Pitts Kevin T",
#             "Pitts T",
#             "Pitts, K",
#             "Pitts, K T",
#             "Pitts, Kevin",
#             "Pitts, Kevin T",
#             "Pitts, T",
#             "T Pitts"
#           ],
#           "output": "Pitts, Kevin T.",
#           "payload": {
#             "bai": None
#           }
#         },
#         "name_variations": [
#           "K Pitts",
#           "K T Pitts",
#           "Kevin Pitts",
#           "Kevin T Pitts",
#           "Pitts",
#           "Pitts K",
#           "Pitts K T",
#           "Pitts Kevin",
#           "Pitts Kevin T",
#           "Pitts T",
#           "Pitts, K",
#           "Pitts, K T",
#           "Pitts, Kevin",
#           "Pitts, Kevin T",
#           "Pitts, T",
#           "T Pitts"
#         ],
#         "uuid": "800ba182-b01a-4fbb-896b-3afc3896f5de"
#         }
#         ]}
#
#     expected_merged = head
#     expected_conflict = None
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
#

# def test_merging_affiliations_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict


def test_merging_book_series_field():
    root = {
        'book_series': [
            {
                'title': 'IEEE Nucl.Sci.Symp.Conf.Rec.',
                'volume': 'bar'
            }
        ]
    }
    # record_id: 1212189
    head = {
        'book_series': [
            {
                'title': 'IEEE Nucl.Sci.Symp.Conf.Rec.',
                'volume': 'baz'
            }, {
                'title': 'CMS Web-Based Monitoring',
                'volume': 'spam'
            }
        ]
    }
    update = {
        'book_series': [
            {
                'title': 'IEEE Nucl.Sci.Symp.Conf.Rec.',
                'volume': 'spam'
            }, {
                'title': 'Proposal for Web Based Monitoring and Database Browsing"',
                'volume': 'spam'
            }
        ]
    }

    expected_merged = head
    expected_conflict = [['SET_FIELD', ['book_series', 0, 'volume'], 'spam']]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_citeable_field():
    root = {'citeable': False}
    head = {'citeable': False}
    update = {'citeable': True}

    expected_merged = update
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_collaborations_field():
    root = {
        'collaborations': [
            {
                'record':
                    {
                        '$ref': 'http://newlabs.inspirehep.net/api/literature/684121'
                    },
                'value': 'LHCb'
            }
        ]
    }
    # record_id: 1517390
    head = {
        'collaborations': [
            {
                'record':
                    {
                        '$ref': 'http://newlabs.inspirehep.net/api/literature/684121'
                    },
                'value': 'ATLAS'
            }, {
                'record':
                    {
                        '$ref': 'http://newlabs.inspirehep.net/api/literature/684122'
                    },
                'value': 'CMS'
            }
        ]
    }
    update = {
        'collaborations': [
            {
                'record':
                    {
                        '$ref': 'http://newlabs.inspirehep.net/api/literature/684121'
                    },
                'value': 'ALICE'
            }
        ]
    }

    expected_merged = {
        'collaborations': [
            {
                'record':
                    {
                        '$ref': 'http://newlabs.inspirehep.net/api/literature/684121'
                    },
                'value': 'ALICE'
            }, {
                'record':
                    {
                        '$ref': 'http://newlabs.inspirehep.net/api/literature/684122'
                    },
                'value': 'CMS'
            }
        ]
    }
    expected_conflict = [['SET_FIELD', ['collaborations', 0, 'value'], 'ATLAS']]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_control_number_field():
    root = {'control_number': 963517}
    head = {'control_number': 963518}
    update = {'control_number': 963519}
    # record_id:

    expected_merged = head
    expected_conflict = [['SET_FIELD', ['control_number'], 963519]]

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_copyright_field():
    root = {
        'copyright': [
            {
                'holder': 'Elsevier',
                'material': 'For open access articles',
                'statement': 'Copyright @ unknown. Published by Elsevier B.V.',
                'url': 'https://www.elsevier.com/about/our-business/policies/copyright',
                'year': 2011
            }
        ]
    }
    # record_id: 963517
    head = {
        'copyright': [
            {
                'holder': 'elsevier',
                'material': 'For open access articles',
                'statement': 'Copyright @ unknown. Published by Elsevier B.V.',
                'url': 'https://www.elsevier.com/about/our-business/policies/copyright',
                'year': 2011
            }
        ]
    }
    update = {
        'copyright': [
            {
                'holder': 'Elsevier',
                'material': 'For open access articles',
                'statement': 'Copyright @ unknown. Published by Elsevier B.V.',
                'url': 'https://www.elsevier.com/about/our-business/policies/copyright',
                'year': 2011
            }
        ]
    }
    expected_merged = update
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_core_field():
    root = {'core': False}
    head = {'core': False}
    update = {'core': True}

    expected_merged = update
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_corporate_author_field():
    root = {
        'corporate_author': [
            'The LHCb Collaboration'
        ]
    }
    # record_id: 1517390
    head = {
        'corporate_author': [
            'The LHCb Collaboration',
            'CMS Collaboration'
        ]
    }
    update = {
        'corporate_author': [
            'CMS Collaboration'
        ]
    }

    expected_merged = update
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_deleted_field():
    root = {'deleted': False}
    head = {'deleted': False}
    update = {'deleted': True}

    expected_merged = update
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


def test_merging_deleted_records_field():
    root = {
        'deleted_records': [
            {
                '$ref': 'http://newlabs.inspirehep.net/api/record/980409'
            }
        ]
    }
    # record_id: 963741
    head = {

        'deleted_records': [
            {
                '$ref': 'http://newlabs.inspirehep.net/api/record/980410'
            }
        ]
    }
    update = {
        'deleted_records': [
            {
                '$ref': 'http://newlabs.inspirehep.net/api/record/980419'
            }
        ]
    }

    expected_merged = head
    expected_conflict = None

    merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)

    assert merged == expected_merged
    assert conflict == expected_conflict


# def test_merging_document_type_field():
#     root = {}
#     head = {}
#     update = {}
#
#     expected_merged = {}
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
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
#     expected_conflict = None
#
#     merged, conflict = json_merger_arxiv_to_arxiv(root, head, update)
#
#     assert merged == expected_merged
#     assert conflict == expected_conflict
