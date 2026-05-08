# Global Monitoring and News Intelligence Platform

# Project Overview
World Monitor collects and processes live global datasets from multiple APIs and displays them on an interactive globe interface.

The platform is designed for:

🌎 Global event tracking </br>
📡 Real-time data visualization </br>
🛰️ Geospatial intelligence </br>
📈 Monitoring worldwide activities </br>
📰 News and disaster awareness </br>
📊 Data engineering + visualization learning </br>

---

# Features 🎯
🌍 Interactive 3D Globe
- Real-time Earth visualization
- Smooth navigation and zooming
- Event markers plotted geographically </br>
🌋 Earthquake Monitoring
- Live earthquake tracking
- Magnitude-based visualization
- Location-based filtering
- Time-based filtering </br>
🌦️ Weather Monitoring
- City weather ingestion
- Weather API integration
- Temperature and condition visualization </br>
📰 Global News Feed
- News aggregation from multiple APIs
- RSS feed integration
- Region/category-based news expansion </br>
💰 Cryptocurrency Monitoring
- Live crypto market data
- Multi-coin tracking
- Future-ready analytics support </br>
🔄 Data Pipelines
- Automated ingestion scripts
= JSON transformation
- Data merging workflows
- Database loading utilities 

---

# Screenshot 📸
![img_alt](https://github.com/vinutmaradur/Global_Monitoring-and-News_Intelligence_Platform/blob/main/screenshot2.png?raw=true)
![img_alt](https://github.com/vinutmaradur/Global_Monitoring-and-News_Intelligence_Platform/blob/main/screenshot1.png?raw=true)
![img_alt](https://github.com/vinutmaradur/Global_Monitoring-and-News_Intelligence_Platform/blob/main/screenshot3.png?raw=true)

---

# Tech Stack 🏗️
1. Frontend
- React
- Vite
- CesiumJS
- Axios
- JavaScript
2. Backend
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite / PostgreSQL (extendable)
3. Data Pipeline
- Python
- Requests
- JSON Processing
- Scheduled ingestion scripts

---

# Project Structure 📂
```bash
WORLD-MONITOR
│
├── Backend
│   ├── routers
│   │   ├── countries.py
│   │   ├── earthquake.py
│   │   ├── news.py
│   │   └── weather.py
│   │
│   ├── utils
│   │   └── time_filter.py
│   │
│   ├── crud.py
│   ├── database.py
│   ├── init_db.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── seed_data.py
│
├── Data_Pipeline
│   ├── crypto
│   ├── Earthquake
│   ├── news
│   ├── weather
│   ├── merge_data.py
│   └── config.py
│
├── Frontend
│   ├── src
│   │   ├── components
│   │   ├── pages
│   │   ├── services
│   │   └── assets
│   └── package.json
│
└── data/raw
  ```

---

# How to run 🚀

1. Clone Repository :
```bash 
git clone <your-repo-url>
cd WORLD-MONITOR
```

# 1. Backend Setup
Create Virtual Environment
```bash
python -m venv venv
```
Activate Environment
Windows
```bash
venv\Scripts\activate
```
Linux/Mac
```bash
source venv/bin/activate
```
Install Dependencies
```bash
pip install -r requirements.txt
```
Run Backend
```bash
uvicorn Backend.main:app --reload
```
Backend runs at:
```bash
http://127.0.0.1:8000
```
Swagger Docs:
```bash
http://127.0.0.1:8000/docs
```
# 2. Frontend Setup
```bash
cd Frontend
npm install
npm run dev
```
Frontend runs at:
```bash
http://localhost:5173
```
# 3. Cesium Setup

Create a free Cesium Ion account:

Cesium Ion

Add your token:
```bash
Cesium.Ion.defaultAccessToken = "YOUR_TOKEN";
```
API Endpoints
Earthquakes
```bash
GET /earthquakes
```
Example:
```bash
/earthquakes?place=Alaska
```
Weather
```bash
GET /weather
```
News
```bash
GET /news
```
Countries
```bash
GET /countries
```

---

# Data Sources 📊

Possible APIs used:

- USGS Earthquake API
- NewsAPI
- GDELT Project
- OpenWeatherMap
- CoinGecko API

---

# Excellent Real-Time Data Engineering Practice
The project demonstrates:

- ETL workflows
- API ingestion
- Data normalization
- Geospatial visualization
- Multi-source integration

These are valuable skills for:

- Data Engineering
- Backend Engineering
- GIS Systems
- AI Platforms
- Intelligence Systems

---

Strong Portfolio Project

This project stands out because it combines:

- Frontend
- Backend
- Data pipelines
- Maps
- Real-time systems
- Visualization

Most portfolio projects only cover CRUD apps.

---

# Practical Use Cases 🌍
🚨 Disaster Monitoring

- Track earthquakes and severe weather events globally.

🛰️ Geospatial Intelligence Platform

- Visualize worldwide activity geographically.

📰 Media Intelligence Dashboard

- Monitor news trends by region.

📈 Financial + Crypto Monitoring

- Track global crypto fluctuations alongside world events.

🧠 AI/ML Research Platform

- Can be extended into:

    - Event prediction
    - Sentiment analysis
    - Anomaly detection
    - Risk analysis
      
🏛️ Government / NGO Monitoring

- Useful for:

    - Emergency response
    - Crisis management
    - Climate tracking

---

# Contributing 🤝
Contributions are welcome.
```bash
Fork → Clone → Create Branch → Commit → Push → Pull Request
```

---

# License 📄
This project is licensed under the MIT License. See the LICENSE file for details.

---

# Happy coding! 💻

Let me know if you’d like to customize any sections further!

---

**👨‍💻 Author** </br>
Vinut Maradur </br>
MCA (Data Science) Graduate | Data Analyst | Data Science Enthusiast </br>
Global Monitoring and News Intelligence platform
