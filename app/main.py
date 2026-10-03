from fastapi import FastAPI
from app.routes.product_routes import router as products_router

app = FastAPI(
    title="Learning FastAPI",
    version="1.0.0",
)

app.include_router(products_router)


#Root Folder
@app.get("/")
def health_check():
    return {"Status": "OK"}