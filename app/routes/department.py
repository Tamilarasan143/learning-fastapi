from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.department import DepartmentResponse, DepartmentWithProductsResponse
from app.services.department import get_department as get_department_service
from app.services.department import get_departments as get_departments_service
from app.services.department import (
    get_departments_with_products as get_departments_with_products_service,
)

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get(
    "/", response_model=list[DepartmentResponse], status_code=status.HTTP_200_OK
)
def get_departments(db: Session = Depends(get_db)):
    return get_departments_service(db)


@router.get(
    "/with-products",
    response_model=list[DepartmentWithProductsResponse],
    status_code=status.HTTP_200_OK,
)
def get_departments_with_products(db: Session = Depends(get_db)):
    return get_departments_with_products_service(db)


@router.get(
    "/{department_id}",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK,
)
def get_department(department_id: int, db: Session = Depends(get_db)):
    department = get_department_service(db, department_id)
    if department is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )
    return department
