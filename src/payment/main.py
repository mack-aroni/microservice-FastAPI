import os
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

# redis_payment = get_redis_connection(
#     host=os.getenv("REDIS_PAY_HOST"),
#     port=int(os.getenv("REDIS_PORT", 0)),
#     password=os.getenv("REDIS_PASSWORD"),
#     decode_responses=True,
# )


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

    try:
        req = requests.get("http://localhost:8000/products/%s" % body["id"])
        product = req.json()

        # check if there is enough product quantity to make the purchase
        if int(body["quantity"]) <= product["quantity"]:
            order = Order(
                product_id=body["id"],
                price=product["price"],
                fee=FEE * product["price"] * float(body["quantity"]),
                total=(1 + FEE) * product["price"] * float(body["quantity"]),
                quantity=body["quantity"],
                status="pending",
            )
            order.save()

            # adds order as a background task to eventually be completed
            background_tasks.add_task(process_order, order)
        else:
            raise HTTPException(status_code=400, detail="Insufficient stock")
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Product not found")

    return order


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
        "id": order.pk,
        "pid": order.product_id,
        "price": order.price,
        "quantity": order.quantity,
        "fee": order.fee,
        "total": order.total,
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

    # call the Inventory API to attempt to update quantity
    inventory_service_url = "http://localhost:8000/update_quantity/%s" % (
        order.product_id
    )
    response = requests.put(inventory_service_url, json={"quantity": order.quantity})

    # successfully updated
    if response.status_code == 200:
        order.status = "completed"
        order.save()
        redis_payment.xadd("order_completed", order.dict(), "*")
    # error/unsuccesful update
    else:
        order.status = "refunded"
        order.save()
        redis_payment.xadd("order_refunded", order.dict(), "*")
