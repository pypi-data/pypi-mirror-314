# -*- coding: utf-8 -*-

"""
Provides CRUD operations to search for or
edit entities in a HERA element tree.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""

from lxml import etree as _et
from .util.tree import (
        get_node as _get_node,
        get_nodes as _get_nodes,
        get_root as _get_root,
        create_node as _create_node,
        create_nodes as _create_nodes,
        maybe_update_node_values as _maybe_update_values,
        maybe_update_node_children as _maybe_update_children,
    )
from .attributes import getAttribute, createAttribute, updateAttribute


def getEntity(tree, filter):
    """Retrieves a single entity.

    :param tree: (:py:class:`lxml.etree._ElementTree`) -- HERA element tree
    :param filter: (:py:class:`function`) -- Filtering function
    :return: Entity element
    :rtype: :py:class:`lxml.etree._Element`

    This function returns a single entity from ``tree`` as defined by ``filter``, or ``None`` if there is no entity in ``tree`` corresponing to ``filter`` (or if ``tree`` has no entity).
    It works exactly like :py:class:`heimdall.getEntities`, but raises an ``IndexError`` if ``filter`` returns more than one result.
    """  # nopep8: E501
    return _get_node(tree, 'entity', filter)


def getEntities(tree, filter=None):
    """Retrieves a collection of entities.

    :param tree: (:py:class:`lxml.etree._ElementTree`) -- HERA element tree
    :param filter: (:py:class:`function`, optional) -- Filtering function
    :return: List of Entity elements
    :rtype: :py:class:`list`

    This function can be used to retrieve all entities in a database: ::

      >>> import heimdall
      >>> ...  # create config
      >>> tree = heimdall.getDatabase(config)  # load HERA tree
      >>> entities = heimdall.getEntities(tree)  # retrieve all entities

    To retrieve only *some* entities, you can use a filter.
    A filter is a function which takes only an item as a parameter, and returns either ``True`` (we want this entity to be part of the list returned by ``getEntities``) or ``False`` (we don't want it). ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>>
      >>> def by_attribute_property(attribute):  # attribute filter
      >>>     return attribute.get('pid', 'dc:title')
      >>>
      >>> def by_property(entity):  # entity filter
      >>>     attribute = getAttribute(entity, by_attribute_property)
      >>>     return attribute is not None
      >>>
      >>> # retrieve only entities reusing a property of id 'dc:title'
      >>> entities = heimdall.getEntities(tree, by_property)

    For simple filters, anonymous functions can of course be used: ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>> # retrieve one entity of a specific id
      >>> heimdall.getEntities(tree, lambda e: e.getValue('id') == '42')
    """  # nopep8: E501
    return _get_nodes(tree, 'entity', filter)


def createEntity(tree, id, **kwargs):
    r"""Creates a single entity.

    :param tree: (:py:class:`lxml.etree._ElementTree`) -- HERA element tree
    :param id: (:py:class:`str`) Entity unique identifier
    :param \**kwargs: (:py:class:`dict`, optional) -- Keyword arguments, see below.
    :Keyword arguments:
        * **name** (:py:class:`str`\ \|\ :py:class:`dict`, optional) -- Human-readable name
        * **type** (:py:class:`str`\ \|\ :py:class:`dict`, optional) -- Human-readable documentation
        * **uri** (:py:class:`list`, optional) -- URI list
    :return: Entity that was just created
    :rtype: :py:class:`lxml.etree._Element`

    This function can be used to add a new entity to a database.
    Entities created by ``createEntity`` will always be added to the ``<entities/>`` container element.

    In its simplest usage, ``createEntity`` simply creates a new ``<entity id='xxx'/>`` element: ::

      >>> import heimdall
      >>> ...
      >>> tree = heimdall.getDatabase(config)  # load HERA tree
      >>> heimdall.createEntity(tree, 'xxx')  # create a new entity
      >>> # the following child is now added to entities list:
      >>> # <entity pid='xxx' />

    Additional supported parameters are ``type``, ``name``, ``description``, and ``uri``.
    Each of these parameters creates appropriate children for the attribute.
    Here is an example: ::

      >>> import heimdall
      >>> ...  # load HERA tree
      >>> heimdall.createEntity(tree,
      >>>     id='person', name='Person',
      >>>     description="Real person or fictional character.",
      >>>     )
      >>> # the following entity is now added to entities list:
      >>> # <entity id='person'>
      >>> #     <name>Person</name>
      >>> #     <description>Person, real or not</description>
      >>> # </entity>

    Please note that ``name`` and ``description`` can be localized, if they are
    of type :py:class:`dict` instead of :py:class:`str` (:py:class:`dict` keys are language codes).
    The following example shows entity localization: ::

      >>> import heimdall
      >>> ...  # create HERA element tree
      >>>  heimdall.createEntity(tree,
      >>>      id='person',
      >>>      name={
      >>>          'de': "Person",
      >>>          'en': "Person",
      >>>          'fr': "Personne",
      >>>      },
      >>>      description={
      >>>          'en': "Person, real or not",
      >>>          'fr': "Personne réelle ou non",
      >>>      })
      >>> # the following entity is now added to the entities list:
      >>> # <entity id='person'>
      >>> #     <name xml:lang='de'>Person</name>
      >>> #     <name xml:lang='en'>Person</name>
      >>> #     <name xml:lang='fr'>Persone</name>
      >>> #     <description xml:lang='en'>Person, real or not</description>
      >>> #     <description xml:lang='fr'>Personne réelle ou non</description>
      >>> # </entity>

    Once an entity is created, some attributes can be added to it.
    For example: ::

      >>> import heimdall
      >>> ...  # load HERA tree
      >>> e = heimdall.createEntity(tree, id='person', name='Person')
      >>> heimdall.createAttribute(e, pid='name', name="Name")
      >>> heimdall.createAttribute(e, pid='eyes', name="Eye color")
      >>> # the following entity is now added to entities list:
      >>> # <entity id='person'>
      >>> #     <name>Person</name>
      >>> #     <attribute pid='name'>
      >>> #         <name>Name</name>
      >>> #     </attribute>
      >>> #     <attribute pid='eyes'>
      >>> #         <name>Eye color</name>
      >>> #     </attribute>
      >>> # </entity>

    See :py:class:`heimdall.createAttribute` for more info about adding attributes to an entity.
    """  # nopep8: E501
    container = tree.findall('.//entities')
    if container:
        container = container[0]
        nodes = container.getchildren()
    else:  # Create <entities/> node
        container = _et.SubElement(_get_root(tree), 'entities')
        nodes = []
    # Check entity unique id (eid) does not exist
    if len([n for n in nodes if n.get('id') == id]) > 0:
        raise ValueError(f"Entity id '{id}' already exists")
    # Create entity
    node = _et.SubElement(container, 'entity', id=id)
    param = kwargs.get('name', None)
    if param is not None:
        _create_nodes(node, 'name', param)
    param = kwargs.get('description', None)
    if param is not None:
        _create_nodes(node, 'description', param)
    param = kwargs.get('uri', [])
    if type(param) is not list:
        raise TypeError(f"'uri' expected:'list', got:'{type(param).__name__}'")
    for value in param:
        _create_node(node, 'uri', value)
    return node


def replaceEntity(entity, **kwargs):
    """TODO: Not Implemented
    """
    raise ValueError("TODO: Not Implemented")


def updateEntity(entity, **kwargs):
    """TODO
    """
    VALUES = ['id', ]
    CHILDREN = ['name', 'description', 'uri', ]
    _maybe_update_values(entity, VALUES, **kwargs)
    _maybe_update_children(entity, CHILDREN, **kwargs)

    attributes = kwargs.get('attributes', [])
    for attribute_payload in attributes:
        pid = attribute_payload.get('pid', None)
        aid = attribute_payload.get('id', None)

        def by_payload(a):
            return a.get('id') == aid and a.get('pid') == pid
        attribute = getAttribute(entity, by_payload)
        if attribute is None:
            createAttribute(entity, **attribute_payload)
        else:
            updateAttribute(attribute, **attribute_payload)


def deleteEntity(tree, filter):
    """Deletes a single entity.

    :param tree: (:py:class:`lxml.etree._ElementTree`) -- HERA element tree
    :param filter: (:py:class:`function`) -- Filtering function
    :return: None
    :rtype: :py:class:`NoneType`

    This function can be used to delete a single entity from ``tree``.
    It  performs the entity deletion "in place"; in other words, parameter ``tree`` is directly modified, and this function returns nothing.

    This function raises an ``IndexError`` if the filtering method ``filter`` returns more than one result.
    If ``filter`` returns no result, this function does nothing, and does not raise any error.

    This method doesn't delete any item documented by the deleted entity.
    All items referencing this entity, if any, will become invalid.
    One can either delete these items afterwards, or change their ``eid``, or recreate a new entity and update these items accordingly.

    Usage ::

      >>> import heimdall
      >>> ...  # create config, load HERA tree
      >>> # delete a entity using its unique id
      >>> heimdall.deleteEntity(tree, lambda e: e.get('id') == '42')
    """  # nopep8: E501
    node = _get_node(tree, 'entity', filter)
    if node is not None:
        node.getparent().remove(node)


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
__all__ = [
    'getEntity', 'getEntities',
    'createEntity', 'deleteEntity',
    'replaceEntity', 'updateEntity',
    '__copyright__', '__license__',
    ]
