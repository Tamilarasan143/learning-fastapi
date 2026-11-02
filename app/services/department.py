from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Department


def get_departments(db: Session):
    statement = select(Department)
    return db.execute(statement).scalars().all()


def get_departments_with_products(db: Session):
    statement = select(Department).options(selectinload(Department.products))
    return db.execute(statement).scalars().all()


def get_department(db: Session, department_id: int):
    statement = select(Department).where(Department.id == department_id)
    department = db.execute(statement).scalar_one_or_none()
    if department is None:
        return department
    return department
