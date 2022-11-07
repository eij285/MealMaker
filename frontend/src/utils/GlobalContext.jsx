import React from 'react';
import PropTypes from 'prop-types';
import { backendRequest, defaultFilterOptions } from '../helpers';
const config = require('../config.json');

const GlobalContext = React.createContext(null);

/**
 * Application state management
 */
export const GlobalProvider = ({ children }) => {
  // variable availble globally
  const getToken = () => {
    const value = window.localStorage.getItem('token');
    return value === null || value === '' ? '' : value;
  };

  const [token, setToken] = React.useState(getToken('token'));
  const [userPreferences, setUserPreferences] = React.useState({
    ...defaultFilterOptions()
  });

  const login = (userToken) => {
    window.localStorage.setItem('token', userToken);
    setToken(userToken);
  };

  const logout = () => {
    window.localStorage.setItem('token', '');
    setToken('');
  };

  React.useEffect(() => {
    if (token) {
      // load user preferences into filter on login
      backendRequest('/user/preferences', {}, 'POST', token, (data) => {
        setUserPreferences({
          ...userPreferences,
          breakfast: data.breakfast,
          lunch: data.lunch,
          dinner: data.dinner,
          snack: data.snack,
          vegetarian: data.vegetarian,
          vegan: data.vegan,
          kosher: data.kosher,
          halal: data.halal,
          dairyFree: data.dairy_free,
          glutenFree: data.gluten_free,
          nutFree: data.nut_free,
          eggFree: data.egg_free,
          shellfishFree: data.shellfish_free,
          soyFree: data.soy_free,
          efficiency: data.efficiency,
        });
      });
    } else {
      // reset filter on logout
      setUserPreferences({...defaultFilterOptions()});
    }
  }, [token]);

  const globals = {
    token: token,
    login: login,
    logout: logout,
    userPreferences: userPreferences,
    setUserPreferences: setUserPreferences
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
