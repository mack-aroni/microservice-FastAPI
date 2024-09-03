from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel, NotFoundError
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

# redis-db2
redis_payment = get_redis_connection(
    host="redis-13809.c246.us-east-1-4.ec2.redns.redis-cloud.com",
    port="13809",
    password="HbpjwqZHJ7MbcjJtAiqciajv0kWmhF4A",
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
    background_tasks.add_task(process_order, order)

    return order


""" @app.post("/orders")
async def create_order(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()

    # call the Inventory API to update quantity
    inventory_service_url = "http://localhost:8000/update_quantity/%s" % body["id"]
    response = requests.post(inventory_service_url, json={"quantity": body["quantity"]})

    if response.status_code == 200:
        # successfully created order
        product_data = response.json()["product"]
        order = Order(
            product_id=body["id"],
            price=product_data["price"],
            fee=product_data["price"] * FEE,
            total=product_data["price"] * (1 + FEE),
            quantity=body["quantity"],
            status="pending",
        )
        order.save()

        # adds order as a background task to eventually be completed
        background_tasks.add_task(order_completed, order)
        return order
    else:
        # insufficient stock or other errors
        raise HTTPException(
            status_code=response.status_code, detail=response.json()["detail"]
        ) """


# RETURN endpoint
@app.get("/orders/{pk}")
def get(pk: str):
    try:
        return Order.get(pk)
    except NotFoundError as e:
        return {"error": str(e)}


# RETURN ALL endpoint
@app.get("/orders")
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
def process_order(order: Order):
    time.sleep(5)  # temporary
    order.status = "completed"
    order.save()
    redis_payment.xadd("order_completed", order.dict(), "*")
