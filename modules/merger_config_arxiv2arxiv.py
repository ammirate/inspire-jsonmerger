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

from json_merger.config import DictMergerOps, UnifierOps
from json_merger.comparator import PrimaryKeyComparator
from json_merger.contrib.inspirehep.author_util import (
    AuthorNameDistanceCalculator,
    AuthorNameNormalizer,
    NameToken,
    NameInitial
)
from json_merger.contrib.inspirehep.comparators import (
        DistanceFunctionComparator
)

from inspirehep.modules.authors.utils import scan_author_string_for_phrases


def author_tokenize(name):
    """This is how the name should be tokenized for the matcher."""
    phrases = scan_author_string_for_phrases(name)
    res = {'lastnames': [], 'nonlastnames': []}
    for key, tokens in phrases.items():
        lst = res.get(key)
        if lst is None:
            continue
        for token in tokens:
            if len(token) == 1:
                lst.append(NameInitial(token))
            else:
                lst.append(NameToken(token))
    return res


class NewIDNormalizer(object):
    """Callable that can be used to normalize by a given id for authors.
    Because now all the ids are in the list."""
    def __init__(self, id_type):
        self.id_type = id_type

    def __call__(self, author):
        """Sadly this will get only the first one. but well, it's just an
        optimisation for faster matches."""

        for id_field in author.get('ids', []):
            if id_field.get('type').lower() == self.id_type.lower():
                return id_field.get('value')
        # This is safe since the normalization is not the final decider.
        return None


# class AuthorComparator(DistanceFunctionComparator):
#     threhsold = 0.12
#     distance_function = AuthorNameDistanceCalculator(author_tokenize)
#     norm_functions = [
#             NewIDNormalizer('ORCID'),
#             NewIDNormalizer('INSPIRE BAI'),
#             AuthorNameNormalizer(author_tokenize),
#             AuthorNameNormalizer(author_tokenize, 1),
#             AuthorNameNormalizer(author_tokenize, 1, True)
#     ]


def get_pk_comparator(primary_key_fields, normalization_functions=None):
    class Ret(PrimaryKeyComparator):
        pass
    Ret.primary_key_fields = primary_key_fields
    Ret.normalization_functions = normalization_functions or {}
    return Ret

# already present
SourceComparator = get_pk_comparator(['source'])
ValueComparator = get_pk_comparator(['value'])
CollectionsComparator = get_pk_comparator(['primary'])
ExtSysNumberComparator = get_pk_comparator(['institute'])
URLComparator = get_pk_comparator(['url'])
PubInfoComparator = get_pk_comparator(
    [
        ['journal_title', 'journal_volume', 'page_start'],
        ['journal_title', 'journal_volume', 'artid']
    ]
)

#new comparators
DateComparator = get_pk_comparator(['date'])
CreationDatetimeComparator = get_pk_comparator(['creation_datetime'])
AffiliationComparator = get_pk_comparator(['recid'])
AuthorComparator = get_pk_comparator(['full_name'])
FilesComparator = get_pk_comparator(['version_id'])
AcceleratorExperimentsComparator = get_pk_comparator(['version_id'])
AcquisitionSourceComparator = get_pk_comparator(['version_id'])
TitleComparator = get_pk_comparator(['title'])
RecordComparator = get_pk_comparator(['record.$ref'])
HolderComparator = get_pk_comparator(['holder'])
RefComparator = get_pk_comparator(['$ref'])


COMPARATORS = {
    '_desy_bookkeeping': DateComparator,
    '_fft': CreationDatetimeComparator,
    '_files': FilesComparator,
    '_private_notes': SourceComparator,
    'abstracts': SourceComparator,
    'accelerator_experiments': AcceleratorExperimentsComparator,
    'acquisition_source': SourceComparator,
    'arxiv_eprints': ValueComparator,
    # 'authors': AuthorComparator,
    # 'authors.affiliations': AffiliationComparator,
    # 'authors.alternative_names': 'has to be defined/implemented',
    # 'authors.credit_roles': 'has to be defined/implemented',
    # 'authors.curated_relation': 'has to be defined/implemented',
    # 'authors.emails': 'has to be defined/implemented',
    # 'authors.full_name': 'has to be defined/implemented',
    # 'authors.ids': 'has to be defined/implemented',
    # 'authors.inspire_roles': 'has to be defined/implemented',
    # 'authors.raw_affiliations': 'has to be defined/implemented',
    # 'authors.record': 'has to be defined/implemented',
    # 'authors.signature_block': 'has to be defined/implemented',
    # 'authors.uuid': 'has to be defined/implemented',
    'book_series': TitleComparator,
    'collaborations': RecordComparator,
    'copyright': HolderComparator,
    'deleted_records': RefComparator,
    # 'document_type': 'has to be defined/implemented',
    # 'dois': 'has to be defined/implemented',
    # 'editions': 'has to be defined/implemented',
    # 'energy_ranges': 'has to be defined/implemented',
    # 'external_system_identifiers': 'has to be defined/implemented',
    # 'funding_info': 'has to be defined/implemented',
    # 'imprints': 'has to be defined/implemented',
    # 'inspire_categories': 'has to be defined/implemented',
    # 'isbns': 'has to be defined/implemented',
    # 'keywords': 'has to be defined/implemented',
    # 'languages': 'has to be defined/implemented',
    # 'legacy_creation_date': 'has to be defined/implemented',
    # 'license': 'has to be defined/implemented',
    # 'new_record': 'has to be defined/implemented',
    # 'number_of_pages': 'has to be defined/implemented',
    # 'persistent_identifiers': 'has to be defined/implemented',
    # 'preprint_date': 'has to be defined/implemented',
    # 'public_notes': 'has to be defined/implemented',
    # 'publication_info': PubInfoComparator,
    # 'publication_type': 'has to be defined/implemented',
    # 'refereed': 'has to be defined/implemented',
    # 'references': 'has to be defined/implemented',
    # 'report_numbers': 'has to be defined/implemented',
    # 'self': 'has to be defined/implemented',
    # 'special_collections': 'has to be defined/implemented',
    # 'succeeding_entry': 'has to be defined/implemented',
    # 'texkeys': 'has to be defined/implemented',
    # 'thesis_info': 'has to be defined/implemented',
    # 'title_translations': 'has to be defined/implemented',
    # 'titles': 'has to be defined/implemented',
    # 'urls': 'has to be defined/implemented',
    # 'wirthdrawn': 'has to be defined/implemented'
}

