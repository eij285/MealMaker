import React from 'react';
import PropTypes from 'prop-types';

const GlobalContext = React.createContext(null);

/**
 * Application state management
 */
export const GlobalProvider = ({ children }) => {
  // variable availble globally
  /*const getToken = () => {
    const value = window.localStorage.getItem('token');
    return value === null || value === '' ? '' : value;
  };

  const [token, setToken] = React.useState(getToken('token'));*/

  const [token, setToken] = React.useState('testing');

  const login = (userToken) => {
    window.localStorage.setItem('token', userToken);
    setToken(userToken);
  };

  const logout = () => {
    setToken('');
  };

  const globals = {
    token: token,
    login: login,
    logout: logout
  };

  return (
    <GlobalContext.Provider value={globals}>
      {children}
    </GlobalContext.Provider>
  );
};

GlobalProvider.propTypes = {
  children: PropTypes.any,
};

export default GlobalContext;
