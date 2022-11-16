import React from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import {
  Grid
} from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import {
  ErrorAlert,
  SuccessAlert
} from '../../components/StyledNodes';
import { PageTitle } from '../../components/TextNodes';
import { backendRequest, isPositiveInteger } from '../../helpers';
const config = require('../../config.json');

function ViewCartPage () {
  const { cartId } = useParams();
  const globals = React.useContext(GlobalContext);
  const token = globals.token;

  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const displayCart = () => {
    const body = {
      cart_id: cartId,
    };
    backendRequest('/cart/display', body, 'POST', token, (data) => {

    }, (error) => {
      setResponseError(error);
    });
  };

  React.useEffect(() => {
    displayCart();
  }, [token]);

  return (
    <ManageLayout>
      <Grid item xl={6} lg={8} md={10} sm={12} xs={12}>
        <PageTitle>View Cart</PageTitle>
        {responseSuccess !== '' &&
        <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />
        }
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
      </Grid>
    </ManageLayout>
  );
}

export default ViewCartPage;
