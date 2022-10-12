import React from 'react';
import { Checkbox, FormControlLabel, FormControl, FormGroup, Grid, InputLabel, MenuItem, Select } from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { TextInput } from '../../components/InputFields';
import { CentredElementsForm } from '../../components/Forms';
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import { FlexColumn, FlexRow, FlexRowWrap } from '../../components/StyledNodes';
import { LeftAlignedSubmitButton } from '../../components/Buttons';

function UserPreferencesPage () {
  const token = React.useContext(GlobalContext).token;
  return (
    <ManageLayout>
      <Grid item xl={4} lg={6} md={8} sm={10} xs={12}>
        <PageTitle>User Preferences</PageTitle>
        <FlexColumn>
          <CentredElementsForm noValidate>
            <FormGroup>
              <SubPageTitle>Recommended Meals</SubPageTitle>
              <FlexRowWrap>
                <FormControlLabel control={<Checkbox />} label="Breakfast" />
                <FormControlLabel control={<Checkbox />} label="Lunch" />
                <FormControlLabel control={<Checkbox />} label="Dinner" />
                <FormControlLabel control={<Checkbox />} label="Snack" />
              </FlexRowWrap>
            </FormGroup>
            <FormGroup>
              <SubPageTitle>Dietary Needs</SubPageTitle>
              <FlexRowWrap>
                <FormControlLabel control={<Checkbox />} label="Vegetarian" />
                <FormControlLabel control={<Checkbox />} label="Vegan" />
                <FormControlLabel control={<Checkbox />} label="Kosher" />
                <FormControlLabel control={<Checkbox />} label="Halal" />
                <FormControlLabel control={<Checkbox />} label="Dairy Free" />
                <FormControlLabel control={<Checkbox />} label="Gluten Free" />
                <FormControlLabel control={<Checkbox />} label="Nut Free" />
                <FormControlLabel control={<Checkbox />} label="Egg Free" />
                <FormControlLabel control={<Checkbox />} label="Shellfish Free" />
                <FormControlLabel control={<Checkbox />} label="Soy Free" />
              </FlexRowWrap>
            </FormGroup>
            <Grid container spacing={2} sx={{ mt: 2 }}>
              <Grid item sm={6} xs={12}>
                <FormControl fullWidth>
                  <InputLabel id="cooking-efficiency">Cooking Efficiency</InputLabel>
                  <Select labelId="cooking-efficiency" label="Cooking Efficiency" value="Intermediate">
                    <MenuItem value="Beginner">Beginner</MenuItem>
                    <MenuItem selected value="Intermediate">Intermediate</MenuItem>
                    <MenuItem value="Expert">Expert</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item sm={6} xs={12}>
                <FormControl fullWidth>
                  <InputLabel id="measuring-unit">Measuring Unit</InputLabel>
                  <Select labelId="measuring-unit" label="Measuring Unit" value="Metric">
                    <MenuItem selected value="Metric">Metric</MenuItem>
                    <MenuItem value="Imperial">Imperial</MenuItem>
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
