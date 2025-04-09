import React from 'react';
import { useLocation } from 'react-router-dom';
import ResultScreen from './ResultScreen';

const ResultScreenWrapper = () => {
  const location = useLocation();
  const phq9 = location.state?.phq9 ?? null;
  const gad7 = location.state?.gad7 ?? null;

  return <ResultScreen phq9={phq9} gad7={gad7} />;
};

export default ResultScreenWrapper;
