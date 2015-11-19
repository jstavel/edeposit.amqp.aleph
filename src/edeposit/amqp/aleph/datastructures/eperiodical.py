#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
# Imports =====================================================================
from collections import namedtuple

from marcxml_parser import MARCXMLRecord

from .author import Author
from .format_enum import FormatEnum

from ..aleph import DocumentNotFoundException


# Structures ==================================================================
class EPeriodical(namedtuple("EPeriodical", ["url",
                                             'ISSN',
                                             'nazev',
                                             'format',
                                             'anotace',
                                             'podnazev',
                                             "id_number",
                                             'mistoVydani',
                                             'internal_url',
                                             'nakladatelVydavatel'])):
    """
    This structure is returned as result of users :class:`.SearchRequest`.

    In case of :class:`Search <.SearchRequest>`/:class:`Count <.CountRequest>`
    requests, this structure is filled with data from MARC XML record.

    Attributes:
        url (str): Url specified by publisher (THIS IS NOT INTERNAL URL!).
        ISSN (list): List of ISSNs for the periodical.
        nazev (str): Name of the periodical.
        format (str): Format of the periodical - see :class:`FormatEnum`.
        anotace (str): Anotation. Max lenght: 500 chars.
        podnazev (str): Subname of the book.
        id_number  (str): Identification number in aleph.
        mistoVydani (str): City/country origin of the publication.
        internal_url (str): Link to edeposit/kramerius system.
        nakladatelVydavatel (str): Publisher's name.
    """

    @staticmethod
    def from_xml(xml):
        """
        Convert :class:`.MARCXMLRecord` object to :class:`.EPublication`
        namedtuple.

        Args:
            xml (str/MARCXMLRecord): MARC XML which will be converted to
                EPublication. In case of str, ``<record>`` tag is required.

        Returns:
            structure: :class:`.EPublication` namedtuple with data about \
                       publication.
        """
        parsed = xml
        if not isinstance(xml, MARCXMLRecord):
            parsed = MARCXMLRecord(str(xml))

        # check whether the document was deleted
        if "DEL" in parsed.datafields:
            raise DocumentNotFoundException("Document was deleted.")

        # i know, that this is not PEP8, but you dont want to see it without
        # proper formating (it looks bad, really bad)
        return EPeriodical(
            url                 = parsed.get_urls(),
            ISSN                = parsed.get_ISSNs(),
            nazev               = parsed.get_name(),
            format              = parsed.get_format(),
            anotace             = None, # TODO: read the annotation
            podnazev            = parsed.get_subname(),
            id_number           = parsed.controlfields.get("001", None),
            mistoVydani         = parsed.get_pub_place(),
            internal_url        = parsed.get_internal_urls(),
            nakladatelVydavatel = parsed.get_publisher(),
        )
