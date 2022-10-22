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
import { ErrorAlert, FlexColumn, FlexRow } from '../../components/StyledNodes';
import { LeftAlignedSubmitButton } from '../../components/Buttons';
import { backendRequest, validateServings } from '../../helpers';

function ViewRecipePage () {
  const { recipeId } = useParams();
  const globals = React.useContext(GlobalContext);
  const token = globals.token;

  const loadRecipe = () => {
    const body = {
      recipe_id: recipeId
    };
    backendRequest('/recipe/details', body, 'POST', token, (data) => {
      console.log(data);
    }, (error) => {
      console.log(error);
    });
  };

  React.useEffect(() => {
    loadRecipe();
  }, [recipeId, token]);

  return (
    <ExploreLayout>
      <FlexColumn>
        <Box>
          <PageTitle>View Recipe</PageTitle>
          <SubPageTitle>Cuisine</SubPageTitle>
        </Box>
      </FlexColumn>
    </ExploreLayout>
  );
}

export default ViewRecipePage;
