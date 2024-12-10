# -*- coding: utf-8 -*-

"""
Provide connectors to various types of databases.

In addition to the connectors available here as submodules, anyone (for example, *you*!) can implement her or his own connector for any given database format, with no need to integrate them in pyHeimdall proper whatsoever.
Any "third party" (from pyHeimdall contributors point of view) connector will be automatically detected and made available by pyHeimdall, with no need to import the connector explicitely.
This connector will be usable without any need for the user to know which connector supports which format, simply by using :py:class:`heimdall.getDatabase` or :py:class:`heimdall.serialize` as usual.
This is true as long as both pyHeimdall and the connector are available (*ie.* installed) on the computer.

Examples of custom connectors independent from pyHeimdall proper are made available `in the following repositories <https://gitlab.huma-num.fr/datasphere/heimdall/connectors>`_.
For the interested reader, `this example connector <https://gitlab.huma-num.fr/datasphere/heimdall/connectors/example/-/blob/main/src/heimdall/connectors/example.py>`_ can be used as a tutorial, for example by following the following steps:

#. Fork `the example repository <https://gitlab.huma-num.fr/datasphere/heimdall/connectors/example/>`_
#. Rename ``src/heimdall/connectors/example.py`` as something you like.
#. Modify it to implement your new behaviour(s).
#. Don't forget to change the format your connector will be registered as in the parameter of ``@get_database`` and/or ``@create_database``.

| ... aaand you're done!
| Don't forget to publish it, share it, and welcome in the community!

:copyright: The pyHeimdall contributors.
:licence: Afero GPL, see LICENSE for more details.
:SPDX-License-Identifier: AGPL-3.0-or-later
"""  # nopep8: E501

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
