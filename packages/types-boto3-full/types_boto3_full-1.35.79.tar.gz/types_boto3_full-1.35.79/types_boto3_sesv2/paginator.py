"""
Type annotations for sesv2 service client paginators.

[Open documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sesv2/paginators/)

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_sesv2.client import SESV2Client
    from types_boto3_sesv2.paginator import (
        ListMultiRegionEndpointsPaginator,
    )

    session = Session()
    client: SESV2Client = session.client("sesv2")

    list_multi_region_endpoints_paginator: ListMultiRegionEndpointsPaginator = client.get_paginator("list_multi_region_endpoints")
    ```

Copyright 2024 Vlad Emelianov
"""

import sys
from typing import Generic, Iterator, TypeVar

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListMultiRegionEndpointsRequestListMultiRegionEndpointsPaginateTypeDef,
    ListMultiRegionEndpointsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ListMultiRegionEndpointsPaginator",)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(PageIterator, Generic[_ItemTypeDef]):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListMultiRegionEndpointsPaginator(Paginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListMultiRegionEndpoints.html#SESV2.Paginator.ListMultiRegionEndpoints)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sesv2/paginators/#listmultiregionendpointspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListMultiRegionEndpointsRequestListMultiRegionEndpointsPaginateTypeDef],
    ) -> _PageIterator[ListMultiRegionEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListMultiRegionEndpoints.html#SESV2.Paginator.ListMultiRegionEndpoints.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sesv2/paginators/#listmultiregionendpointspaginator)
        """
