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
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import { ErrorAlert, FlexColumn, FlexRow, FlexRowWrapSpaced, UserImageNameLink } from '../../components/StyledNodes';
import { RightAlignMedButton, SmallAlternateButton } from '../../components/Buttons';
import { RecipeImg, RecipeInfoPanel, RecipeLikes, RecipeRating } from '../../components/Recipe/RecipeNodes';
import { backendRequest, validateServings } from '../../helpers';

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

  const initCurrData = (data) => {
    setCurrData({
      servings: `${data.servings}`,
      energy: data.energy === null ? -1 : data.energy,
      protein: data.protein === null ? -1 : data.protein,
      carbohydrates: data.carbohydrates === null ? -1 : data.carbohydrates,
      fats: data.fats === null ? -1 : data.fats,
      ingredients: data.ingredients,
      likes: {
        likesCount: data.likes.likes_count,
        hasLiked: data.likes.has_liked
      }
    });
    console.log(currData);
  };

  const calcPortion = (origServes, currServes, value) => {
    if (isNaN(origServes) || isNaN(currServes), isNaN(value)) {
      return -1;
    }
  };

  const updateCurrData = () => {
    if (Object.keys(recipeData).length === 0) {
      return;
    }
    const validServings = !isNaN(servings);
    setCurrData({
      servings: servings,
      energy: -1,
      protein: -1,
      carbohydrates: -1,
      fats: -1,
      ingredients: [],
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
    }, (error) => {
      console.log(error);
    });
  };

  const likeRecipe = () => {
    console.log('like');
  };

  const subscribeToUser = () => {
    console.log('subscribe');
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
        {Object.keys(recipeData).length > 0 &&
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
          <SubPageTitle>{recipeData.cuisine}</SubPageTitle>}
          <RecipeImg src={recipeData.recipe_photo} alt={recipeData.recipe_name} />
          <FlexRowWrapSpaced>
            <FlexRow>
              <RecipeRating reviews={recipeData.reviews} />
              <RecipeLikes likesObject={recipeData.likes} likeRecipe={likeRecipe} />
            </FlexRow>
            <FlexRow>
              <UserImageNameLink src={recipeData.author_image}
                name={recipeData.author_display_name}
                to={`/user/${recipeData.author_id}`} />
              {token && recipeData.user_is_author &&
              <SmallAlternateButton onClick={subscribeToUser}>
                Subscribe
              </SmallAlternateButton>}
            </FlexRow>
          </FlexRowWrapSpaced>
          <RecipeInfoPanel data={recipeData} currData={currData} 
            setServings={setServings} />
        </Box>}
      </FlexColumn>
    </ExploreLayout>
  );
}

export default ViewRecipePage;
