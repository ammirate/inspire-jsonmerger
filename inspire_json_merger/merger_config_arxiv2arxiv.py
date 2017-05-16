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
            if id_field.get('schema').lower() == self.id_type.lower():
                return id_field.get('value')
        # This is safe since the normalization is not the final decider.
        return None


class AuthorComparator(DistanceFunctionComparator):
    threhsold = 0.12
    distance_function = AuthorNameDistanceCalculator(author_tokenize)
    norm_functions = [
            NewIDNormalizer('ORCID'),
            NewIDNormalizer('INSPIRE BAI'),
            AuthorNameNormalizer(author_tokenize),
            AuthorNameNormalizer(author_tokenize, 1),
            AuthorNameNormalizer(author_tokenize, 1, True)
    ]


def get_pk_comparator(primary_key_fields, normalization_functions=None):
    class Ret(PrimaryKeyComparator):
        pass
    Ret.primary_key_fields = primary_key_fields
    Ret.normalization_functions = normalization_functions or {}
    return Ret


AffiliationComparator = get_pk_comparator(['record.$ref', 'value'])
CollectionsComparator = get_pk_comparator(['primary'])
CreationDatetimeComparator = get_pk_comparator(['creation_datetime'])
DateComparator = get_pk_comparator(['date'])
ExtSysNumberComparator = get_pk_comparator(['institute'])
FilesComparator = get_pk_comparator(['version_id'])
FundingInfoComparator = get_pk_comparator(['project_number'])
ImprintsComparator = get_pk_comparator(['publisher'])
LanguageComparator = get_pk_comparator(['language'])
LicenseComparator = get_pk_comparator(['imposing'])
MaterialComparator = get_pk_comparator(['material'])
RecordComparator = get_pk_comparator(['record.$ref'])
RefComparator = get_pk_comparator(['$ref'])
SchemaComparator = get_pk_comparator(['schema'])
SourceComparator = get_pk_comparator(['source'])
TitleComparator = get_pk_comparator(['title'])
URLComparator = get_pk_comparator(['url'])
ValueComparator = get_pk_comparator(['value'])


SingleReferenceComparator = get_pk_comparator([
    ['arxiv_eprint'],
    ['dois'],
    ['isbn'],
    ['book_series.title'],
    ['pubblication_info']
])

COMPARATORS = {
    '_desy_bookkeeping': DateComparator,
    '_fft': CreationDatetimeComparator,
    '_files': FilesComparator,
    '_private_notes': SourceComparator,
    'abstracts': SourceComparator,
    'acquisition_source': SourceComparator,
    'arxiv_eprints': ValueComparator,
    'authors': AuthorComparator,
    'authors.affiliations': AffiliationComparator,
    'authors.ids': SchemaComparator,
    'authors.raw_affiliations': SourceComparator,
    'book_series': TitleComparator,
    'collaborations': RecordComparator,
    'copyright': MaterialComparator,
    'deleted_records': RefComparator,
    'dois': ValueComparator,
    'external_system_identifiers': SchemaComparator,
    'funding_info': FundingInfoComparator,
    'imprints': ImprintsComparator,
    'isbns': ValueComparator,
    'keywords': ValueComparator,
    'license': LicenseComparator,
    'new_record': RefComparator,
    'persistent_identifiers': ValueComparator,
    'public_notes': SourceComparator,
    'references': RecordComparator,
    'references.reference.authors': AuthorComparator,
    'report_numbers': SourceComparator,
    'title_translations': LanguageComparator,
    'titles': LanguageComparator
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
    'authors': UnifierOps.KEEP_UPDATE_ENTITIES_CONFLICT_ON_HEAD_DELETE,
    'authors.affiliations': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    'authors.alternative_names': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST,
    'authors.credit_roles': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST,
    'authors.emails': UnifierOps.KEEP_UPDATE_ENTITIES_CONFLICT_ON_HEAD_DELETE,
    'authors.full_name': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    'authors.ids': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    'authors.inspire_roles': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    'authors.raw_affiliations': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
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
    'inspire_categories': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_UPDATE_FIRST,
    'isbns': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_UPDATE_FIRST,
    'keywords': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_UPDATE_FIRST,
    'languages': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'license': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_UPDATE_FIRST,
    'persistent_identifiers': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    'public_notes': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'publication_info': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST,
    'publication_type': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'references': UnifierOps.KEEP_UPDATE_ENTITIES_CONFLICT_ON_HEAD_DELETE,
    'references.raw_refs': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'references.reference.authors': UnifierOps.KEEP_UPDATE_ENTITIES_CONFLICT_ON_HEAD_DELETE,
    'references.reference.book_series': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST,
    'references.reference.collaboration': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'references.reference.dois': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'references.reference.misc': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'references.reference.persistent_identifiers': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'references.reference.urls': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'report_numbers': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'special_collections': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    'texkeys': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    'thesis_info.institutions': UnifierOps.KEEP_ONLY_UPDATE_ENTITIES,
    'title_translations': UnifierOps.KEEP_ONLY_HEAD_ENTITIES,
    'titles': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST,
    'urls': UnifierOps.KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST
}

FIELD_MERGE_OPS = {
    '$schema': DictMergerOps.FALLBACK_KEEP_HEAD,
    '_desy_bookkeeping': DictMergerOps.FALLBACK_KEEP_HEAD,
    '_export_to': DictMergerOps.FALLBACK_KEEP_HEAD,
    '_fft': DictMergerOps.FALLBACK_KEEP_HEAD,
    '_private_notes': DictMergerOps.FALLBACK_KEEP_HEAD,
    'accelerator_experiments': DictMergerOps.FALLBACK_KEEP_HEAD,
    'acquisition_source': DictMergerOps.FALLBACK_KEEP_HEAD,
    'authors': DictMergerOps.FALLBACK_KEEP_HEAD,
    'authors.affiliations': DictMergerOps.FALLBACK_KEEP_HEAD,
    'authors.curated_relation': DictMergerOps.FALLBACK_KEEP_HEAD,
    'authors.full_name': DictMergerOps.FALLBACK_KEEP_HEAD,
    'authors.ids': DictMergerOps.FALLBACK_KEEP_HEAD,
    'authors.inspire_roles': DictMergerOps.FALLBACK_KEEP_HEAD,
    'authors.record': DictMergerOps.FALLBACK_KEEP_HEAD,
    'authors.raw_affiliations': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'authors.signature_block': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'authors.uuid': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'book_series': DictMergerOps.FALLBACK_KEEP_HEAD,
    'control_number': DictMergerOps.FALLBACK_KEEP_HEAD,
    'deleted': DictMergerOps.FALLBACK_KEEP_HEAD,
    'deleted_records': DictMergerOps.FALLBACK_KEEP_HEAD,
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
    'references': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'references.reference': DictMergerOps.FALLBACK_KEEP_HEAD,
    'references.reference.arxiv_eprint': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'references.reference.authors': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'references.reference.book_series': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'references.reference.document_type': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'references.reference.dois': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'references.reference.imprint': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'references.reference.isbn': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'references.reference.label': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'references.reference.persistent_identifiers': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'references.reference.report_number': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'references.reference.texkey': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'references.reference.title': DictMergerOps.FALLBACK_KEEP_UPDATE,
    'references.reference.urls': DictMergerOps.FALLBACK_KEEP_UPDATE
}
