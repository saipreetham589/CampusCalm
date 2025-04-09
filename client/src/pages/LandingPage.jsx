import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../assets/CampusCalm_tran.png'; // Adjust the path as necessary


const LandingPage = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-50 via-white to-blue-100 dark:from-gray-900 dark:to-gray-800 transition">
      <img src={logo} alt="Logo" className="mb-9" style={{ width: '130px', height: '130px' }} />

      <h1 className="text-5xl font-bold text-center mb-4 dark:text-white">
       Welcome to <span style={{ color: '#0496BE' }}>CampusCalm</span>
      </h1>

      <p className="text-lg text-gray-700 dark:text-gray-300 text-center max-w-xl">
        Your AI-powered mental wellness companion. Talk, vent, and heal—wherever you are.
      </p>
      
      <Link
        to="/home"
        style={{ backgroundColor: '#0496BE' }}
        className="mt-8 px-6 py-3 text-white rounded-full hover:opacity-90 transition shadow-md"      >
        Get Started
      </Link>
    </div>
  );
};

export default LandingPage;
