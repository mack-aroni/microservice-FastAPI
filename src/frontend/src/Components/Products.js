import { useEffect, useState } from "react";
import { Wrapper } from "./Wrapper";
import { Link } from "react-router-dom";

/*
 * Products component that retrieves all products objects
 * in the backend and formats them in a tablized list
 */
export const Products = () => {
  const [products, setProducts] = useState([]);

  // asyncronous call to retrieve all products data
  useEffect(() => {
    (async () => {
      const response = await fetch("http://localhost:8000/products");
      const content = await response.json();
      setProducts(content);
    })();
  }, []);

  // delete logic to call product DELETE endpoint
  const del = async (id) => {
    if (window.confirm("Are You Sure To Delete?")) {
      await fetch(`http://localhost:8000/products/${id}`, { method: "DELETE" });
      setProducts(products.filter((p) => p.id !== id));
    }
  };

  // page refresh button logic
  const handleRefresh = () => {
    window.location.reload();
  };

  return (
    <Wrapper>
      <div className="pt-3 pb-2 mb-3 border-button">
        <Link to={`/create`} className="btn btn-sm btn-outline-secondary">
          Add
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
              <th scope="col">Name</th>
              <th scope="col">Price</th>
              <th scope="col">Quantity</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => {
              return (
                <tr key={product.id}>
                  <td>{product.id}</td>
                  <td>{product.name}</td>
                  <td>{parseFloat(product.price).toFixed(2)}</td>
                  <td>{product.quantity}</td>
                  <td>
                    <a
                      href="#"
                      className="btn btn-sm btn-outline-secondary"
                      onClick={(e) => del(product.id)}
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
