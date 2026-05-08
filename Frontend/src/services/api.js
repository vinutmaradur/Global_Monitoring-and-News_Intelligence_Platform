import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000"
});

// 🔹 Earthquake API
export const getEarthquakes = () => API.get("/earthquakes");
export const getNews = () => API.get("/news");

export default API;