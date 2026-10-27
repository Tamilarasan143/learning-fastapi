from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


def get_products(db: Session):
    statement = select(Product)
    result = db.execute(statement)
    return result.scalars().all()


def get_product(db: Session, product_id: int):
    statement = select(Product).where(Product.id == product_id)
    result = db.execute(statement)
    return result


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
