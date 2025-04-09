import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import ThemeToggle from './ThemeToggle';
import ProfileMenu from './ProfileMenu';

const Navbar = () => {
  const location = useLocation();

  const isLoginPage = location.pathname === '/login';

  return (
    <nav
      className={`flex justify-between items-center px-6 py-4 bg-white dark:bg-gray-900 shadow-md z-20 ${
        isLoginPage ? 'absolute top-0 left-0 right-0' : ''
      }`}
    >
      <Link to="/" className="text-xl font-bold dark:text-white" style={{ color: '#0496BE' }}>
        CampusCalm
      </Link>

      
      <div className="flex items-center gap-4">
        <ThemeToggle />
        <ProfileMenu />
      </div>
      
    </nav>
  );
};

export default Navbar;
