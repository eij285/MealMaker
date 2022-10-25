import React from 'react';
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
const config = require('../../config.json');

function UserPreferencesPage () {
  const token = React.useContext(GlobalContext).token;

  const [breakfast, setBreakfast] = React.useState(true);
  const [lunch, setLunch] = React.useState(true);
  const [dinner, setDinner] = React.useState(true);
  const [snack, setSnack] = React.useState(true);

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

  const [efficiency, setEfficiency] = React.useState(config.EFFICIENCY[1]);
  const [measuringUnits, setMeasuringUnits] = React.useState(config.UNITS[0]);

  // response messages
  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const loadPreferences = (data) => {
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
    setEfficiency(data.efficiency);
    setMeasuringUnits(data.units);
  };

  React.useEffect(() => {
    backendRequest('/user/preferences', {}, 'POST', token, (data) => {
      loadPreferences(data);
    }, (error) => {
      setResponseError(error);
    });
  }, [token]);

  const updatePreferences = (e) => {
    e.preventDefault();

    const body = {
      breakfast: breakfast,
      lunch: lunch,
      dinner: dinner,
      snack: snack,
      vegetarian: vegetarian,
      vegan: vegan,
      kosher: kosher,
      halal: halal,
      dairy_free: dairyFree,
      gluten_free: glutenFree,
      nut_free: nutFree,
      egg_free: eggFree,
      shellfish_free: shellfishFree,
      soy_free: soyFree,
      efficiency: efficiency,
      units: measuringUnits,
    };
    backendRequest('/user/preferences/update', body, 'PUT', token, (data) => {
      setResponseSuccess('Details Updated Successfully');
    }, (error) => {
      setResponseError(error);
    });
  }

  return (
    <ManageLayout>
      <Grid item xl={4} lg={6} md={8} sm={10} xs={12}>
        <PageTitle>User Preferences</PageTitle>
        <FlexColumn>
          {responseSuccess !== '' &&
          <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
          {responseSuccess === '' && responseError !== '' &&
          <ErrorAlert message={responseError} setMessage={setResponseError} />}
          <CentredElementsForm noValidate onSubmit={updatePreferences}>
            <FormGroup>
              <SubPageTitle>Recommended Meals</SubPageTitle>
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
              <SubPageTitle>Dietary Needs</SubPageTitle>
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
            </FormGroup>
            <Grid container spacing={2} sx={{ mt: 2 }}>
              <Grid item sm={6} xs={12}>
                <FormControl fullWidth>
                  <InputLabel id="cooking-efficiency">Cooking Efficiency</InputLabel>
                  <Select labelId="cooking-efficiency"
                    label="Cooking Efficiency" value={efficiency}
                    onChange={(e) => setEfficiency(e.target.value)}>
                    {config.EFFICIENCY.map((dataItem, index) => (
                    <MenuItem key={index} value={dataItem}>
                      {dataItem}
                    </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item sm={6} xs={12}>
                <FormControl fullWidth>
                  <InputLabel id="measuring-unit">Measuring Unit</InputLabel>
                  <Select labelId="measuring-unit" label="Measuring Unit"
                    value={measuringUnits}
                    onChange={(e) => setMeasuringUnits(e.target.value)}>
                    {config.UNITS.map((dataItem, index) => (
                    <MenuItem key={index} value={dataItem}>
                      {dataItem}
                    </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
            <FlexRow>
              <LeftAlignedSubmitButton>
                Update Preferences
              </LeftAlignedSubmitButton>
            </FlexRow>
          </CentredElementsForm>
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default UserPreferencesPage;
