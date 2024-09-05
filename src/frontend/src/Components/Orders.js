import { useEffect, useState } from "react";
import { Wrapper } from "./Wrapper";
import { Link } from "react-router-dom";

/*
 * Orders component that retrieves all orders objects
 * in the backend and formats them in a tablized list
 */
export const Orders = () => {
  const [orders, setOrders] = useState([]);

  // asyncronous call to retrieve all objects data
  useEffect(() => {
    (async () => {
      const response = await fetch("http://localhost:8001/orders");
      const content = await response.json();
      setOrders(content);
    })();
  }, []);

  // delete logic to call order DELETE endpoint
  const del = async (id) => {
    if (window.confirm("Are You Sure To Delete?")) {
      await fetch(`http://localhost:8001/orders/${id}`, { method: "DELETE" });
      setOrders(orders.filter((p) => p.id !== id));
    }
  };

  // page refresh button logic
  const handleRefresh = () => {
    window.location.reload();
  };

  return (
    <Wrapper>
      <div className="pt-3 pb-2 mb-3 border-button">
        <Link to={`/order`} className="btn btn-sm btn-outline-secondary">
          Order
        </Link>
        <button
          onClick={handleRefresh}
          className="btn btn-sm btn-outline-secondary"
        >
          Refresh
        </button>
      </div>

      <div className="table-responsive">
        <table className="table table-striped table-sm">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">PID</th>
              <th scope="col">Price</th>
              <th scope="col">Quantity</th>
              <th scope="col">Fee</th>
              <th scope="col">Total</th>
              <th scope="col">Status</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            {orders.map((order) => {
              return (
                <tr key={order.id}>
                  <td>{order.id}</td>
                  <td>{order.pid}</td>
                  <td>{parseFloat(order.price).toFixed(2)}</td>
                  <td>{order.quantity}</td>
                  <td>{parseFloat(order.fee).toFixed(2)}</td>
                  <td>{parseFloat(order.total).toFixed(2)}</td>
                  <td>{order.status}</td>
                  <td>
                    <a
                      href="#"
                      className="btn btn-sm btn-outline-secondary"
                      onClick={(e) => del(order.id)}
                    >
                      Delete
                    </a>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </Wrapper>
  );
};
