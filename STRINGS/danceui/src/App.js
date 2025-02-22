import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import Navbar from "./component/Navbar";
import Home from "./component/Home";
import Compare from "./component/Compare";

function App() {
	return (
		<Router>
			<div className='App'>
				<Navbar />
				<Routes>
					<Route
						path='/home'
						element={<Home />}
					/>
					<Route
						path='/compare'
						element={<Compare />}
					/>
				</Routes>
			</div>
		</Router>
	);
}

export default App;
