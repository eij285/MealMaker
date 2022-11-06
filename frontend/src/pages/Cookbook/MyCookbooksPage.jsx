import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Divider,
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
  // TODO: complete this page
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
          <Box>
            <Typography>Published: {1}</Typography>
            <Typography>Total: {2}</Typography>
            <Typography>Followed: {1}</Typography>
          </Box>
          <FlexRow>
            <LeftAlignedButton component={RouterLink} to="/create-cookbook">
              Create New Cook Book
            </LeftAlignedButton>
          </FlexRow>
          <Divider />
          <PageTitle>Followed Cook Books</PageTitle>
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default MyCookbooksPage;
