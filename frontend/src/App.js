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
import Forbidden403Page from './pages/Error/Forbidden403Page';
import NotFound404Page from './pages/Error/NotFound404Page';
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
          <Route exact path="/forbidden-403" element={<Forbidden403Page />} />
          <Route path="*" element={<NotFound404Page />} />
        </Routes>
      </Router>
    </GlobalProvider>
  );
}

export default App;
