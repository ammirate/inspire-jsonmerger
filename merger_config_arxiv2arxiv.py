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

from json_merger.comparator import PrimaryKeyComparator
from json_merger.contrib.inspirehep.author_util import (
    AuthorNameDistanceCalculator, AuthorNameNormalizer, NameToken, NameInitial)
from json_merger.contrib.inspirehep.comparators import (
        DistanceFunctionComparator)

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


SourceComparator = get_pk_comparator(['source'])
AffiliationComparator = get_pk_comparator(['value'])
CollectionsComparator = get_pk_comparator(['primary'])
ExtSysNumberComparator = get_pk_comparator(['institute'])
URLComparator = get_pk_comparator(['url'])
PubInfoComparator = get_pk_comparator([
    ['journal_title', 'journal_volume', 'page_start'],
    ['journal_title', 'journal_volume', 'artid']])


COMPARATORS = {
    '_desy_bookkeeping': 'has to be defined/implmented',
    '_export_to': 'has to be defined/implmented',
    '_fft': 'has to be defined/implmented',
    '_files': 'has to be defined/implmented',
    '_private_notes': 'has to be defined/implmented',
    'abstracts': 'has to be defined/implmented',
    'accelerator_experiments': 'has to be defined/implmented',
    'acquisition_source': 'has to be defined/implmented',
    'arxiv_eprints': 'has to be defined/implmented',
    'authors': AuthorComparator,
    'authors.affiliations': AffiliationComparator,
    'authors.alternative_names': 'has to be defined/implmented',
    'authors.credit_roles': 'has to be defined/implmented',
    'authors.curated_relation': 'has to be defined/implmented',
    'authors.emails': 'has to be defined/implmented',
    'authors.full_name': 'has to be defined/implmented',
    'authors.ids': 'has to be defined/implmented',
    'authors.inspire_roles': 'has to be defined/implmented',
    'authors.raw_affiliations': 'has to be defined/implmented',
    'authors.record': 'has to be defined/implmented',
    'authors.signature_block': 'has to be defined/implmented',
    'authors.uuid': 'has to be defined/implmented',
    'book_series': 'has to be defined/implmented',
    'citeable': 'has to be defined/implmented',
    'collaborations': 'has to be defined/implmented',
    'control_number': 'has to be defined/implmented',
    'copyright': 'has to be defined/implmented',
    'core': 'has to be defined/implmented',
    'corporate_author': 'has to be defined/implmented',
    'deleted': 'has to be defined/implmented',
    'deleted_records': 'has to be defined/implmented',
    'document_type': 'has to be defined/implmented',
    'dois': 'has to be defined/implmented',
    'editions': 'has to be defined/implmented',
    'energy_ranges': 'has to be defined/implmented',
    'external_system_identifiers': 'has to be defined/implmented',
    'funding_info': 'has to be defined/implmented',
    'imprints': 'has to be defined/implmented',
    'inspire_categories': 'has to be defined/implmented',
    'isbns': 'has to be defined/implmented',
    'keywords': 'has to be defined/implmented',
    'languages': 'has to be defined/implmented',
    'legacy_creation_date': 'has to be defined/implmented',
    'license': 'has to be defined/implmented',
    'new_record': 'has to be defined/implmented',
    'number_of_pages': 'has to be defined/implmented',
    'persistent_identifiers': 'has to be defined/implmented',
    'preprint_date': 'has to be defined/implmented',
    'public_notes': 'has to be defined/implmented',
    'publication_info': PubInfoComparator,
    'publication_type': 'has to be defined/implmented',
    'refereed': 'has to be defined/implmented',
    'references': 'has to be defined/implmented',
    'report_numbers': 'has to be defined/implmented',
    'self': 'has to be defined/implmented',
    'special_collections': 'has to be defined/implmented',
    'succeeding_entry': 'has to be defined/implmented',
    'texkeys': 'has to be defined/implmented',
    'thesis_info': 'has to be defined/implmented',
    'title_translations': 'has to be defined/implmented',
    'titles': 'has to be defined/implmented',
    'urls': 'has to be defined/implmented',
    'wirthdrawn': 'has to be defined/implmented'
}

# We an always default to KEEP_UPDATE_AND_HEAD_ENTITIES_HEAD_FIRST so
# this is less verbose.
LIST_MERGE_OPS = {
    '_collections': 'has to be defined',
    '_desy_bookkeeping': 'has to be defined',
    '_export_to': 'has to be defined',
    '_fft': 'has to be defined',
    '_files': 'has to be defined',
    '_private_notes': 'has to be defined',
    'abstracts': 'has to be defined',
    'accelerator_experiments': 'has to be defined',
    'acquisition_source': 'has to be defined',
    'arxiv_eprints': 'has to be defined',
    'authors': 'has to be defined',
    'authors.affiliations': 'has to be defined',
    'authors.alternative_names': 'has to be defined',
    'authors.credit_roles': 'has to be defined',
    'authors.curated_relation': 'has to be defined',
    'authors.emails': 'has to be defined',
    'authors.full_name': 'has to be defined',
    'authors.ids': 'has to be defined',
    'authors.inspire_roles': 'has to be defined',
    'authors.raw_affiliations': 'has to be defined',
    'authors.record': 'has to be defined',
    'authors.signature_block': 'has to be defined',
    'authors.uuid': 'has to be defined',
    'book_series': 'has to be defined',
    'citeable': 'has to be defined',
    'collaborations': 'has to be defined',
    'control_number': 'has to be defined',
    'copyright': 'has to be defined',
    'core': 'has to be defined',
    'corporate_author': 'has to be defined',
    'deleted': 'has to be defined',
    'deleted_records': 'has to be defined',
    'document_type': 'has to be defined',
    'dois': 'has to be defined',
    'editions': 'has to be defined',
    'energy_ranges': 'has to be defined',
    'external_system_identifiers': 'has to be defined',
    'funding_info': 'has to be defined',
    'imprints': 'has to be defined',
    'inspire_categories': 'has to be defined',
    'isbns': 'has to be defined',
    'keywords': 'has to be defined',
    'languages': 'has to be defined',
    'legacy_creation_date': 'has to be defined',
    'license': 'has to be defined',
    'new_record': 'has to be defined',
    'number_of_pages': 'has to be defined',
    'persistent_identifiers': 'has to be defined',
    'preprint_date': 'has to be defined',
    'public_notes': 'has to be defined',
    'publication_info': 'has to be defined',
    'publication_type': 'has to be defined',
    'refereed': 'has to be defined',
    'references': 'has to be defined',
    'report_numbers': 'has to be defined',
    'self': 'has to be defined',
    'special_collections': 'has to be defined',
    'succeeding_entry': 'has to be defined',
    'texkeys': 'has to be defined',
    'thesis_info': 'has to be defined',
    'title_translations': 'has to be defined',
    'titles': 'has to be defined',
    'urls': 'has to be defined',
    'wirthdrawn': 'has to be defined'
}
