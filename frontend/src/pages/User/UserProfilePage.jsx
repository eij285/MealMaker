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
import { backendRequest } from '../../helpers';
const config = require('../../config.json');

function UserProfilePage () {
  const token = React.useContext(GlobalContext).token;

  const [pronoun, setPronoun] = React.useState('Mr');
  const [givenNames, setGivenNames] = React.useState('');
  const [lastName, setLastName] = React.useState('');
  const [displayName, setDisplayName] = React.useState('noone');
  const [email, setEmail] = React.useState('someone@nowhere.com');
  const [country, setCountry] = React.useState('Australia');
  const [about, setAbout] = React.useState('');
  const [visibility, setVisibility] = React.useState('private');

  React.useEffect(() => {
    backendRequest('/user/info', {}, 'GET', token, (data) => {
      console.log(data);
    }, (error) => {
    });
  }, []);

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
                <Select value={pronoun} onChange={(e) => setPronoun(e.target.value)}>
                {config.PRONOUNS.map((value, index) => (
                  <MenuItem key={index} value={value}>{value}</MenuItem>
                ))}
                </Select>
              </FormControl>
              <TextInput label="Given Name(s)" onChange={(e) => setGivenNames(e.target.value)} />
              <TextInput label="Last Name" onChange={(e) => setLastName(e.target.value)} />
            </FlexRow>
            <TextInput label="Display Name" required onChange={(e) => setDisplayName(e.target.value)} />
            <EmailInput label="Email" required onChange={(e) => setEmail(e.target.value)} />
            <FormControl fullWidth>
              <InputLabel id="user-country-select">Country</InputLabel>
              <Select labelId="user-country-select" label="Country"
                value={country} onChange={(e) => setCountry(e.target.value)}>
              {config.COUNTRIES.map((dataItem, index) => (
                <MenuItem key={index} value={dataItem}>
                  {dataItem}
                </MenuItem>
              ))}
              </Select>
            </FormControl>
            <TextInput label="About Me" multiline minRows={5} onChange={(e) => setAbout(e.target.value)} />
            <FlexRow>
              <FormControl>
                <InputLabel id="user-visibility">Visibility</InputLabel>
                <Select labelId="user-visibility" label="Visibility"
                  value={visibility} onChange={(e) => setVisibility(e.target.value)}>
                  <MenuItem value="private">private</MenuItem>
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
