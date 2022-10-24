import React from 'react';
import { useNavigate, useParams } from 'react-router-dom';
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
import { TextInput, NumericInput } from '../../components/InputFields';
import { CentredElementsForm } from '../../components/Forms';
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import { ErrorAlert, FlexColumn, FlexRow, FlexRowWrapSpaced, UserImageNameLink } from '../../components/StyledNodes';
import { LeftAlignedSubmitButton } from '../../components/Buttons';
import { RecipeImg, RecipeLikes, RecipeRating } from '../../components/Recipe/RecipeNodes';
import { backendRequest, validateServings } from '../../helpers';

function ViewRecipePage () {
  const { recipeId } = useParams();
  const globals = React.useContext(GlobalContext);
  const token = globals.token;
  const [recipeData, setRecipeData] = React.useState({});

  const loadRecipe = () => {
    const body = {
      recipe_id: recipeId
    };
    backendRequest('/recipe/details', body, 'POST', token, (data) => {
      const body = data.body;
      setRecipeData({...body});
    }, (error) => {
      console.log(error);
    });
    console.log(recipeData);
  };

  const likeRecipe = () => {

  };

  React.useEffect(() => {
    loadRecipe();
  }, [recipeId, token]);

  return (
    <ExploreLayout>
      <FlexColumn>
        {recipeData &&
        <Box>
          <PageTitle>{recipeData.recipe_name}</PageTitle>
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
            </FlexRow>
          </FlexRowWrapSpaced>
        </Box>}
      </FlexColumn>
    </ExploreLayout>
  );
}

export default ViewRecipePage;
