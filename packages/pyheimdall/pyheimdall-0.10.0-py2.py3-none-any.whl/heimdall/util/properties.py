# -*- coding: utf-8 -*-

"""
Provides utility functions around HERA properties refactoring or cleanup.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""
import heimdall


def delete_unused_properties(tree, relational=True):
    """Deletes unused properties from a HERA element tree.

    :param tree: (:py:class:`lxml.etree._ElementTree`) -- HERA elements tree
    :param relational: (:py:class:`bool`, optional, default: ``True``) -- Set this parameter to ``False`` for non-relational specific behaviour (see description)
    :return: None
    :rtype: :py:class:`NoneType`

    This function deletes unused properties from a HERA element tree.
    It performs its modifications "in place".
    In other words, parameter ``tree`` is directly modified,
    and this function returns nothing.

    Usage: ::

      >>> import heimdall
      >>> from heimdall.util import delete_unused_properties
      >>> tree = heimdall.getDatabase(...)
      >>> delete_unused_properties(tree)  # get rid of some clutter

    An unused property is not referenced by any attribute in the same tree
    (an attribute reuses a property via its ``pid``).
    Please note that if no attribute references a property, this property is
    deleted, even if one or more items in the tree reference this property.
    If an item metadata references an unused property,  the corresponding
    property is deleted anyway, as it has no use if the item's entity doesn't
    use the property via one of its attribute.

    | The previous paragraph description is valid for relational databases,
      but not for non-relational databases, where items directly use
      properties, and generally don't belong to any entities.
    | If your database is non-relational, a property isn't unused and
      shouldn't be deleted if one or more items reference it.
      To avoid this, set the ``relational`` parameter to ``False`` when using
      ``delete_unused_properties``.

    :see also: :py:class:`heimdall.util.update_entities` can be used to make sure entities are properly set up. As an alternative, it can be used to make a non-relational database relational.
    """  # nopep8: E501

    # give ourselves a map of unused properties, initialized with all of them
    properties = {}
    for p in heimdall.getProperties(tree):
        properties[p.get('id')] = p
    # let's check which properties are really unused
    for e in heimdall.getEntities(tree):
        for a in heimdall.getAttributes(e):
            pid = a.get('pid')
            if pid in properties.keys():
                # this property is in use ; so we mustn't delete it
                properties.pop(pid)

    to_keep = []
    if not relational:
        for pid in properties.keys():
            for item in heimdall.getItems(tree):
                metadata = heimdall.getMetadata(item, pid=pid)
                if len(metadata) > 0:
                    # item references pid, so property won't be deleted
                    to_keep.append(pid)

    # the map now only contains unused ones ; so, delete them
    # (if not relational, pid in `to_keep` ARE NOT deleted)
    for pid, p in properties.items():
        if pid not in to_keep:
            p.getparent().remove(p)
    # end of function, don't bother with properties.clear()


def merge_properties(tree, properties):
    """Merge duplicate properties.

    :param tree: (:py:class:`lxml.etree._ElementTree`) -- HERA elements tree
    :param properties: (:py:class:`dict`) -- Map containing old property identifiers as keys, and new property identifiers as values
    :return: None
    :rtype: :py:class:`NoneType`

    This function allows to merge similar properties into an existing one.
    This makes the resulting database schema more readable, because
    similarities between items and entities are more apparent when
    properties are systematically reused.

    This function updates the ``pid`` referenced by every metadata, as long as
    the ``pid`` referenced by every attribute, if these ``pid`` correspond to
    keys of the ``properties`` map parameter.
    The updated value is the key's value in ``properties``.

    Please note that only each relevant attribute ``pid`` is modified, so
    each one keeps its custom names, descriptions and whatnot.

    | As each key of ``properties`` has its own value, this method
      can be used to merge many "duplicate" properties into different
      "factorized" ones, all at once.
    | However, each value of ``properties`` must be the unique
      identifier of an existing property in ``tree``.

    After using ``merge_properties``, previous duplicate properties remain in place, albeit now unused.
    Thus, :py:class:`heimdall.util.delete_unused_properties` can be called on the same ``tree`` to get rid of them.

    Please note that this function performs its modifications "in place".
    In other words, parameter ``tree`` is directly modified,
    and this function returns nothing.

    Please also note that this function does *not* create any property.
    Thus, if some values in ``properties`` don't relate to an existing
    property identifier, ``tree`` will become inconsistent.
    To solve the problem, :py:class:`heimdall.createProperty` can be used.

    **Usage example**

    The example below shows how to reuse what is in fact the
    ``title`` property from Dublin Core, instead of entity-specific
    property names which are conceptually the same: ::

      >>> import heimdall
      >>> from heimdall.util import *
      >>> ...  # create config, load HERA tree
      >>> heimdall.createProperty(tree, 'dc:title', name="Name")
      >>> merge_properties(tree, {  # make reusage more apparent
      >>>     'book_title': 'dc:title',
      >>>     'author_name': 'dc:title',
      >>>     'character_name': 'dc:title',
      >>>     'thesaurus_keyword': 'dc:title',
      >>>     })
      >>> delete_unused_properties(tree)  # optional, but nice

    Of course, entity-specific labels can still exist: that's what attributes
    are for ; see for example functions :py:class:`heimdall.createAttribute`
    or :py:class:`heimdall.updateAttribute` for more info.

    :see also: After using ``merge_properties``, previous duplicate properties remain in place; :py:class:`heimdall.util.delete_unused_properties` can get rid of them.
    """  # nopep8: E501
    for item in heimdall.getItems(tree):
        for old, now in properties.items():
            metadata = heimdall.getMetadata(item, pid=old)
            for m in metadata:
                m.set('pid', now)

    for entity in heimdall.getEntities(tree):
        for old, now in properties.items():
            for attribute in heimdall.getAttributes(
                        entity, lambda a: a.get('pid') == old):
                heimdall.updateAttribute(attribute, pid=now)


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
