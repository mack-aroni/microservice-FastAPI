import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# main redis db connection
redis_inventory = get_redis_connection(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT", 0)),
    password=os.getenv("REDIS_ PASSWORD"),
    decode_responses=True,
)


# storage class for redis Product objects
class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis_inventory


# pydantic class for a quantity update request
class UpdateQuantityRequest(BaseModel):
    quantity: int


# CREATE endpoint
@app.post("/products")
def create(product: Product):
    return product.save()


# RETURN endpoint
@app.get("/products/{pk}")
def get(pk: str):
    return Product.get(pk)


# RETURN ALL endpoint
@app.get("/products")
def get_all():
    return [format(pk) for pk in Product.all_pks()]


# helper function to format the data of each product
def format(pk: str):
    product = Product.get(pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
    }


# DELETE endpoint
@app.delete("/products/{pk}")
def delete(pk: str):
    return Product.delete(pk)


# DELETE ALL endpoint
@app.delete("/products")
def delete_all(pk: str):
    return [Product.delete(pk) for pk in Product.all_pks()]


# REST API call to update product quantity if present
@app.put("/update_quantity/{product_id}")
def update_quantity(product_id: str, request: UpdateQuantityRequest):
    # attempt to update product quantity from an order
    try:
        product = Product.get(product_id)
        if product.quantity >= request.quantity:
            product.quantity -= request.quantity
            product.save()
            return {"message": "Quantity updated", "product": product}
        else:
            raise HTTPException(status_code=400, detail="Insufficient stock")
    except Product.DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
