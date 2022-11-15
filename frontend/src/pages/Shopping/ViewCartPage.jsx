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
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
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
import { PageTitle } from '../../components/TextNodes';
import { LeftAlignedButton, MediumAlternateButton } from '../../components/Buttons';
import { NumericInput, TextInput } from '../../components/InputFields';
import { backendRequest, isPositiveInteger } from '../../helpers';
const config = require('../../config.json');

function ViewCartPage () {
  const globals = React.useContext(GlobalContext);
  const token = globals.token;

  const [quantity, setQuantity] = React.useState('');
  const [ingredientUnit, setIngredientUnit] = React.useState(config.METRIC_UNITS[0]);
  const [ingredientName, setIngredientName] = React.useState(config.INGREDIENTS[0]);

  const [ingredientMessage, setIngredientMessage] = React.useState('');

  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const cartId = globals.cartId;
  const cartItems = globals.cartItems;
  const setCartItems = globals.setCartItems;

  const dataGridStyles = {
    height: 'calc(100vh - 600px)',
  };

  const addIngredientToCart = () => {
    if(!ingredientName || !quantity || !ingredientUnit ||
      !isPositiveInteger(`${quantity}`)) {
      setIngredientMessage('All ingredients must have size, unit and name');
    }
  };
  console.log(cartItems);
  
  const navigate = useNavigate();

  const columns = [
    { field: 'id', headerName: 'ID', hide: true },
    {
      field: 'item_id',
      headerName: 'Item ID',
      width: 70,
    },
    {
      field: 'item_name',
      headerName: 'First name',
      flex: 1
    },
    {
      field: 'package_size',
      headerName: 'Package Size',
      valueGetter: (params) =>
      `${params.row.unit_quantity || ''} ${params.row.unit_type || ''}`,
      width: 130,
    },
    {
      field: 'item_quantity',
      headerName: 'Quantity',
      width: 100,
    },
    {
      field: 'item_cost',
      headerName: 'Cost',
      valueFormatter: ({value}) => new Intl.NumberFormat('en-AU', {
        style: 'currency',
        currency: 'AUD',
      }).format(value)
    },
  ];

  return (
    <ExploreLayout>
      <FlexRowWrapSpaced>
        <FlexRowVCentred>
          <ShoppingCartIcon sx={{fontSize: '2.5em'}} />
          <PageTitle>
            Shopping Cart
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
      <FlexColumn>
        <Box sx={dataGridStyles}>
          <DataGrid
            rows={cartItems}
            columns={columns}
            getRowId={(row) => row.item_id}
            pageSize={100}
            rowsPerPageOptions={[100]}
          />
        </Box>
        <Box sx={{maxWidth: '600px'}}>
          <FlexRow>
            <NumericInput
              sx={{ maxWidth:'120px' }}
              label="Size"
              inputProps={{ min: 1, max: 100000 }}
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
            />
            <FormControl fullWidth sx={{ maxWidth:'150px' }}>
              <InputLabel id="add-ingredient-unit">Unit</InputLabel>
              <Select labelId="add-ingredient-unit" label="Unit"
                value={ingredientUnit}
                onChange={(e) => setIngredientUnit(e.target.value)}>
              {config.METRIC_UNITS.map((dataItem, idx) => (
                <MenuItem key={idx} value={dataItem}>
                  {dataItem}
                </MenuItem>
              ))}
              </Select>
            </FormControl>
            <Autocomplete
              fullWidth
              options={config.INGREDIENTS}
              value={ingredientName}
              onChange={(e, newVal) => setIngredientName(newVal)}
              renderInput={(params) => (
                <TextInput
                  label="Ingredient"
                  {...params}
                />
              )}
            />
          </FlexRow>
          {ingredientMessage !== '' &&
          <ErrorAlert message={ingredientMessage} setMessage={setIngredientMessage} />}
        </Box>
        <FlexRow>
          <Button color="success"
            size="large"
            onClick={addIngredientToCart}
            sx={{textTransform: 'none'}}
            startIcon={<AddCircleIcon />}>
            Add ingredient to cart
          </Button>
        </FlexRow>
        <Divider />
        <FlexRow>
          <LeftAlignedButton component={RouterLink} to="/checkout">
            <ShoppingCartCheckoutIcon />&nbsp;
            Checkout
          </LeftAlignedButton>
        </FlexRow>
      </FlexColumn>
    </ExploreLayout>
  );
}

export default ViewCartPage;
