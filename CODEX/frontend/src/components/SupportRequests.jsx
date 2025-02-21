import React, { useState, useEffect } from "react";
import { db } from "../firebase-config";
import { ref, push, onValue } from "firebase/database";

const SupportRequests = () => {
  const [requests, setRequests] = useState([]);
  const [newRequest, setNewRequest] = useState("");

  useEffect(() => {
    const requestsRef = ref(db, "supportRequests");
    onValue(requestsRef, (snapshot) => {
      if (snapshot.exists()) {
        setRequests(Object.values(snapshot.val()));
      }
    });
  }, []);

  const handleRequest = () => {
    if (newRequest.trim()) {
      push(ref(db, "supportRequests"), { text: newRequest, timestamp: Date.now() });
      setNewRequest("");
    }
  };

  return (
    <div>
      <h2> Emergency Support Requests</h2>
      <input
        type="text"
        placeholder="Need help with something?"
        value={newRequest}
        onChange={(e) => setNewRequest(e.target.value)}
      />
      <button onClick={handleRequest}>Request Help</button>

      <ul>
        {requests.map((req, index) => (
          <li key={index}>{req.text} -  {new Date(req.timestamp).toLocaleTimeString()}</li>
        ))}
      </ul>
    </div>
  );
};

export default SupportRequests;
