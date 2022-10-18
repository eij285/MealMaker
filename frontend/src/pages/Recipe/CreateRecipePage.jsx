import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Typography
} from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { TextInput, NumericInput } from '../../components/InputFields';
import { CentredElementsForm } from '../../components/Forms';
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import { ErrorAlert, FlexColumn, FlexRow } from '../../components/StyledNodes';
import { LeftAlignedSubmitButton } from '../../components/Buttons';
import { backendRequest, isPositiveInteger } from '../../helpers';

function CreateRecipePage () {
  const token = React.useContext(GlobalContext).token;
  const [recipeName, setRecipeName] = React.useState('');
  const [recipeNameMessage, setRecipeNameMessage] = React.useState('');
  const [description, setDescription] = React.useState('');
  const [descriptionMessage, setDescriptionMessage] = React.useState('');
  const [servings, setServings] = React.useState(4);
  const [servingsMessage, setServingsMessage] = React.useState('');
  const [recipeStatus, setRecipeStatus] = React.useState('draft');

  const [responseError, setResponseError] = React.useState('');

  const navigate = useNavigate();

  const validateServings = (value) => {
    if (value === '') {
      setServingsMessage('Servings required');
    } else if (!isPositiveInteger(value)) {
      setServingsMessage('Servings requires positive integer');
    } else {
      setServingsMessage('');
    }
  };

  const createRecipe = (e) => {
    e.preventDefault();
    // value cannot be blank and message must be blank
    if (recipeName !== '' && recipeNameMessage === '' && 
        description !== '' && descriptionMessage === '' &&
        servings > 0 && servingsMessage === '') {
      // send to backend
      const body = {
        name: recipeName,
        description: description,
        servings: servings,
        recipe_status: recipeStatus,
      };
      backendRequest('/recipe/create', body, 'POST', token, (data) => {
        const recipeId = data.body.recipe_id;
        navigate(`/edit-recipe/${recipeId}`);
      }, (error) => {
        setResponseError(error);
      });
    } else {
      setRecipeNameMessage(recipeName?'':'Recipe name required');
      setDescriptionMessage(description?'':'Recipe description required');
      validateServings();
    }
  };

  return (
    <ManageLayout>
      <Grid item xl={6} lg={8} md={10} sm={12} xs={12} spacing={2}>
        <PageTitle>Create Recipe</PageTitle>
        <FlexColumn>
          {responseError !== '' &&
          <ErrorAlert message={responseError} setMessage={setResponseError} />}
          <CentredElementsForm noValidate onSubmit={createRecipe}>
            <TextInput
              label="Recipe Name"
              required
              value={recipeName}
              onChange={(e) => setRecipeName(e.target.value)}
              onBlur={(e) =>
                setRecipeNameMessage(e.target.value?'':'Recipe name required')}
              error={recipeNameMessage !== ''}
              helperText={recipeNameMessage}
            />
            <TextInput
              label="Description"
              multiline
              minRows={5}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              onBlur={(e) =>
                setDescriptionMessage(e.target.value?'':'Recipe description required')}
              error={descriptionMessage !== ''}
              helperText={descriptionMessage}
            />
            <NumericInput
              label="Servings"
              required
              value={servings}
              onChange={(e) => setServings(e.target.value)}
              onBlur={(e) => validateServings(e.target.value)}
              error={servingsMessage !== ''}
              helperText={servingsMessage}
            />
            <FlexRow>
              <FormControl>
                <InputLabel id="recipe-status">Status</InputLabel>
                <Select labelId="recipe-status" label="Status"
                  sx={{ width: '150px' }}
                  value={recipeStatus}
                  onChange={(e) => setRecipeStatus(e.target.value)}>
                  <MenuItem value="draft">draft</MenuItem>
                  <MenuItem value="published">published</MenuItem>
                </Select>
              </FormControl>
            </FlexRow>
            <FlexRow>
              <LeftAlignedSubmitButton>
                Create Recipe
              </LeftAlignedSubmitButton>
            </FlexRow>
          </CentredElementsForm>
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default CreateRecipePage;
