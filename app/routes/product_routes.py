from app.schemas.product import ProductResponse ,ProductCreate
from typing import List
from fastapi import APIRouter, HTTPException, Query, status, Response
from app.services.product_services import  ProductNotFoundError, get_products as get_products_service, get_product as get_product_service, create_product as create_product_service, update_product as update_product_service, delete_product as delete_product_service

router = APIRouter(prefix="/products",tags=["products"])

def product_not_found_error(error: ProductNotFoundError)->None:
     raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(error),
    )
@router.get("/",response_model=List[ProductResponse],status_code=status.HTTP_200_OK)
def get_products(limit: int = Query(default=10, ge=1, le=100)):
    return get_products_service(limit)

@router.get("/{product_id}",response_model=ProductResponse,status_code=status.HTTP_200_OK)
def get_product(product_id:int):
    try:
        return get_product_service(product_id)
    except ProductNotFoundError as error:
        product_not_found_error(error)

@router.post("/",response_model=ProductResponse,status_code=status.HTTP_200_OK)
def create_product(new_product:ProductCreate):
    return create_product_service(new_product.model_dump())

@router.put("/{product_id}",response_model=ProductResponse,status_code=status.HTTP_200_OK)
def update_product(product_id:int,updated_product:ProductResponse):
    try:
        return update_product_service(product_id,updated_product.model_dump())
    except ProductNotFoundError as error:
        product_not_found_error(error)

@router.delete("/{product_id}",status_code=status.HTTP_204_NO_CONTENT)
def get_product(product_id:int):
    try:
        delete_product_service(product_id)
        return Response(content= "Product Delete Successfully", status_code=status.HTTP_204_NO_CONTENT)
    except ProductNotFoundError as error:
        product_not_found_error(error)