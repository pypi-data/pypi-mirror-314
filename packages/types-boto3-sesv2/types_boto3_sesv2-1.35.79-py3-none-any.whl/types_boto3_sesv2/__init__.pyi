"""
Main interface for sesv2 service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sesv2 import (
        Client,
        ListMultiRegionEndpointsPaginator,
        SESV2Client,
    )

    session = Session()
    client: SESV2Client = session.client("sesv2")

    list_multi_region_endpoints_paginator: ListMultiRegionEndpointsPaginator = client.get_paginator("list_multi_region_endpoints")
    ```

Copyright 2024 Vlad Emelianov
"""

from .client import SESV2Client
from .paginator import ListMultiRegionEndpointsPaginator

Client = SESV2Client

__all__ = ("Client", "ListMultiRegionEndpointsPaginator", "SESV2Client")
