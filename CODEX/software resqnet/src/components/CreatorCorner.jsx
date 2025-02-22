import React, { useState, useEffect } from "react";
import { db } from "../firebase-config";
import { ref, push, onValue } from "firebase/database";

const CreatorCorner = () => {
  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState("");

  useEffect(() => {
    const postsRef = ref(db, "creatorCorner");
    onValue(postsRef, (snapshot) => {
      if (snapshot.exists()) {
        setPosts(Object.values(snapshot.val()));
      }
    });
  }, []);

  const handlePost = () => {
    if (newPost.trim()) {
      push(ref(db, "creatorCorner"), {
        text: newPost,
        timestamp: Date.now(),
      });
      setNewPost("");
    }
  };

  return (
    <div>
      <h2>✍️ Creator Corner - Share Your Knowledge</h2>
      <textarea
        placeholder="Share a safety tip, experience, or knowledge..."
        value={newPost}
        onChange={(e) => setNewPost(e.target.value)}
        style={{ width: "100%", height: "80px" }}
      />
      <button onClick={handlePost}>Post</button>

      <h3>Community Contributions</h3>
      <ul>
        {posts.map((post, index) => (
          <li key={index}>{post.text} - {new Date(post.timestamp).toLocaleTimeString()}</li>
        ))}
      </ul>
    </div>
  );
};

export default CreatorCorner;
