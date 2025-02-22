
import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { db } from "../firebase-config";
import { ref, onValue } from "firebase/database";

const SensorMap = () => {
  const [sensorData, setSensorData] = useState([]);

  useEffect(() => {
    const sensorRef = ref(db, "sensorData"); 
    onValue(sensorRef, (snapshot) => {
      if (snapshot.exists()) {
        const data = snapshot.val();
        
        const sensorList = Object.keys(data).map((key) => ({
          id: key,
          ...data[key],
        }));
        setSensorData(sensorList);
      } else {
        setSensorData([]);
      }
    });
  }, []);

  return (
    <MapContainer
      center={[20.5937, 78.9629]}
      zoom={5}
      style={{ height: "500px", width: "100%" }}
    >
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {sensorData.map((sensor) => (
        <Marker
          key={sensor.id}
          position={[sensor.latitude, sensor.longitude]}
        >
          <Popup>
            <strong>Sensor ID:</strong> {sensor.id} <br />
            <strong>Flame:</strong>{" "}
            {sensor.flameDetected ? " Fire Detected!" : "✅ Normal"} <br />
            <strong>Smoke:</strong>{" "}
            {sensor.smokeLevel > 50 ? " High" : "✅ Safe"} <br />
            <strong>Vibration:</strong>{" "}
            {sensor.vibration ? " Detected!" : "✅ Stable"} <br />
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default SensorMap;
