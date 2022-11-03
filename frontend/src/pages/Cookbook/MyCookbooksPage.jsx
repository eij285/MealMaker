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
import { LeftAlignedButton } from '../../components/Buttons';
import { backendRequest } from '../../helpers';

function MyCookbooksPage () {
  const token = React.useContext(GlobalContext).token;
  const [cookbooks, setCookbooks] = React.useState(0);

  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const loadCookbooks = () => {
    /*backendRequest('/cookbooks/', {}, 'POST', token, (data) => {
      setRecipesList([...data.body]);
      setNumPublished(data.body.filter(recipe => 
        recipe.recipe_status === 'published').length);
      setTotalRecipes(data.body.length);
    }, (error) => {
      setResponseError(error);
    });*/
  };

  React.useEffect(() => {
    loadCookbooks();
  }, [token]);

  return (
    <ManageLayout>
      <Grid item xs={12}>
        <PageTitle>My Cook Books</PageTitle>
        <FlexColumn>
          {responseSuccess !== '' &&
          <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
          {responseError !== '' &&
          <ErrorAlert message={responseError} setMessage={setResponseError} />}
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default MyCookbooksPage;
