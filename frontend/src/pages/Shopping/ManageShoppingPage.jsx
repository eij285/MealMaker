import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Box, Button, Grid } from '@mui/material';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { backendRequest } from '../../helpers';
import { ErrorAlert, FlexColumn, FlexRow, SuccessAlert } from '../../components/StyledNodes';
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import { TextInput } from '../../components/InputFields';

function ManageShoppingPage () {
  // TODO: complete this page
  const token = React.useContext(GlobalContext).token;
  const [deliveryAddress, setDeliveryAddress] = React.useState('');
  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const loadPaymentMethod = () => {
    
    const body = {
      
    };
    backendRequest('/cart/payment-method/get', body, 'POST', token, (data) => {
      
    }, (error) => {
      
    });
  };

  return (
    <ManageLayout>
      <Grid item xl={6} lg={8} md={10} sm={12} xs={12}>
        <PageTitle>Shopping</PageTitle>
        {responseSuccess !== '' &&
        <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
        <FlexColumn>
          <Box>
            <SubPageTitle>Orders</SubPageTitle>
          </Box>
          <Box>
            <SubPageTitle>Saved Shopping Carts</SubPageTitle>
          </Box>
          <Box>
            <SubPageTitle>Payment Methods</SubPageTitle>
            <FlexRow>
              <Button color="success"
                component={RouterLink}
                to="/add-payment-method"
                size="large"
                sx={{textTransform: 'none'}}
                startIcon={<AddCircleIcon />}>
                Add Payment Method
              </Button>
            </FlexRow>
          </Box>
          <Box>
            <SubPageTitle>Delivery Options</SubPageTitle>
            <TextInput
              label="Delivery Address"
              multiline
              minRows={5}
              value={deliveryAddress}
              onChange={(e) => setDeliveryAddress(e.target.value)}
            />
          </Box>
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default ManageShoppingPage;
