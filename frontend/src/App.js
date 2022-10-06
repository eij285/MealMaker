import React from 'react';
import { GlobalProvider } from './utils/GlobalContext';
import {
  BrowserRouter as Router,
  Routes,
  Route
 } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginPage from './pages/Auth/LoginPage';
import SignupPage from './pages/Auth/SignupPage';
import ForgotPasswordPage from './pages/Auth/ForgotPasswordPage';
import PasswordResetPage from './pages/Auth/PasswordResetPage';
import './App.css';

function App() {
  return (
    <GlobalProvider>
      <Router>
        <Routes>
          <Route exact path="/" element={<HomePage />} />
          <Route exact path="/login" element={<LoginPage />} />
          <Route exact path="/signup" element={<SignupPage />} />
          <Route exact path="/forgot-password" element={<ForgotPasswordPage />} />
          <Route exact path="/password-reset" element={<PasswordResetPage />} />
        </Routes>
      </Router>
    </GlobalProvider>
  );
}

export default App;
