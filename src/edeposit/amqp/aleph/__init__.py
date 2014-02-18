#! /usr/bin/env python
# -*- coding: utf-8 -*-
# This package may contain traces of nuts
from collections import namedtuple


import aleph
import convertors


# from .. import AMQPMessage
class AMQPMessage(namedtuple('AMQPMessage',  # TODO: Remove
                             ['data',
                              'headers',
                              'properties'
                              ])):
    """
    data ... serialized main message
    headers
    """
    pass


###############################################################################
# Search Aleph ################################################################
###############################################################################
"""
Workflow is pretty simple:

To query Aleph, just create one of the Queries - ISBNQuery for example and put
it into SearchRequest wrapper with UUID. Then encode it by calling
toAMQPMessage() and send the message to the Aleph exchange.

---
isbnq = ISBNQuery("80-251-0225-4")
request = SearchRequest(isbnq, UUID)

amqp.send(
    toAMQPMessage(request)
    "ALEPH'S_EXCHANGE"
)
---

and you will get back AMQP message, and after decoding with fromAMQPMessage()
also SearchResult.

If you want to just get count of how many items is there in Aleph (you should
use this instead of just calling len() to SearchResult.records - it doesn't put
that much load to Aleph), just wrap the ISBNQuery with CountQuery:

---
isbnq = CountQuery(ISBNQuery("80-251-0225-4"))
# rest is same..
---

and you will get back (after decoding) CountResult.
"""

class AlephRecord(namedtuple("AlephRecord",
                             ['library',
                              'docNumber',
                              'xml',
                              'epublication'])):
    pass


class SearchResult(namedtuple("SearchResult",
                              ['records',
                               'UUID'])):
    pass
    """ result of search request """


class CountResult(namedtuple("CountResult",
                             ['num_of_records',
                              'UUID'])):
    pass


class _QueryTemplate:
    """
    This class is here to just save some effort by using common ancestor with
    same .getSearchResult() and .getCountResult() definition.
    """
    def getSearchResult(self, UUID):
        records = []
        for doc_id, library in self._getIDs():
            xml = aleph.downloadAlephDocument(doc_id, library)

            records.append(
                AlephRecord(
                    library,
                    doc_id,
                    xml,
                    convertors.toEPublication(xml)
                )
            )

        return SearchResult(records, UUID)

    def getCountResult(self, UUID):
        return CountResult(
            self._getCount(),
            UUID
        )


class GenericQuery(namedtuple("GenericQuery",
                              ['base',
                               'phrase',
                               'considerSimilar',
                               'field']), _QueryTemplate):
    """
    Used for generic queries to aleph.

    For details of parameters, see aleph.py : searchInAleph().
    """
    def _getIDs(self):
        return aleph.getDocumentIDs(
            aleph.searchInAleph(
                self.base,
                self.phrase,
                self.considerSimilar,
                self.field
            )
        )

    def _getCount(self):
        return aleph.searchInAleph(
            self.base,
            self.phrase,
            self.considerSimilar,
            self.field
        )["no_entries"]


class ISBNQuery(namedtuple("ISBNQuery", ["ISBN"]), _QueryTemplate):
    def _getIDs(self):
        return aleph.getISBNsIDs(self.ISBN)

    def _getCount(self):
        return aleph.getISBNCount(self.ISBN)


class AuthorQuery(namedtuple("AuthorQuery", ["author"]), _QueryTemplate):
    def _getIDs(self):
        return aleph.getAuthorsBooksIDs(self.author)

    def _getCount(self):
        return aleph.getAuthorsBooksCount(self.author)


class PublisherQuery(namedtuple("PublisherQuery", ["publisher"]), _QueryTemplate):
    def _getIDs(self):
        return aleph.getPublishersBooksIDs(self.publisher)

    def _getCount(self):
        return aleph.getPublishersBooksCount(self.publisher)


class CountQuery(namedtuple("CountQuery", ["query_type"])):
    """
    Put one of the Queries to .query_type property and it will return just
    number of records, instead of records itself.
    """
    pass


class SearchRequest(namedtuple("SearchRequest",
                               ['query',
                                'UUID'])):
    """
    query -- GenericQuery, ISBNQuery, .. *Query
    UUID -- identification of a query in a result response
    """


