# -*- coding: utf-8 -*-
import heimdall
from ..decorators import get_database, create_database
from .json import is_url, _create_tree, _tree2object
from urllib.parse import urlparse
from urllib.request import urlopen
try:
    from yaml import safe_load, dump
    _installed = True
except ModuleNotFoundError:  # pragma: no cover
    _installed = False

"""
Provides connectors to HERA-formatted YAML files.

This module defines input and output connectors to databases composed in full or in part of YAML files following the HERA schema.

* :py:class:`heimdall.connectors.yaml.getDatabase` is the input connector
* :py:class:`heimdall.connectors.yaml.serialize` is the output connector

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""  # nopep8: E501


def check_available():
    if not _installed:
        raise ModuleNotFoundError("Module 'pyyaml' required.")
    return _installed


@get_database('hera:yaml')
def getDatabase(**options):
    r"""Imports a database from a HERA YAML file

    :param \**options: Keyword arguments, see below.
    :Keyword arguments:
        * **url** (:py:class:`str`) -- Local ou remote path of the YAML file to import
        * **format** (:py:class:`str`, optional) Always ``hera:yaml``
        * **encoding** (:py:class:`str`, optional, default: ``utf-8``) -- ``url`` file encoding
    :return: HERA element tree
    :rtype: :py:class:`lxml.etree._ElementTree`

    Usage example: ::

      >>> import heimdall
      >>> tree = heimdall.getDatabase(format='hera:yaml', url='some/input.yaml')
      >>> # ... do stuff ...

    .. CAUTION::
       For future compability, this function shouldn't be directly called; as shown in the usage example above, it should only be used through :py:class:`heimdall.getDatabase`.
    """  # nopep8: E501
    check_available()  # breaks if not
    url = options['url']
    encoding = options.get('encoding', 'utf-8')
    if not is_url(url):
        with open(url, 'r') as f:
            data = safe_load(f)
    else:
        with urlopen(url) as response:
            data = safe_load(response.read().decode(encoding))
    return _create_tree(data or dict())


@create_database('hera:yaml')
def serialize(tree, url, **options):
    r"""Serializes a HERA elements tree into a YAML file

    :param tree: HERA elements tree
    :param url: Path of the YAML output file
    :param \**options: Keyword arguments, see below.

    :Keyword arguments:
        * **style** (``str``, default: ``block``) -- YAML flow style for
          output file. Valid values are ``flow`` of ``block``.
          Any value other than ``flow`` will be interpreted as ``block``.
        * **sort** (``bool``, default: ``False``) -- If ``True``, keys will be
          sorted in output file; if ``False`` keys will be written to ``url``
          as they are found in ``tree``.
    """
    check_available()  # breaks if not
    data = _tree2object(tree)
    # write data to file
    style = options.get('style', 'block')
    style = (style == 'flow')
    sort = options.get('sort', False)
    with open(url, 'w', encoding='utf-8') as f:
        dump(data, f, default_flow_style=style, sort_keys=sort)
