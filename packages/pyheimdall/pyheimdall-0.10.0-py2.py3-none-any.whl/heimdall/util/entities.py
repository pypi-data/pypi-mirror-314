# -*- coding: utf-8 -*-

"""
Provides utility functions around HERA entities refactoring or cleanup.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""
import heimdall
from heimdall.util import get_node, create_node
from lxml import etree as _et


ENTITIES = 'entities'
ATTRIBUTES = 'attributes'
PROPERTIES = 'properties'
INT_MAX_VALUE = 999999  # should theorically be `sys.maxsize * 2 + 1` but heck


def update_entities(tree, delete_orphans=False):
    """Updates entities in a database according to items present in it.

    :param tree: (:py:class:`lxml.etree._ElementTree`) -- HERA elements tree
    :param delete_orphans: (:py:class:`bool`, optional, default: ``False``) -- If ``delete_orphans`` is ``True``, metadata with neither ``aid`` nor ``pid`` will be deleted from their containing item, as they cannot be linked to any entity or property. If ``False`` (default), these metadata will be left untouched.
    :return: None
    :rtype: :py:class:`NoneType`

    This function updates entities and their attributes in a HERA element tree, according to the items and their metadata present in said tree.
    It attempts to do the following modifications:

    #. create entities referenced by items ``eid`` if they are missing ;
    #. create attributes referenced by items metadata ``aid`` if they are missing ;
    #. set attributes ``id`` to their ``pid`` if it has no value ;
    #. set attributes ``min`` to ``0``, if it is missing from at least one of the metadata of the corresponding entity ;
    #. set attributes ``max`` to its maximum occurences in the metadata of the corresponding entity ;
    #. set attributes ``type`` to be the most restrictive, according to corresponding metadata values ;
    #. (optional -- see ``delete_orphan`` parameter)
       deletes any item metadata referencing a property that is missing.

    This function can be used to make non-relational databases relational.
    It performs its modifications "in place" ; in other words, parameter ``tree`` is directly modified, and this function returns nothing.

    :see also: :py:class:`heimdall.util.delete_unused_properties` is always useful to further remove clutter from a database.
    """  # nopep8: E501
    data = dict()
    data[ENTITIES] = dict()
    data[PROPERTIES] = dict()
    all_entities = set()
    ALL_ATTRIBUTES = 'all'
    for item in heimdall.getItems(tree):
        eid = item.get('eid')
        if eid is None:
            continue  # we can't do anything if item has no entity
        entity = _get_entity(tree, data, eid)
        metas = dict()  # {aid <> counter} of already encountered metadata
        for metadata in heimdall.getMetadata(item):
            # (1) retrieve attribute and property for metadata
            (pid, aid, attribute) = _get_metadata_info(metadata, entity)
            property_ = _get_property(tree, data, pid, aid)
            if property_ is None:
                # pid AND aid should be null here, so metadata is orphan
                if delete_orphans:
                    metadata.getparent().remove(metadata)
                continue  # rest of the loop is moot for orphan

            assert attribute is not None
            assert property_ is not None
            # (2) infer attribute type
            value = metadata.text
            type_ = attribute.get('type', None)
            if type_ != 'text':
                attribute['type'] = _infer_type(value)
            # (2a) infer attribute length
            # TODO: kinda useful for SQL, but not really used yet
            attribute['length'] = max(attribute.get('length', 0), len(value))
            # (3) count metadata in this item to infer min and max later
            all_attributes = entity.get(ALL_ATTRIBUTES, set())
            if eid in all_entities:
                if aid not in all_attributes:
                    # there was already an item for this entity, and this item
                    # did not have this metadata ; thus metadata is optional
                    attribute['min'] = 0
            # track that we saw this attribute, and how much times
            all_attributes.add(aid)
            entity[ALL_ATTRIBUTES] = all_attributes
            count = metas.get(aid, 0)
            count += 1
            metas[aid] = count
            # NOTE: name, description or uri cannot be infered from metadata

        # track we already saw this entity (this was the first item with it)
        all_entities.add(eid)
        # (4) update attributes min and max
        for aid, count in metas.items():
            attribute = [a for a in entity[ATTRIBUTES] if a['id'] == aid][0]
            amin = int(attribute.get('min', INT_MAX_VALUE))
            amax = int(attribute.get('max', 0))
            attribute['min'] = min(amin, count)
            attribute['max'] = max(amax, count)
    # cleanup
    for entity in data[ENTITIES].values():
        del entity[ALL_ATTRIBUTES]

    # TODO (5) infer properties types form all attributes that use it

    # (6) create/update tree nodes from infered data
    _update_tree(tree, data)
    return tree


def _get_metadata_info(metadata, entity):
    pid = metadata.get('pid', None)
    aid = metadata.get('aid', None)
    if (pid is None) and (aid is None):
        return (None, None, None)  # can't do anything
    # try to get `metadata`'s attribute in entity by attribute ID
    attribute = _get_attribute_by(entity, 'id', aid)
    if attribute is None:
        # try to get `metadata`'s attribute in entity by property ID
        attribute = _get_attribute_by(entity, 'pid', pid)
    if attribute is None:
        # `entity` doesn't contain any attribute referenced by `metadata`
        # thus, we need to fix entity by adding its missing attribute
        (pid, aid, attribute) = _create_attribute(entity, pid, aid)
    (pid, aid) = _update_attribute(attribute, pid, aid)
    return (pid, aid, attribute)


def _infer_type(value):
    try:
        float(value)
        return 'number'
    except ValueError:
        pass  # not a number
    try:
        from dateutil.parser import parse
        parse(value)
        return 'datetime'
    except ModuleNotFoundError:
        pass  # dateutils missing, we can't say if it's a date
    except:  # nopep8: E722
        # I'm not explicit on error catched because dateutil.parser.parse
        # raises custom Errors that I may be unable to import
        pass  # not a date
    return 'text'


def _get_entity(tree, data, eid):
    """Retrieves the current state of an entity as an plain object.
    """
    entity = data[ENTITIES].get(eid, None)
    if entity is not None:
        return entity
    node = heimdall.getEntity(tree, lambda n: n.get('id') == eid)
    if node is not None:
        from heimdall.connectors.json import _entity2object
        data[ENTITIES][eid] = _entity2object(node)
    else:
        data[ENTITIES][eid] = {'id': eid, }
    return data[ENTITIES][eid]


def _get_attribute_by(entity, param, value):
    if value is None:
        return None
    attributes = entity.get(ATTRIBUTES, list())
    attributes = [a for a in attributes if a.get(param, None) == value]
    assert len(attributes) < 2
    attribute = attributes[0] if len(attributes) > 0 else None
    return attribute


def _create_attribute(entity, pid, aid):
    """Adds a new attribute (which is a dict) to `entity` (a dict, too).
    Prerequisite: `pid` and `aid` can't both be `None`.
    """
    attribute = dict()
    (pid, aid) = _update_attribute(attribute, pid, aid)
    attributes = entity.get(ATTRIBUTES, list())
    attributes.append(attribute)
    entity[ATTRIBUTES] = attributes
    return (pid, aid, attribute)


def _update_attribute(attribute, pid, aid):
    """Set `attribute`(which is a dict) `pid` and `id`.
    `id` is set to `pid` if missing, but NOT the contrary.
    """
    if attribute.get('pid', None) is None:
        if pid is not None:
            attribute['pid'] = pid
    if attribute.get('id', None) is None:
        if aid is not None:
            attribute['id'] = aid
        else:
            attribute['id'] = pid
    return (attribute.get('pid', None), attribute.get('id', None))


def _get_property(tree, data, pid, aid):
    if pid is None:
        if aid is None:
            return None
        pid = aid
    property_ = data[PROPERTIES].get(pid, None)
    if property_ is not None:
        return property_
    node = heimdall.getProperty(tree, lambda n: n.get('id') == pid)
    if node is not None:
        from heimdall.connectors.json import _property2object
        data[PROPERTIES][pid] = _property2object(node)
    else:
        data[PROPERTIES][pid] = {'id': pid, }
    return data[PROPERTIES][pid]


def _update_tree(tree, data):
    """Update HERA element tree with new data
    """
    for pid, payload in data[PROPERTIES].items():
        property_ = heimdall.getProperty(tree, lambda n: n.get('id') == pid)
        if property_ is None:
            _get_container(tree, 'properties')  # creates if missing
            heimdall.createProperty(tree, **payload)
        else:
            heimdall.updateProperty(property_, **payload)

    for eid, payload in data[ENTITIES].items():
        entity = heimdall.getEntity(tree, lambda n: n.get('id') == eid)
        if entity is None:
            _get_container(tree, 'entities')  # creates if missing
            entity = heimdall.createEntity(tree, **payload)
        else:
            heimdall.updateEntity(entity, **payload)
        for a in payload[ATTRIBUTES]:
            aid = a['id']
            attr = heimdall.getAttribute(entity, lambda n: n.get('id') == aid)
            if attr is None:
                attr = heimdall.createAttribute(entity, **a)
            else:
                heimdall.updateAttribute(attr, **a)
            try:
                length = a['length']
                prefix = heimdall.connectors.mysql.LENGTH_PREFIX
                create_node(attr, 'rule', f'{prefix}{str(length)}')
            except KeyError:
                pass  # no length


def _get_container(tree, tag):
    container = get_node(tree, tag)
    if container is None:
        container = _et.SubElement(tree, tag)
    return container
