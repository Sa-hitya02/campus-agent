import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./Navbar.css";

const Navbar = () => {
  const { pathname } = useLocation();

  return (
    <nav className="navbar">
      <div className="nav-brand">🧠 SmartCampus</div>
      <div className="nav-links">
        <Link to="/" className={pathname === "/" ? "active" : ""}>Submit Complaint</Link>
        <Link to="/dashboard" className={pathname === "/dashboard" ? "active" : ""}>Dashboard</Link>
      </div>
    </nav>
  );
};

export default Navbar;
