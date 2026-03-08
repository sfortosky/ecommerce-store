from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product_model import Product as ProductModel
from app.schemas.product_schema import Product, ProductCreate

router = APIRouter()


# GET - Get one product by ID
@router.get("/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):

    # Look for the product in the database
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    # If it doesn't exist, raise an error
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

    # If it does exist, return the product
    return product


# GET - Get all products
@router.get("/", response_model=List[Product])
def read_products(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = Query(10, ge=1, le=100), # Apply an upper and lower limit
        search: str = "",
        sort: str = "id_asc"
):
    # Create a base query
    query = db.query(ProductModel)

    # Apply search filters to the query
    if search:
        query = query.filter(ProductModel.name.ilike(f"%{search}%"))

    # Apply sorting
    if sort == "price_asc":
        query = query.order_by(ProductModel.price.asc())
    elif sort == "price_desc":
        query = query.order_by(ProductModel.price.desc())
    else:
        query = query.order_by(ProductModel.id.asc())

    # Create a list by executing the query (with limits)
    products = query.offset(skip).limit(limit).all()

    # Return the filtered list of products
    return products


# POST - Create a product
@router.post("/", response_model=Product)
def create_product(product_create: ProductCreate, db: Session = Depends(get_db)):

    # Convert product details to JSON/dictionary
    new_product_json = product_create.model_dump()

    # Unpack JSON/dictionary into format readable by pydantic
    new_product = ProductModel(**new_product_json)

    # Attempt to add to database
    try:
        # Add to database
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        # Return database entry
        return new_product

    # Raise an error if any issues are encountered
    except Exception as e:
        db.rollback()
        # TODO: Make error message handle more specific cases
        raise HTTPException(status_code=500, detail=f"Product creation failed: {str(e)}")


# PUT - Update a product
@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product_update: ProductCreate, db: Session = Depends(get_db)):
    # Look for the product in the database
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    # If it doesn't exist, raise an error
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Convert product details to JSON/dictionary
    update_data = product_update.model_dump()

    # Attempt to update the database entry
    try:
        # Update the attributes of the object
        for key, value in update_data.items():
            setattr(db_product, key, value)

        # Attempt to save the changes
        db.commit()
        db.refresh(db_product)
        return db_product

    # Raise an error if any issues are encountered
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Product update failed: {str(e)}")


# DELETE - Delete a product
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # Look for the product in the database
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()

    # If it doesn't exist, raise an error
    if not product:
        raise HTTPException(status_code=404, detail="Cannot delete. Product not found.")

    # If it does exist, delete it and commit the changes
    try:
        db.delete(product)
        db.commit()
        return {"message": f"Product {product_id} has been deleted"}

    # Raise an error if any issues are encountered
    except Exception as e:
        db.rollback()
        # TODO: Make error message handle more specific cases
        raise HTTPException(status_code=500, detail=f"Product removal failed: {str(e)}")