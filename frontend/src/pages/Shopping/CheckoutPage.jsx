import React from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import {
  Autocomplete,
  Box,
  Button,
  Divider,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Typography 
} from '@mui/material';
import { DataGrid } from '@mui/x-data-grid';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import RemoveCircleIcon from '@mui/icons-material/RemoveCircle';
import ShoppingCartCheckoutIcon from '@mui/icons-material/ShoppingCartCheckout';
import GlobalContext from '../../utils/GlobalContext';
import ExploreLayout from '../../components/Layout/ExploreLayout';
import {
  FlexColumn,
  FlexRow,
  FlexRowWrap,
  ErrorAlert,
  SuccessAlert,
  FlexRowWrapSpaced,
  FlexRowVCentred,
  FlexColumnVCentred
} from '../../components/StyledNodes';
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import { LeftAlignedButton, MediumAlternateButton } from '../../components/Buttons';
import { NumericInput, TextInput } from '../../components/InputFields';
import { backendRequest, isPositiveInteger } from '../../helpers';
import { CheckoutItemsTable } from '../../components/Shopping/ShoppingNodes';
const config = require('../../config.json');

function CheckoutPage () {
  const globals = React.useContext(GlobalContext);
  const token = globals.token;

  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const cartId = globals.cartId;
  const cartItems = globals.cartItems;

  const navigate = useNavigate();

  return (
    <ExploreLayout>
      <FlexRowWrapSpaced>
        <FlexRowVCentred>
          <ShoppingCartCheckoutIcon sx={{fontSize: '2.5em'}} />
          <PageTitle>
            Checkout
          </PageTitle>
        </FlexRowVCentred>
        <FlexColumnVCentred>
          <MediumAlternateButton onClick={() => navigate(-1)}>
            Back
          </MediumAlternateButton>
        </FlexColumnVCentred>
      </FlexRowWrapSpaced>
      {responseSuccess !== '' &&
      <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
      {responseError !== '' &&
      <ErrorAlert message={responseError} setMessage={setResponseError} />}
      {cartItems.length < 1 &&
      <Typography sx={{fontSize: '18pt'}}>No items in cart</Typography>}
      {cartItems.length > 0 &&
      <FlexColumn>
        <CheckoutItemsTable cartItems={cartItems} />
      </FlexColumn>}
    </ExploreLayout>
  );
}

export default CheckoutPage;
