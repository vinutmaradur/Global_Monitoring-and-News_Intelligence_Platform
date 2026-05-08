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
- Event markers plotted geographically
🌋 Earthquake Monitoring
- Live earthquake tracking
- Magnitude-based visualization
- Location-based filtering
- Time-based filtering
🌦️ Weather Monitoring
- City weather ingestion
- Weather API integration
- Temperature and condition visualization
📰 Global News Feed
- News aggregation from multiple APIs
- RSS feed integration
- Region/category-based news expansion
💰 Cryptocurrency Monitoring
- Live crypto market data
- Multi-coin tracking
- Future-ready analytics support
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

