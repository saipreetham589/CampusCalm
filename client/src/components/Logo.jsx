// src/components/Logo.jsx
import React from 'react';
import logo from '../assets/CampusCalm_tran.png';

const Logo = ({ size = 'w-10 h-10', text = true }) => (
  <div className="flex items-center gap-2">
    <img src={logo} alt="Logo" className={`${size}`} />
    {text && <h1 className="font-bold text-xl text-white">CampusCalm</h1>}
  </div>
);

export default Logo;