# We an always default to KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST so
# this is less verbose.
LIST_MERGE_OPS = {
    '_collections': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    '_desy_bookkeeping': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    '_fft': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    '_files': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    '_private_notes': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    'abstracts': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_UPDATE_FIRST,
    'accelerator_experiments': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    'arxiv_eprints': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST,
    # 'authors': UnifierOps.KEEP_UPDATE_ENTITIES_CONFLICT_ON_HEAD_DELETE,
    # 'authors.affiliations': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    # 'authors.alternative_names': 'has to be defined',
    # 'authors.credit_roles': 'has to be defined',
    # 'authors.curated_relation': 'has to be defined',
    # 'authors.emails': 'has to be defined',
    # 'authors.full_name': 'has to be defined',
    # 'authors.ids': 'has to be defined',
    # 'authors.inspire_roles': 'has to be defined',
    # 'authors.raw_affiliations': 'has to be defined',
    # 'authors.record': 'has to be defined',
    # 'authors.signature_block': 'has to be defined',
    # 'authors.uuid': 'has to be defined',
    'book_series': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    'collaborations': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST,
    'copyright': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'corporate_author': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'deleted_records': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    # 'document_type': 'has to be defined',
    # 'dois': 'has to be defined',
    # 'editions': 'has to be defined',
    # 'energy_ranges': 'has to be defined',
    # 'external_system_identifiers': 'has to be defined',
    # 'funding_info': 'has to be defined',
    # 'imprints': 'has to be defined',
    # 'inspire_categories': 'has to be defined',
    # 'isbns': 'has to be defined',
    # 'keywords': 'has to be defined',
    # 'languages': 'has to be defined',
    # 'legacy_creation_date': 'has to be defined',
    # 'license': 'has to be defined',
    # 'new_record': 'has to be defined',
    # 'number_of_pages': 'has to be defined',
    # 'persistent_identifiers': 'has to be defined',
    # 'preprint_date': 'has to be defined',
    # 'public_notes': 'has to be defined',
    # 'publication_info': 'has to be defined',
    # 'publication_type': 'has to be defined',
    # 'refereed': 'has to be defined',
    # 'references': 'has to be defined',
    # 'report_numbers': 'has to be defined',
    # 'self': 'has to be defined',
    # 'special_collections': 'has to be defined',
    # 'succeeding_entry': 'has to be defined',
    # 'texkeys': 'has to be defined',
    # 'thesis_info': 'has to be defined',
    # 'title_translations': 'has to be defined',
    # 'titles': 'has to be defined',
    # 'urls': 'has to be defined',
    # 'wirthdrawn': 'has to be defined'
}

FIELD_MERGE_OPS = {
    '$schema': DictMergerOps.FALLBACK_KEEP_HEAD,
    '_desy_bookkeeping': DictMergerOps.FALLBACK_KEEP_HEAD,
    '_export_to': DictMergerOps.FALLBACK_KEEP_HEAD,
    '_fft': DictMergerOps.FALLBACK_KEEP_HEAD,
    '_private_notes': DictMergerOps.FALLBACK_KEEP_HEAD,
    'accelerator_experiments': DictMergerOps.FALLBACK_KEEP_HEAD,
    'acquisition_source': DictMergerOps.FALLBACK_KEEP_HEAD,
    'book_series': DictMergerOps.FALLBACK_KEEP_HEAD,
    'control_number': DictMergerOps.FALLBACK_KEEP_HEAD,
    'deleted': DictMergerOps.FALLBACK_KEEP_HEAD,
    'deleted_records': DictMergerOps.FALLBACK_KEEP_HEAD,
    # '': DictMergerOps.FALLBACK_KEEP_HEAD,

}
