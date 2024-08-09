from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

redis = get_redis_connection(
    host="redis-18976.c325.us-east-1-4.ec2.redns.redis-cloud.com",
    port="18976",
    password="okJcZKA3idkxU9wpmETECt5oOd9ii8ml",
    decode_responses=True,
)


# storage class for redis database objects
class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


# endpoint that returns products
@app.get("/products")
def products():
    return [format(pk) for pk in Product.all_pks()]


# helper funciton to format the data of each product
def format(pk: str):
    product = Product.get(pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity,
    }


# endpoint that saves products
@app.post("/products")
def create(product: Product):
    return product.save()


# endpoint to return a specific product
@app.get("/products/{pk}")
def get(pk: str):
    return Product.get(pk)


# endpoint to delete a specific product
@app.delete("/products/{pk}")
def delete(pk: str):
    return Product.delete(pk)
