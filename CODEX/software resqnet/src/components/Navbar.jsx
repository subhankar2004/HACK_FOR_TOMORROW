import { Link } from "react-router-dom";
import EmergencyButton from "./EmergencyButton";
import EmergencyButtonSmall from "./EmergencyButtonSmall";


const Navbar = () => {
  return (
    <nav style={{ padding: "10px", background: "#333", color: "white" , margin:"0px"}}>
        
      <Link to="/" style={{ margin: "10px", color: "white" }}>Home</Link>
      <Link to="/alerts" style={{ margin: "10px", color: "white" }}>Alerts</Link>
      <Link to="/logs" style={{ margin: "10px", color: "white" }}>Logs</Link>
      <Link to="/settings" style={{ margin: "10px", color: "white" }}>Settings</Link>
      <Link to="/community" style={{ margin: "10px", color: "white" }}>Community</Link>
      
      <EmergencyButtonSmall />
    </nav>
  );
};

export default Navbar;
