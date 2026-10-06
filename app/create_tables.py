from app.database import engine , Base
from app.models.product import Product

Base.metadata.create_all(bind=engine)

print("Tables created successfully")