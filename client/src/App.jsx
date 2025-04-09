import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import ChatPage from './pages/ChatPage';
import Navbar from './components/Navbar';
import PrivateRoute from './utils/PrivateRoute';
import Home from './pages/Home';
import ResultScreenWrapper from './pages/ResultScreenWrapper'; // ✅ use wrapper

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route 
          path="/home"
          element={
            <PrivateRoute>
              <Home />
            </PrivateRoute>
          }
        />

        <Route 
          path="/result"
          element={
            <PrivateRoute>
              <ResultScreenWrapper />
            </PrivateRoute>
          }
        />
      </Routes>
    </Router>
  );
};

export default App;
