from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_services import create_product as create_product_service
from app.services.product_services import delete_product as delete_product_service
from app.services.product_services import get_product as get_product_service
from app.services.product_services import get_products as get_products_service
from app.services.product_services import patch_product as patch_product_service
from app.services.product_services import update_product as update_product_service

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
def get_products(
    sort_by: str = Query(default="id"),
    sort_order: str = Query(default="asc"),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return get_products_service(db, limit, offset, sort_by, sort_order)


@router.get(
    "/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK
)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_service(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def create_product(new_product: ProductCreate, db: Session = Depends(get_db)):
    return create_product_service(db, new_product)


@router.put(
    "/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK
)
def update_product(
    product_id: int, updated_product: ProductResponse, db: Session = Depends(get_db)
):
    product = update_product_service(db, product_id, updated_product)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@router.patch(
    "/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK
)
def patch_update(
    product_id: int, patch_product: ProductUpdate, db: Session = Depends(get_db)
):
    product = patch_product_service(db, product_id, patch_product)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = delete_product_service(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return Response(
        content="Product Delete Successfully", status_code=status.HTTP_204_NO_CONTENT
    )
