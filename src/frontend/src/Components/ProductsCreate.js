import { useNavigate } from "react-router-dom";
import { Wrapper } from "./Wrapper";
import { useState } from "react";

// component to create a product throught the management panel
export const ProductsCreate = () => {
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [quantity, setQuantity] = useState("");
  const navigate = useNavigate();

  // submit function to send (name,price,quantity) to database
  const submit = async (e) => {
    // prevent page refresh
    e.preventDefault();

    // send POST call to backend
    await fetch("http://localhost:8000/products", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, price, quantity }),
    });

    // go to previous page
    await navigate(-1);
  };

  // return dynamic HTML component
  return (
    <Wrapper>
      <form className="mt-3" onSubmit={submit}>
        <div className="form-floating pb-3">
          <input
            className="form-control"
            placeholder="Name"
            onChange={(e) => setName(e.target.value)}
          />
          <label>Name</label>
        </div>

        <div className="form-floating pb-3">
          <input
            type="number"
            className="form-control"
            placeholder="Price"
            onChange={(e) => setPrice(e.target.value)}
          />
          <label>Price</label>
        </div>

        <div className="form-floating pb-3">
          <input
            type="number"
            className="form-control"
            placeholder="Quantity"
            onChange={(e) => setQuantity(e.target.value)}
          />
          <label>Quantity</label>
        </div>

        <button className="w-100 btn btn-lg btn-primary" type="submit">
          Submit
        </button>
      </form>
    </Wrapper>
  );
};
