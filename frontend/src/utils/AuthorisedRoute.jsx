import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import GlobalContext from './GlobalContext';

/**
 * Ensures only an authenticated user can access route(s)
 */
function AuthorisedRoute () {
  const token = React.useContext(GlobalContext).token;
  return (
    <>
      {!token && <Navigate replace to="/login" />}
      {token && <Outlet />}
    </>
  );
}

export default AuthorisedRoute;
