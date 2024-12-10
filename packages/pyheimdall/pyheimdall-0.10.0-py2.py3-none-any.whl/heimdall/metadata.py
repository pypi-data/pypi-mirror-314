# -*- coding: utf-8 -*-

"""
Provides CRUD operations to search for or
edit metadata in a HERA item.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""

import heimdall
from .util import (
        get_node as _get_node,
        create_nodes as _create_nodes,
    )


def getMetadata(item, **options):
    r"""Retrieves metadata elements from an item.

    :param item: (:py:class:`lxml.etree._Element`) -- HERA item
    :param \**options: (:py:class:`dict`, optional) -- Keyword arguments, see description.
    :return: Metadata list
    :rtype: :py:class:`list` of :py:class:`lxml.etree._Element`

    Usage examples: ::

      >>> import heimdall
      >>> # ... do stuff ...
      >>> item = getItem(...)
      >>> # consider we just got the following item:
      >>> # <item eid='person'>
      >>> #   <metadata pid='dc:title' xml:lang='en'>William</metadata>
      >>> #   <metadata pid='dc:title' xml:lang='fr'>Guillaume</metadata>
      >>> #   <metadata pid='pet' xml:lang='en'>Chirpy</metadata>
      >>> #   <metadata pid='pet' xml:lang='en'>Claws</metadata>
      >>> #   <metadata pid='pet'>Blackie</metadata>
      >>> # </item>
      >>> # then we'll have the following results
      >>> metadata = heimdall.getMetadata(item, pid='dc:title')
      >>> # len(metadata) == 2  (metadata of values William, Guillaume)
      >>> metadata = heimdall.getMetadata(item, pid='pet')
      >>> # len(metadata) == 3  (metadata of values Chirpy, Claws, Blackie)
      >>> metadata = heimdall.getMetadata(item, pid='meats')
      >>> # len(metadata) == 0  (no metadata in item with this pid)

    This function can be used to retrieve metadata in a specific language,
    using the ``lang`` parameter: ::

      >>> import heimdall
      >>> # ... do stuff ...
      >>> item = getItem(...)
      >>> # consider we just got the following item:
      >>> # <item eid='person'>
      >>> #   <metadata pid='dc:title' xml:lang='en'>William</metadata>
      >>> #   <metadata pid='dc:title' xml:lang='fr'>Guillaume</metadata>
      >>> #   <metadata pid='pet' xml:lang='en'>Chirpy</metadata>
      >>> #   <metadata pid='pet' xml:lang='en'>Claws</metadata>
      >>> #   <metadata pid='pet'>Blackie</metadata>
      >>> # </item>
      >>> # then we'll have the following results
      >>> metadata = heimdall.getMetadata(item, lang='en')
      >>> # len(metadata) == 3  (metadata of values William, Chirpy, Claws)
      >>> metadata = heimdall.getMetadata(item, lang='fr')
      >>> # len(metadata) == 1  (metadata of value Guillaume)
      >>> metadata = heimdall.getMetadata(item, lang=None)
      >>> # len(metadata) == 1  (metadata of value Blackie is not localized)
      >>> metadata = heimdall.getMetadata(item, lang='ar')
      >>> # len(metadata) == 0  (no metadata localized in arabic in item)
      >>> metadata = heimdall.getMetadata(item, pid='pet', lang='ar')
      >>> # len(metadata) == 0  (no metadata 'pet' localized in arabic in item)
      >>> metadata = heimdall.getMetadata(item, pid='dc:title', lang='fr')
      >>> # len(metadata) == 3  (metadata of value Guillaume)
      >>> metadata = heimdall.getMetadata(item, pid='pet', lang='fr')
      >>> # len(metadata) == 0  (no metadata 'pet' is localized in french)
      >>> metadata = heimdall.getMetadata(item, pid='pet', lang='en')
      >>> # len(metadata) == 2  (metadata of values Chirpy, Claws)

    Parameter ``options`` can be anything you want to filter metadata with,
    even if you target something outside of the scope of the HERA specification: ::

      >>> import heimdall
      >>> # ... do stuff ...
      >>> item = getItem(...)
      >>> # consider we just got the following item:
      >>> # <item eid='person'>
      >>> #   <metadata pid='dc:title' xml:lang='en'>William</metadata>
      >>> #   <metadata pid='dc:title' xml:lang='fr' floofs='mild'>Guillaume</metadata>
      >>> #   <metadata pid='pet' xml:lang='en' floofs='high'>Chirpy</metadata>
      >>> #   <metadata pid='pet' xml:lang='en' floofs='mild'>Claws</metadata>
      >>> #   <metadata pid='pet' floofs='high'>Blackie</metadata>
      >>> # </item>
      >>> # then we'll have the following results
      >>> metadata = heimdall.getMetadata(item, floofs='high')
      >>> # len(metadata) == 2  (metadata of values Chirpy, Blackie)
      >>> metadata = heimdall.getMetadata(item, floofs='mild')
      >>> # len(metadata) == 2  (metadata of values Guillaume, Claws)
      >>> metadata = heimdall.getMetadata(item, floofs='high', lang='en')
      >>> # len(metadata) == 1  (metadata of value Chirpy)
      >>> metadata = heimdall.getMetadata(item, floofs=None)
      >>> # len(metadata) == 1  (metadata of values William, Guillaum, Blackie)

    If ``options`` are left undefined, ``getMetadata`` simply returns all metadata elements of an item.
    In the above examples, ``heimdall.getMetadata(item)`` would return a list of all (5) metadata elements of ``item``.

    To get results directly as :py:class:`str` values instead of as metadata elements, :py:class:`heimdall.getValues` can be used with a similar behavior.
    """  # nopep8: E501
    filters = dict()
    for key, wanted in options.items():
        if key == 'lang':
            filters[key] = (wanted, lambda m, _: heimdall.util.get_language(m))
        else:
            filters[key] = (wanted, lambda m, param: m.get(param))
    metadata = item.getchildren()
    for param, (wanted, _get) in filters.items():
        metadata = [m for m in metadata if _get(m, param) == wanted]
    return metadata


def getValues(item, **options):
    r"""Retrieves metadata values from an item.

    :param item: (:py:class:`lxml.etree._Element`) -- HERA item
    :param \**options: (:py:class:`dict`, optional) -- Keyword arguments, see description.
    :return: Metadata values list
    :rtype: :py:class:`list` of :py:class:`str`

    This function can be used to retrieve metadata values from an item ``item``.
    It behaves exactly like :py:class:`heimdall.getMetadata`, but returns directly metadata values as a :py:class:`list` of :py:class:`str`, instead of metadata as a :py:class:`list` of :py:class:`lxml.etree._Element`.

    Please note that if some of ``item``'s metadata value are empty, this function returns empty strings, not :py:class:`NoneType` elements: ::

      >>> import heimdall
      >>> # ... do stuff ...
      >>> item = getItem(...)
      >>> # consider we just got the following item:
      >>> # <item>
      >>> #   <metadata>Donald</metadata>
      >>> #   <metadata aid='nephew'>Huey</metadata>
      >>> #   <metadata aid='nephew'></metadata>
      >>> #   <metadata aid='nephew'>Louie</metadata>
      >>> # </item>
      >>> # then we'll have the following results
      >>> values = heimdall.getValues(item)
      >>> # values = ["Donald", "Huey", "", "Louie"]
      >>> values = heimdall.getValues(item, aid='nephew')
      >>> # values = ["Huey", "", "Louie"]
    """  # nopep8: E501
    metadata = heimdall.getMetadata(item, **options)
    values = list()
    for m in metadata:
        if m.text is not None:
            values.append(m.text)
        else:
            values.append('')
    return values


def getValue(item, **options):
    r"""Retrieves a single metadata value from an item.

    :param item: (:py:class:`lxml.etree._Element`) -- HERA item
    :param \**options: (:py:class:`dict`, optional) -- Keyword arguments, see description.
    :return: Metadata value
    :rtype: :py:class:`str`

    This function works exactly like :py:class:`heimdall.getValues`, but raises an :py:class:`IndexError` if there is more than one metadata corresponding to parameters.
    """  # nopep8: E501
    values = getValues(item, **options)
    if len(values) == 0:
        return None
    if len(values) == 1:
        return values[0]
    raise IndexError("Too many metadata ({count})".format(count=len(values)))


def createMetadata(item, value, **options):
    r"""Adds a single metadata to an item.

    :param item: (:py:class:`lxml.etree._Element`) -- HERA item
    :param value: (:py:class:`str`\ \|\ :py:class:`dict`) -- Metadata value
    :param \**options: (:py:class:`dict`, optional) -- Keyword arguments, see description.
    :return: Metadata list
    :rtype: :py:class:`list` of :py:class:`lxml.etree._Element`

    Metadata created by ``createMetadata`` will always be added to the item ``item``, with no consistency check.
    For example, ``createMetadata`` does not verify that ``pid`` is a valid property identifier in the database ``item`` comes from.
    Should ``item`` have a related entity, ``createMetadata`` does not check that the new metadata makes sense for the entity (*ie.* that the entity defines an attribute reusing the property ``pid``).

    The following example adds a new metadata to an existing item: ::

      >>> import heimdall
      >>> # ... do stuff ...
      >>> item = getItem(...)
      >>> heimdall.createMetadata(item, 'Bill', pid='dc:title', aid='name')
      >>> # we just added the following metadata to `item`:
      >>> # <metadata aid='name' pid='dc:title'>Bill</metadata>

    Metadata added to ``item`` can be localized, if their value is given as a :py:class:`dict` instead of a :py:class:`str` (the :py:class:`dict` keys should be valid language codes).
    Here is an example: ::

      >>> import heimdall
      >>> # ... do stuff ...
      >>> item = getItem(...)
      >>> heimdall.createMetadata(item, {
      >>>     'en_AU': 'Bill',
      >>>     'de_DE': 'Wilhelm',
      >>>     },
      >>>     pid='dc:title',
      >>>     aid='name')
      >>> # we just added the following 2 metadata to `item`:
      >>> # <metadata aid='name' pid='dc:title' xml:lang='en_AU'>Bill</metadata>
      >>> # <metadata aid='name' pid='dc:title' xml:lang='de_DE'>Wilhelm</metadata>
    """  # nopep8: E501
    nodes = _create_nodes(item, 'metadata', value)
    for node in nodes:
        for key, param in options.items():
            node.set(key, param)
    return nodes


def deleteMetadata(item, pid):
    """TODO
    """
    node = _get_node(item, 'metadata', lambda m: m.get('pid') == pid)
    if node is not None:
        node.getparent().remove(node)


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
__all__ = [
    'getMetadata', 'getValue', 'getValues',
    'createMetadata', 'deleteMetadata',
    '__copyright__', '__license__',
    ]
