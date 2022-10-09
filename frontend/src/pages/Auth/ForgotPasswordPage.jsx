import React from 'react';
import { Box, Typography } from '@mui/material';
import AuthLayout from '../../components/Layout/AuthLayout';
import { EmailInput } from '../../components/InputFields';
import { CentredPageTitle, CustomLink } from '../../components/TextNodes';
import { LargeSubmitButton } from '../../components/Buttons';
import { CentredElementsForm } from '../../components/Forms';
import { isValidEmail } from '../../helpers';

function ForgotPasswordPage () {
  const resetText = {
    textAlign: 'center',
    margin: '20px 0'
  };

  const [email, setEmail] = React.useState('');
  const [error, setError] = React.useState(false);
  
  const sendEmail = (e) => {
    e.preventDefault();
    const currEmail = e.target.email.value;
    setEmail(currEmail);
    if (isValidEmail(currEmail)) {
      setError(false);
      //send to backend
    } else {
      setError(true);
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
          name="email"
          label="Email"
          required
          defaultValue={email}
          error={error}
          helperText={error && email === '' ? 'Email not supplied' : 'Invalid email'}
        />
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
