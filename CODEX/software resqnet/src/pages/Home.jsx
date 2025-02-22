import React, { useState, useEffect } from "react";
import EmergencyButton from "../components/EmergencyButton"; 


const Home = () => {
  return (
    <div className="p-4">
      

      <h2 className="text-2xl font-bold mt-4"> ResQNet - Home</h2>

      <EmergencyButton />
      
      
    </div>
  );
};

export default Home;
