import { useEffect, useState } from "react";
import API from "../services/api";
import MapView from "../components/Mapview";

function Home() {
  const [weather, setWeather] = useState([]);

  useEffect(() => {
    API.get("/weather")
      .then(res => {
        console.log(res.data);
        setWeather(res.data);
      })
      .catch(err => console.log(err));
  }, []);

  return (
    <div>
      <h2>🌍 World Map</h2>
      <MapView data={weather} />
    </div>
  );
}

export default Home;