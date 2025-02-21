import React, { useState, useEffect } from "react";
import { db } from "../firebase-config";
import { ref, onValue } from "firebase/database";

const LogsPage = () => {
  const [emergencies, setEmergencies] = useState([]);

  useEffect(() => {
    const emergencyRef = ref(db, "emergencyAlerts");

    onValue(emergencyRef, (snapshot) => {
      if (snapshot.exists()) {
        const data = snapshot.val();
        const emergencyList = Object.values(data).reverse(); // Show latest first
        setEmergencies(emergencyList);
      } else {
        setEmergencies([]);
      }
    });
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2> Emergency Logs</h2>
      {emergencies.length === 0 ? (
        <p>No emergency alerts yet.</p>
      ) : (
        emergencies.map((emergency, index) => (
          <div key={index} style={{ marginBottom: "20px", border: "1px solid #ddd", padding: "10px", borderRadius: "8px" }}>
            <img src={emergency.imageUrl} alt="Emergency" style={{ width: "100%", maxWidth: "300px", borderRadius: "8px" }} />
            <p><strong> Location:</strong> {emergency.location.latitude}, {emergency.location.longitude}</p>
            <p><strong> Timestamp:</strong> {new Date(emergency.timestamp).toLocaleString()}</p>
          </div>
        ))
      )}
    </div>
  );
};

export default LogsPage;
