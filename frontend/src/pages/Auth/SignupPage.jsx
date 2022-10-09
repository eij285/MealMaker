import React from 'react';
import { Box, Typography } from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import AuthLayout from '../../components/Layout/AuthLayout';
import { EmailInput, PasswordInput, TextInput } from '../../components/InputFields';
import { CentredPageTitle, CustomLink } from '../../components/TextNodes';
import { LargeSubmitButton } from '../../components/Buttons';
import { CentredElementsForm } from '../../components/Forms';
import { isValidEmail, isValidPassword } from '../../helpers';

function SignupPage () {
  const initialData = {
    displayName: {
      value: '',
      error: false,
      message: ''
    },
    email: {
      value: '',
      error: false,
      message: ''
    },
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
  
  const signup = (e) => {
    e.preventDefault();
    const displayName = e.target.displayName.value;
    const email = e.target.email.value;
    const password = e.target.password.value;
    const confirm = e.target.confirm.value;
    let dataState = {...formData};
    dataState.displayName.value = displayName;
    dataState.email.value = email;
    dataState.password.value = password;
    dataState.confirm.value = confirm;
    let isError = false;
    if (displayName === '') {
      dataState.displayName.error = true;
      dataState.displayName.message = 'A name is required';
      isError = true;
    }
    if (email === '') {
      dataState.email.error = true;
      dataState.email.message = 'An email required';
      isError = true;
    } else if(isValidEmail(email) === false) {
      dataState.email.error = true;
      dataState.email.message = 'Email format is not valid';
      isError = true;
    }
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
    if (isError === false) {
      // send to backend
    }
    setFormData({...dataState});
  };

  return (
    <AuthLayout>
      <CentredPageTitle>Sign up</CentredPageTitle>
      <CentredElementsForm noValidate onSubmit={signup}>
        <TextInput
          name="displayName"
          label="Display Name"
          required
          defaultValue={formData.displayName.value}
          error={formData.displayName.error}
          helperText={formData.displayName.error && formData.displayName.message}
        />
        <EmailInput
          name="email"
          label="Email"
          required
          defaultValue={formData.email.value}
          error={formData.email.error}
          helperText={formData.email.error && formData.email.message}
        />
        <PasswordInput
          name="password"
          label="Password"
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
