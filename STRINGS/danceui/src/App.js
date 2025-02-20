import "./App.css";
import Compare from "./component/Compare";
import Home from "./component/Home";
import Navbar from "./component/Navbar";

function App() {
	return (
		<div className='App'>
			<Navbar />
			{/* <Home /> */}
			<Compare />
		</div>
	);
}

export default App;
