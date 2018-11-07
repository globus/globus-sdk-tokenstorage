Globus SDK TokenStorage
=======================

A Globus SDK contrib module providing simple token storage.

Basic Usage
-----------

Install with ``pip install globus-sdk-tokenstorage``

You can then import helpers from ``globus_sdk_tokenstorage``. For example:

.. code-block:: python

    import os
    import globus_sdk
    from globus_sdk_tokenstorage import SimpleJSONFileAdapter

    my_file_adapter = SimpleJSONFileAdapter(
        os.path.expanduser('~/mytokens.json'),
        resource_server='transfer.api.globus.org')

    if not my_file_adapter.file_exists():
        # ... do a login low, getting back initial tokens
        # elided for simplicity here
        token_response = ...
        # now store the tokens, and pull out the tokens for the resource server
        # we want
        my_file_adapter.store(token_response)
        by_rs = token_response.by_resource_server
        tokens = by_rs['transfer.api.globus.org']
    else:
        # otherwise, we already did this whole song-and-dance, so just load the
        # tokens from that file
        tokens = my_file_adapter.read_as_dict()


    # RereshTokenAuthorizer and ClientCredentialsAuthorizer both use
    # `on_refresh` callbacks -- this feature is therefore only relevant for
    # those auth types
    # auth_client is the internal auth client used for refreshes, which was
    # used in the login flow
    # note that this is all normal SDK usage
    auth_client = ...
    authorizer = globus_sdk.RefreshTokenAuthorizer(
        tokens['refresh_token'], auth_client,
        tokens['access_token'], tokens['access_token_expires'],
        on_refresh=my_file_adapter.on_refresh)

    # or, for client credentials
    authorizer = globus_sdk.ClientCredentialsAuthorizer(
        auth_client, ['urn:globus:auth:transfer.api.globus.org:all'],
        on_refresh=m_file_adapter.on_refresh)

    # and then use as normal, tada!
    tc = globus_sdk.TransferClient(authorizer=authorizer)

Full Library Contents
---------------------

.. module:: globus_sdk_tokenstorage

.. autoclass:: globus_sdk_tokenstorage.abstract_base.AbstractStorageAdapter
   :members:
   :member-order: bysource
   :show-inheritance:

.. autoclass:: globus_sdk_tokenstorage.file_adapters.AbstractFileAdapter
   :members:
   :member-order: bysource
   :show-inheritance:

.. autoclass:: globus_sdk_tokenstorage.SimpleJSONFileAdapter
   :members:
   :member-order: bysource
   :show-inheritance:
