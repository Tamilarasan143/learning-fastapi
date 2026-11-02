from fastapi import FastAPI

from app.routes import department, product_routes

app = FastAPI(
    title="Learning FastAPI",
    version="1.0.0",
)

app.include_router(product_routes.router)
app.include_router(department.router)


# Root Folder
@app.get("/")
def health_check():
    return {"Status": "OK"}
