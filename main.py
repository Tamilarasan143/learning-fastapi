from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello World"}


@app.get("/products")
def get_projects():
    return {"products": [{"id": 1, "name": "Laptop"}, {"id": 2, "name": "Phone"}]}
