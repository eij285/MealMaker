import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Grid } from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { backendRequest } from '../../helpers';
import { ErrorAlert } from '../../components/StyledNodes';
import { PageTitle } from '../../components/TextNodes';

function ManageShoppingPage () {
  const token = React.useContext(GlobalContext).token;
  const [responseError, setResponseError] = React.useState('');

  return (
    <ManageLayout>
      <Grid item xl={8} lg={12} xs={12}>
        <PageTitle>Shopping</PageTitle>
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
      </Grid>
    </ManageLayout>
  );
}

export default ManageShoppingPage;
