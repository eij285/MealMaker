import React from 'react';
import { Redirect, Route } from 'react-router-dom';
import GlobalContext from './GlobalContext';

/**
 * Route accessible by authenticated users only
 */
function AuthorisedRoute (props) {
  const token = React.useContext(GlobalContext).token;
  return (
    <>
      {!token && <Redirect to="/login" />}
      {token && <Route {...props} />}
    </>
  );
}

export default AuthorisedRoute;
