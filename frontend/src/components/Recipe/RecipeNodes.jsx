import React from 'react';
import styled from '@emotion/styled';
import { Box, IconButton, Rating, Tooltip, Typography } from '@mui/material';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';
import FoodBankIcon from '@mui/icons-material/FoodBank';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import ThumbUpOutlinedIcon from '@mui/icons-material/ThumbUpOutlined';
import GlobalContext from '../../utils/GlobalContext';
import { AlertToast, FlexRow, FlexRowVCentred, FlexRowWrapSpaced } from '../StyledNodes';
import {
  MediumGreyText,
  MediumBlackText,
  SmallBlackText,
  SmallGreyText,
  SubPageTitle
} from '../TextNodes';
import { NumericInput } from '../../components/InputFields';
import {
  backendRequest,
  customPrepTime,
  formatIngredient,
  formatNutrient,
  getAverageRating
} from '../../helpers';
import { MediumDefaultButton, SmallDefaultButton } from '../Buttons';
const config = require('../../config.json');

const RecipeImgContainer = styled.div`
  display: flex;
  position: relative;
  flex-direction: row;
  justify-content: center;
  height: 33vh;
  & img, & svg {
    height: 100%;
    width: auto;
    object-fit: contain;
  }
`;

/**
 * Recipe image component
 */
export const RecipeImg = ({src, alt}) => {
  return (
    <RecipeImgContainer>
      {src && <img src={src} alt={alt} />}
      {!src && <FoodBankIcon/>}
    </RecipeImgContainer>
  );
};

/**
 * Recipe rating component
 */
export const RecipeRating = ({reviews}) => {
  const [avgRating, setAvgRating] = React.useState(0);
  React.useEffect(() => {
    setAvgRating(getAverageRating(reviews));
  }, [reviews]);
  return (
    <Box sx={{ alignSelf: 'center', textAlign: 'center' }}>
      {typeof reviews === typeof [] && <>
        {reviews.length < 1 && <MediumGreyText>No Reviews</MediumGreyText>}
        {reviews.length > 0 && <>
        <Rating value={avgRating} precision={0.1} readOnly />
        <MediumGreyText>
          {avgRating.toFixed(1)}&nbsp;
          ({reviews.length}&nbsp;
          {reviews.length !== 1 && <span>reviews</span>}
          {reviews.length === 1 && <span>review</span>})
        </MediumGreyText>
        </>}
      </>}
    </Box>
  );
};

/**
 * Like/unlike recipe component
 */
export const RecipeLikes = ({likesObject, likeRecipe}) => {
  return (
    <>
    {typeof likesObject === typeof {} &&
    <Tooltip title="Like Recipe" placement="top" arrow>
      <IconButton color="info" onClick={likeRecipe}>
        {likesObject.hasLiked && <ThumbUpIcon />}
        {!likesObject.hasLiked && <ThumbUpOutlinedIcon />}
        &nbsp;{likesObject.likesCount}
      </IconButton>
    </Tooltip>}
    </>
  );
};


const RecipeInfoPanelContainer = styled(FlexRowWrapSpaced)`
  border: 1px solid #333333;
  border-radius: 5px;
  padding: 8px;
  row-gap: 20px;
  align-items: center;
`;

const NutritionText = ({topVal, bottomVal, units}) => {
  return (
    <Box sx={{textAlign: 'center'}}>
      <Typography>{topVal}</Typography>
      <Typography>{bottomVal}</Typography>
    </Box>
  );
};

