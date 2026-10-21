from sqlalchemy.orm import Session

from app.models.product import Product


def get_products(db: Session):
    return db.query(Product).all()


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


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
        product = db.query(Product).filter(Product.id == product_id).first()
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


def delete_product(db: Session, product_id: int):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product is None:
            return None
        db.delete(product)
        db.commit()

        return product
    except Exception:
        db.rollback()
        raise
