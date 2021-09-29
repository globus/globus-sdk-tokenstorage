.. image:: https://github.com/globus/globus-sdk-tokenstorage/actions/workflows/build.yaml/badge.svg
    :alt: build status
    :target: https://github.com/globus/globus-sdk-tokenstorage/actions/workflows/build.yaml

.. image:: https://img.shields.io/pypi/v/globus-sdk-tokenstorage.svg
    :alt: Latest Released Version
    :target: https://pypi.org/project/globus-sdk-tokenstorage/

.. image:: https://img.shields.io/pypi/pyversions/globus-sdk-tokenstorage.svg
    :alt: Supported Python Versions
    :target: https://pypi.org/project/globus-sdk-tokenstorage/

.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :alt: License
    :target: https://opensource.org/licenses/Apache-2.0


Globus SDK TokenStorage
=======================

Th Globus SDK provides a convenient Pythonic interface to
`Globus <https://www.globus.org>`_ APIs.

This library provides an interface for handling the storage and management of
tokens acquired through the SDK more easily.

It takes tokens, stores and loads them to and from files, and additionally
provides ``on_refresh`` callbacks which can be used in
``globus_sdk.RefreshTokenAuthorizer`` and
``globus_sdk.ClientCredentialsAuthorizer`` to keep those files up-to-date.

Intentional limitation: this library does not generate Authorizers or Clients,
and is limited only to token and file management.

In the future, this may expand to include storage mechanisms which are not
files.

Links
-----

- Full documentation: https://globus-sdk-tokenstorage.readthedocs.io/en/latest/

Changelog
---------

0.4.1 (2021-09-29)
~~~~~~~~~~~~~~~~~~

* Allow use with SDK version 3

0.4.0 (2021-06-03)
~~~~~~~~~~~~~~~~~~

* *Bugfix:* Set umask to ``0o177`` when creating sqlite DB, so that it will only
  be readable and writable by the current user

* Abstract base clases now inherit from ``abc.ABC``

* Rename abstract base classes to ``StorageAdapter`` and ``FileAdapter``

* ``SQLiteStorageAdapter`` is now a ``FileAdapter`` where ``filename`` is the
  db name

0.3.0 (2021-05-03)
~~~~~~~~~~~~~~~~~~

* Drop support for python versions < 3.6

0.2.1 (2019-11-12)
~~~~~~~~~~~~~~~~~~

* Add methods to ``SQLiteStorageAdapter`` for removing tokens and removing config

0.2.0 (2019-11-12)
~~~~~~~~~~~~~~~~~~

* Add ``SQLiteStorageAdapter`` which stores tokens and config under namespaces in
  a sqlite db

0.1.0 (2018-11-07)
~~~~~~~~~~~~~~~~~~

* Initial version of the library, implementing ``SimpleJSONStorageAdapter``