const PreparationTimeText = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
`;

const RecipePrepartionTimeText = React.forwardRef((props, ref) => {
  //  Spread the props to the underlying DOM element.
  return (<div {...props} ref={ref}>
    <Typography>
      {props.hours > 0 && `${props.hours}hrs`}&nbsp;
      {props.minutes > 0 && `${props.minutes}mins`}
    </Typography>
    <SmallGreyText>{props.level}</SmallGreyText>
  </div>
  );
});

/**
 * Recipe preparation time and user efficiency component
 */
export const RecipePrepartionTime = ({hours, minutes, level,
  useSmall = false}) => {
  const totalMinutes = customPrepTime(hours, minutes, level);
  let ttMsg = '';
  if (hours !== null) {
    ttMsg = `${hours}hrs`;
  }
  if (minutes !== null) {
    ttMsg += `${ttMsg?' ':''}${minutes}mins`;
  }
  const customHours = parseInt(totalMinutes / 60);
  const customMinutes = totalMinutes - (customHours * 60);
  if (hours !== null && minutes !== null) {
    ttMsg += ' @ Intermediate' + (!useSmall ? ' Efficiency' : '');
  }
  const iconStyle = {
    fontSize: `${useSmall? 2 : 3}em`
  };
  const unspecTypo = {
    fontSize: '10pt'
  };

  return (
    <FlexRow>
      <AccessTimeIcon sx={iconStyle} />
      <PreparationTimeText>
        {hours !== null && minutes !== null && level !== config.EFFICIENCY[1] &&
        <Tooltip title={ttMsg} placement="top" arrow>
          <RecipePrepartionTimeText hours={customHours} minutes={customMinutes}
            level={level} />
        </Tooltip>}
        {hours !== null && minutes !== null && level === config.EFFICIENCY[1] &&
        <RecipePrepartionTimeText hours={customHours} minutes={customMinutes}
          level={level} />}
        {hours === null && minutes === null && <>
        {useSmall && <Typography sx={unspecTypo}>Unspecified</Typography>}
        {!useSmall && <Typography>Unspecified Preparation Time</Typography>}
        </>}
      </PreparationTimeText>
    </FlexRow>
  );
};

/**
 * Recipe tags (alergens and dietary needs) component
 */
const RecipeTags = ({data}) => {
  let tags = [];
  data.vegetarian && tags.push('Vegetarian');
  data.vegan && tags.push('Vegan');
  data.kosher && tags.push('Halal');
  data.dairy_free && tags.push('Dairy Free');
  data.gluten_free && tags.push('Gluten Free');
  data.nut_free && tags.push('Nut Free');
  data.egg_free && tags.push('Egg Free');
  data.shellfish_free && tags.push('Shellfish Free');
  data.soy_free && tags.push('Gluten Free');
  return (
    <SmallBlackText>
      {tags.join(', ')}
    </SmallBlackText>
  );
};

/**
 * Recipe information component, allows selection of servings and displays
 * nutritional information, cooking time and recipe tags
 */
export const RecipeInfoPanel = ({data, currData, setServings}) => {
  const reqImperial = data.units === 'Imperial';
  const energy = formatNutrient(currData.energy, false, reqImperial);
  const protein = formatNutrient(currData.protein, true, reqImperial);
  const carbohydrates = formatNutrient(currData.carbohydrates, true, reqImperial);
  const fats = formatNutrient(currData.fats, true, reqImperial);
  return (
    <RecipeInfoPanelContainer>
      <FlexRow>
        <NumericInput
          label="Servings"
          sx={{ width: '100px' }}
          inputProps={{ min: 1, max: 200 }}
          value={currData.servings}
          onChange={(e) =>
            setServings(e.target.value ? `${parseInt(e.target.value)}`: '')}
        />
        <NutritionText topVal="Energy" bottomVal={energy} />
        <NutritionText topVal="Protein" bottomVal={protein} />
        <NutritionText topVal="Carbs" bottomVal={carbohydrates} />
          <NutritionText topVal="Fats" bottomVal={fats} />
      </FlexRow>
      <RecipePrepartionTime hours={data.preparation_hours}
        minutes={data.preparation_minutes} level={data.efficiency} />
      <RecipeTags data={data} />
    </RecipeInfoPanelContainer>
  );
};

/**
 * Meal suitability tags (Breakfast, Lunch, Dinner, Snack)
 */
export const MealSuitabilityTags = ({data}) => {
  let tags = [];
  data.breakfast && tags.push('Breakfast');
  data.lunch && tags.push('Lunch');
  data.dinner && tags.push('Dinner');
  data.snack && tags.push('Snack');
  return (
    <>
    {tags.length > 0 &&
    <MediumBlackText>
      Meal Suitability: {tags.join(', ')}
    </MediumBlackText>}
    </>
  );
};

const IngredientsListingContainer = styled.div`
  display: flex;
  flex-direction: column;
`;

const IngredientsListingGrid = ({useThreeCols, children}) => {
  const cols = 'max-content max-content' + (useThreeCols ? ' max-content' : '');
  const styles = {
    display: 'grid',
    gridTemplateColumns: cols,
    columnGap: '8px',
    rowGap: '4px',
    marginBottom: '30px',
    alignItems: 'center'
  };
  return (
    <Box sx={styles}>
      {children}
    </Box>
  );
};

/**
 * Displays information for a single ingredient
 */
const SingleIngredient = ({ingredient, reqImperial, addToCart, token}) => {
  return (
    <>
      <Typography sx={{fontWeight: '600'}}>
        {formatIngredient(ingredient, reqImperial)}
      </Typography>
      <Typography>{ingredient.ingredient_name}</Typography>
      {token &&
      <IconButton size="small" onClick={() => addToCart(ingredient.ingredient_id)}>
        <AddShoppingCartIcon />
      </IconButton>}
    </>
  );
};

/**
 * Displays a listing of all ingredients
 */
export const IngredientsListing = ({data, recipeId, reqImperial}) => {
  const globals = React.useContext(GlobalContext);
  const token = globals.token;
  const setCartId = globals.setCartId;
  const cartItems = globals.cartItems;
  const setCartItems = globals.setCartItems;
  const servings = parseInt(data.servings);
  const [toastMessage, setToastMessage] = React.useState('');
  const [toastState, setToastState] = React.useState('error');
  const addToCart = () => {
    const body = {
      recipe_id: recipeId,
      servings: servings
    };
    backendRequest('/cart/add-all', body, 'POST', token, (data) => {
      setCartId(data.body.cart_id);
      setCartItems([...cartItems, ...data.body.ingredients]);
    }, (error) => {
      setToastMessage(error);
    });
  };

  const addOneToCart = (ingredientId) => {
    const body = {
      recipe_ingredient_id: ingredientId
    };
    backendRequest('/cart/add-ingredient/id', body, 'POST', token, (data) => {
      console.log(cartItems);
      /*setCartItems([...cartItems, {

      }]);*/
    }, (error) => {
      setToastMessage(error);
    });
  };
  return (<>
    <IngredientsListingContainer>
      <FlexRowVCentred>
        <SubPageTitle>Ingredients</SubPageTitle>
        {token &&
        <MediumDefaultButton onClick={addToCart} disabled={isNaN(servings)}>
          <AddShoppingCartIcon />&nbsp;Add all to cart
        </MediumDefaultButton>}
      </FlexRowVCentred>
      <IngredientsListingGrid useThreeCols={token !== null && token !== ''}>
      {data.ingredients.map((ingredient, index) => (
        <SingleIngredient key={index} ingredient={ingredient}
          reqImperial={reqImperial} addToCart={addOneToCart} token={token} />
      ))}
      </IngredientsListingGrid>
    </IngredientsListingContainer>
    <AlertToast content={toastMessage} setContent={setToastMessage}
      state={toastState} />
  </>);
};
