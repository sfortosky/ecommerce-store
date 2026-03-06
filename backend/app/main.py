from fastapi import FastAPI
from app.database import Base, engine

from app.models.user_model import User
from app.models.product_model import Product

# Create all db tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my Ecommerce Store"}