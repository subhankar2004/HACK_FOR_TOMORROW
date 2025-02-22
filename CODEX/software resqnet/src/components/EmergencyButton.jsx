import React, { useState } from "react";
import { db } from "../firebase-config";
import { ref as dbRef, push, set } from "firebase/database";

const EmergencyButton = () => {
  const handleEmergency = async () => {
    try {
    
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      const video = document.createElement("video");
      video.srcObject = stream;
      await new Promise((resolve) => (video.onloadedmetadata = resolve));
      video.play();

      
      await new Promise((resolve) => setTimeout(resolve, 3000));

      
      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      const imageData = canvas.toDataURL("image/png");

      stream.getTracks().forEach((track) => track.stop()); // Stop Camera

      
      navigator.geolocation.getCurrentPosition(async (position) => {
        const { latitude, longitude } = position.coords;

        const emergencyRef = dbRef(db, "emergencyAlerts");
        const newEmergencyRef = push(emergencyRef);
        await set(newEmergencyRef, {
          imageUrl: imageData, 
          location: { latitude, longitude },
          timestamp: new Date().toISOString(), 
        });

        alert("🚨 Emergency Alert Sent!");
      });
    } catch (error) {
      console.error("Emergency button error:", error);
      alert("Error capturing emergency data!");
    }
  };

  return (
    <button
      onClick={handleEmergency}
      style={{
        padding: "20px 35px",
        fontSize: "20px",
        backgroundColor: "red",
        color: "white",
        border: "none",
        borderRadius: "8px",
        cursor: "pointer",
        boxShadow: "0px 4px 10px rgba(0,0,0,0.2)",
        margin: "0px 0px 0px 15px",
      }}
    >
      Emergency
    </button>
  );
};

export default EmergencyButton;
