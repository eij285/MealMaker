const config = require('./config.json');

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
  const requestUrl = `${config.BACKEND_SERVER}${path}`;
  console.log(requestUrl);

  const requestObject = {
    method: method,
    headers: {
      'Content-Type': 'application/json',
    },
  };
  if (body !== null && token !== null && token !== '') {
    body.token = token;
  }
  if ((method === 'POST' || method === 'PUT') && body !== null) {
    requestObject.body = JSON.stringify(body);
  }
  /*try {
    const request = await fetch(requestUrl, requestObject);
    const status = await request.status;
    if (status === 200 || status === 201) {
      const data = await request.json();
      onSuccess(data);
      return data;
    } else if (status === 400 || status === 401 || status === 403) {
      const data = await request.json();
      throw new Error(data.error);
    } else {
      throw new Error('Something went wrong');
    }
  } catch (error) {
    if (onFail !== null) {
      onFail(error.message);
    } else {
      console.log(error.message);
    }
  }*/
  try {
    const request = await fetch(requestUrl, requestObject);
    const status = await request.status;
    if (status === 200) {
      const data = await request.json();
      const innerStatus = data.status_code;
      if (innerStatus >= 200 && innerStatus < 300) {
        onSuccess(data);
      } else if (innerStatus >= 400 && innerStatus <= 500) {
        throw new Error(`${data.error}`);
      } else {
        throw new Error('Something went wrong');
      }
      console.log(data);
      return data;
    } else if (status >= 400 && status < 500) {
      const data = await request.json();
      throw new Error(data.error);
    } else {
      throw new Error('Something went wrong');
    }
  } catch (error) {
    if (onFail !== null) {
      onFail(error.message);
    } else {
      console.log(error.message);
    }
  }
};

export const isValidEmail = (str) => {
  return /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(str) !== false;
};

// check if password string is valid, returning valid status and message if not
export const isValidPassword = (str) => {
  if (str.length < 8) {
    return {
      valid: false,
      message: str ? 'Password is less than 8 characters'
        : 'A password is required'
    };
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
      return {
        valid: true,
        message: ''
      };
    }
  }
  let missing = ' ';
  if (!hasLower) {
    missing = 'a lower-case character';
  } else if(!hasUpper) {
    missing = 'an upper-case character';
  } else if(!hasDigit) {
    missing = 'a decimal digit';
  } else if(!hasSymbol) {
    missing = 'a special character';
  }
  return {
    valid: false,
    message: `Password does not contain ${missing}`
  };
};

// display name is required
export const validateDisplayName = (displayName, setMessage) => {
  if (displayName === '') {
    setMessage('Display name is required');
  } else {
    setMessage('');
  }
};

// email must not be blank, and must match required format
export const validateEmail = (email, setMessage) => {
  if (email === '') {
    setMessage('An email is required')
  } else if (isValidEmail(email) === false) {
    setMessage('Email format is not valid');
  } else {
    setMessage('');
  }
};

// password must safisfy complexity requirements
export const validatePassword = (password, setMessage) => {
  setMessage(isValidPassword(password).message);
};

// ensure confirmation matches password, thus user didn't enter random values
export const validatePasswordMatch = (password, confirm, setMessage) => {
  if (confirm === '') {
    setMessage('A confirmation password is required');
  } else if (password !== confirm) {
    setMessage('Passwords do not match');
  } else {
    setMessage('');
  }
};