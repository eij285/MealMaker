import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Divider,
  Grid,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  FormHelperText
} from '@mui/material';
import { CKEditor } from '@ckeditor/ckeditor5-react';
import ClassicEditor from 'ckeditor5-build-classic-base64-upload';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { EmailInput, ImageInput, TextInput } from '../../components/InputFields';
import { CentredElementsForm } from '../../components/Forms';
import { PageTitle } from '../../components/TextNodes';
import { FlexColumn, FlexRow, ErrorAlert, SuccessAlert } from '../../components/StyledNodes';
import { LeftAlignedButton, LeftAlignedSubmitButton, LeftAltButton } from '../../components/Buttons';
import { validateDisplayName, validateEmail, backendRequest, emptyStringToNull, tokenToUserId } from '../../helpers';
const config = require('../../config.json');

function UserProfilePage () {
  const globals = React.useContext(GlobalContext);
  const token = globals.token;
  const globalUserPreferences = globals.userPreferences;
  const setGlobalUserPreferences = globals.setUserPreferences;

  // user data
  const [pronoun, setPronoun] = React.useState('Mr');
  const [givenNames, setGivenNames] = React.useState('');
  const [lastName, setLastName] = React.useState('');
  const [displayName, setDisplayName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [base64Image, setBase64Image] = React.useState('');
  const [country, setCountry] = React.useState('Australia');
  const [about, setAbout] = React.useState('');
  const [visibility, setVisibility] = React.useState('private');

  // recommended meal preferences
  const [breakfast, setBreakfast] = React.useState(true);
  const [lunch, setLunch] = React.useState(true);
  const [dinner, setDinner] = React.useState(true);
  const [snack, setSnack] = React.useState(true);

  // dietary needs
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

  // user preferences
  const [efficiency, setEfficiency] = React.useState(config.EFFICIENCY[1]);
  const [measuringUnits, setMeasuringUnits] = React.useState(config.UNITS[0]);

  // error messages
  const [displayNameMessage, setDisplayNameMessage] = React.useState('');
  const [emailMessage, setEmailMessage] = React.useState('');

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

  const loadUserData = (data) => {
    setPronoun(data.pronoun ? data.pronoun : config.PRONOUNS[0]);
    setGivenNames(data.given_names ? data.given_names : '');
    setLastName(data.last_name ? data.last_name : '');
    setDisplayName(data.display_name ? data.display_name : '');
    setEmail(data.email ? data.email : '');
    setBase64Image(data.base64_image ? data.base64_image : '');
    setCountry(data.country ? data.country : config.COUNTRIES[0]);
    setAbout(data.about ? data.about : '');
    setVisibility(data.visibility ? data.visibility : 'private');
  };

  React.useEffect(() => {
    // backend request for user info
    backendRequest('/user/info', {}, 'POST', token, (data) => {
      loadUserData(data);
    }, (error) => {
      setResponseError(error);
    });
    // backend request for user preferences
    backendRequest('/user/preferences', {}, 'POST', token, (data) => {
      loadPreferences(data);
    }, (error) => {
      setResponseError(error);
    });
  }, [token]);

  const updateGlobalPreferences = (data) => {
    setGlobalUserPreferences({
      ...globalUserPreferences,
      breakfast: data.breakfast,
      lunch: data.lunch,
      dinner: data.dinner,
      snack: data.snack,
      vegetarian: data.vegetarian,
      vegan: data.vegan,
      kosher: data.kosher,
      halal: data.halal,
      dairyFree: data.dairy_free,
      glutenFree: data.gluten_free,
      nutFree: data.nut_free,
      eggFree: data.egg_free,
      shellfishFree: data.shellfish_free,
      soyFree: data.soy_free,
      efficiency: data.efficiency,
    });
  };

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
      updateGlobalPreferences(body);
    }, (error) => {
      setResponseError(error);
    });
  }

  const updateProfile = (e) => {
    e.preventDefault();

    if (displayName !== '' && displayNameMessage === '' && 
        email !== '' && emailMessage === '') {
      const body = {
        'token': token,
        'pronoun': pronoun,
        'given-names': givenNames,
        'last-name': lastName,
        'display-name': displayName,
        'email': email,
        'base64-image': emptyStringToNull(base64Image),
        'country': country,
        'about': about,
        'visibility': visibility
      };
      backendRequest('/user/update', body, 'PUT', token, (data) => {
        setResponseSuccess('Details Updated Successfully');
      }, (error) => {
        setResponseError(error);
      });
    } else {
      validateDisplayName(displayName, setDisplayNameMessage);
      validateEmail(email, setEmailMessage);
    }
  };

  return (
    <ManageLayout>
      <Grid item xl={6} lg={8} md={10} sm={12} xs={12}>
        <PageTitle>Settings</PageTitle>
        <FlexColumn>
          <FlexRow>
            <LeftAlignedButton component={RouterLink} to="/update-password">
              Update Password
            </LeftAlignedButton>
          </FlexRow>
          <Divider />
          {responseSuccess !== '' &&
          <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
          {responseSuccess === '' && responseError !== '' &&
          <ErrorAlert message={responseError} setMessage={setResponseError} />}
          <CentredElementsForm noValidate onSubmit={updateProfile}>
            <ImageInput elementTitle="Profile Image" icon={AccountCircleIcon}
              image={base64Image} setImage={setBase64Image} />
            <FlexRow>
              <FormControl sx={{ minWidth: '80px' }}>
                <Select
                  value={pronoun}
                  onChange={(e) => setPronoun(e.target.value)}>
                {config.PRONOUNS.map((value, index) => (
                  <MenuItem key={index} value={value}>{value}</MenuItem>
                ))}
                </Select>
              </FormControl>
              <TextInput
                label="Given Name(s)"
                value={givenNames}
                onChange={(e) => setGivenNames(e.target.value)}
              />
              <TextInput
                label="Last Name"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
              />
            </FlexRow>
            <TextInput
              label="Display Name"
              required
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              onBlur={() => validateDisplayName(displayName, setDisplayNameMessage)}
              error={displayNameMessage !== ''}
              helperText={displayNameMessage}
            />
            <EmailInput
              label="Email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              onBlur={() => validateEmail(email, setEmailMessage)}
              error={emailMessage !== ''}
              helperText={emailMessage}
            />
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
            <Box>
              <InputLabel>About</InputLabel>
              <CKEditor
                id="user-about"
                editor={ ClassicEditor }
                data={ about }
                config={{
                  removePlugins: ['MediaEmbed']
                }}
                onReady={ editor => {
                  editor.editing.view.change((writer) => {
                    writer.setStyle(
                        "min-height",
                        "200px",
                        editor.editing.view.document.getRoot()
                    );
                  })
                }}
                onChange={ ( _, editor ) => {
                  setAbout(editor.getData())
                }}
              />
            </Box>
            <FlexRow>
              <FormControl sx={{ width: '300px', maxWidth: '100%' }}>
                <InputLabel id="user-visibility">Visibility</InputLabel>
                <Select labelId="user-visibility" label="Visibility"
                  value={visibility}
                  onChange={(e) => setVisibility(e.target.value)}>
                  <MenuItem value="private">private</MenuItem>
                  <MenuItem value="public">public</MenuItem>
                </Select>
                {visibility === 'private' &&
                <FormHelperText sx={{color: 'warning.main'}}>
                  Warning: private profile cannot have followers
                </FormHelperText>}
              </FormControl>
            </FlexRow>
            <FlexRow>
              <LeftAlignedSubmitButton>
                Update Profile
              </LeftAlignedSubmitButton>
              <LeftAltButton component={RouterLink}
                to={`/user/${tokenToUserId(token)}`}>
                View Profile
              </LeftAltButton>
            </FlexRow>
          </CentredElementsForm>
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default UserProfilePage;
