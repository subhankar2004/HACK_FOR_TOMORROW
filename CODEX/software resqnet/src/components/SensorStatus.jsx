// src/components/SensorStatus.jsx
import React, { useEffect, useState } from "react";
import { db } from "../firebase-config";
import { ref, onValue } from "firebase/database";

const SMOKE_THRESHOLD = 5; // Set your own smoke threshold

const SensorStatus = () => {
  const [sensorData, setSensorData] = useState({
    flameDetected: false,
    vibration: false,
    smokeLevel: 0,
  });

  useEffect(() => {
    const sensorRef = ref(db, "sensorData");

    onValue(sensorRef, (snapshot) => {
      if (snapshot.exists()) {
        const data = snapshot.val();
        setSensorData({
          flameDetected: data.flameDetected || false,
          vibration: data.vibration || false,
          smokeLevel: data.smokeLevel || 0,
        });
      } else {
        console.warn("No sensor data available from Firebase!");
      }
    });
  }, []);

  return (
    <div style={containerStyle}>
      <h2>📊 Sensor Status</h2>

      <div style={statusItemStyle(sensorData.flameDetected ? "alert" : "normal")}>
        🔥 Flame Status:{" "}
        {sensorData.flameDetected ? <b style={{ color: "red" }}>ALERT</b> : <b>Normal</b>}
      </div>

      <div style={statusItemStyle(sensorData.vibration ? "alert" : "normal")}>
        ⚠️ Vibration Status:{" "}
        {sensorData.vibration ? <b style={{ color: "red" }}>ALERT</b> : <b>Normal</b>}
      </div>

      <div
        style={statusItemStyle(sensorData.smokeLevel > SMOKE_THRESHOLD ? "alert" : "normal")}
      >
        🌫️ Smoke Level: <b>{sensorData.smokeLevel}</b> →{" "}
        {sensorData.smokeLevel > SMOKE_THRESHOLD ? (
          <b style={{ color: "red" }}>DANGER</b>
        ) : (
          <b>Safe</b>
        )}
      </div>
    </div>
  );
};

const containerStyle = {
  marginTop: "20px",
  padding: "20px",
  border: "1px solid #ddd",
  borderRadius: "8px",
  backgroundColor: "#f9f9f9",
  textAlign: "center",
};

const statusItemStyle = (status) => ({
  padding: "10px",
  margin: "10px 0",
  borderRadius: "5px",
  fontWeight: "bold",
  backgroundColor: status === "alert" ? "#ffcccc" : "#ccffcc",
});

export default SensorStatus;
