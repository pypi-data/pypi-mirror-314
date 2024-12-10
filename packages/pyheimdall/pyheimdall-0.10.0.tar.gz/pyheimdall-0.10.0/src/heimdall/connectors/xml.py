# -*- coding: utf-8 -*-
from lxml import etree as _etree
from urllib.parse import urlparse
from urllib.request import urlopen
from ..decorators import get_database, create_database

"""
Provides connectors to HERA-formatted XML files.

This module defines input and output connectors to databases composed in full or in part of XML files following the HERA schema.

* :py:class:`heimdall.connectors.xml.getDatabase` is the input connector
* :py:class:`heimdall.connectors.xml.serialize` is the output connector

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""  # nopep8: E501


@get_database('hera:xml')
def getDatabase(**options):
    r"""Imports a database from a HERA XML file

    :param \**options: Keyword arguments, see below.
    :Keyword arguments:
        * **url** (:py:class:`str`) -- Local ou remote path of the XML file to import
        * **format** (:py:class:`str`, optional) Always ``hera:xml``
        * **encoding** (:py:class:`str`, optional, default: ``utf-8``) -- ``url`` file encoding
    :return: HERA element tree
    :rtype: :py:class:`lxml.etree._ElementTree`

    Usage example: ::

      >>> import heimdall
      >>> tree = heimdall.getDatabase(format='hera:xml', url='some/input.xml')
      >>> # ... do stuff ...

    .. CAUTION::
       For future compability, this function shouldn't be directly called; as shown in the usage example above, it should only be used through :py:class:`heimdall.getDatabase`.
    """  # nopep8: E501
    url = options['url']
    encoding = options.get('encoding', 'utf-8')
    if not is_url(url):
        tree = _etree.parse(url)
        # can raise OSError (file not found, ...)
    else:
        with urlopen(url) as response:
            tree = _etree.fromstring(response.read().decode(encoding))
            # can raise urllib.error.HTTPError (HTTP Error 404: Not Found, ...)
    return tree


def is_url(path):
    schemes = ('http', 'https', 'file', )
    return urlparse(path).scheme in schemes


def createDatabase():
    r"""Creates an empty HERA database

    :return: HERA element tree
    :rtype: :py:class:`lxml.etree._ElementTree`

    Usage example: ::
      >>> import heimdall
      >>> tree = heimdall.createDatabase()
      >>> # ... do stuff ...
    """
    xml_schema = 'http://www.w3.org/2001/XMLSchema-instance'
    hera_xsd = 'https://gitlab.huma-num.fr/datasphere/hera/schema/schema.xsd'
    qname = _etree.QName(xml_schema, 'schemaLocation')
    root = _etree.Element('hera', {qname: hera_xsd})
    properties = _etree.SubElement(root, 'properties')
    entities = _etree.SubElement(root, 'entities')
    items = _etree.SubElement(root, 'items')
    return root


@create_database('hera:xml')
def serialize(tree, url, pretty=True, **options):
    r"""Serializes a HERA elements tree into an XML file

    :param tree: (:py:class:`lxml.etree._ElementTree`) HERA elements tree
    :param url: (:py:class:`str`) Path of the XML file to create
    :param format: (:py:class:`str`) Always ``hera:xml``
    :return: None
    :rtype: :py:class:`NoneType`

    Usage example: ::
      >>> import heimdall
      >>> tree = heimdall.getDatabase(format='hera:xml', url='some/input.xml')
      >>> # ... do stuff ...
      >>> heimdall.serialize(tree, format='hera:xml', url='some/output.xml')
    """
    with open(url, 'w') as f:
        f.write(_etree.tostring(tree, encoding=str, pretty_print=True))


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
__all__ = [
    'getDatabase',
    'createDatabase',
    'serialize',

    '__copyright__', '__license__',
    ]
