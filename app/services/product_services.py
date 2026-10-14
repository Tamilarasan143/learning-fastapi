from ast import Pass
from typing import List , Dict , Any
from app.storage.json_data import read_products , write_products
from sqlalchemy.orm import Session
from app.models.product import Product 

class ProductNotFoundError(Exception):
    Pass

def get_products(db:Session):
    return db.query(Product).all()

def get_product(product_id:int) -> Dict[str,Any]:
    for product in read_products():
        if product["id"] == product_id:
            return product
    raise ProductNotFoundError(f"Product {product_id} not found")

def create_product(db:Session,product_data):
   product = Product(**product_data.model_dump())
   db.add(product)
   db.commit()
   db.refresh(product)

   return product

def update_product(product_id: int, product_data: Dict[str, Any],) -> Dict[str,Any]:
    products = read_products()
    for index , product in enumerate(products):
        if product["id"] == product_id:
           updated_product = {
            "id":product_id,
            **product_data
           }
           products[index] = updated_product
           write_products(products)
           return updated_product
    raise ProductNotFoundError(f"Product {product_id} not found")
    
def delete_product(product_id: int)-> None:
     products = read_products()
     for index, product in enumerate(products):
        if product["id"] == product_id:
            products.pop(index)
            write_products(products)
            return

     raise ProductNotFoundError(f"Product {product_id} not found")