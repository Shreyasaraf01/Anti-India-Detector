import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-gray-800 text-white p-4 fixed w-full top-0 z-50 shadow-lg">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-2xl font-bold">
          <Link to="/">Detector</Link>
        </div>
        <ul className="flex space-x-6">
          <li>
            <Link to="/" className="hover:text-indigo-400 transition-colors">Home</Link>
          </li>
          <li>
            <Link to="/features" className="hover:text-indigo-400 transition-colors">Features</Link>
          </li>
          <li>
            <Link to="/analyze" className="hover:text-indigo-400 transition-colors">Analyze</Link>
          </li>
          <li>
            <Link to="/contact" className="hover:text-indigo-400 transition-colors">Contact</Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;