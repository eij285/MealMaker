import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography } from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import AuthLayout from '../../components/Layout/AuthLayout';
import { EmailInput, PasswordInput, TextInput } from '../../components/InputFields';
import { CentredPageTitle, CustomLink } from '../../components/TextNodes';
import { LargeSubmitButton } from '../../components/Buttons';
import { CentredElementsForm } from '../../components/Forms';
import { ErrorAlert } from '../../components/StyledNodes';
import {
  validateDisplayName,
  validateEmail,
  validatePassword,
  validatePasswordMatch,
  backendRequest
} from '../../helpers';

function SignupPage () {
  const login = React.useContext(GlobalContext).login;

  // values
  const [displayName, setDisplayName] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [confirm, setConfirm] = React.useState('');

  // error messages
  const [displayNameMessage, setDisplayNameMessage] = React.useState('');
  const [emailMessage, setEmailMessage] = React.useState('');
  const [passwordMessage, setPasswordMessage] = React.useState('');
  const [confirmMessage, setConfirmMessage] = React.useState('');
  
  const [responseError, setResponseError] = React.useState('');

  const navigate = useNavigate();

  const signup = (e) => {
    e.preventDefault();
    // value cannot be blank and message must be blank
    if (displayName !== '' && displayNameMessage === '' && 
        email !== '' && emailMessage === '' &&
        password !== '' && passwordMessage === '' &&
        confirm != '' && confirmMessage === '') {
      // send to backend
      const body = {
        username: displayName,
        email: email,
        password: password,
      };
      backendRequest('/auth/register', body, 'POST', null, (data) => {
        login(data.token);
        navigate('/');
      }, (error) => {
        setResponseError(error);
      });
    } else {
      validateDisplayName(displayName, setDisplayNameMessage);
      validateEmail(email, setEmailMessage);
      validatePassword(password, setPasswordMessage);
      validatePasswordMatch(password, confirm, setConfirmMessage);
    }
  };

  return (
    <AuthLayout>
      <CentredPageTitle>Sign up</CentredPageTitle>
      <CentredElementsForm noValidate onSubmit={signup}>
        <TextInput
          label="Display Name"
          required
          onChange={(e) => setDisplayName(e.target.value)}
          onBlur={() => validateDisplayName(displayName, setDisplayNameMessage)}
          error={displayNameMessage !== ''}
          helperText={displayNameMessage}
        />
        <EmailInput
          label="Email"
          required
          onChange={(e) => setEmail(e.target.value)}
          onBlur={() => validateEmail(email, setEmailMessage)}
          error={emailMessage !== ''}
          helperText={emailMessage}
        />
        <PasswordInput
          label="Password"
          required
          onChange={(e) => setPassword(e.target.value)}
          onBlur={() => validatePassword(password, setPasswordMessage)}
          error={passwordMessage !== ''}
          helperText={passwordMessage}
        />
        <PasswordInput
          label="Confirm Password"
          required
          onChange={(e) => setConfirm(e.target.value)}
          onBlur={() => validatePasswordMatch(password, confirm, setConfirmMessage)}
          error={confirmMessage !== ''}
          helperText={confirmMessage}
        />
        <LargeSubmitButton>Sign up</LargeSubmitButton>
      </CentredElementsForm>
      {responseError !== '' &&
      <ErrorAlert message={responseError} setMessage={setResponseError} />}
      <Box sx={{ textAlign: 'center' }}>
        <Typography component="span">Already have an account? </Typography>
        <CustomLink to="/login" sx={{ textAlign: 'right' }}>
          Log in
        </CustomLink>
      </Box>
    </AuthLayout>
  );
}

export default SignupPage;
