import React from "react";
import "./Home.css";
import danceImage from "../assets/UI3-removebg-preview.png"; // Importing the image

const Home = () => {
  return (
    <div className="home-container">
      <div className="text-container">
        <p className="title">Groove wherever you want!!</p>
        <h1 className="subtitle">
          Get your moves so accurate that anyone can't even compare to you! HAHAHA
        </h1>
        <button className="read-more-btn">Read more about this app</button>
      </div>

      <div className="image-container">
        <img src={danceImage} alt="Dancing bro" className="dance-image" />
      </div>
    </div>
  );
};

export default Home;
