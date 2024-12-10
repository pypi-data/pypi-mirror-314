# -*- coding: utf-8 -*-
import heimdall
from heimdall.util import get_node, get_nodes, get_language
from ..decorators import get_database, create_database
from json import load, loads, dump
from urllib.parse import urlparse
from urllib.request import urlopen
from lxml import etree

"""
Provides connectors to HERA-formatted JSON files.

This module defines input and output connectors to databases composed in full or in part of JSON files following the HERA schema.

* :py:class:`heimdall.connectors.json.getDatabase` is the input connector
* :py:class:`heimdall.connectors.json.serialize` is the output connector

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""  # nopep8: E501


@get_database('hera:json')
def getDatabase(**options):
    r"""Imports a database from a HERA JSON file

    :param \**options: Keyword arguments, see below.
    :Keyword arguments:
        * **url** (:py:class:`str`) -- Local ou remote path of the JSON file to import
        * **format** (:py:class:`str`, optional) Always ``hera:json``
        * **encoding** (:py:class:`str`, optional, default: ``utf-8``) -- ``url`` file encoding
    :return: HERA element tree
    :rtype: :py:class:`lxml.etree._ElementTree`

    Usage example: ::

      >>> import heimdall
      >>> tree = heimdall.getDatabase(format='hera:json', url='some/input.json')
      >>> # ... do stuff ...

    .. CAUTION::
       For future compability, this function shouldn't be directly called; as shown in the usage example above, it should only be used through :py:class:`heimdall.getDatabase`.
    """  # nopep8: E501
    url = options['url']
    encoding = options.get('encoding', 'utf-8')
    if not is_url(url):
        with open(url, 'r') as f:
            data = load(f)
    else:
        with urlopen(url) as response:
            data = loads(response.read().decode(encoding))
    return _create_tree(data)


def is_url(path):
    schemes = ('http', 'https', )
    return urlparse(path).scheme in schemes


def _create_tree(data):
    root = heimdall.createDatabase()

    # create Properties if any
    properties = data.get('properties', None)
    if properties is not None:
        elements = root.xpath('//properties')[0]
        for o in properties:
            uid = o['id']  # id is mandatory
            e = etree.SubElement(elements, 'property', id=uid)
            _add_xml_element_from_json(e, o, 'type')
            _add_xml_element_from_json(e, o, 'name')
            _add_xml_element_from_json(e, o, 'description')
            _add_xml_element_from_json(e, o, 'uri')
            # _add_xml_element_from_json(e, o, 'uris')  # TODO property.uris

    # create Entities if any
    entities = data.get('entities', None)
    if entities is not None:
        elements = root.xpath('//entities')[0]
        for o in entities:
            uid = o['id']  # id is mandatory
            e = etree.SubElement(elements, 'entity', id=uid)
            _add_xml_element_from_json(e, o, 'name')
            _add_xml_element_from_json(e, o, 'description')
            _add_xml_element_from_json(e, o, 'uri')
            attributes = o.get('attributes', list())
            for c in attributes:
                pid = c['pid']  # pid is mandatory
                a = etree.SubElement(e, 'attribute', pid=pid)
                aid = c.get('id', None)
                if aid is not None:
                    a.attrib['id'] = aid
                min = c.get('min', 0)
                a.attrib['min'] = min
                max = c.get('max', None)
                if max is not None:
                    a.attrib['max'] = max
                _add_xml_element_from_json(a, c, 'type')
                _add_xml_element_from_json(a, c, 'name')
                _add_xml_element_from_json(a, c, 'description')
                _add_xml_element_from_json(a, c, 'uri')

    # create Items if any
    items = data.get('items', None)
    if items is not None:
        elements = root.xpath('//items')[0]
        for o in items:
            e = etree.SubElement(elements, 'item')
            _add_attribute_from_json(e, o, 'eid')
            metadata = o.get('metadata', [])
            for m in metadata:
                pid = m['pid']  # pid is mandatory
                meta = etree.SubElement(e, 'metadata', pid=pid)
                meta.text = m['value']  # value is mandatory, too

    return etree.ElementTree(root)


def _add_xml_element_from_json(e, o, attr):
    value = o.get(attr, None)
    if value is not None:
        sub = etree.SubElement(e, attr)
        sub.text = value


def _add_attribute_from_json(e, o, attr):
    value = o.get(attr, None)
    if value is not None:
        e.set(attr, value)


@create_database('hera:json')
def serialize(tree, url, **options):
    r"""Serializes a HERA elements tree into a JSON file

    :param tree: HERA elements tree
    :param url: Path of the JSON file to create

    .. ERROR::
       This feature is not implemented yet.
       This can be either due to lack of resources, lack of demand, because it
       wouldn't be easily maintenable, or any combination of these factors.

       Interested readers can submit a request to further this topic.
       See the ``CONTRIBUTING`` file at the root of the repository for details.
    """
    data = _tree2object(tree)
    # write data to file
    indent = options.get('indent', 2)
    protek = options.get('ensure_ascii', False)
    with open(url, 'w', encoding='utf-8') as f:
        dump(data, f, indent=indent, ensure_ascii=protek)


def _tree2object(tree):
    data = dict()
    # convert properties to json-ready objects, add them to data
    elements = heimdall.getProperties(tree)
    if len(elements) > 0:
        data['properties'] = list()
    for element in elements:
        data['properties'].append(_property2object(element))
    # convert entities to json-ready objects, add them to data
    elements = heimdall.getEntities(tree)
    if len(elements) > 0:
        data['entities'] = list()
    for element in elements:
        data['entities'].append(_entity2object(element))
    # convert items to json-ready objects, add them to data
    elements = heimdall.getItems(tree)
    if len(elements) > 0:
        data['items'] = list()
    for element in elements:
        data['items'].append(_item2object(element))

    return data


def _property2object(p):
    return _xml2object(p)


def _entity2object(e):
    data = _xml2object(e)
    elements = heimdall.getAttributes(e)
    if len(elements) > 0:
        data['attributes'] = list()
    for element in elements:
        data['attributes'].append(_attribute2object(element))
    return data


def _attribute2object(a):
    data = _xml2object(a)
    data['pid'] = a.get('pid')
    data['min'] = a.get('min', 0)
    _param2text(a, data, 'max', None)
    return data


def _xml2object(x):
    data = dict()
    value = x.get('id', None)
    if value is not None:
        data['id'] = value
    # child --> unique value
    for tag in ['type', ]:
        array_of_one = [c.text for c in x.getchildren() if c.tag == tag]
        assert len(array_of_one) < 2
        if len(array_of_one) > 0 and array_of_one[0] is not None:
            data[tag] = array_of_one[0]
    # child --> localized object
    for tag in ['name', 'description', ]:
        obj = _nodes2object(get_nodes(x, tag))
        if obj is not None:
            data[tag] = obj
    # child --> repeatable value
    for tag in ['uri', ]:
        array = _nodes2array(get_nodes(x, tag))
        if len(array) > 0:
            data[tag] = array
    return data


def _item2object(i):
    data = dict()
    for key in ['eid', ]:
        _param2text(i, data, key)
    elements = heimdall.getMetadata(i)
    if len(elements) > 0:
        data['metadata'] = list()
    for element in elements:
        data['metadata'].append(_metadata2object(element))
    return data


def _metadata2object(m):
    data = dict()
    for key in ['pid', 'aid', ]:
        _param2text(m, data, key)
    value = get_language(m)
    if value is not None:
        data['language'] = value
    value = _node2text(m)
    if value is not None:
        data['value'] = value
    return data


def _param2text(x, data, key, default=None):
    value = x.get(key, default)
    if value is not None:
        data[key] = value


def _node2text(node):
    return node.text


def _nodes2object(nodes):
    data = dict()
    for node in nodes:
        language = get_language(node)
        if language is not None:
            data[language] = node.text
        else:
            # emergency exit:
            # if there is even only 1 node with no language,
            # we'll return this one only
            return node.text
    if len(data) < 1:
        return None
    return data


def _nodes2array(nodes):
    data = list()
    for node in nodes:
        if node.text is not None:
            data.append(node.text)
    return data
