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
  const token = React.useContext(GlobalContext).token;

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

  // error messages
  const [displayNameMessage, setDisplayNameMessage] = React.useState('');
  const [emailMessage, setEmailMessage] = React.useState('');

  // response messages
  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

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
    backendRequest('/user/info', {}, 'POST', token, (data) => {
      loadUserData(data);
      console.log(data);
    }, (error) => {
      setResponseError(error);
    });
  }, [token]);

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
        <PageTitle>User Profile</PageTitle>
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
                onReady={ editor => {
                  editor.editing.view.change((writer) => {
                    writer.setStyle(
                        "min-height",
                        "200px",
                        editor.editing.view.document.getRoot()
                    );
                  })
                } }
                onChange={ ( _, editor ) => {
                  setAbout(editor.getData())
                } }
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
