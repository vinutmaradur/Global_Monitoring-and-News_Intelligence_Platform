import React from "react";
import Globe from "./components/Globe"; // ✅ your Cesium component
import "./App.css";

function App() {
  return (
    <div className="App">

      {/* Globe */}
      <div className="globe-container">
        <Globe />   {/* ✅ Use this instead of <Viewer /> */}
      </div>

    </div>
  );
}

export default App;