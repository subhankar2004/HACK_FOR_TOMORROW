
import './App.css'
import "tailwindcss";


import React, { useState, useEffect } from 'react';

const PoliceStationDashboard = () => {
  const [currentDateTime, setCurrentDateTime] = useState(new Date());
  const [searchTerm, setSearchTerm] = useState('');
  const [showOnlyAlerts, setShowOnlyAlerts] = useState(false);
  const [activeCCTV, setActiveCCTV] = useState(null);
  const [showAssaultAlert, setShowAssaultAlert] = useState(false);
  const [cctvFeeds, setCCTVFeeds] = useState([
    { id: 1, location: 'Ground Floor', hasAlert: false, x: 50, y: 50 },
    { id: 2, location: 'Parking', hasAlert: true, x: 150, y: 100 },
    { id: 3, location: 'First Floor', hasAlert: false, x: 80, y: 150 },
    { id: 4, location: 'Lane Area', hasAlert: true, x: 200, y: 80 },
    { id: 5, location: 'Barricade', hasAlert: false, x: 120, y: 200 },
    { id: 6, location: 'Lawn', hasAlert: false, x: 180, y: 170 },
  ]);

  useEffect(() => {
    const timer = setInterval(() => setCurrentDateTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (activeCCTV) {
      const timeout = setTimeout(() => {
        setShowAssaultAlert(true);
      }, 5000);
      return () => clearTimeout(timeout);
    }
  }, [activeCCTV]);

  const filteredFeeds = cctvFeeds.filter(feed => 
    (feed.location.toLowerCase().includes(searchTerm.toLowerCase()) || feed.id.toString().includes(searchTerm)) &&
    (!showOnlyAlerts || feed.hasAlert)
  );

  const CCTVFeed = ({ id, location }) => (
    <div className="relative bg-gray-300 h-64 flex items-center justify-center">
      <div className="absolute top-0 left-0 bg-red-500 text-white px-2 py-1 text-sm">
        CCTV #{id} - {location}
      </div>
      <p>Simulated CCTV Feed {id}</p>
    </div>
  );


  const startMonitoring = async()=>{
    const response = await fetch('http://localhost:5000/start-monitoring');
    const data = await response.json();
  };


    
  const SimpleMap = ({ x, y }) => (
    <svg width="300" height="300" viewBox="0 0 300 300" className="border border-gray-300">
      <rect x="0" y="0" width="300" height="300" fill="#f0f0f0" />
      <circle cx={x} cy={y} r="5" fill="red" />
      <text x={x + 10} y={y - 10} fontSize="12">CCTV Location</text>
      {/* Simple roads */}
      <line x1="0" y1="150" x2="300" y2="150" stroke="gray" strokeWidth="2" />
      <line x1="150" y1="0" x2="150" y2="300" stroke="gray" strokeWidth="2" />
      {/* City blocks */}
      <rect x="50" y="50" width="50" height="50" fill="#e0e0e0" stroke="gray" />
      <rect x="200" y="100" width="50" height="50" fill="#e0e0e0" stroke="gray" />
      <rect x="100" y="200" width="50" height="50" fill="#e0e0e0" stroke="gray" />
    </svg>
  );

  const LandingPage = () => (
    <>
      {/* Search and Filter */}
      <div className="mb-4 flex space-x-4">
        <input
          type="text"
          placeholder="Search by location or feed number"
          className="flex-grow p-2 border rounded"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={showOnlyAlerts}
            onChange={() => setShowOnlyAlerts(!showOnlyAlerts)}
            className="mr-2"
          />
          Show only alerts
        </label>
      </div>

      {/* CCTV Matrix */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {filteredFeeds.map((feed) => (
          <button
            key={feed.id}
            className={`p-4 rounded-lg shadow ${
              feed.hasAlert ? 'bg-red-500 text-white' : 'bg-white hover:bg-gray-100'
            }`}
            onClick={() => setActiveCCTV(feed)}
          >
            <div className="font-bold">CCTV {feed.id}</div>
            <div>{feed.location}</div>
            {feed.hasAlert && <div className="mt-2">⚠ Alert</div>}
          </button>
        ))}
      </div>

      {/* Alerts Section */}
      <div className="mt-8 bg-white p-4 rounded-lg shadow">
        <h2 className="text-xl font-bold mb-4 bg-white">Active Alerts</h2>
        <div className="space-y-4">
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4">
            <p className="font-bold">Violence Detected</p>
            <p>CCTV 2 - Parking | Time: {currentDateTime.toLocaleTimeString()}</p>
          </div>
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4">
            <p className="font-bold">Violence Detected</p>
            <p>CCTV 4 - Lane Area | Time: {currentDateTime.toLocaleTimeString()}</p>
          </div>
        </div>
      </div>
    </>
  );

  const DetailedView = () => (
    <div className="space-y-4">
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-2">CCTV Feed Details</h3>
        <CCTVFeed id={activeCCTV.id} location={activeCCTV.location} />
        <div className="mt-4">
          <h4 className="text-md font-semibold mb-2">Location Map</h4>
          <SimpleMap x={activeCCTV.x} y={activeCCTV.y} />
        </div>
        <button
          onClick={() => setActiveCCTV(null)}
          className="mt-4 bg-blue-600 text-white px-4 py-2 rounded"
        >
          Back to CCTV Grid
        </button>
      </div>

      {/* Alerts/Incident Overview */}
      <div className="bg-white p-4 rounded-lg shadow mb-4">
        <h3 className="text-lg font-semibold mb-2">Alerts & Incidents</h3>
        {showAssaultAlert && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4" role="alert">
            <p className="font-bold">Emergency: Potential Assault Detected</p>
            <p>Feme-vision system has identified a potential violent incident in CCTV #{activeCCTV.id}, {activeCCTV.location}. Immediate response required.</p>
          </div>
        )}
      </div>

      {/* Analytics & Monitoring Section (placeholder) */}
      <div className="bg-white p-4 rounded-lg shadow">
        <h3 className="text-lg font-semibold mb-2">Analytics Dashboard</h3>
        <div className="bg-gray-200 h-64 flex items-center justify-center">
          <p>Analytics and monitoring data for CCTV #{activeCCTV.id} would be displayed here</p>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-700 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <h1 className="text-2xl font-bold">Central CCTV Monitor</h1>
            <button  className="bg-white text-blue-700 px-4 py-2 rounded flex flex-row items-center"
            onSubmit={startMonitoring}>
              Start Monitoring
            </button>
          </div>d
          <div className="text-right">
            <p>{currentDateTime.toLocaleString()}</p>
            <p className="text-yellow-300">2 Active Alerts</p>
          </div>
        </div>
      </header>

      <main className="container mx-auto p-4">
        {activeCCTV ? <DetailedView /> : <LandingPage />}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white p-4 mt-8">
        <div className="container mx-auto flex justify-between items-center">
          <div>
            <a href="#" className="mr-4 hover:underline">Real-Time Dashboard</a>
            <a href="#" className="mr-4 hover:underline">Incidents History</a>
            <a href="#" className="hover:underline">Report Generation</a>
          </div>
          <div className="text-right">
            <p>Emergency: 911</p>
            <p>Non-Emergency: 555-1234</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default PoliceStationDashboard;


