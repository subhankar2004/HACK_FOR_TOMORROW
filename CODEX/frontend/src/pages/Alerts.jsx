import React, { useState, useEffect } from "react";
import SensorGraph from "../components/SensorGraph";
import EmergencyButton from "../components/EmergencyButton"; // ✅ Added
import { getDatabase, ref, onValue } from "firebase/database";

const Alerts = () => {
  const [selectedSensor, setSelectedSensor] = useState("smoke");
  const [sensorStatus, setSensorStatus] = useState({
    smoke: "Loading...",
    flame: "Loading...",
    vibration: "Loading...",
  });

  useEffect(() => {
    const db = getDatabase();
    const sensorRef = ref(db, "sensorNodes");

    onValue(sensorRef, (snapshot) => {
      if (snapshot.exists()) {
        const data = snapshot.val();

        setSensorStatus({
          smoke: data.smokeLevel > 50 ? "High Smoke" : "✅ Normal",
          flame: data.flameDetected ? "Fire Detected!" : "✅ Normal",
          vibration: data.vibration ? "Vibration Alert!" : "✅ Normal",
        });
      } else {
        setSensorStatus({
          smoke: "No Data",
          flame: "No Data",
          vibration: "No Data",
        });
      }
    });
  }, []);

  return (
    <div className="p-4">
      
      <div className="mt-4 grid grid-cols-3 gap-4">
        {["flame", "smoke", "vibration"].map((sensor) => (
          <div
            key={sensor}
            className={`p-4 rounded-lg shadow-lg text-white ${
              sensorStatus[sensor].includes("Normal")
                ? "bg-green-500"
                : "bg-red-500"
            }`}
          >
            <h3 className="font-semibold capitalize">{sensor} Sensor</h3>
            <p>{sensorStatus[sensor]}</p>
          </div>
        ))}
      </div>

      
      <div className="mt-6">
        <label className="mr-2 font-medium">Select Sensor:</label>
        <select
          onChange={(e) => setSelectedSensor(e.target.value)}
          value={selectedSensor}
          className="border p-2 rounded-md"
        >
          <option value="smoke">Smoke</option>
          <option value="flame">Flame</option>
          <option value="vibration">Vibration</option>
        </select>
      </div>

      
      <div className="mt-6 p-4 bg-white rounded-lg shadow-lg">
        <SensorGraph sensorType={selectedSensor} />
      </div>
    </div>
  );
};

export default Alerts;
