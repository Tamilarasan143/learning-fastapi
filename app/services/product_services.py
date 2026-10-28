from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductSortBy, SortOrder


def get_products(
    db: Session,
    limit: int,
    offset: int,
    sort_by: ProductSortBy,
    sort_order: SortOrder,
    min_price: Optional[float],  # noqa: UP045
    max_price: Optional[float],  # noqa: UP045
    in_stock: Optional[bool],  # noqa: UP045
):
    sort_columns = {
        "id": Product.id,
        "name": Product.name,
        "price": Product.price,
        "stock": Product.stock,
    }
    column = sort_columns[sort_by.value]
    statement = select(Product)
    if min_price is not None:
        statement = select(Product).where(Product.price >= min_price)
    if max_price is not None:
        statement = select(Product).where(Product.price <= max_price)
    if in_stock is True:
        statement = select(Product).where(Product.stock > 0)
    if in_stock is False:
        statement = select(Product).where(Product.stock == 0)
    if sort_order == SortOrder.desc:
        statement = statement.order_by(column.desc())
    else:
        statement = statement.order_by(column.asc())
    statement = statement.limit(limit).offset(offset)
    result = db.execute(statement)
    return result.scalars().all()


def get_product(db: Session, product_id: int):
    try:
        statement = select(Product).where(Product.id == product_id)
        result = db.execute(statement).scalar_one_or_none()
        if result is None:
            return None
        return result.scalar_one_or_none()
    except Exception:
        db.rollback()
        raise


def create_product(db: Session, product_data):
    try:
        product = Product(**product_data.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)

        return product
    except Exception:
        db.rollback()
        raise


def update_product(db: Session, product_id: int, product_data):
    try:
        statement = select(Product).where(Product.id == product_id)
        product = db.execute(statement).scalar_one_or_none()
        if product is None:
            return None
        for field, value in product_data.model_dump().items():
            setattr(product, field, value)
        db.commit()
        db.refresh(product)

        return product
    except Exception:
        db.rollback()
        raise


def patch_product(db: Session, product_id: int, product_data):
    try:
        statement = select(Product).where(Product.id == product_id)
        product = db.execute(statement).scalar_one_or_none()
        if product is None:
            return None
        for field, value in product_data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        db.commit()
        db.refresh(product)
        return product
    except Exception:
        db.rollback()
        raise


def delete_product(db: Session, product_id: int):
    try:
        statement = select(Product).where(Product.id == product_id)
        product = db.execute(statement).scalar_one_or_none()
        if product is None:
            return None
        db.delete(product)
        db.commit()

        return product
    except Exception:
        db.rollback()
        raise
