# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ClientDescribeHierarchyParams"]


class ClientDescribeHierarchyParams(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["database", "row", "workspace"]]

    database_id: Annotated[str, PropertyInfo(alias="databaseId")]
