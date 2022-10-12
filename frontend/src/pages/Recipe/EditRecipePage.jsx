import React from 'react';
import { useParams } from 'react-router-dom';
import {
  Checkbox,
  FormControlLabel,
  FormControl,
  FormGroup,
  Grid,
  InputLabel,
  MenuItem,
  Select
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
import { LeftAlignedSubmitButton } from '../../components/Buttons';
import { backendRequest } from '../../helpers';

function EditRecipePage () {
  const { recipeId } = useParams();

  return (
    <ManageLayout>
      <Grid item xl={6} lg={8} md={10} sm={12} xs={12}>
      <PageTitle>Edit Recipe {recipeId}</PageTitle>
      </Grid>
    </ManageLayout>
  );
}

export default EditRecipePage;