###############################################################################
# Add new record to Aleph #####################################################
###############################################################################
#
## Aleph's data wrappers ######################################################
class Author(namedtuple("Author", ['firstName', 'lastName', 'title'])):
    pass


class Producent(namedtuple("Producent",
                           ['title',
                            'phone',
                            'fax',
                            'email',
                            'url',
                            'identificator',
                            'ico'])):
    pass


class EPublication(namedtuple("EPublication",
                              ['nazev',
                               'podnazev',
                               'vazba',
                               'cena',
                               'castDil',
                               'nazevCasti',
                               'nakladatelVydavatel',
                               'datumVydani',
                               'poradiVydani',
                               'zpracovatelZaznamu',
                               'kategorieProRIV',
                               'mistoDistribuce',
                               'distributor',
                               'datumDistribuce',
                               'datumProCopyright',
                               'format',
                               'url',
                               'mistoVydani',
                               'ISBNSouboruPublikaci',
                               'autori',
                               'originaly'])):
    """
    see https://e-deposit.readthedocs.org/cs/latest/dm01.html
    """
    pass


class OriginalFile(namedtuple("OriginalFile",
                              ['url', 'format', 'file', 'isbns'])):
    """ type of isbn: ISBN"""
    pass


## Protocol query wrappers ####################################################
class AlephExport(namedtuple("AlephExport",
                             ['epublication',
                              'linkOfEPublication'])):
    """ epublication ... type of EPublication
    linkOfEPublication  ... url with epublication

    User will fill this record.
    """
    pass


class ExportRequest(namedtuple("ExportRequest",
                               ['export',
                                'UUID'])):
    pass


class AlephExportResult(namedtuple("AlephExportResult",
                                   ['docNumber',
                                    'base',
                                    'xml',
                                    'success',
                                    'message'])):
    """ docNumber ... docNumber of a record in Aleph
    base      ... base of Aleph
    success   ... whether import was successfull
    message   ... message of error or success
    """
    pass


class ExportResult(namedtuple("ExportResult",
                              ['result',
                               'UUID'])):
    """
    ... result is type of AlephExportResult
    ... UUID is UUID used in ExportRequest
    """
    pass


###############################################################################
#  Interface for an external world  ###########################################
###############################################################################

# Variables ###################################################################
QUERY_TYPES = [
    ISBNQuery,
    AuthorQuery,
    PublisherQuery,
    GenericQuery
]


# Functions ###################################################################
def toAMQPMessage(request):
    """
    Serialize nested structure of objects defined in this module into
    AMQPMessage.

    request -- tree consisting of namedtuples and other python datatypes

    Return AMQPMessage with filled .body property with serialized data.
    """

    return AMQPMessage(
        data=convertors.toJSON(request),
        headers="",
        properties=""
    )


def fromAMQPMessage(message):
    """
    Deserialize structures defined in this module from AMQPMessage.

    message -- AMQPMessage, in which .body property is expected to be
               serialized data.

    Returns nested structure of Requests/Results (see other objects defined
    here).
    """
    return convertors.fromJSON(message.body)


def reactToAMQPMessage(message, response_callback):
    """
    React to given AMQPMessage. Return data thru given callback function.

    message -- AMQPMessage instance.
    response_callback -- function taking exactly ONE parameter - AMQPMessage
                         with response. Function take care of sending the
                         response thru AMQP.

    Returns result of response_callback() call.

    Raise:
        ValueError if bad type of |message| structure is given.

    TODO:
        React to Export requests.
    """
    decoded = fromAMQPMessage(message)

    if type(decoded) != SearchRequest:  # TODO: pridat podporu exportnich typu
        raise ValueError("Unknown type of message: '" + type(decoded) + "'!")

    query = decoded.query

    response = None
    if type(query) == CountQuery and query.query_type in QUERY_TYPES:
        response = query.query_type.getCountResult(decoded.UUID)
    elif type(query) in QUERY_TYPES:  # react to search requests
        response = query.getSearchResult(decoded.UUID)
    else:
        raise ValueError("Unknown type of query: '" + type(query) + "'!")

    if response is not None:
        return response_callback(toAMQPMessage(response))
