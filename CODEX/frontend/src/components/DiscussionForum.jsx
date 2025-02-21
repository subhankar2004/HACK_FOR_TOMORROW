import React, { useState, useEffect } from "react";
import { db } from "../firebase-config";
import { ref, push, onValue } from "firebase/database";

const DiscussionForum = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");

  useEffect(() => {
    const forumRef = ref(db, "communityForum");
    onValue(forumRef, (snapshot) => {
      if (snapshot.exists()) {
        setMessages(Object.values(snapshot.val()));
      }
    });
  }, []);

  const handlePost = () => {
    if (newMessage.trim()) {
      push(ref(db, "communityForum"), {
        text: newMessage,
        timestamp: Date.now(),
      });
      setNewMessage("");
    }
  };

  return (
    <div>
      <h2>💬 Live Discussion Forum</h2>
      <input
        type="text"
        placeholder="Write your message..."
        value={newMessage}
        onChange={(e) => setNewMessage(e.target.value)}
      />
      <button onClick={handlePost}>Post</button>

      <ul>
        {messages.map((msg, index) => (
          <li key={index}>{msg.text} -  {new Date(msg.timestamp).toLocaleTimeString()}</li>
        ))}
      </ul>
    </div>
  );
};

export default DiscussionForum;
