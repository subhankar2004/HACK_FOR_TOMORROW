import React, { useEffect, useState } from "react";
import { db } from "../firebase-config";
import { ref, onValue } from "firebase/database";

const Leaderboard = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    const leaderboardRef = ref(db, "communityLeaderboard");
    onValue(leaderboardRef, (snapshot) => {
      if (snapshot.exists()) {
        setUsers(Object.values(snapshot.val()));
      }
    });
  }, []);

  return (
    <div>
      <h2> Top Responders</h2>
      <ul>
        {users.map((user, index) => (
          <li key={index}>{user.name} - {user.points} points</li>
        ))}
      </ul>
    </div>
  );
};

export default Leaderboard;
