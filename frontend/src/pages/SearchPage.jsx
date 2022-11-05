import React from 'react';
import { useParams } from 'react-router-dom';
import { Grid } from '@mui/material';
import GlobalContext from '../utils/GlobalContext';
import ExploreLayout from '../components/Layout/ExploreLayout';
import { backendRequest, filterRecipes } from '../helpers';
import {
  ErrorAlert,
  FlexColumn,
  UserPreferencesComponent
} from '../components/StyledNodes';
import { PageTitle } from '../components/TextNodes';
import { RecipeItem } from '../components/Recipe/RecipeItems';


function SearchPage () {
  const { query } = useParams();
  const searchTerm = typeof query !== 'undefined' ? query : '';

  const userPreferences = React.useContext(GlobalContext).userPreferences;
  const [allRecipes, setAllRecipes] = React.useState([]);
  const [recipes, setRecipes] = React.useState([]);
  const [responseError, setResponseError] = React.useState('');

  const loadResults = () => {
    const reqURL = `/search?search_term=${searchTerm}`;
    backendRequest(reqURL, null, 'GET', null, (data) => {
      const body = data.body;
      if (Array.isArray(body) && body.length > 0) {
        setAllRecipes([...body]);
        filterRecipes(userPreferences, [...body], setRecipes);
      }
    }, (error) => {
      setResponseError(error);
    });
  };

  React.useEffect(() => {
    loadResults();
  }, [searchTerm]);

  React.useEffect(() => {
    filterRecipes(userPreferences, allRecipes, setRecipes);
  }, [userPreferences]);

  return (
    <ExploreLayout>
      <UserPreferencesComponent />
      <PageTitle>Search: {searchTerm}</PageTitle>
      <FlexColumn>
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
        <Grid>
          <Grid container spacing={2}>
            {recipes.map((recipe, index) => (
            <Grid item xl={3} lg={4} md={6} sm={6} xs={12} key={index}>
              <RecipeItem recipe={recipe} level={userPreferences.efficiency} />
            </Grid>))}
          </Grid>
        </Grid>
      </FlexColumn>
    </ExploreLayout>
  );
}

export default SearchPage;
