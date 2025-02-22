import React, { useState } from "react";
import "./Navbar.css";

const Navbar = () => {
	const [isOpen, setIsOpen] = useState(false);

	const toggleMenu = () => {
		setIsOpen(!isOpen);
	};

	return (
		<header className='navbar'>
			<div className='logo'>
				<a href='/'>Dance Zero</a>
			</div>
			<nav className={`nav-links ${isOpen ? "active" : ""}`}>
				<a href='/home'>Home</a>
				<a href='/compare'>Dance-Compare</a>
				<a href='/services'>Feedback</a>
				<a
					href='/login'
					className='login-btn'>
					<i className='fa fa-user'></i> Logout
				</a>
				<button className='search-btn'>
					<i className='fa fa-search'></i>
				</button>
			</nav>
			<div
				className='menu-toggle'
				onClick={toggleMenu}>
				☰
			</div>
		</header>
	);
};

export default Navbar;
