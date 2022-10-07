import React from 'react';
import { Box, Typography } from '@mui/material';
import AuthLayout from '../../components/Layout/AuthLayout';
import { EmailInput, PasswordInput, TextInput } from '../../components/InputFields';
import { CentredPageTitle, CustomLink } from '../../components/TextNodes';
import { LargeSubmitButton } from '../../components/Buttons';
import { CentredElementsForm } from '../../components/Forms';

function SignupPage () {
  return (
    <AuthLayout>
      <CentredPageTitle>Sign up</CentredPageTitle>
      <CentredElementsForm noValidate>
        <TextInput label="Name" required />
        <EmailInput label="Email" required />
        <PasswordInput label="Password" required />
        <PasswordInput label="Confirm Password" required />
        <LargeSubmitButton>Sign up</LargeSubmitButton>
        <Box sx={{ textAlign: 'center' }}>
          <Typography component="span">Already have an account? </Typography>
          <CustomLink to="/login" sx={{ textAlign: 'right' }}>
            Log in
          </CustomLink>
        </Box>
      </CentredElementsForm>
    </AuthLayout>
  );
}

export default SignupPage;
