import { useEffect, useRef, useState } from "react";
import * as Cesium from "cesium";
import "cesium/Build/Cesium/Widgets/widgets.css";

function Globe() {
  const viewerRef = useRef(null);
  const cesiumViewer = useRef(null);

  const [earthquakes, setEarthquakes] = useState([]);
  const [rssNews, setRssNews] = useState([]);
  const [weatherData, setWeatherData] = useState([]);
  const [timeRange, setTimeRange] = useState("24");
  const [loading, setLoading] = useState(false);

  const initialView = Cesium.Cartesian3.fromDegrees(
    78.9629,
    20.5937,
    20000000
  );

  // ✅ BUTTON FUNCTION
  const handleResetView = () => {
    const viewer = cesiumViewer.current;
    if (!viewer) return;

    viewer.camera.flyTo({
      destination: initialView,
      orientation: {
        pitch: -Math.PI / 3,
      },
      duration: 1.5,
    });
  };

  // =========================
  // 1. INIT VIEWER
  // =========================
  useEffect(() => {
    const viewer = new Cesium.Viewer(viewerRef.current, {
      animation: false,
      timeline: false,
      infoBox: true,
      selectionIndicator: true,
      maximumRenderTimeChange: Infinity,
    });

    cesiumViewer.current = viewer;

    // Terrain
    Cesium.createWorldTerrainAsync().then((terrain) => {
      if (!viewer.isDestroyed()) {
        viewer.terrainProvider = terrain;
      }
    });

    // ✅ Initial top view
    viewer.camera.setView({
      destination: initialView,
      orientation: {
        heading: 0.0,
        pitch: -Math.PI / 3,
        roll: 0.0,
      },
    });

    // 🌍 SMOOTH AUTO ROTATION
    // =========================
    let isUserHolding = false;
    let isCameraMoving = false;
    let isUserInteracting = false;
    let resumeTimeout = null;
    let lastTime = performance.now();
    let rotationVelocity = 0.03;
    let targetVelocity = 0.03;

    viewer.clock.shouldAnimate = true;
    viewer.scene.requestRenderMode = false;

    viewer.scene.preRender.addEventListener(() => {
    const now = performance.now();
    let delta = (now - lastTime) / 1000;
    lastTime = now;

    delta = Math.min(delta, 0.05);

    // ONLY depend on user input
    if (isUserInteracting || isCameraMoving) {
      targetVelocity = 0;
    } else {
      targetVelocity = 0.03;
    }

    // smooth easing
    rotationVelocity += (targetVelocity - rotationVelocity) * 0.03;

    viewer.scene.camera.rotateRight(rotationVelocity * delta);
  });

  const stopAndResumeRotation = () => {
  isUserInteracting = true;

  if (resumeTimeout) clearTimeout(resumeTimeout);

  // ⏳ Resume after 3 seconds of no interaction
  resumeTimeout = setTimeout(() => {
    isUserInteracting = false;
  }, 3000);
  };

    // 🖱️ INTERACTION DETECTION
    // =========================
    const handler = viewer.screenSpaceEventHandler;

    // Mouse drag
    handler.setInputAction(stopAndResumeRotation, Cesium.ScreenSpaceEventType.LEFT_DOWN);
    handler.setInputAction(stopAndResumeRotation, Cesium.ScreenSpaceEventType.LEFT_UP);

    // Touch pinch
    handler.setInputAction(stopAndResumeRotation, Cesium.ScreenSpaceEventType.PINCH_START);
    handler.setInputAction(stopAndResumeRotation, Cesium.ScreenSpaceEventType.PINCH_END);

    // 🔥 MOST IMPORTANT → ZOOM
    handler.setInputAction(stopAndResumeRotation, Cesium.ScreenSpaceEventType.WHEEL);

    // 🎥 CAMERA MOVEMENT
    // =========================
    viewer.camera.moveStart.addEventListener(stopAndResumeRotation);
    viewer.camera.moveEnd.addEventListener(stopAndResumeRotation);

    // 🔥 CAMERA CONTROL FIX
    const controller = viewer.scene.screenSpaceCameraController;
    controller.enableTilt = false;              // ❌ disable tilt
    controller.enableLook = false;              // ❌ disable free look
    controller.maximumZoomDistance = 30000000;  // limit zoom out

    // 🔥 Reset view on double click
    viewer.screenSpaceEventHandler.setInputAction(() => {
      viewer.camera.flyTo({
        destination: initialView,
        orientation: {
          pitch: -Math.PI / 3,
        },
        duration: 1.5,
      });
    }, Cesium.ScreenSpaceEventType.LEFT_DOUBLE_CLICK);

    return () => {
      if (!viewer.isDestroyed()) viewer.destroy();
    };
  }, [timeRange]);

  // =========================
  // 2. FETCH DATA
  // =========================
  useEffect(() => {
    setLoading(true);
    fetch(`http://127.0.0.1:8000/earthquakes?last_hour=${timeRange}`)
      .then((res) => res.json())
      .then((data) => {
        setEarthquakes(data);
        setLoading(false);
      })
      .catch(console.error);

    fetch(`http://127.0.0.1:8000/rss?last_hour=${timeRange}`)
      .then((res) => res.json())
      .then((data) => {
        setRssNews(data);
        setLoading(false);
      })
      .catch(console.error);

    fetch(`http://127.0.0.1:8000/weather`)
      .then((res) => res.json())
      .then((data) => {
        setWeatherData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [timeRange]);

  // =========================
  // 3. RENDER DATA
  // =========================
  useEffect(() => {
    const viewer = cesiumViewer.current;
    if (!viewer) return;

    viewer.dataSources.removeAll();

    const dataSource = new Cesium.CustomDataSource("filtered-events");
    viewer.dataSources.add(dataSource);

    const entities = dataSource.entities;

    const jitter = (lon, lat) => {
      const offset = (Math.random() - 0.5) * 0.05;
      return Cesium.Cartesian3.fromDegrees(lon + offset, lat + offset);
    };

    // Earthquakes
    earthquakes.forEach((eq) => {
      const lat = parseFloat(eq.lat ?? eq.latitude);
      const lon = parseFloat(eq.lon ?? eq.lng ?? eq.longitude);
      if (isNaN(lat) || isNaN(lon)) return;

      const magRaw = parseFloat(eq.magnitude);
      const mag = isNaN(magRaw) ? 3 : magRaw;

      entities.add({
        name: eq.place || "Earthquake",
        position: jitter(lon, lat),
        point: {
          pixelSize: Math.max(mag * 3, 8),
          color: mag > 5 ? Cesium.Color.RED : Cesium.Color.ORANGE,
        },
        description: `
          <h3><b>Event Name:</b> ${eq.place || "Unknown"}</h3>
          <p><b>Magnitude:</b> ${isNaN(magRaw) ? "N/A" : magRaw.toFixed(1)}</p>
          <p><b>Latitude:</b> ${lat.toFixed(4)}</p>
          <p><b>Longitude:</b> ${lon.toFixed(4)}</p>
          <p><b>Time:</b> ${eq.time || "N/A"}</p>
        `,
      });
    });

    // RSS News
    rssNews.forEach((n) => {
      const lat = parseFloat(n.latitude);
      const lon = parseFloat(n.longitude);
      if (isNaN(lat) || isNaN(lon)) return;

      entities.add({
        name: n.title || "RSS News",
        position: jitter(lon, lat),
        billboard: {
          image: "https://cdn-icons-png.flaticon.com/512/684/684908.png",
          width: 28,
          height: 28,
        },
        description: `
          <h3><b>News:</b> ${n.title || "No title"}</h3>
          <p><b>Location:</b> ${n.place || "Unknown"}</p>
          <p><b>Latitude:</b> ${lat.toFixed(4)}</p>
          <p><b>Longitude:</b> ${lon.toFixed(4)}</p>
          <p><b>Published:</b> ${n.published_at || "N/A"}</p>
          <a href="${n.url}" target="_blank">Read full article</a>
        `,
      });
    });

    // =========================
    // WEATHER
    // =========================
    weatherData.forEach((w) => {
      const lat = parseFloat(w.lat);
      const lon = parseFloat(w.lon);

      if (isNaN(lat) || isNaN(lon)) return;

      let weatherIcon =
        "https://cdn-icons-png.flaticon.com/512/869/869869.png";

      const desc = (w.description || "").toLowerCase();

      if (desc.includes("cloud")) {
        weatherIcon =
          "https://cdn-icons-png.flaticon.com/512/414/414825.png";
      }

      if (desc.includes("rain")) {
        weatherIcon =
          "https://cdn-icons-png.flaticon.com/512/3351/3351979.png";
      }

      if (desc.includes("storm")) {
        weatherIcon =
          "https://cdn-icons-png.flaticon.com/512/1146/1146869.png";
      }

      if (desc.includes("clear")) {
        weatherIcon =
          "https://cdn-icons-png.flaticon.com/512/869/869869.png";
      }

      entities.add({
        name: w.city || "Weather",

        position: Cesium.Cartesian3.fromDegrees(lon, lat),

        billboard: {
          image: weatherIcon,

          width: 34,
          height: 34,

          verticalOrigin:
            Cesium.VerticalOrigin.BOTTOM,
        },

        description: `
          <h3>${w.city}</h3>

          <p><b>Temperature:</b> ${w.temperature}°C</p>

          <p><b>Humidity:</b> ${w.humidity}%</p>

          <p><b>Weather:</b> ${w.description}</p>

          <p><b>Country:</b> ${w.country || "N/A"}</p>
        `,
      });
    });

    // Clustering
    dataSource.clustering.enabled = true;
    dataSource.clustering.pixelRange = 25;
    dataSource.clustering.minimumClusterSize = 3;

    // 🚀 attach cluster event ONLY ONCE globally
    if (!viewer._clusterEventAdded) {
      viewer._clusterEventAdded = true;

      dataSource.clustering.clusterEvent.addEventListener(
        (clusteredEntities, cluster) => {
          cluster.label.show = true;
          cluster.billboard.show = true;
          cluster.point.show = false;

          cluster.label.text = clusteredEntities.length.toString();

          let color = Cesium.Color.GREEN;
          if (clusteredEntities.length > 20) color = Cesium.Color.ORANGE;
          if (clusteredEntities.length > 50) color = Cesium.Color.RED;

          cluster.billboard.image = createClusterCanvas(
            clusteredEntities.length,
            color
          );
        }
      );
    }

    viewer.zoomTo(dataSource);
    let lastEntity = null;

    viewer.screenSpaceEventHandler.setInputAction((movement) => {
      const picked = viewer.scene.pick(movement.endPosition);

      if (picked && picked.id) {
        if (lastEntity !== picked.id) {
          viewer.selectedEntity = picked.id;
          lastEntity = picked.id;
        }
      } else {
        viewer.selectedEntity = undefined;
        lastEntity = null;
      }
    }, Cesium.ScreenSpaceEventType.MOUSE_MOVE);
  }, [earthquakes, rssNews, weatherData]);

  // UI
  // =========================
  return (
    <div style={{ position: "relative", width: "100%", height: "100vh" }}>
      
      {/* 🌍 Globe */}
      <div ref={viewerRef} style={{ width: "100%", height: "100%" }} />
      {/* 🎛️ FILTER PANEL */}
      <div style={panelStyle}>
        {["24", "168", "720"].map((range) => (
          <button
            key={range}
            onClick={() => setTimeRange(range)}
            style={{
              ...btnStyle,
              background: timeRange === range ? "#ff4757" : "#1e90ff",
            }}
          >
            {range === "24" && "Last 24 Hours"}
            {range === "168" && "Last 7 Days"}
            {range === "720" && "Last Month"}
          </button>
        ))}
      </div>

      {/* ⏳ Loading */}
      {loading && <div style={loadingStyle}>Loading...</div>}

      {/* 📊 Count */}
      <div style={countStyle}>
      🌍 {earthquakes.length} EQ | 📰 {rssNews.length} RSS | 🌦️ {weatherData.length} Weather
      <br />
      <b>Total: {earthquakes.length + rssNews.length + weatherData.length}</b>
      </div>
    </div>
  );
}

// STYLES
// =========================
const panelStyle = {
  position: "absolute",
  top: "20px",
  left: "20px",
  display: "flex",
  flexDirection: "column",
  gap: "10px",
  zIndex: 1000,
};

const btnStyle = {
  padding: "10px",
  border: "none",
  color: "white",
  borderRadius: "6px",
  cursor: "pointer",
  fontWeight: "bold",
};

const loadingStyle = {
  position: "absolute",
  top: "20px",
  right: "20px",
  background: "black",
  color: "white",
  padding: "8px 12px",
  borderRadius: "6px",
};

const countStyle = {
  position: "absolute",
  bottom: "20px",
  left: "20px",
  background: "black",
  color: "white",
  padding: "8px 12px",
  borderRadius: "6px",
};

// Cluster icon
function createClusterCanvas(count, color) {
  const canvas = document.createElement("canvas");
  canvas.width = 40;
  canvas.height = 40;

  const ctx = canvas.getContext("2d");

  ctx.beginPath();
  ctx.arc(20, 20, 18, 0, 2 * Math.PI);
  ctx.fillStyle = color.toCssColorString();
  ctx.fill();

  ctx.fillStyle = "white";
  ctx.font = "bold 16px Arial";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(count, 20, 20);

  return canvas;
}

export default Globe;