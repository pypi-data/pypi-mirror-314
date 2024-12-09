"""
Main interface for dataexchange service.

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_dataexchange import (
        Client,
        DataExchangeClient,
        ListDataSetRevisionsPaginator,
        ListDataSetsPaginator,
        ListEventActionsPaginator,
        ListJobsPaginator,
        ListRevisionAssetsPaginator,
    )

    session = get_session()
    async with session.create_client("dataexchange") as client:
        client: DataExchangeClient
        ...


    list_data_set_revisions_paginator: ListDataSetRevisionsPaginator = client.get_paginator("list_data_set_revisions")
    list_data_sets_paginator: ListDataSetsPaginator = client.get_paginator("list_data_sets")
    list_event_actions_paginator: ListEventActionsPaginator = client.get_paginator("list_event_actions")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_revision_assets_paginator: ListRevisionAssetsPaginator = client.get_paginator("list_revision_assets")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import DataExchangeClient
from .paginator import (
    ListDataSetRevisionsPaginator,
    ListDataSetsPaginator,
    ListEventActionsPaginator,
    ListJobsPaginator,
    ListRevisionAssetsPaginator,
)

Client = DataExchangeClient


__all__ = (
    "Client",
    "DataExchangeClient",
    "ListDataSetRevisionsPaginator",
    "ListDataSetsPaginator",
    "ListEventActionsPaginator",
    "ListJobsPaginator",
    "ListRevisionAssetsPaginator",
)
