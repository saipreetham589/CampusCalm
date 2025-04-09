import React from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


const ResultScreen = ({ phq9, gad7 }) => {
  const navigate = useNavigate();

  const ResultBlock = ({ label, score, level }) => (
    <div className="flex flex-col items-center">
      <div className="relative w-32 h-32 mb-2">
        <div className="absolute inset-0 flex items-center justify-center text-xl font-bold text-blue-800 dark:text-blue-400">
          {typeof score === 'number' ? `${score}%` : '--'}
        </div>
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="45" stroke="currentColor" strokeWidth="10" fill="transparent" className="text-gray-300 dark:text-gray-700" />
          <circle cx="50" cy="50" r="45" stroke="currentColor" strokeWidth="10" fill="transparent" strokeDasharray="283" strokeDashoffset={283 - (score / 100) * 283} className="text-blue-600 dark:text-blue-400" />
        </svg>
      </div>
      <p className="text-gray-700 dark:text-gray-300 text-sm">{label}</p>
    </div>
  );

  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] px-4 text-center bg-white dark:bg-gray-900 transition-colors duration-300">
      <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-100 mb-2">Test Completed</h2>
      <p className="text-gray-500 dark:text-gray-400 mb-6">
        Thank you for completing the assessment
      </p>

      <div className="flex gap-10 mb-8">
        <ResultBlock label="PHQ-9" score={phq9.percent}  />
        <ResultBlock label="GAD-7" score={gad7.percent}  />
      </div>

      <button
        onClick={() => navigate('/home', { state: { tab: 1 } })}
        className="px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
      >
        Continue to Chat Support
      </button>
    </div>
  );
};

export default ResultScreen;
