from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import Optional
app = FastAPI()

class UserRequest(BaseModel):
    name:str
    email:EmailStr
    age:Optional[int] =None
    is_active: bool = True

@app.get("/")
def hello():
    return {"message": "Hello World"}


@app.get("/products")
def get_products(limit: int = 10):
    return {
        "products": [{"id": 1, "name": "Laptop"}, {"id": 2, "name": "Phone"}],
        "limit": limit,
        "message": "product found",
    }


@app.get("/products/{product_id}")
def get_product(product_id: int,include_reviews:bool=True):
    return {"product_id": product_id,"include_reviews":include_reviews, "message": "product found"}

@app.post("/users")
def create_user(user:UserRequest):
    return {"message": "user_created","user":user}