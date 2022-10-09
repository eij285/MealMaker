import BACKEND_SERVER from './config.json';

/**
 * Send or receive data to or from backend server.
 * Parameters:-
 * ============
 * path: the backend URL path where the request is sent
 * body: the data sent to the backend
 * method: the request method ('POST', 'GET', 'PUT', or 'DELETE')
 * token: the JSON Web Token
 * onSuccess: how to handle success (200) response
 * onFail: how to handle failed or non-200 response
 */
export const backendRequest = async (path, body, method, token, onSuccess, onFail = null) => {
  const requestUrl = `${BACKEND_SERVER}${path}`;
};

export const isValidEmail = (str) => {
  return /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(str) !== false;
};

export const isValidPassword = (str) => {
  if (str.length < 8) {
    return false;
  }
  let [hasUpper, hasLower, hasDigit, hasSymbol] = [false, false, false, false];
  for (const ch of str) {
    if (/[\`~!@#$%^&*()\[\]\-_=+;:\'\“,<.>\/?]/.test(ch)) {
      hasSymbol = true;
    } else if(isNaN(ch) === false) {
      hasDigit = true;
    } else if(ch.toLowerCase() === ch) {
      hasLower = true;
    } else if(ch.toUpperCase() === ch) {
      hasUpper = true;
    }
    if (hasUpper && hasLower && hasDigit && hasSymbol) {
      return true;
    }
  }
  return false;
};
