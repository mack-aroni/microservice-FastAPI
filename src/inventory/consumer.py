from main import redis_inventory, Product
import time

key = "order_completed"
group = "inventory-group"

# make redis group
try:
    redis_inventory.xgroup_create(key, group)
except:
    print("Group already exists")

# runloop
while True:
    try:
        results = redis_inventory.xreadgroup(group, key, {key: ">"}, None)

        if results != []:
            for result in results:
                obj = result[1][0][1]

                # check if product exists, else refund
                try:
                    product = Product.get(obj["product_id"])
                    product.quantity = product.quantity - int(obj["quantity"])
                    print(product)
                    product.save()
                except:
                    redis_inventory.xadd("refund_order", obj, "*")

    except Exception as e:
        print(str(e))
    time.sleep(1)
