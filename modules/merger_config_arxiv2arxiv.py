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
AcceleratorExperimentsComparator = get_pk_comparator(['version_id'])
AcquisitionSourceComparator = get_pk_comparator(['version_id'])
FilesComparator = get_pk_comparator(['version_id'])

AffiliationComparator = get_pk_comparator(['recid'])
AuthorComparator = get_pk_comparator(['full_name'])
CreationDatetimeComparator = get_pk_comparator(['creation_datetime'])
DateComparator = get_pk_comparator(['date'])

FundingInfoComparator = get_pk_comparator(['project_number'])
HolderComparator = get_pk_comparator(['holder'])
ImprintsComparator = get_pk_comparator(['publisher'])
LanguageComparator = get_pk_comparator(['language'])
LicenseComparator = get_pk_comparator(['imposing'])

PIDComparator = get_pk_comparator(['value'])
ValueComparator = get_pk_comparator(['value'])

RecordComparator = get_pk_comparator(['record.$ref'])
RefComparator = get_pk_comparator(['$ref'])
SchemaComparator = get_pk_comparator(['schema'])
TitleComparator = get_pk_comparator(['title'])

# RecordComparator = get_pk_comparator(['thesis_info.record.$ref'])


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
    # 'document_type': 'has to be defined/implmented',
    'dois': ValueComparator,
    # 'editions': 'has to be defined/implmented',
    # 'energy_ranges': 'has to be defined/implmented',
    'external_system_identifiers': SchemaComparator,
    'funding_info': FundingInfoComparator,
    'imprints': ImprintsComparator,
    # 'inspire_categories': 'has to be defined/implmented',
    'isbns': ValueComparator,
    'keywords': ValueComparator,
    # 'languages': 'has to be defined/implmented',
    # 'legacy_creation_date': 'has to be defined/implmented',
    'license': LicenseComparator,
    'new_record': RefComparator,
    # 'number_of_pages': 'has to be defined/implmented',
    'persistent_identifiers': ValueComparator,
    # 'preprint_date': ,
    'public_notes': SourceComparator,
    'publication_info': PubInfoComparator,
    # 'publication_type': 'has to be defined/implmented',
    # 'refereed': 'has to be defined/implmented',
    'references': 'has to be defined/implmented',
    'report_numbers': SourceComparator,
    # 'self': 'has to be defined/implmented',
    # 'special_collections': 'has to be defined/implmented',
    # 'succeeding_entry': 'has to be defined/implmented',
    # 'texkeys': 'has to be defined/implmented',
    # 'thesis_info.institutions': RecordComparator,
    'title_translations': LanguageComparator,
    'titles': LanguageComparator,
    # 'urls': 'has to be defined/implmented',
    # 'withdrawn': 'has to be defined/implmented'
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
    'document_type': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'dois': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST,
    'editions':  UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST,
    'energy_ranges': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'external_system_identifiers': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'funding_info': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    # 'imprints': 'has to be defined',
    'inspire_categories': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_UPDATE_FIRST,
    'isbns': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_UPDATE_FIRST,
    'keywords': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_UPDATE_FIRST,
    'languages': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    # 'legacy_creation_date': 'has to be defined',
    'license': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_UPDATE_FIRST,
    # 'new_record': 'has to be defined',
    # 'number_of_pages': 'has to be defined',
    'persistent_identifiers': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    # 'preprint_date': 'has to be defined',
    'public_notes': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'publication_info': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST,
    'publication_type': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    # 'refereed': 'has to be defined',
    'references': 'has to be defined',
    'report_numbers': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    # 'self': 'has to be defined',
    'special_collections': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    # 'succeeding_entry': 'has to be defined',
    'texkeys': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    'thesis_info.institutions': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'title_translations': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    'titles': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST,
    'urls': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST,
    # 'withdrawn': 'has to be defined'
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
    'external_system_identifiers': DictMergerOps.FALLBACK_KEEP_HEAD,
    'funding_info': DictMergerOps.FALLBACK_KEEP_HEAD,
    'legacy_creation_date': DictMergerOps.FALLBACK_KEEP_HEAD,
    'new_record': DictMergerOps.FALLBACK_KEEP_HEAD,
    'persistent_identifiers': DictMergerOps.FALLBACK_KEEP_HEAD,
    'preprint_date': DictMergerOps.FALLBACK_KEEP_HEAD,
    'self': DictMergerOps.FALLBACK_KEEP_HEAD,
    'special_collections': DictMergerOps.FALLBACK_KEEP_HEAD,
    'succeeding_entry': DictMergerOps.FALLBACK_KEEP_HEAD,
    'texkeys': DictMergerOps.FALLBACK_KEEP_HEAD,
    'thesis_info.institutions': DictMergerOps.FALLBACK_KEEP_HEAD,
    'title_translations': DictMergerOps.FALLBACK_KEEP_HEAD,
    'urls': DictMergerOps.FALLBACK_KEEP_HEAD,
}
