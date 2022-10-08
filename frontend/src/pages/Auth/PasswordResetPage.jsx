import React from 'react';
import { Navigate } from 'react-router-dom';
import { Box, Typography } from '@mui/material';
import AuthLayout from '../../components/Layout/AuthLayout';
import { PasswordInput } from '../../components/InputFields';
import { CentredPageTitle, CustomLink } from '../../components/TextNodes';
import { LargeSubmitButton } from '../../components/Buttons';
import { CentredElementsForm } from '../../components/Forms';
import { isValidEmail, isValidPassword } from '../../helpers';

function PasswordResetPage () {
  const query = new URLSearchParams(window.location.search);
  
  const [email, setEmail] = React.useState(query.get("email"));
  const [code, setCode] = React.useState(query.get("code"));

  const initialData = {
    password: {
      value: '',
      error: false,
      message: ''
    },
    confirm: {
      value: '',
      error: false,
      message: ''
    }
  };

  const [formData, setFormData] = React.useState(initialData);
  
  let valid = true;

  if (!email || !code || isValidEmail(email) === false || code.length < 2) {
    valid = false;
  }
  
  const resetPassword = (e) => {
    e.preventDefault();
    const password = e.target.password.value;
    const confirm = e.target.confirm.value;
    let dataState = {...formData};
    dataState.password.value = password;
    dataState.confirm.value = confirm;
    let isError = false;
    if (password === '') {
      dataState.password.error = true;
      dataState.password.message = 'A password is required';
      isError = true;
    } else if (isValidPassword(password) === false) {
      dataState.password.error = true;
      dataState.password.message = 'A complex password is required';
      isError = true;
    }
    if (confirm === '') {
      dataState.confirm.error = true;
      dataState.confirm.message = 'A password confirmation is required';
      isError = true;
    } else if (password !== confirm) {
      dataState.confirm.error = true;
      dataState.confirm.message = 'Passwords do not match';
      isError = true;
    }
    console.log(password, confirm);
    if (isError === false) {
      // send to backend (email, code, password)
      console.log('valid password');
      dataState.password.error = false;
      dataState.confirm.error = false;
    }
    setFormData({...dataState});
  };
  
  
  return (
    <>
      {!valid && <Navigate to="/403-forbidden" />}
      <AuthLayout>
        <CentredPageTitle>Password Reset</CentredPageTitle>
        <CentredElementsForm noValidate onSubmit={resetPassword}>
          <PasswordInput
            name="password"
            label="New Password"
            required
            defaultValue={formData.password.value}
            error={formData.password.error}
            helperText={formData.password.error && formData.password.message}
          />
          <PasswordInput
            name="confirm"
            label="Confirm Password"
            required
            defaultValue={formData.confirm.value}
            error={formData.confirm.error}
            helperText={formData.confirm.error && formData.confirm.message}
          />
          <LargeSubmitButton>Reset Password</LargeSubmitButton>
          <Box sx={{ textAlign: 'center' }}>
            <Typography component="span">Return to </Typography>
            <CustomLink to="/login">
              Log in
            </CustomLink>
          </Box>
        </CentredElementsForm>
      </AuthLayout>
    </>
  );
}

export default PasswordResetPage;
