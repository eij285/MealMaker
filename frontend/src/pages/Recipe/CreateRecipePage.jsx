import React from 'react';
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
import { FlexRow } from '../../components/StyledNodes';
import { LeftAlignedSubmitButton } from '../../components/Buttons';
import { backendRequest } from '../../helpers';

function CreateRecipePage () {
  const token = React.useContext(GlobalContext).token;
  const [recipeName, setRecipeName] = React.useState('');
  const [desciption, setDesciption] = React.useState('');
  const [recipeStatus, setRecipeStatus] = React.useState('draft');
  const [prepHours, setPrepHours] = React.useState(0);
  const [prepMinutes, setPrepMinutes] = React.useState(30);
  const [servings, setServings] = React.useState(4);
  const [energy, setEnergy] = React.useState(null);
  const [protein, setProtein] = React.useState(null);
  const [carbs, setCarbs] = React.useState(null);
  const [fat, setFat] = React.useState(null);
  const [method, setMethod] = React.useState('');

  const createRecipe = (e) => {
    e.preventDefault();
    const body = {
      name: recipeName,
      desciption: desciption,
      status: recipeStatus,
      method: method,
      servings: servings
    };
    backendRequest('/recipe/create', body, 'POST', token, (data) => {
      
    }, (error) => {
      
    });
  };

  return (
    <ManageLayout>
      <Grid item xl={6} lg={8} md={10} sm={12} xs={12}>
        <PageTitle>Create Recipe</PageTitle>
        <CentredElementsForm noValidate onSubmit={createRecipe}>
          <TextInput
            label="Recipe Name"
            required
            value={recipeName}
            onChange={(e) => setRecipeName(e.target.value)}
          />
          <TextInput
            label="Description"
            multiline
            minRows={5}
            value={desciption}
            onChange={(e) => setDesciption(e.target.value)}
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
            <Typography sx={{ whiteSpace: 'nowrap' }}>Preparation Time: </Typography>
            <NumericInput
              label="hours"
              required
              value={prepHours}
              onChange={(e) => setPrepHours(e.target.value)}
            />
            <NumericInput
              label="minutes"
              required
              value={prepMinutes}
              onChange={(e) => setPrepMinutes(e.target.value)}
            />
          </FlexRow>
          <NumericInput
            label="Servings"
            required
            value={servings}
            onChange={(e) => setServings(e.target.value)}
          />
          <FlexRow>
            <Typography sx={{ whiteSpace: 'nowrap' }}>Nutrition: </Typography>
            <NumericInput
              label="Energy"
              value={energy}
              onChange={(e) => setEnergy(e.target.value)}
            />
            <NumericInput
              label="Protein"
              value={protein}
              onChange={(e) => setProtein(e.target.value)}
            />
            <NumericInput
              label="Carbs"
              value={carbs}
              onChange={(e) => setCarbs(e.target.value)}
            />
            <NumericInput
              label="Fat"
              value={fat}
              onChange={(e) => setFat(e.target.value)}
            />
          </FlexRow>
          <TextInput
            label="Method"
            required
            multiline
            minRows={5}
            value={method}
            onChange={(e) => setMethod(e.target.value)}
          />
          <FlexRow>
            <LeftAlignedSubmitButton>
              Create Recipe
            </LeftAlignedSubmitButton>
          </FlexRow>
        </CentredElementsForm>
      </Grid>
    </ManageLayout>
  );
}

export default CreateRecipePage;
