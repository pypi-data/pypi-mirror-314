#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Provides CRUD operations to search in or edit a HERA elements tree.

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""

CONNECTORS = {
    'get_database': dict(),
    'create_database': dict(),
    }


def discover():
    from pkgutil import iter_modules
    from importlib import import_module
    from heimdall import connectors
    for submodule in iter_modules(connectors.__path__):
        path = f'heimdall.connectors.{submodule.name}'
        import_module(path)


def getDatabase(**options):
    r"""Imports a database as a HERA element tree

    :param \**options: Keyword arguments, see below.
    :return: HERA element tree
    :rtype: :py:class:`lxml.etree._ElementTree`

    :Keyword arguments:
        * **url** (``str``) -- Location of the database to load
        * **format** (``str``) -- Format of the database to load, see below

    This function can be used to import an HERA element tree from different
    formats, depending of the ``format`` option.
    Supported formats are:

    * ``hera:xml``: XML file; see
      :py:class:`heimdall.connectors.xml.getDatabase`
    * ``hera:yaml``: YAML file; see
      :py:class:`heimdall.connectors.yaml.getDatabase`
    * ``hera:json``: JSON file; see
      :py:class:`heimdall.connectors.json.getDatabase`
    * ``csv``: CSV files; see
      :py:class:`heimdall.connectors.csv.getDatabase`
    * ``sql:mariadb``: MariaDB database; see
      :py:class:`heimdall.connectors.mysql.getDatabase`
    * ``sql:mysql``: MySQL database; see
      :py:class:`heimdall.connectors.mysql.getDatabase`

    Depending on ``format`` option, ``getDatabase`` may accept more options.
    See the individual module ``getDatabase`` documentation for more info.
    """
    fun = CONNECTORS['get_database'][options['format']]
    return fun(**options)


def createDatabase():
    """Creates an empty database

    :return: HERA element tree
    :rtype: :py:class:`lxml.etree._ElementTree`
    """
    from .connectors import xml
    return xml.createDatabase()


def serialize(tree, **options):
    r"""Exports a HERA element tree

    :param tree: HERA element tree
    :param \**options: (optional) Keyword arguments, see description.

    This function can be used to export an HERA element tree in different
    formats, depending of the ``format`` parameter.
    Supported formats are:

    * ``hera:xml``: XML file; see
      :py:class:`heimdall.connectirs.xml.serialize`
    * ``hera:yaml``: YAML file; see
      :py:class:`heimdall.connectors.yaml.serialize`
    * ``hera:json``: JSON file; see
      :py:class:`heimdall.connectors.json.serialize`
    * ``csv``: CSV files; see
      :py:class:`heimdall.connectors.csv.serialize`
    * ``sql:mariadb``: MariaDB database; see
      :py:class:`heimdall.connectors.mysql.serialize`
    * ``sql:mysql``: MySQL database; see
      :py:class:`heimdall.connectors.mysql.serialize`

    Depending on ``format`` option, ``serialize`` may accept more options.
    See the individual module ``serialize`` documentation for more info.
    """
    fun = CONNECTORS['create_database'][options['format']]
    return fun(tree, **options)


__copyright__ = "Copyright the pyHeimdall contributors."
__license__ = 'AGPL-3.0-or-later'
__all__ = [
    'getDatabase',
    'createDatabase',
    'serialize',

    '__copyright__', '__license__',
    ]
