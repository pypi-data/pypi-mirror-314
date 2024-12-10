# -*- coding: utf-8 -*-

"""
Provides all `CRUD operations <https://en.wikipedia.org/wiki/Create,_read,_update_and_delete>`_ to search or edit a HERA element tree.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""  # nopep8: E501

from pkgutil import extend_path
from .heimdall import *

from .properties import (
    getProperty, getProperties,
    createProperty, deleteProperty,
    replaceProperty, updateProperty,
    )
from .entities import (
    getEntity, getEntities,
    createEntity, deleteEntity,
    replaceEntity, updateEntity,
    )
from .attributes import (
    getAttribute, getAttributes,
    createAttribute, deleteAttribute,
    replaceAttribute, updateAttribute,
    )
from .items import (
    getItem, getItems,
    createItem, deleteItem,
    replaceItem, updateItem,
    )
from .metadata import (
    getMetadata, getValue, getValues,
    createMetadata, deleteMetadata,
    )
from .util import (
        get_node as _get_node,
        get_nodes as _get_nodes,
        get_root as _get_root,
        create_nodes as _create_nodes,
    )


__path__ = extend_path(__path__, __name__)
from .heimdall import discover
discover()


__version__ = '0.10.0'
__all__ = [
    'getDatabase',
    'createDatabase',
    'serialize',

    'getProperty', 'getProperties',
    'createProperty', 'deleteProperty',
    'replaceProperty', 'updateProperty',

    'getEntity', 'getEntities',
    'createEntity', 'deleteEntity',
    'replaceEntity', 'updateEntity',
    'getAttribute', 'getAttributes',
    'createAttribute', 'deleteAttribute',
    'replaceAttribute', 'updateAttribute',

    'getItem', 'getItems',
    'createItem', 'deleteItem',
    'replaceItem', 'updateItem',

    'getMetadata', 'getValue', 'getValues',
    'createMetadata', 'deleteMetadata',

    '__copyright__', '__license__', '__version__',
    ]
