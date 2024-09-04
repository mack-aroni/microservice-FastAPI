import { Products } from "./Components/Products";
import { Orders } from "./Components/Orders";
import { Purchase } from "./Components/Purchase";
import { ProductsCreate } from "./Components/ProductsCreate";
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Products />} />
        <Route path="/orders" element={<Orders />} />
        <Route path="/create" element={<ProductsCreate />} />
        <Route path="/order" element={<Purchase />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
