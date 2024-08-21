from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests, time


# static fee variable
FEE = 0.2

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_payment = get_redis_connection(
    host="redis-18976.c325.us-east-1-4.ec2.redns.redis-cloud.com",
    port="18976",
    password="okJcZKA3idkxU9wpmETECt5oOd9ii8ml",
    decode_responses=True,
)


# storage class for redis Order objects
class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending/completed/refunded

    class Meta:
        database = redis_payment


# CREATE endpoint
@app.post("/orders")
async def create(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

    req = requests.get("http://localhost:8000/products/%s" % body["id"])
    product = req.json()

    order = Order(
        product_id=body["id"],
        price=product["price"],
        fee=FEE * product["price"],
        total=(1 + FEE) * product["price"],
        quantity=body["quantity"],
        status="pending",
    )
    order.save()

    # adds order as a background task to eventually be completed
    background_tasks.add_task(order_completed, order)

    return order


# RETURN endpoint
@app.get("/orders/{pk}")
def get(pk: str):
    return Order.get(pk)


# RETURN ALL endpoint
@app.get("/orders/all")
def get_all():
    return [format(pk) for pk in Order.all_pks()]


# helper function to format the data of each order
def format(pk: str):
    order = Order.get(pk)
    return {
        "id": order.product_id,
        "price": order.price,
        "fee": order.fee,
        "total": order.total,
        "quantity": order.quantity,
        "status": order.status,
    }


# DELETE endpoint
@app.delete("/orders/{pk}")
def delete(pk: str):
    return Order.delete(pk)


# DELETE ALL endpoint
@app.delete("/orders")
def delete_all():
    return [Order.delete(pk) for pk in Order.all_pks()]


# helper function to set an order status to completed
def order_completed(order: Order):
    time.sleep(5)  # temporary
    order.status = "completed"
    order.save()
    redis_payment.xadd("order_completed", order.dict(), "*")
