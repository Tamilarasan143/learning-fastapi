from typing import List

from pydantic import BaseModel


class DepartmentResponse(BaseModel):
    id: int
    name: str


class ProductSummaryResponse(BaseModel):
    id: int
    name: str


class DepartmentWithProductsResponse(BaseModel):
    id: int
    name: str
    total_products: int
    products: List[ProductSummaryResponse]  # noqa: UP006
