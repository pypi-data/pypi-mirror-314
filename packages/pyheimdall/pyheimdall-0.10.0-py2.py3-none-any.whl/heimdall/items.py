# -*- coding: utf-8 -*-

"""
Provides CRUD operations to search for or
edit items in a HERA element tree.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""

import heimdall as _h
from lxml import etree as _et
from .util import (
        get_node as _get_node,
        get_nodes as _get_nodes,
        get_root as _get_root,
    )


def getItem(tree, filter):
    """Retrieves a single item.

    :param entity: (:py:class:`lxml.etree._ElementTree`) -- HERA element tree
    :param filter: (:py:class:`function`) -- Filtering function
    :return: Item element
    :rtype: :py:class:`lxml.etree._Element`

    This function returns a single item from ``tree`` as defined by ``filter``, or ``None`` if there is no item in ``tree`` corresponing to ``filter`` (or if ``tree`` has no item).
    This function works exactly like :py:class:`heimdall.getItems`, but raises an ``IndexError`` if ``filter`` returns more than one result.
    """  # nopep8: E501
    return _get_node(tree, 'item', filter)


def getItems(tree, filter=None):
    """Retrieves a collection of items.

    :param entity: (:py:class:`lxml.etree._ElementTree`) -- HERA element tree
    :param filter: (:py:class:`function`, optional) -- Filtering function
    :return: Item list
    :rtype: :py:class:`list`

    This function can be used to retrieve all items in a database: ::

      >>> import heimdall
      >>> ...  # create config
      >>> tree = heimdall.getDatabase(config)  # load HERA tree
      >>> items = heimdall.getItems(tree)  # retrieve all items

    To retrieve only *some* items, you can use a filter.
    A filter is a function which takes only an item as a parameter, and returns either ``True`` (we want this item to be part of the list returned by ``getItems``) or ``False`` (we don't want it). ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>> my_favourite_author = 'Van Damme, Jean-Claude'
      >>> def by_author(item):  # create filtering function
      >>>     authors = getValues(item, 'author')
      >>>     return my_favourite_author in authors
      >>> # retrieve only items whose author is JCVD
      >>> items = heimdall.getItems(tree, by_author)

    For simple filters, anonymous functions can of course be used: ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>> # retrieve only items of a specific id
      >>> heimdall.getItems(tree, lambda e: e.getValue('id') == '42')
    """  # nopep8: E501
    return _get_nodes(tree, 'item', filter)


def createItem(tree, **kwargs):
    r"""Creates a single item.

    :param entity: (:py:class:`lxml.etree._ElementTree`) -- HERA element tree
    :param \**kwargs: (:py:class:`dict`, optional) -- Keyword arguments, see description.
    :return: Item that was just created
    :rtype: :py:class:`lxml.etree._Element`

    This function can be used to add a new item to a database.
    Elements created by ``createItem`` will always be added to the ``<items/>`` container element.

    With no additional keyword arguments, ``createItem`` simply creates a new ``<item/>`` element: ::

      >>> import heimdall
      >>> ...  # create config
      >>> tree = heimdall.getDatabase(config)  # load HERA tree
      >>> heimdall.createItem(tree)  # create an empty item

    Items can be linked to a specific entity, using this entity id ``eid``.
    The following example creates the new element ``<item eid='42' />``: ::

      >>> import heimdall
      >>> ...  # create HERA element tree
      >>> heimdall.createItem(tree, eid='42')  # create a new item
      >>> # the corresponding entity could be created later, like this:
      >>> # heimdall.createEntity(tree, id='42', ...)

    Please note that ``createItem`` makes no consistency check, *eg.* it does not validate that an entity identified by ``eid`` exists in ``tree``.

    Additional keyword arguments to ``createItem`` each add a metadata child element to the created item.
    The name of each keyword argument is the property identifier of the metadata, and its value is the metadata value.
    The following example creates an item element with metadata: ::

      >>> import heimdall
      >>> ...  # create HERA element tree
      >>> heimdall.createItem(tree, name='Chirpy', type='birb')
      >>> # the following element is now added to the ``<items/>`` container element:
      >>> # <item>
      >>> #   <metadata pid='name'>Chirpy</metadata>
      >>> #   <metadata pid='type'>birb</metadata>
      >>> # </item>
      >>> # the corresponding properties could be created later, like this:
      >>> # heimdall.createProperty(tree, id='name', ...)
      >>> # heimdall.createProperty(tree, id='type', ...)

    As stated before, ``createItem`` makes no consistency check, *eg.* it does not validate that each created metadata belongs to an existing property.

    Metada added to a new item can be localized, if their value is given as a ``dict`` instead of a ``str`` (``dict`` keys are language codes).
    Here is an example: ::

      >>> import heimdall
      >>> ...  # create HERA element tree
      >>>  heimdall.createItem(tree, eid='pet',
      >>>      name={'en': 'Chirpy', 'fr': 'Cui-Cui', },
      >>>      type={'en': 'birb', 'fr': 'wazo', },
      >>>      floof='yes')
      >>> # the following element is now added to the items list:
      >>> # <item eid='pet'>
      >>> #   <metadata pid='name' xml:lang='en'>Chirpy</metadata>
      >>> #   <metadata pid='name' xml:lang='fr'>Cui-Cui</metadata>
      >>> #   <metadata pid='type' xml:lang='en'>birb</metadata>
      >>> #   <metadata pid='type' xml:lang='fr'>wazo</metadata>
      >>> #   <metadata pid='floof'>yes</metadata>
      >>> # </item>

    Let's state it one last time: ``createItem`` makes no consistency check.
    Thus, language codes are not verified.

    Please note that, as the ``eid`` parameter is used to create a link between the item to create and its governing entity, ``createItem`` cannot be used to create an item containing a metadata child linked to a property identified by the property id ``eid``.
    """  # nopep8: E501
    container = tree.findall('.//items')
    if container:
        container = container[0]
    else:  # Create <items/> node
        container = _et.SubElement(_get_root(tree), 'items')
    # Create item
    node = _et.SubElement(container, 'item')
    for key, value in kwargs.items():
        if key != 'eid':
            _h.createMetadata(node, value, pid=key)
    param = kwargs.get('eid', None)
    if param:
        node.set('eid', param)
    return node


def replaceItem(item, **kwargs):
    """TODO: Not Implemented
    """
    raise ValueError("TODO: Not Implemented")


def updateItem(item, **kwargs):
    """TODO: Not Implemented
    """
    raise ValueError("TODO: Not Implemented")


def deleteItem(tree, filter):
    """Deletes a single item.

    :param entity: (:py:class:`lxml.etree._ElementTree`) -- HERA element tree
    :param filter: (:py:class:`function`) -- Filtering function
    :return: None
    :rtype: :py:class:`NoneType`

    This function can be used to delete a single item from ``tree``.
    It performs the item deletion "in place"; in other words, parameter ``tree`` is directly modified, and this function returns nothing.

    This function raises an ``IndexError`` if the filtering method ``filter`` returns more than one result.
    If ``filter`` returns no result, this function does nothing, and does not raise any error.

    Usage ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>> # delete an item using its unique id metadata
      >>> heimdall.deleteItem(tree, lambda e: e.getValue('id') == '42')
    """  # nopep8: E501
    node = _get_node(tree, 'item', filter)
    if node is not None:
        node.getparent().remove(node)


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
__all__ = [
    'getItem', 'getItems',
    'createItem', 'deleteItem',
    'replaceItem', 'updateItem',
    '__copyright__', '__license__',
    ]
