import React from 'react';
import './Waveform.css';

const VoiceVisualizer = ({ isActive }) => {
  return (
    <div className={`voice-waveform-container ${isActive ? 'active' : ''}`}>
      <div className="waveform-bar bar1"></div>
      <div className="waveform-bar bar2"></div>
      <div className="waveform-bar bar3"></div>
      <div className="waveform-bar bar4"></div>
      <div className="waveform-bar bar5"></div>
    </div>
  );
};

export default VoiceVisualizer;
