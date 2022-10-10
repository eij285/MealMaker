import React from 'react';
import { Box, Typography } from '@mui/material';
import AuthLayout from '../../components/Layout/AuthLayout';
import { EmailInput } from '../../components/InputFields';
import { CentredPageTitle, CustomLink } from '../../components/TextNodes';
import { LargeSubmitButton } from '../../components/Buttons';
import { CentredElementsForm } from '../../components/Forms';
import { validateEmail, backendRequest } from '../../helpers';
import { ErrorAlert, SuccessAlert } from '../../components/StyledNodes';

function ForgotPasswordPage () {
  const resetText = {
    textAlign: 'center',
    margin: '20px 0'
  };

  const [email, setEmail] = React.useState('');
  const [emailMessage, setEmailMessage] = React.useState('');
  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');
  
  const sendEmail = (e) => {
    e.preventDefault();
    if (email !== '' && emailMessage === '') {
      //send to backend
      const body = { email: email };
      backendRequest('/auth/reset-link', body, 'PUT', null, (data) => {
        setResponseSuccess('Check email for password reset instructions');
      }, (error) => {
        setResponseError(error);
      });
    } else {
      validateEmail(email, setEmailMessage);
    }
  };

  return (
    <AuthLayout>
      <CentredPageTitle>Password Reset</CentredPageTitle>
      <Typography component="p" sx={ resetText }>
        Enter email to recieve password reset instructions
      </Typography>
      <CentredElementsForm noValidate onSubmit={sendEmail}>
        <EmailInput
          label="Email"
          required
          onChange={(e) => setEmail(e.target.value)}
          onBlur={() => validateEmail(email, setEmailMessage)}
          error={emailMessage !== ''}
          helperText={emailMessage}
        />
        <LargeSubmitButton>Send Email</LargeSubmitButton>
      </CentredElementsForm>
      {responseError !== '' &&
      <ErrorAlert message={responseError} setMessage={setResponseError} />}
      {responseSuccess !== '' &&
      <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
      <Box sx={{ textAlign: 'center' }}>
        <Typography component="span">Return to </Typography>
        <CustomLink to="/login">
          Log in
        </CustomLink>
      </Box>
    </AuthLayout>
  );
}

export default ForgotPasswordPage;
