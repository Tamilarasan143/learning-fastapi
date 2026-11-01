from decimal import Decimal
from typing import Optional

from sqlalchemy import ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False, default=0)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # noqa: UP045
    department_id: Mapped[Optional[int]] = mapped_column(  # noqa: UP045
        ForeignKey("departments.id"), nullable=True
    )

    department = relationship(
        "Department",
        back_populates="products",
    )
