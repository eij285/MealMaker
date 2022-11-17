import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { Box, Button, Grid } from '@mui/material';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import {
  ConfirmationDialog,
  ErrorAlert,
  FlexColumn,
  FlexRow,
  SuccessAlert
} from '../../components/StyledNodes';
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import {
  PaymentMethodsContainer,
  SinglePaymentMethod,
  ShoppingCartsContainer,
  SingleShoppingCart
} from '../../components/Shopping/ShoppingNodes';
import { backendRequest } from '../../helpers';

function ManageShoppingPage () {
  const token = React.useContext(GlobalContext).token;
  const [paymentMethods, setPaymentMethods] = React.useState([]);
  const [shoppingCarts, setShoppingCarts] = React.useState([]);

  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [deleteCartId, setDeleteCartId] = React.useState(-1);
  const [deleteDescription, setDeleteDesciption] = React.useState('');

  const loadShoppingCarts = () => {
    backendRequest('/cart/display/all', {}, 'POST', token, (data) => {
      setShoppingCarts([...data.carts]);
    }, (error) => {
      setResponseError(error);
    });
  };

  const loadPaymentMethods = () => {
    backendRequest('/cart/payment-method/list', {}, 'POST', token, (data) => {
      setPaymentMethods([...data.body]);
    }, (error) => {
      setResponseError(error);
    });
  };

  const deleteCart = () => {
    const body = {
      cart_id: deleteCartId
    };
    backendRequest('/cart/delete', body, 'POST', token, (data) => {
      console.log(data);
      setResponseSuccess('Successfully deleted shopping cart');
      loadShoppingCarts();
    }, (error) => {
      setResponseError(error);
    });
    setDialogOpen(false);
  };

  React.useEffect(() => {
    loadShoppingCarts();
    loadPaymentMethods();
  }, [token]);

  React.useEffect(() => {
    if (!dialogOpen) {
      setDeleteCartId(-1);
    }
  }, [dialogOpen, deleteCartId]);

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
            <ShoppingCartsContainer>
            {shoppingCarts.map((cart, index) => (
              <SingleShoppingCart key={index} data={cart}
                setDeleteId={setDeleteCartId} setDialogOpen={setDialogOpen}
                setDeleteDesciption={setDeleteDesciption} />
            ))}
            </ShoppingCartsContainer>
          </Box>
          <Box>
            <SubPageTitle>Payment Methods</SubPageTitle>
            <PaymentMethodsContainer>
            {paymentMethods.map((method, index) => (
              <SinglePaymentMethod key={index} data={method} />
            ))}
            </PaymentMethodsContainer>
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
        </FlexColumn>
      </Grid>
      <ConfirmationDialog title="Are you sure you want to delete shopping cart?"
        description={deleteDescription}
        acceptContent="Delete" rejectContent="Cancel"
        openState={dialogOpen} setOpenState={setDialogOpen} 
        execOnAccept={deleteCart} />
    </ManageLayout>
  );
}

export default ManageShoppingPage;
