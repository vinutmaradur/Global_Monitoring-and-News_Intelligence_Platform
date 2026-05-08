import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// ✅ Create custom icon (best reliable approach)
const customIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

function MapView({ data }) {
  return (
    <MapContainer
      center={[20, 77]}
      zoom={3}
      style={{ height: "500px", width: "100%" }}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* ✅ REAL DATA MARKERS */}
      {data.map((item, i) => (
        <Marker
          key={i}
          position={[Number(item.lat), Number(item.lon)]}
          icon={customIcon}
        >
          <Popup>
            <b>{item.city}</b> <br />
            🌡️ Temp: {item.temperature}°C
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default MapView;