import react, { useState } from "react";
import Navbar from "./components/navbar/navbar";
import './App.css'
import Selector from "./components/selector/selector";
import Payment from "./pages/payment/payment";
import Explorer from "./pages/explorer/explorer";
import axios from "axios";

function App() {

  const [selected, setSelected] = useState(0)
  // axios.defaults.baseURL = 'http://localhost:9000'
  return (
    <div className="App">
      <Navbar />
      <Selector setSelected={setSelected} />
      {selected == 0 ? <Payment /> : <Explorer />}
    </div>
  );
}

export default App;
