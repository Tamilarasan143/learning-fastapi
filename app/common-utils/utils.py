from typing import (  # noqa: UP035
    Generic,
    List,
    TypeVar,
)

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    page: int
    pageSize: int
    totalRecords: int
    data: List[T]  # noqa: UP006

