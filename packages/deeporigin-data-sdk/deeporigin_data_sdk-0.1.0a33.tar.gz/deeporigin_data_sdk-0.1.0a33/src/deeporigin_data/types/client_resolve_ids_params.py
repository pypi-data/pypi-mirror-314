# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ClientResolveIDsParams", "Row"]


class ClientResolveIDsParams(TypedDict, total=False):
    database_ids: Annotated[List[str], PropertyInfo(alias="databaseIds")]

    rows: Iterable[Row]

    workspace_ids: Annotated[List[str], PropertyInfo(alias="workspaceIds")]


class Row(TypedDict, total=False):
    database_id: Required[Annotated[str, PropertyInfo(alias="databaseId")]]

    row_id: Required[Annotated[str, PropertyInfo(alias="rowId")]]
