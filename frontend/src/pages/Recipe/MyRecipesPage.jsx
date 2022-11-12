import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Grid,
  Typography,
} from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { PageTitle } from '../../components/TextNodes';
import {
  ConfirmationDialog,
  FlexColumn,
  FlexRow,
  ErrorAlert,
  SuccessAlert
} from '../../components/StyledNodes';
import { OwnRecipeItem } from '../../components/Recipe/RecipeItems';
import { LeftAlignedButton } from '../../components/Buttons';
import { backendRequest } from '../../helpers';

function MyRecipesPage () {
  const token = React.useContext(GlobalContext).token;
  const [numPublished, setNumPublished] = React.useState(0);
  const [totalRecipes, setTotalRecipes] = React.useState(0);
  const [recipesList, setRecipesList] = React.useState([]);

  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [deleteIndex, setDeleteIndex] = React.useState(-1);
  const [deleteDescription, setDeleteDesciption] = React.useState("");

  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const loadRecipes = () => {
    backendRequest('/recipes/fetch-own', {}, 'POST', token, (data) => {
      setRecipesList([...data.body]);
      setNumPublished(data.body.filter(recipe => 
        recipe.recipe_status === 'published').length);
      setTotalRecipes(data.body.length);
    }, (error) => {
      setResponseError(error);
    });
  };

  const cloneRecipe = (index) => {
    const recipeId = recipesList[index].recipe_id;
    const body = {
      recipe_id: recipeId
    };
    backendRequest('/recipe/clone', body, 'POST', token, (data) => {
      loadRecipes();
      setResponseSuccess(
        `Successfully cloned recipe (New recipe id: ${data.body.recipe_id})`);
    }, (error) => {
      setResponseError(error);
    });
  };

  const deleteRecipe = () => {
    const recipeId = recipesList[deleteIndex].recipe_id;
    const body = {
      recipe_id: recipeId
    };
    backendRequest('/recipe/delete', body, 'POST', token, (data) => {
      loadRecipes();
      setResponseSuccess(
        `Successfully deleted recipe (recipe id: ${data.body.recipe_id})`);
    }, (error) => {
      setResponseError(error);
    });
    setDialogOpen(false);
  };

  const publishRecipe = (index) => {
    const recipeId = recipesList[index].recipe_id;
    const isPublished = recipesList[index].recipe_status === 'published';
    const reqURL = isPublished ? '/recipe/unpublish' : '/recipe/publish';
    const body = {  
      recipe_id: recipeId
    };
    backendRequest(reqURL, body, 'PUT', token, (data) => {
      loadRecipes();
    }, (error) => {
      setResponseError(error);
    });
    console.log(index);
  };

  React.useEffect(() => {
    loadRecipes();
  }, [token]);

  React.useEffect(() => {
    if (!dialogOpen) {
      setDeleteIndex(-1);
    }
  }, [dialogOpen, deleteIndex]);

  return (
    <ManageLayout>
      <Grid item xs={12}>
        <PageTitle>My Recipes</PageTitle>
        <FlexColumn>
          {responseSuccess !== '' &&
          <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
          {responseError !== '' &&
          <ErrorAlert message={responseError} setMessage={setResponseError} />}
          <Box>
            <Typography>Published: {numPublished}</Typography>
            <Typography>Total: {totalRecipes}</Typography>
          </Box>
          <FlexRow>
            <LeftAlignedButton component={RouterLink} to="/create-recipe">
              Create Recipe
            </LeftAlignedButton>
          </FlexRow>
          <Grid container spacing={2}>
            {recipesList.length > 0 && recipesList.map((recipe, index) => (
            <Grid item xl={3} lg={4} md={6} sm={6} xs={12} key={index}>
              <OwnRecipeItem data={recipe} index={index} 
                cloneRecipe={cloneRecipe} setDeleteIndex={setDeleteIndex}
                setDialogOpen={setDialogOpen}
                setDeleteDesciption={setDeleteDesciption}
                publishRecipe={publishRecipe}
              />
            </Grid>))}
          </Grid>
        </FlexColumn>
      </Grid>
      <ConfirmationDialog title="Confirm deletion of:"
        description={deleteDescription}
        acceptContent="Delete" rejectContent="Cancel" openState={dialogOpen}
        setOpenState={setDialogOpen} execOnAccept={deleteRecipe} />
    </ManageLayout>
  );
}

export default MyRecipesPage;
