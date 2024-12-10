# -*- coding: utf-8 -*-
import requests
import heimdall
from heimdall.decorators import get_database, create_database


@get_database('api:wikidata')
def getDatabase(url, **options):
    r"""Imports a database from Wikidata

    :param url: Wikidata API URL
    :return: HERA element tree
    :rtype: :py:class:`lxml.etree._ElementTree`

    ``url`` should start with `https://www.wikidata.org/w/api.php`

    See https://www.wikidata.org/wiki/Help:Wikidata_datamodel for details.
    """
    headers = {'accept': 'application/json', }
    payload = {'page': 1, 'limit': 25, }
    response = _request(url, headers, payload)
    tree = heimdall.createDatabase()
    for id_, data in response.get('entities', {}).items():
        names = dict()
        for v in data['labels'].values():
            names[v['language']] = v['value']
        descriptions = dict()
        for v in data['descriptions'].values():
            descriptions[v['language']] = v['value']
        item = heimdall.createItem(
                tree,
                eid=data['type'],
                id=data['id'],
                title=names,
                description=descriptions,
                )
        # add aliases as title metadata
        for aliases in data['aliases'].values():
            for v in aliases:
                values = {v['language']: v['value'], }
                heimdall.createMetadata(item, values, pid='title')
        for claim in data['claims'].values():
            for statement in claim:
                eid = statement['type']  # should always be 'statement'
                snak = statement['mainsnak']
                P = snak['property']
                value = snak['datavalue']['value']
                print(f"{P}: {value} -- {str(type(value))}")
                createMetadata = DATATYPES[snak['datatype']]
                createMetadata(item, P, value)
    return tree


def _request(url, headers, payload):
    response = requests.get(url, headers=headers, params=payload)
    if response.status_code != requests.codes.ok:
        response.raise_for_status()
    # NOTE: maybe check for response.headers, too?
    return response.json()


def _string2metadata(item, P, value):
    return heimdall.createMetadata(item, value, pid=P)


def _item2metadata(item, P, data):
    value = data['id']
    return heimdall.createMetadata(item, value, pid=P)


def _time2metadata(item, P, data):
    value = data['time']
    return heimdall.createMetadata(item, value, pid=P)
    # TODO: this may NOT be enough to return `data['time']`, because there is
    # a lot more info in `data` to qualify the exact time; for example:
    #   'time': '+2011-00-00T00:00:00Z',
    #   'timezone': 0,
    #   'before': 0, 'after': 0,
    #   'precision': 9,
    #   'calendarmodel': 'http://www.wikidata.org/entity/Q1985727'


def _quantity2metadata(item, P, data):
    value = data['amount']
    return heimdall.createMetadata(item, value, pid=P)
    # TODO: this may NOT be enough to return `data['amount']`, because there is
    # a lot more info in `data` to qualify the exact quantity; for example:
    #   'amount': '+2535861',
    #   'unit': '1'
    # (there could be lowerBound and upperBound, too)
    # @see: https://www.wikidata.org/wiki/Help:Wikidata_datamodel


def _text2metadata(item, P, data):
    values = dict()
    values[data['language']] = data['text']
    return heimdall.createMetadata(item, values, pid=P)


DATATYPES = {
    'string': _string2metadata,
    'url': _string2metadata,
    'time': _time2metadata,
    'quantity': _quantity2metadata,
    'monolingualtext': _text2metadata,
    'commonsMedia': _string2metadata,
    'external-id': _string2metadata,
    'wikibase-item': _item2metadata,
    }
