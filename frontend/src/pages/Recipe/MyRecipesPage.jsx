import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Grid,
  Typography,
} from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { TextInput } from '../../components/InputFields';
import { CentredElementsForm } from '../../components/Forms';
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import {
  FlexColumn,
  FlexRow,
  FlexRowWrap,
  ErrorAlert,
  SuccessAlert
} from '../../components/StyledNodes';
import { LeftAlignedButton, LeftAlignedSubmitButton } from '../../components/Buttons';
import { backendRequest } from '../../helpers';

function MyRecipesPage () {
  const token = React.useContext(GlobalContext).token;
  const [numPublished, setNumPublished] = React.useState(0);
  const [totalRecipes, setTotalRecipes] = React.useState(0);

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
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default MyRecipesPage;
