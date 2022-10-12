import React from 'react';
import { Grid } from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { PasswordInput } from '../../components/InputFields';
import { PageTitle } from '../../components/TextNodes';
import { LeftAlignedSubmitButton } from '../../components/Buttons';
import { CentredElementsForm } from '../../components/Forms';
import { ErrorAlert, SuccessAlert, FlexColumn } from '../../components/StyledNodes';
import { backendRequest, validatePassword, validatePasswordMatch } from '../../helpers';

function UpdatePasswordPage () {
  const token = React.useContext(GlobalContext).token;

  // password fields
  const [password, setPassword] = React.useState('');
  const [confirm, setConfirm] = React.useState('');

  // error messages
  const [passwordMessage, setPasswordMessage] = React.useState('');
  const [confirmMessage, setConfirmMessage] = React.useState('');

  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');
  
  const updatePassword = (e) => {
    e.preventDefault();
    
    if (password !== '' && passwordMessage === '' &&
        confirm != '' && confirmMessage === '') {
      // send to backend
      const body = {
        token: token,
        password: password
      };
      backendRequest('/auth/update-password', body, 'PUT', null, (data) => {
        setResponseSuccess('Password Updated Successfully');
      }, (error) => {
        setResponseError(error);
      });
    } else {
      validatePassword(password, setPasswordMessage);
      validatePasswordMatch(password, confirm, setConfirmMessage);
    }
  };

  return (
    <ManageLayout>
      <Grid item xl={3} lg={5} md={7} sm={10} xs={12}>
        <PageTitle>Update Password</PageTitle>
        <FlexColumn>
          {responseSuccess !== '' &&
          <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
          {responseSuccess === '' && responseError !== '' &&
          <ErrorAlert message={responseError} setMessage={setResponseError} />}
          <CentredElementsForm noValidate onSubmit={updatePassword}>
            <PasswordInput
              label="New Password"
              required
              onChange={(e) => setPassword(e.target.value)}
              onBlur={() => validatePassword(password, setPasswordMessage)}
              error={passwordMessage !== ''}
              helperText={passwordMessage}
            />
            <PasswordInput
              label="Confirm Password"
              required
              onChange={(e) => setConfirm(e.target.value)}
              onBlur={() => validatePasswordMatch(password, confirm, setConfirmMessage)}
              error={passwordMessage !== ''}
              helperText={passwordMessage}
            />
            <LeftAlignedSubmitButton>Update Password</LeftAlignedSubmitButton>
          </CentredElementsForm>
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default UpdatePasswordPage;
