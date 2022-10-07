import React from 'react';
import { Box, Typography } from '@mui/material';
import AuthLayout from '../../components/Layout/AuthLayout';
import { EmailInput } from '../../components/InputFields';
import { CentredPageTitle, CustomLink } from '../../components/TextNodes';
import { LargeSubmitButton } from '../../components/Buttons';
import { CentredElementsForm } from '../../components/Forms';

function ForgotPasswordPage () {
  const resetText = {
    textAlign: 'center',
    margin: '20px 0'
  }
  return (
    <AuthLayout>
      <CentredPageTitle>Password Reset</CentredPageTitle>
      <Typography component="p" sx={ resetText }>
        Enter email to recieve password reset instructions
      </Typography>
      <CentredElementsForm noValidate>
        <EmailInput label="Email" required />
        <LargeSubmitButton>Send Email</LargeSubmitButton>
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

export default ForgotPasswordPage;
