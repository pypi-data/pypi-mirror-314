##########
pyHeimdall
##########

.. image:: https://sharedocs.huma-num.fr/wl/?id=bTXaJHOJwSa2swWiqdHxHPbfqMouu38u&fmode=download
   :target: https://datasphere.readthedocs.io/projects/heimdall/en/latest/
   :width: 100%
   :align: center

.. image:: https://img.shields.io/badge/license-AGPL3.0-informational?logo=gnu&color=success
   :target: https://www.gnu.org/licenses/agpl-3.0.html
.. image:: https://www.repostatus.org/badges/latest/wip.svg
   :target: https://www.repostatus.org/#project-statuses
.. image:: https://img.shields.io/pypi/v/pyheimdall
   :target: https://pypi.org/project/pyheimdall/
   :alt: PyPI - Python Version
.. image:: https://img.shields.io/badge/documentation-api-green
   :target: https://datasphere.gitpages.huma-num.fr/heimdall/python/doc/

.. image:: https://gitlab.huma-num.fr/datasphere/heimdall/python/badges/main/pipeline.svg
   :target: https://gitlab.huma-num.fr/datasphere/heimdall/python/pipelines/latest
.. image:: https://gitlab.huma-num.fr/datasphere/heimdall/python/badges/main/coverage.svg
   :target: https://datasphere.gitpages.huma-num.fr/heimdall/python/coverage/index.html
.. image:: https://datasphere.gitpages.huma-num.fr/heimdall/python/badges/loc.svg
   :target: https://gitlab.huma-num.fr/datasphere/heimdall/python/-/tree/main/src/heimdall
.. image:: https://datasphere.gitpages.huma-num.fr/heimdall/python/badges/hoc.svg
   :target: https://www.yegor256.com/2014/11/14/hits-of-code.html

*************
What is this?
*************

Heimdall is a tool for converting more easily one or more databases from one format to another.



********************
Why should I use it?
********************

If, for example, you find yourself in one of the following situations...

- you need access to data, but it is not stored in a format compatible with your favorite software...
- you'd prefer to merge several heterogeneous databases into a single corpus, easier to analyze...
- you're considering which input format to use for your software or database...
- you want to make your data more accessible and interoperable...

... then Heimdall can offer you an exchange format, and abstract the details of data implementation: yours, but also those of others.

Thanks to Heimdall, you can also switch from one technology to another in a matter of moments, as and when you need to, without ever losing, disorganizing or corrupting your data.

In a nutshell, **HEIMDALL** is your **H**\ igh **E**\ nd **I**\ nteroperability **M**\ odule when **D**\ ata is **ALL** over the place.
It's a bridge between scattered islands of data.



*****************
How can I use it?
*****************

Setup
=====

You can install Heimdall using the `pip <https://pip.pypa.io/en/stable/>`_ package manager:

.. code-block:: bash

   pip install pyheimdall

You can use `pip <https://pip.pypa.io/en/stable/>`_ to either upgrade or uninstall Heimdall, too:

.. code-block:: bash

   pip install --upgrade pyheimdall
   pip uninstall pyheimdall

Usage
=====

.. code-block:: python

   import heimdall

   config = {
       'format': 'sql:mysql',
       'url': 'mysql://user:password@localhost:3306/database',
   }
   tree = heimdall.getDatabase(**config)



*****************
Is it documented?
*****************

Sure!
Here's `the link <https://datasphere.gitpages.huma-num.fr/heimdall/python/doc/>`_.



*************
Is it tested?
*************

Of course!
Here's `the coverage report <https://datasphere.gitpages.huma-num.fr/heimdall/python/coverage/index.html>`_.


*********************
How can I contribute?
*********************

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

*******
License
*******

`GNU Affero General Public License version 3.0 or later <https://choosealicense.com/licenses/agpl/>`_
