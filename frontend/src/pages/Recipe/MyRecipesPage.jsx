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
  FlexColumn,
  FlexRow,
} from '../../components/StyledNodes';
import { OwnRecipeItem } from '../../components/Recipe/RecipeItems';
import { LeftAlignedButton } from '../../components/Buttons';
import { backendRequest } from '../../helpers';

function MyRecipesPage () {
  const token = React.useContext(GlobalContext).token;
  const [numPublished, setNumPublished] = React.useState(0);
  const [totalRecipes, setTotalRecipes] = React.useState(0);
  const [recipesList, setRecipesList] = React.useState([]);

  const loadRecipes = () => {
    backendRequest('/recipes/fetch-own', {}, 'POST', token, (data) => {
      setRecipesList([...data.body]);
      setNumPublished(data.body.filter(recipe => 
        recipe.recipe_status === 'published').length);
      setTotalRecipes(data.body.length);
    }, (error) => {
      //setResponseError(error);
      console.log(error);
    });
  };

  React.useEffect(() => {
    loadRecipes();
  }, [token]);

  return (
    <ManageLayout>
      <Grid item xs={12}>
        <PageTitle>My Recipes</PageTitle>
        <FlexColumn>
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
              <OwnRecipeItem data={recipe} />
            </Grid>))}
          </Grid>
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default MyRecipesPage;
