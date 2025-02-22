
import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import { db } from "../firebase-config";
import { ref, onValue } from "firebase/database";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";


ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const SensorGraph = ({ sensorType }) => {
  const [sensorValues, setSensorValues] = useState([]);
  const [timestamps, setTimestamps] = useState([]);

  useEffect(() => {
    if (!sensorType) return;

    const sensorRef = ref(db, "sensorData");
    onValue(sensorRef, (snapshot) => {
      if (snapshot.exists()) {
        const data = snapshot.val();

        
        const timeLabel = data.timestamp
          ? new Date(data.timestamp).toLocaleTimeString()
          : "N/A";

        setTimestamps((prev) => [...prev.slice(-9), timeLabel]);

        
        let newValue = 0;
        if (sensorType === "smoke") newValue = data.smokeLevel || 0;
        else if (sensorType === "flame") newValue = data.flameDetected ? 1 : 0;
        else if (sensorType === "vibration") newValue = data.vibration ? 1 : 0;

        setSensorValues((prev) => [...prev.slice(-9), newValue]);
      } else {
        console.warn("No data available from Firebase!");
      }
    });
  }, [sensorType]);

  if (!sensorType)
    return <p style={{ textAlign: "center" }}>🔍 Select a sensor to view its graph.</p>;

  return (
    <div style={graphContainerStyle}>
      <h2>{sensorType.charAt(0).toUpperCase() + sensorType.slice(1)} Sensor Graph</h2>
      <Line
        data={{
          labels: timestamps,
          datasets: [
            {
              label: `${sensorType.toUpperCase()} Sensor`,
              data: sensorValues,
              borderColor:
                sensorType === "smoke"
                  ? "red"
                  : sensorType === "flame"
                  ? "orange"
                  : "blue",
              borderWidth: 2,
              fill: false,
            },
          ],
        }}
      />
    </div>
  );
};

const graphContainerStyle = {
  marginTop: "20px",
  padding: "20px",
  border: "1px solid #ddd",
  borderRadius: "8px",
  backgroundColor: "#f9f9f9",
  textAlign: "center",
};

export default SensorGraph;
