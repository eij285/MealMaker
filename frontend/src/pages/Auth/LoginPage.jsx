import React from 'react';
import { Box, Typography } from '@mui/material';
import AuthLayout from '../../components/Layout/AuthLayout';
import { EmailInput, PasswordInput } from '../../components/InputFields';
import { CentredPageTitle, CustomLink } from '../../components/TextNodes';
import { LargeSubmitButton } from '../../components/Buttons';
import { CentredElementsForm } from '../../components/Forms';

function LoginPage () {
  const [email, setEmail] = React.useState('');
  const [password, setPassword] = React.useState('');

  const login = (e) => {
    e.preventDefault();
    //send to backend
  };

  return (
    <AuthLayout>
      <CentredPageTitle>Log in</CentredPageTitle>
      <CentredElementsForm noValidate onSubmit={login}>
        <EmailInput
          name="email"
          label="Email"
          required
          defaultValue={email}
        />
        <PasswordInput
          name="password"
          label="Password"
          required
          defaultValue={password}
        />
        <CustomLink to="/forgot-password" sx={{ textAlign: 'right' }}>
          Forgot password?
        </CustomLink>
        <LargeSubmitButton>Log in</LargeSubmitButton>
        <Box sx={{ textAlign: 'center' }}>
          <Typography component="span">Don't have an account? </Typography>
          <CustomLink to="/signup" sx={{ textAlign: 'right' }}>
            Sign up
          </CustomLink>
        </Box>
      </CentredElementsForm>
    </AuthLayout>
  );
}

export default LoginPage;
