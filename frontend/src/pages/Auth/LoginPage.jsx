import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Typography } from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import AuthLayout from '../../components/Layout/AuthLayout';
import { EmailInput, PasswordInput } from '../../components/InputFields';
import { CentredPageTitle, CustomLink } from '../../components/TextNodes';
import { LargeSubmitButton, LeftAltButton } from '../../components/Buttons';
import { CentredElementsForm } from '../../components/Forms';
import { ErrorAlert } from '../../components/StyledNodes';
import { backendRequest } from '../../helpers';

function LoginPage () {
  const context = React.useContext(GlobalContext);
  const login = context.login;
  const logout = context.logout;
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [emailError, setEmailError] = React.useState(false);
  const [passwordError, setPasswordError] = React.useState(false);
  const [responseError, setResponseError] = React.useState('');
  const [notLoggedOut, setNotLoggedOut] = React.useState(false);

  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (!emailError && email === '') {
      setEmailError(true);
    }
    if (!passwordError && password === '') {
      setPasswordError(true);
    }
    if (email === '' || password === '' || emailError || passwordError) {
      return;
    }
    const body = {
      email: email,
      password: password,
    };
    backendRequest('/auth/login', body, 'POST', null, (data) => {
      login(data.token);
      navigate('/');
    }, (error) => {
      setResponseError(error);
      if (error === 'User already logged in') {
        setNotLoggedOut(true);
      }
    });
  };

  const logoutEverywhere = () => {
    const body = {
      email: email,
      password: password,
    };
    backendRequest('/auth/logout-everywhere', body, 'POST', null, (data) => {
      logout();
      navigate('/');
    }, (error) => {
      setResponseError(error);
    });
  };

  return (
    <AuthLayout>
      <CentredPageTitle>Log in</CentredPageTitle>
      <CentredElementsForm noValidate onSubmit={handleLogin}>
        <EmailInput
          label="Email"
          onChange={(e) => setEmail(e.target.value)}
          onBlur={(e) => setEmailError(email === '')}
          required
          error={emailError}
          helperText={emailError ? 'Email required' : ''}
        />
        <PasswordInput
          label="Password"
          onChange={(e) => setPassword(e.target.value)}
          onBlur={(e) => setPasswordError(password === '')}
          required
          error={passwordError}
          helperText={passwordError ? 'Password required' : ''}
        />
        <CustomLink to="/forgot-password" sx={{ textAlign: 'right' }}>
          Forgot password?
        </CustomLink>
        <LargeSubmitButton>Log in</LargeSubmitButton>
      </CentredElementsForm>
      {responseError !== '' &&
      <ErrorAlert message={responseError} setMessage={setResponseError} />}
      {notLoggedOut && <LeftAltButton onClick={logoutEverywhere}>
        Log out everywhere</LeftAltButton>}
      <Box sx={{ textAlign: 'center' }}>
        <Typography component="span">Don't have an account? </Typography>
        <CustomLink to="/signup" sx={{ textAlign: 'right' }}>
          Sign up
        </CustomLink>
      </Box>
    </AuthLayout>
  );
}

export default LoginPage;
