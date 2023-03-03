import React from "react";
import "./App.css";
import Header from "./components/Header/Header";
import StorePage from "./components/StorePage/StorePage.jsx";


function App() {
  return (
    <React.Fragment>
      <Header></Header>
      <StorePage></StorePage>
    </React.Fragment>
  );
}


export default App;
