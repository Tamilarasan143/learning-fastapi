from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    stock: int = Field(gt=0)
    description: Optional[str] = None  # noqa: UP045


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    price: float
    stock: int
    description: Optional[str] = None  # noqa: UP045


class ProductUpdate(BaseModel):
    name: Optional[str] = None  # noqa: UP045
    price: Optional[float] = None  # noqa: UP045
    description: Optional[str] = None  # noqa: UP045
    stock: Optional[int] = None  # noqa: UP045
