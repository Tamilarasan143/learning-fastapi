from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from app.models import Department, Product


def get_departments(db: Session, limit: int, offset: int):
    statement = select(Department).limit(limit).offset(offset)
    return db.execute(statement).scalars().all()


def get_departments_with_products(db: Session):
    statement = select(Department).options(selectinload(Department.products))
    return db.execute(statement).scalars().all()


def get_department(db: Session, department_id: int):
    statement = select(Department).where(Department.id == department_id)
    department = db.execute(statement).scalar_one_or_none()
    if department is None:
        return None
    return department


def get_department_with_products(
    db: Session, department_id: int, limit: int, offset: int
):
    statement = select(Department).where(Department.id == department_id)
    department = db.execute(statement).scalar_one_or_none()
    if department is None:
        return None
    # 1. Count all matching products
    count_statement = (
        select(func.count())
        .select_from(Product)
        .where(Product.department_id == department_id)
    )

    total_products = db.execute(count_statement).scalar_one()

    # 2. Retrieve the requested page
    products_statement = (
        select(Product)
        .where(Product.department_id == department_id)
        .limit(limit)
        .offset(offset)
    )

    products = db.execute(products_statement).scalars().all()

    return {
        "id": department.id,
        "name": department.name,
        "total_products": total_products,
        "products": [
            {
                "id": product.id,
                "name": product.name,
            }
            for product in products
        ],
    }
