from app.schemas.product import ProductResponse ,ProductCreate
from typing import List
from fastapi import APIRouter, HTTPException, status, Response , Depends
from app.services.product_services import  ProductNotFoundError, get_products as get_products_service, get_product as get_product_service, create_product as create_product_service, update_product as update_product_service, delete_product as delete_product_service
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product

router = APIRouter(prefix="/products",tags=["products"])

def product_not_found_error(error: ProductNotFoundError)->None:
     raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(error),
    )
@router.get("/",response_model=List[ProductResponse],status_code=status.HTTP_200_OK)
def get_products(db:Session = Depends(get_db)):
    return get_products_service(db)

@router.get("/{product_id}",response_model=ProductResponse,status_code=status.HTTP_200_OK)
def get_product(product_id:int):
    try:
        return get_product_service(product_id)
    except ProductNotFoundError as error:
        product_not_found_error(error)

@router.post("/",response_model=ProductResponse,status_code=status.HTTP_200_OK)
def create_product(new_product:ProductCreate,db:Session = Depends(get_db)):
    return create_product_service(db,new_product)

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