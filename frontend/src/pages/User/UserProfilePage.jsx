import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Divider, Grid, FormControl, InputLabel, MenuItem, Select } from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { EmailInput, TextInput } from '../../components/InputFields';
import { CentredElementsForm } from '../../components/Forms';
import { PageTitle } from '../../components/TextNodes';
import { FlexColumn, FlexRow } from '../../components/StyledNodes';
import { LeftAlignedButton, LeftAlignedSubmitButton } from '../../components/Buttons';

function UserProfilePage () {
  const token = React.useContext(GlobalContext).token;
  return (
    <ManageLayout>
      <Grid item xl={6} lg={8} md={10} sm={12} xs={12}>
        <PageTitle>User Profile</PageTitle>
        <FlexColumn>
          <FlexRow>
            <LeftAlignedButton component={RouterLink} to="/update-password">
              Update Password
            </LeftAlignedButton>
          </FlexRow>
          <Divider />
          <CentredElementsForm noValidate>
            <FlexRow>
              <FormControl sx={{ minWidth: '80px' }}>
                <Select value="Mr">
                  <MenuItem selected value="Mr">Mr</MenuItem>
                  <MenuItem value="Ms">Ms</MenuItem>
                  <MenuItem value="Mrs">Mrs</MenuItem>
                  <MenuItem value="Miss">Miss</MenuItem>
                  <MenuItem value="Dr">Dr</MenuItem>
                </Select>
              </FormControl>
              <TextInput label="Given Name(s)" />
              <TextInput label="Surname" />
            </FlexRow>
            <TextInput label="Display Name" required />
            <EmailInput label="Email" required />
            <FormControl fullWidth>
              <InputLabel id="user-country-select">Country</InputLabel>
              <Select labelId="user-country-select" label="Country">
                <MenuItem selected value="Australia">Australia</MenuItem>
                <MenuItem value="USA">USA</MenuItem>
              </Select>
            </FormControl>
            <TextInput label="About Me" multiline minRows={5} />
            <FlexRow>
              <FormControl>
                <InputLabel id="user-visibility">Visibility</InputLabel>
                <Select value="private" label="Visibility">
                  <MenuItem selected value="private">private</MenuItem>
                  <MenuItem value="public">public</MenuItem>
                </Select>
              </FormControl>
            </FlexRow>
            <FlexRow>
              <LeftAlignedSubmitButton>
                Update Profile
              </LeftAlignedSubmitButton>
            </FlexRow>
          </CentredElementsForm>
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default UserProfilePage;
