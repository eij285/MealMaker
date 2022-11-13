import moment from 'moment';
import convert from 'convert';
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
export const backendRequest = async (path, body, method, token, onSuccess,
  onFail = null, setStatus = null) => {
  const requestUrl = `${config.BACKEND_SERVER}${path}`;
  //console.log(requestUrl);

  const requestObject = {
    method: method,
    headers: {
      'Content-Type': 'application/json',
    },
  };
  if (body !== null) {
    body.token = token;
  }
  if ((method === 'POST' || method === 'PUT') && body !== null) {
    requestObject.body = JSON.stringify(body);
  }
  try {
    const request = await fetch(requestUrl, requestObject);
    const status = await request.status;
    if (status === 200) {
      const data = await request.json();
      const innerStatus = data.status_code;
      if (setStatus !== null) {
        setStatus(innerStatus);
      }
      if (innerStatus >= 200 && innerStatus < 300) {
        onSuccess(data);
      } else if (innerStatus >= 400 && innerStatus <= 500) {
        throw new Error(`${data.error}`);
      } else {
        throw new Error('Something went wrong');
      }
      //console.log(data);
      return data;
    } else if (status >= 400 && status < 500) {
      const data = await request.json();
      if (setStatus !== null) {
        setStatus(status);
      }
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

export const tokenToUserId = (token) => {
  try {
    if (token) {
      return JSON.parse(atob(token.split('.')[1])).u_id;
    } else {
      throw new Error();
    }
  } catch (error) {
    return -1;
  }
}

export const isValidEmail = (str) => {
  /* eslint-disable no-useless-escape */
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

// determines if string is a positive integer
export const isPositiveInteger = (str) => {
  return /^[1-9][0-9]*$/.test(str);
};

export const validateServings = (value, setMessage) => {
  if (value === '') {
    setMessage('Servings required');
  } else if (!isPositiveInteger(value)) {
    setMessage('Requires positive integer');
  } else {
    setMessage('');
  }
};

/**
 * Convert a raster image to base64 encoded string
 */
export const imageToBase64 = (file) => {
  // ensure right type of image provided, else return empty string
  if (!['image/jpeg', 'image/png', 'image/jpg'].find(type=>type===file.type)) {
    return '';
  }
  const reader = new FileReader();
  const dataUrlPromise = new Promise((resolve, reject) => {
    reader.onerror = reject;
    reader.onload = () => resolve(reader.result);
  });
  reader.readAsDataURL(file);
  return dataUrlPromise;
};

/**
 * Convert timestamp string to long format date string
 */
export const longDateString = (str) => {
  return moment(str).format('hh:mma dddd, Do MMMM, YYYY');
};

/**
 * Convert timestamp string to long format date string
 */
 export const shortDateString = (str) => {
  return moment(str).format('DD/MM/YYYY');
};

/**
 * Convert timestamp string to short format datetime string
 */
 export const shortDateTimeString = (str) => {
  return moment(str).format('h:mma DD/MM/YYYY');
};

/**
 * Ruturn null if empty string else unchanged
 */
export const emptyStringToNull = (str) => {
  return str ? str : null;
};

/**
 * Ruturn null if empty string else return integer string
 */
 export const intStringOrNull = (str) => {
  return str ? (isNaN(str) ? null : `${parseInt(str, 10)}`) : null;
};

/**
 * Returns average review rating
 */
export const getAverageRating = (reviews) => {
  // fix when have reviews
  if (typeof reviews !== typeof [] || reviews.length === 0) {
    return 0;
  }
  if (reviews.length === 1)  {
    return reviews[0].rating;
  }
  return reviews.map(obj => obj.rating).reduce((a, b) => a + b, 0) / reviews.length;
};

export const formatNumString = (val) => {
  const numStr = `${val}`;
  if (/^\d+$/.test(numStr)) {
    return numStr;
  }
  if (/^\d+\.0+$/.test(numStr) || /^\d+\.0{2,}[0-4]*$/.test(numStr)) {
    return `${parseInt(numStr)}`;
  }
  if (/^\d+\.[1-9]0[0-4]*$/.test(numStr) || /^\d+\.[1-9]0*$/.test(numStr)) {
    return parseFloat(numStr).toFixed(1);
  }
  return parseFloat(numStr).toFixed(2);
};

export const formatNutrient = (qty, isMass, reqImperial) => {
  if (qty === -1) {
    return 'NA';
  }
  if (isMass) {
    return reqImperial ?
      formatNumString(convert(qty, 'gram').to('ounce')) + 'oz.'
      : `${formatNumString(qty)}g`;
  }
  return reqImperial ? formatNumString(qty / 4.184) + 'Cal'
    : `${formatNumString(qty)}kJ`;
};

const formatIngredientUnit = (qty, unit) => {
  return qty === 1 ? unit.replace(/s$/, '') : unit;
};

export const formatIngredient = (ingredient, reqImperial) => {
  if (ingredient.quantity === -1) {
    return 'NA';
  }
  const quantity = ingredient.quantity;
  const unit = ingredient.unit;
  if (!reqImperial) {
    // remove s suffix from singluar to make unit grammatically correct
    return `${formatNumString(quantity)} ${formatIngredientUnit(quantity, unit)}`;
  }
  let obj = null;
  //"litres", "mL", "grams", "kg", "cups", "tbsp", "tsp", "pieces"
  if (unit === 'gram' || unit === 'grams') {
    obj = convert(quantity, 'gram').to('best', 'imperial');
  } else if (unit === 'kg' || unit === 'kilogram' || unit === 'kilograms') {
    obj = convert(quantity, 'kilogram').to('best', 'imperial');
  } else if (unit === 'mL' || unit === 'millilitres' || unit === 'milliliters') {
    obj = convert(quantity, 'mL').to('best', 'imperial');
  } else if (unit === 'litre' || unit === 'litres' || unit === 'liter' ||
             unit === 'liters') {
    obj = convert(quantity, 'litre').to('best', 'imperial');
  }
  if (obj !== null) {
    return `${formatNumString(obj.quantity)} ${
      formatIngredientUnit(obj.quantity, obj.unit)}`;
  }
  return `${formatNumString(quantity)} ${formatIngredientUnit(quantity, unit)}`;
};

export const customPrepTime = (hours, minutes, level) => {
  let totalMinutes = 0;
  if (hours !== null) {
    totalMinutes = hours * 60;
  }
  if (minutes !== null) {
    totalMinutes += minutes;
  }
  if (level === config.EFFICIENCY[2]) {
    totalMinutes *= config.EFFICIENCY_CONV;
  } else if (level === config.EFFICIENCY[0]) {
    totalMinutes /= config.EFFICIENCY_CONV;
  }
  return Math.round(totalMinutes);
};

/**
 * default options for recipe filter (feeds, search)
 */
export const defaultFilterOptions = () => {
  return {
    filtersEnabled: true,
    breakfast: true,
    lunch: true,
    dinner: true,
    snack: true,
    vegetarian: false,
    vegan: false,
    kosher: false,
    halal: false,
    dairyFree: false,
    glutenFree: false,
    nutFree: false,
    eggFree: false,
    shellfishFree: false,
    soyFree: false,
    cuisines: config.CUISINES.reduce((c, v) => ({ ...c, [v]: true}), {}),
    showUnspecifiedCuisines: false,
    efficiency: 'Intermediate',
    minMinutes: 30,
    maxMinutes: 180,
    showUnspecifiedTime: true,
  }
};

/**
 * set filtered recipes from all recipes based on user preferences
 */
export const filterRecipes = (userPreferences, allRecipes, setFiltered) => {
  setFiltered([...allRecipes.filter((recipe) => {
    if (!userPreferences.filtersEnabled) {
      return true;
    }
    // meal must meet all dietary needs
    if ((!recipe.vegetarian && userPreferences.vegetarian) ||
      (!recipe.vegan && userPreferences.vegan) ||
      (!recipe.kosher && userPreferences.kosher) ||
      (!recipe.halal && userPreferences.halal) ||
      (!recipe.dairy_free && userPreferences.dairyFree) ||
      (!recipe.gluten_free && userPreferences.glutenFree) ||
      (!recipe.nut_free && userPreferences.nutFree) ||
      (!recipe.egg_free && userPreferences.eggFree) ||
      (!recipe.shellfish_free && userPreferences.shellfishFree) ||
      (!recipe.soy_free && userPreferences.soyFree)) {
      return false;
    }
    // don't filter by meal where meal suitability unticked, where one or more
    // options ticked must satisfy at least one meal option
    if ((userPreferences.breakfast || userPreferences.lunch ||
      userPreferences.dinner || userPreferences.snack) &&
      ((!recipe.breakfast && userPreferences.breakfast) ||
      (!recipe.lunch && userPreferences.lunch) ||
      (!recipe.dinner && userPreferences.dinner) ||
      (!recipe.snack && userPreferences.snack))) {
      return false;
    }
    // exclude cuisine unspecified, but cuisine type required
    if (recipe.cuisine === null && !userPreferences.showUnspecifiedCuisines) {
      return false;
    } else if (recipe.cuisine !== null) {
      // filter out not null cuisine
      if (!userPreferences.cuisines.hasOwnProperty(recipe.cuisine)) {
        return false;
      }
      if (!userPreferences.cuisines[recipe.cuisine]) {
        return false;
      }
    }
    // include if allowing unspecified preparation time, otherwise exclude
    if (recipe.preparation_hours === null &&
      recipe.preparation_minutes === null) {
      return userPreferences.showUnspecifiedTime;
    }
    // calculation based on user efficiency based time
    const userPrepTime = customPrepTime(recipe.preparation_hours,
      recipe.preparation_minutes, userPreferences.efficiency);
    return userPrepTime >= userPreferences.minMinutes &&
      userPreferences.maxMinutes >= userPrepTime;
  })]);
};

export const initialCookbookData = () => {
  return {
    cookbookId: -1,
    name: '',
    photo: '',
    description: '',
    cookbookStatus: 'draft',
  };
};
