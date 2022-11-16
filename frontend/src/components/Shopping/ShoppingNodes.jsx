import React from 'react';
import styled from '@emotion/styled';
import { Box, IconButton, Rating, Tooltip, Typography } from '@mui/material';
import AddShoppingCartIcon from '@mui/icons-material/AddShoppingCart';
import FoodBankIcon from '@mui/icons-material/FoodBank';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import ThumbUpOutlinedIcon from '@mui/icons-material/ThumbUpOutlined';
import GlobalContext from '../../utils/GlobalContext';
import { AlertToast, FlexRow, FlexRowVCentred, FlexRowWrapSpaced } from '../StyledNodes';
import {
  MediumGreyText,
  MediumBlackText,
  SmallBlackText,
  SmallGreyText,
  SubPageTitle
} from '../TextNodes';
import { NumericInput } from '../../components/InputFields';
import {
  backendRequest,
  customPrepTime,
  formatIngredient,
  formatNutrient,
  getAverageRating
} from '../../helpers';
import { MediumDefaultButton } from '../Buttons';
const config = require('../../config.json');


export const SinglePaymentMethod = () => {
  return (
    <></>
  );
};