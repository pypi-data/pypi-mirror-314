# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel
from .shared.database_row import DatabaseRow

__all__ = ["DescribeDatabaseRowResponse"]


class DescribeDatabaseRowResponse(BaseModel):
    data: DatabaseRow
