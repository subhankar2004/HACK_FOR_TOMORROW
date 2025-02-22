import React, { useState } from "react";
import DiscussionForum from "../components/DiscussionForum";
import TipsResources from "../components/TipsResources";
import Leaderboard from "../components/Leaderboard";
import SupportRequests from "../components/SupportRequests";
import UsefulVideos from "../components/UsefulVideos";
import CreatorCorner from "../components/CreatorCorner";

const CommunityPage = () => {
  const [selectedTab, setSelectedTab] = useState("forum");

  return (
    <div style={{ padding: "20px" }}>
      <h2> Community Hub</h2>

      
      <div style={styles.tabContainer}>
        <button onClick={() => setSelectedTab("forum")}>Discussion Forum</button>
        <button onClick={() => setSelectedTab("tips")}>Emergency Tips</button>
        <button onClick={() => setSelectedTab("leaderboard")}>Leaderboard</button>
        <button onClick={() => setSelectedTab("support")}>Support Requests</button>
        <button onClick={() => setSelectedTab("videos")}>Useful Videos</button>
        <button onClick={() => setSelectedTab("creator")}>Creator Corner</button>
      </div>

      
      {selectedTab === "forum" && <DiscussionForum />}
      {selectedTab === "tips" && <TipsResources />}
      {selectedTab === "leaderboard" && <Leaderboard />}
      {selectedTab === "support" && <SupportRequests />}
      {selectedTab === "videos" && <UsefulVideos />}
      {selectedTab === "creator" && <CreatorCorner />}
    </div>
  );
};

const styles = {
  tabContainer: {
    display: "flex",
    gap: "10px",
    marginBottom: "20px",
  },
};

export default CommunityPage;
