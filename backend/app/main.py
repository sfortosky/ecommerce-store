from fastapi import FastAPI
from app.database import Base, engine

# Import all db models
from app.models.user_model import User
from app.models.product_model import Product

# Import all routers
from app.api.product_api import router as product_router

# Create all db tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(product_router, prefix="/products", tags=["Products"])

@app.get("/")
def read_root():
    return {"message": "Welcome to my Ecommerce Store"}