from ast import Pass
from typing import List , Dict , Any
from app.storage.json_data import read_products , write_products

class ProductNotFoundError(Exception):
    Pass

def get_products(limit=10)->List[Dict[str,Any]]:
    return read_products()[:limit]

def get_product(product_id:int) -> Dict[str,Any]:
    for product in read_products():
        if product["id"] == product_id:
            return product
    raise ProductNotFoundError(f"Product {product_id} not found")

def create_product(product_data:Dict[str,Any]) -> Dict[str,Any]:
    products = read_products()
    next_id = max(
        (product["id"] for product in products),
        default=0,
    ) + 1
    new_product = {
        "id":next_id,
         **product_data
    }
    products.append(new_product)
    write_products(products)
    return new_product

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