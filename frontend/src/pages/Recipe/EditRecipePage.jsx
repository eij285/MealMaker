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
  Select,
  Typography
} from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { TextInput, NumericInput } from '../../components/InputFields';
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

  const token = React.useContext(GlobalContext).token;
  const [recipeName, setRecipeName] = React.useState('');
  const [desciption, setDesciption] = React.useState('');
  const [recipePhoto, setRecipePhoto] = React.useState('');
  const [recipeStatus, setRecipeStatus] = React.useState('draft');
  const [method, setMethod] = React.useState('');
  const [createdOn, setCreatedOn] = React.useState('');
  const [editedOn, setEditedOn] = React.useState('');
  const [prepHours, setPrepHours] = React.useState(0);
  const [prepMinutes, setPrepMinutes] = React.useState(30);
  const [servings, setServings] = React.useState(4);
  const [energy, setEnergy] = React.useState(null);
  const [protein, setProtein] = React.useState(null);
  const [carbs, setCarbs] = React.useState(null);
  const [fats, setFats] = React.useState(null);
  const [cuisine, setCuisine] = React.useState(null);
  const [breakfast, setBreakfast] = React.useState(false);
  const [lunch, setLunch] = React.useState(false);
  const [dinner, setDinner] = React.useState(false);
  const [snack, setSnack] = React.useState(false);
  const [vegetarian, setVegetarian] = React.useState(false);
  const [vegan, setVegan] = React.useState(false);
  const [kosher, setKosher] = React.useState(false);
  const [halal, setHalal] = React.useState(false);
  const [dairyFree, setDairyFree] = React.useState(false);
  const [glutenFree, setGlutenFree] = React.useState(false);
  const [nutFree, setNutFree] = React.useState(false);
  const [eggFree, setEggFree] = React.useState(false);
  const [shellfishFree, setShellfishFree] = React.useState(false);
  const [soyFree, setSoyFree] = React.useState(false);
  
  const loadRecipeData = (data) => {
    setRecipeName(data.recipe_name);
    setDesciption(data.recipe_description);
    setRecipePhoto(data.recipe_photo);
    setRecipeStatus(data.recipe_status);
    setMethod(data.recipe_method);
    setCreatedOn(data.created_on);
    setEditedOn(data.edited_on);
    setPrepHours(data.preparation_hours);
    setPrepMinutes(data.preparation_minutes);
    setServings(data.servings);
    setEnergy(data.energy);
    setProtein(data.protein);
    setCarbs(data.carbohydrates);
    setFats(data.fats);
    setCuisine(data.cuisine);
    setBreakfast(data.breakfast);
    setLunch(data.lunch);
    setDinner(data.dinner);
    setSnack(data.snack);
    setVegetarian(data.vegetarian);
    setVegan(data.vegan);
    setKosher(data.kosher);
    setHalal(data.halal);
    setDairyFree(data.dairy_free);
    setGlutenFree(data.gluten_free);
    setNutFree(data.nut_free);
    setEggFree(data.egg_free);
    setShellfishFree(data.shellfish_free);
    setSoyFree(data.soy_free);
  };

  React.useEffect(() => {
    const body = {
      recipe_id: recipeId
    };
    backendRequest('/recipe/edit', body, 'POST', token, (data) => {
      loadRecipeData(data);
    }, (error) => {
      //setResponseError(error);
    });
  }, [token]);

  const updateRecipe = (e) => {
    e.preventDefault();
    
    /*const body = {
      name: recipeName,
      desciption: desciption,
      status: recipeStatus,
      method: method,
      servings: servings
    };
    backendRequest('/recipe/create', body, 'POST', token, (data) => {
      
    }, (error) => {
      
    });*/
  };

  return (
    <ManageLayout>
      <Grid item xl={6} lg={8} md={10} sm={12} xs={12}>
        <PageTitle>Edit Recipe</PageTitle>
        <FlexColumn>
          <CentredElementsForm noValidate onSubmit={updateRecipe}>
            {/*<TextInput
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
                value={fats}
                onChange={(e) => setFats(e.target.value)}
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
            <FormGroup>
              <SubPageTitle>Meal Suitability</SubPageTitle>
              <FlexRowWrap>
                <FormControlLabel label="Breakfast" control={
                  <Checkbox checked={breakfast} onChange={(e) => setBreakfast(e.target.checked)} />}  />
                <FormControlLabel label="Lunch" control={
                  <Checkbox checked={lunch} onChange={(e) => setLunch(e.target.checked)} />} />
                <FormControlLabel label="Dinner" control={
                  <Checkbox checked={dinner} onChange={(e) => setDinner(e.target.checked)} />} />
                <FormControlLabel label="Snack" control={
                  <Checkbox checked={snack} onChange={(e) => setSnack(e.target.checked)} />} />
              </FlexRowWrap>
            </FormGroup>
            <FormGroup>
              <SubPageTitle>Dietary Attributes</SubPageTitle>
              <FlexRowWrap>
                <FormControlLabel label="Vegetarian" control={
                  <Checkbox checked={vegetarian} onChange={(e) => setVegetarian(e.target.checked)} />}  />
                <FormControlLabel label="Vegan" control={
                  <Checkbox checked={vegan} onChange={(e) => setVegan(e.target.checked)} />}  />
                <FormControlLabel label="Kosher" control={
                  <Checkbox checked={kosher} onChange={(e) => setKosher(e.target.checked)} />}  />
                <FormControlLabel label="Halal" control={
                  <Checkbox checked={halal} onChange={(e) => setHalal(e.target.checked)} />}  />
                <FormControlLabel label="Dairy Free" control={
                  <Checkbox checked={dairyFree} onChange={(e) => setDairyFree(e.target.checked)} />}  />
                <FormControlLabel label="Gluten Free" control={
                  <Checkbox checked={glutenFree} onChange={(e) => setGlutenFree(e.target.checked)} />}  />
                <FormControlLabel label="Nut Free" control={
                  <Checkbox checked={nutFree} onChange={(e) => setNutFree(e.target.checked)} />}  />
                <FormControlLabel label="Egg Free" control={
                  <Checkbox checked={eggFree} onChange={(e) => setEggFree(e.target.checked)} />}  />
                <FormControlLabel label="Shellfish Free" control={
                  <Checkbox checked={shellfishFree} onChange={(e) => setShellfishFree(e.target.checked)} />}  />
                <FormControlLabel label="Soy Free" control={
                  <Checkbox checked={soyFree} onChange={(e) => setSoyFree(e.target.checked)} />} />
              </FlexRowWrap>
                </FormGroup>*/}
            <FlexRow>
              <LeftAlignedSubmitButton>
                Update Recipe
              </LeftAlignedSubmitButton>
            </FlexRow>
          </CentredElementsForm>
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default EditRecipePage;
