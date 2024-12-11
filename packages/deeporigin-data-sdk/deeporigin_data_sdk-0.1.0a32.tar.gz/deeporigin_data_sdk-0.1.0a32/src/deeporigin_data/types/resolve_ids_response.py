# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = ["ResolveIDsResponse", "Data", "DataResolvedDatabaseID", "DataResolvedWorkspaceID", "DataResolvedRowID"]


class DataResolvedDatabaseID(BaseModel):
    id: str

    hid: str

    type: Literal["database"]


class DataResolvedWorkspaceID(BaseModel):
    id: str

    hid: str

    type: Literal["workspace"]


class DataResolvedRowID(BaseModel):
    id: str

    database_id: str = FieldInfo(alias="databaseId")

    hid: str

    type: Literal["row"]


Data: TypeAlias = Annotated[
    Union[DataResolvedDatabaseID, DataResolvedWorkspaceID, DataResolvedRowID], PropertyInfo(discriminator="type")
]


class ResolveIDsResponse(BaseModel):
    data: List[Data]
