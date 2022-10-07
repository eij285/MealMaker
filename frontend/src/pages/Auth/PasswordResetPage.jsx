import React from 'react';
import { Box, Typography } from '@mui/material';
import AuthLayout from '../../components/Layout/AuthLayout';
import { PasswordInput } from '../../components/InputFields';
import { CentredPageTitle, CustomLink } from '../../components/TextNodes';
import { LargeSubmitButton } from '../../components/Buttons';
import { CentredElementsForm } from '../../components/Forms';

function PasswordResetPage () {
  const query = new URLSearchParams(window.location.search);
  const email = query.get("email");
  const resetCode = query.get("code");
  console.log(email, resetCode);
  return (
    <AuthLayout>
      <CentredPageTitle>Password Reset</CentredPageTitle>
      <CentredElementsForm noValidate>
        <PasswordInput label="New Password" required />
        <PasswordInput label="Confirm Password" required />
        <LargeSubmitButton>Reset Password</LargeSubmitButton>
        <Box sx={{ textAlign: 'center' }}>
          <Typography component="span">Return to </Typography>
          <CustomLink to="/login">
            Log in
          </CustomLink>
        </Box>
      </CentredElementsForm>
    </AuthLayout>
  );
}

export default PasswordResetPage;
