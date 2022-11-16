import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import styled from '@emotion/styled';
import { css } from '@emotion/react';
import moment from 'moment';
import  {
  Box,
  IconButton,
  Link,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableFooter,
  TableHead,
  TableRow,
  Tooltip,
  Typography
} from '@mui/material';
import UpdateIcon from '@mui/icons-material/Update';
import RemoveCircleIcon from '@mui/icons-material/RemoveCircle';
import GlobalContext from '../../utils/GlobalContext';
import { AlertToast, FlexRow, FlexRowVCentred, FlexRowWrapSpaced } from '../StyledNodes';
import {
  MediumBlackText,
  SmallBlackText,
  SmallGreyText,
} from '../TextNodes';

const shoppingLineStyles = css`
  display: grid;
  column-gap: 8px;
  align-items: center;
`;

export const PaymentMethodsContainer = styled.div`
  ${shoppingLineStyles}
  grid-template-columns: max-content max-content max-content;
`;

export const SinglePaymentMethod = ({data}) => {
  let chArray = [];
  [...data.card_number].reverse().forEach((ch, index) => {
    chArray.push(index > 3 ? `*${index % 4 === 0 ? ' ': ''}` : ch);
  });
  return (
    <>
      <Typography sx={{fontSize: '1.25em'}}>
        {chArray.reverse().join('')}
      </Typography>
      <SmallGreyText>
        exp: {moment(data.expiration_date).format('MM/YY')}
      </SmallGreyText>
      <Tooltip title="update" placement="right" arrow>
        <IconButton color="warning" component={RouterLink}
          to={`/edit-payment-method/${data.method_id}`}>
          <UpdateIcon />
        </IconButton>
      </Tooltip>
    </>
  );
};

export const ShoppingCartsContainer = styled.div`
  ${shoppingLineStyles}
  grid-template-columns: max-content max-content;
`;

export const SingleShoppingCart = ({data, setDeleteId, setDialogOpen,
  setDeleteDesciption}) => {
  const handleDelete = () => {
    setDeleteId(data.cart_id);
    setDialogOpen(true);
    setDeleteDesciption(`Cart ID: ${data.cart_id}, Status: ${data.cart_status}`);
  };
  return (
    <>
      <Link component={RouterLink} to={`/view-cart/${data.cart_id}`}
        color="primary.dark">
        Cart ID: {data.cart_id}&emsp; Status: {data.cart_status}
      </Link>
      <Tooltip title="delete" placement="right" arrow>
        <IconButton color="error" onClick={handleDelete}>
          <RemoveCircleIcon />
        </IconButton>
      </Tooltip>
    </>
  )
};

const CheckoutSectionHeader = styled.h2`
  font-weight: 600;
  font-size: 1.5em;
  margin: 8px 0;
`;

export const CheckoutItemsTable = ({cartItems}) => {
  console.log(cartItems);
  const totalCost = cartItems.reduce((prev, curr) => {
    return prev + parseFloat(curr.item_cost);
  }, 0);
  const moneyFormat = (value) => new Intl.NumberFormat('en-AU', {
    style: 'currency',
    currency: 'AUD',
  }).format(value);
  return (
    <Box>
      <CheckoutSectionHeader>Items</CheckoutSectionHeader>
      <TableContainer component={Paper}>
        <Table size="small" aria-label="checkout items">
          <TableHead>
            <TableRow>
              <TableCell align="left">Item ID</TableCell>
              <TableCell align="left">Item Name</TableCell>
              <TableCell align="center">Package Size</TableCell>
              <TableCell align="center">Quantity</TableCell>
              <TableCell align="right">Cost</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {cartItems.map((item, index) => (
              <TableRow key={index}>
                <TableCell align="left" component="th" scope="row">
                  {item.item_id}
                </TableCell>
                <TableCell align="left">
                  {item.item_name}
                </TableCell>
                <TableCell align="center">
                  {item.unit_quantity}&nbsp;{item.unit_type}
                </TableCell>
                <TableCell align="center">
                  {item.item_quantity}
                </TableCell>
                <TableCell align="right">
                  {moneyFormat(item.item_cost)}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
          <TableFooter>
            <TableRow>
              <TableCell colSpan={4} align="right" sx={{fontSize: '1.25em'}}>
                Total:
              </TableCell>
              <TableCell align="right" sx={{fontSize: '1.3em'}}>
                {moneyFormat(totalCost)}
              </TableCell>
            </TableRow>
          </TableFooter>
        </Table>
      </TableContainer>
    </Box>
  );
};
