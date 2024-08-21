from main import redis_payment, Order
import time

key = "order_completed"
group = "payment-group"

# make redis group
try:
    redis_payment.xgroup_create(key, group)
except:
    print("Group already exists")

# runloop
while True:
    try:
        results = redis_payment.xreadgroup(group, key, {key: ">"}, None)

        if results != []:
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj["pk"])
                order.status = "refunded"
                print(order)
                order.save()

    except Exception as e:
        print(str(e))
    time.sleep(1)
