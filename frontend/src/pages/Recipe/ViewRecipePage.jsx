import React from 'react';
import { useNavigate, useParams, Link as RouterLink } from 'react-router-dom';
import {
  Box,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
} from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ExploreLayout from '../../components/Layout/ExploreLayout';
import { CentredElementsForm } from '../../components/Forms';
import { PageTitle, SubPageTitleNoMargins } from '../../components/TextNodes';
import {
  ErrorAlert,
  FlexColumn,
  FlexRow,
  FlexRowWrapSpaced,
  UserImageNameLink,
  WYSIWYGOutput
} from '../../components/StyledNodes';
import {
  RightAlignMedButton,
  SmallAlternateButton
} from '../../components/Buttons';
import {
  IngredientsListing,
  MealSuitabilityTags,
  RecipeImg,
  RecipeInfoPanel,
  RecipeLikes,
  RecipeRating
} from '../../components/Recipe/RecipeNodes';
import { backendRequest, formatNumString } from '../../helpers';
import RecipeReviews from '../../components/Recipe/RecipeReviews';

function ViewRecipePage () {
  const { recipeId } = useParams();
  const globals = React.useContext(GlobalContext);
  const token = globals.token;
  const [recipeData, setRecipeData] = React.useState({});
  const [currData, setCurrData] = React.useState({
    servings: '4',
    energy: -1,
    protein: -1,
    carbohydrates: -1,
    fats: -1,
    ingredients: [],
    likes: {
      likesCount: 0,
      hasLiked: false
    }
  });
  const [servings, setServings] = React.useState('4');
  const [responseError, setResponseError] = React.useState('');

  const initCurrData = (data) => {
    setCurrData({
      servings: `${data.servings}`,
      energy: data.energy === null ? -1 : data.energy,
      protein: data.protein === null ? -1 : data.protein,
      carbohydrates: data.carbohydrates === null ? -1 : data.carbohydrates,
      fats: data.fats === null ? -1 : data.fats,
      ingredients: [...data.ingredients],
      likes: {
        likesCount: data.likes.likes_count,
        hasLiked: data.likes.has_liked
      }
    });
  };

  const calcPortion = (origServes, origValue, currServes) => {
    if (isNaN(origServes) || isNaN(origValue) || isNaN(currServes) || 
      parseInt(currServes) < 1 || parseInt(origValue) < 1) {
      return -1;
    }
    return origValue * (currServes / origServes);
  };

  const updateCurrData = () => {
    if (Object.keys(recipeData).length === 0) {
      return;
    }
    let ingredients = [];
    for (let ing of recipeData.ingredients) {
      ingredients.push({
        ingredient_id: ing.ingredient_id,
        ingredient_name: ing.ingredient_name,
        quantity: calcPortion(recipeData.servings, ing.quantity, servings),
        unit: ing.unit
      });
    }
    setCurrData({
      servings: servings,
      energy: calcPortion(recipeData.servings, recipeData.energy, servings),
      protein: calcPortion(recipeData.servings, recipeData.protein, servings),
      carbohydrates: calcPortion(recipeData.servings, recipeData.carbohydrates, servings),
      fats: calcPortion(recipeData.servings, recipeData.fats, servings),
      ingredients: [...ingredients],
      likes: {
        likesCount: recipeData.likes.likes_count,
        hasLiked: recipeData.likes.has_liked
      }
    });
  };

  const loadRecipe = () => {
    const body = {
      recipe_id: recipeId
    };
    const reqURL = '/recipe/details' + (token ? '' : `?recipe_id=${recipeId}`);
    const reqMethod = token ? 'POST' : 'GET';

    backendRequest(reqURL, body, reqMethod, token, (data) => {
      const body = data.body;
      setRecipeData({...body});
      setServings(`${body.servings}`);
      initCurrData(body);
      console.log(body);
    }, (error) => {
      setResponseError(error);
    });
  };

  const likeRecipe = () => {
    const body = {
      recipe_id: recipeId
    };
    backendRequest('/recipe/like', body, 'POST', token, (data) => {
      setCurrData({
        ...currData,
        likes: {
          likesCount: data.body.likes_count,
          hasLiked: data.body.has_liked
        }
      });
    }, (error) => {
      setResponseError(error);
    });
  };

  const subscribeToUser = () => {
    // backend needs fixing - delete request cannot have a body
    /*const reqURL = `/user/${recipeData.is_subscribed?'unsubscribe':'subscribe'}`;
    const reqMethod = recipeData.is_subscribed ? 'DELETE' : 'PUT';
    const body = {
      id: recipeData.author_id
    };
    backendRequest(reqURL, body, reqMethod, token, (data) => {
      console.log(data);
    }, (error) => {
      setResponseError(error);
    });*/
  };

  React.useEffect(() => {
    updateCurrData();
  }, [servings]);

  React.useEffect(() => {
    loadRecipe();
  }, [recipeId, token]);

  return (
    <ExploreLayout>
      <FlexColumn>
        {responseError !== '' &&
        <Box mt={2}>
          <ErrorAlert message={responseError} setMessage={setResponseError} />
        </Box>}
        {Object.keys(recipeData).length > 0 &&<>
        <Box>
          <FlexRowWrapSpaced>
            <PageTitle>{recipeData.recipe_name}</PageTitle>
            {recipeData.user_is_author &&
            <RightAlignMedButton component={RouterLink}
              to={`/edit-recipe/${recipeId}`}>
              Edit Recipe
            </RightAlignMedButton>}
          </FlexRowWrapSpaced>
          {recipeData.cuisine &&
          <SubPageTitleNoMargins>{recipeData.cuisine}</SubPageTitleNoMargins>}
          <RecipeImg src={recipeData.recipe_photo} alt={recipeData.recipe_name} />
          <FlexRowWrapSpaced>
            <FlexRow>
              <RecipeRating reviews={recipeData.reviews} />
              <RecipeLikes likesObject={currData.likes} likeRecipe={likeRecipe} />
            </FlexRow>
            <FlexRow>
              <UserImageNameLink src={recipeData.author_image}
                name={recipeData.author_display_name}
                to={`/user/${recipeData.author_id}`} />
              {token && !recipeData.user_is_author &&
              <SmallAlternateButton onClick={subscribeToUser}>
                {!recipeData.is_subscribed && <>Subscribe</>}
                {recipeData.is_subscribed && <>Unubscribe</>}
              </SmallAlternateButton>}
            </FlexRow>
          </FlexRowWrapSpaced>
          <RecipeInfoPanel data={recipeData} currData={currData} 
            setServings={setServings} />
        </Box>
        <MealSuitabilityTags data={recipeData} />
        <IngredientsListing data={currData}
          reqImperial={recipeData.units === 'Imperial'} />
        <Box>
          <SubPageTitleNoMargins>Method</SubPageTitleNoMargins>
          <WYSIWYGOutput>{recipeData.recipe_method}</WYSIWYGOutput>
        </Box>
        <RecipeReviews recipeId={recipeId} recipeData={recipeData}
          setRecipeData={setRecipeData} /></>}
      </FlexColumn>
    </ExploreLayout>
  );
}

export default ViewRecipePage;
