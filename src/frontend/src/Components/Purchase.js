import { useEffect, useState } from "react";

/*
 * Purchase component thats send an order using the
 * frontend to be processed by the backend
 */
export const Purchase = () => {
  const [id, setId] = useState("");
  const [quantity, setQuantity] = useState("");
  const [message, setMessage] = useState("Buy your favorite product");

  // asyncronous call to retrieve price of selected product
  useEffect(() => {
    (async () => {
      // try-catch block to error check
      try {
        if (id) {
          const response = await fetch(`http://localhost:8000/products/${id}`);
          if (!response.ok) {
            throw new Error("Product not found");
          }
          const content = await response.json();
          const price = parseFloat(content.price).toFixed(2);
          setMessage(`Your product price is $${price}`);
        }
      } catch (e) {
        setMessage("Buy your favorite product");
      }
    })();
  }, [id]);

  // submit function to send a POST request to the orders backend
  const submit = async (e) => {
    e.preventDefault();
    // try-catch block to error check
    try {
      await fetch("http://localhost:8001/orders", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          id,
          quantity,
        }),
      });
      setMessage("Thank you for your order!");
    } catch (e) {
      setMessage("Invalid Product");
    }
  };

  // return dynamic html component
  return (
    <div className="container">
      <main>
        <div className="py-5 text-center">
          <h2>Checkout Form</h2>
          <p className="lead">{message}</p>
        </div>

        <form onSubmit={submit}>
          <div className="row g-3">
            <div className="col-sm-6">
              <label className="form-label">Product</label>
              <input
                className="form-control"
                onChange={(e) => setId(e.target.value)}
              />
            </div>

            <div className="col-sm-6">
              <label className="form-label">Quantity</label>
              <input
                type="number"
                className="form-control"
                onChange={(e) => setQuantity(e.target.value)}
              />
            </div>
          </div>
          <hr className="my-4" />
          <button className="w-100 btn btn-primary btn-lg" type="submit">
            Buy
          </button>
        </form>
      </main>
    </div>
  );
};
