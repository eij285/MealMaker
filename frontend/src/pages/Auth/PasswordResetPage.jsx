import React from 'react';
import { Navigate } from 'react-router-dom';
import { Box, Typography } from '@mui/material';
import AuthLayout from '../../components/Layout/AuthLayout';
import { PasswordInput } from '../../components/InputFields';
import { CentredPageTitle, CustomLink } from '../../components/TextNodes';
import { LargeSubmitButton } from '../../components/Buttons';
import { CentredElementsForm } from '../../components/Forms';
import { isValidEmail, validatePassword, validatePasswordMatch, backendRequest } from '../../helpers';
import { ErrorAlert, SuccessAlert } from '../../components/StyledNodes';

function PasswordResetPage () {
  const query = new URLSearchParams(window.location.search);
  
  // from url query
  const [email] = React.useState(query.get("email"));
  const [code] = React.useState(query.get("code"));

  // password fields
  const [password, setPassword] = React.useState('');
  const [confirm, setConfirm] = React.useState('');

  // error messages
  const [passwordMessage, setPasswordMessage] = React.useState('');
  const [confirmMessage, setConfirmMessage] = React.useState('');

  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');
  
  let valid = true;

  if (!email || !code || isValidEmail(email) === false || code.length < 2) {
    valid = false;
  }
  
  const resetPassword = (e) => {
    e.preventDefault();
    
    if (password !== '' && passwordMessage === '' &&
        confirm != '' && confirmMessage === '') {
      // send to backend (email, code, password)
      const body = { password: password };
      backendRequest('/auth/reset-password', body, 'PUT', null, (data) => {
        setResponseSuccess('Password Reset Successfully');
      }, (error) => {
        setResponseError(error);
      });
    } else {
      validatePassword(password, setPasswordMessage);
      validatePasswordMatch(password, confirm, setConfirmMessage);
    }
  };
  
  return (
    <>
      {!valid && <Navigate to="/forbidden-403" />}
      <AuthLayout>
        <CentredPageTitle>Password Reset</CentredPageTitle>
        {responseSuccess === '' &&
        <CentredElementsForm noValidate onSubmit={resetPassword}>
          <PasswordInput
            label="New Password"
            required
            onChange={(e) => setPassword(e.target.value)}
            onBlur={() => validatePassword(password, setPasswordMessage)}
            error={passwordMessage !== ''}
            helperText={passwordMessage}
          />
          <PasswordInput
            name="confirm"
            label="Confirm Password"
            required
            onChange={(e) => setConfirm(e.target.value)}
            onBlur={() => validatePasswordMatch(password, confirm, setConfirmMessage)}
            error={passwordMessage !== ''}
            helperText={passwordMessage}
          />
          <LargeSubmitButton>Reset Password</LargeSubmitButton>
        </CentredElementsForm>}
        {responseSuccess !== '' &&
        <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
        {responseSuccess === '' && responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
        <Box sx={{ textAlign: 'center' }}>
          <Typography component="span">Return to </Typography>
          <CustomLink to="/login">
            Log in
          </CustomLink>
        </Box>
      </AuthLayout>
    </>
  );
}

export default PasswordResetPage;
