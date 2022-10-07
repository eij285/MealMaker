import React from 'react';
import styled from '@emotion/styled';
import { TextField } from '@mui/material';

const TextInputBlock = styled(TextField)`
  display: block;
`;

/**
 * full width form input
 */
export const GeneralTextInput = (props) => {
  return (
    <TextInputBlock {...props} variant="outlined" size="medium" fullWidth />
  );
};

/**
 * full width text input
 */
export const TextInput = (props) => {
  return (
    <GeneralTextInput {...props} type="text" />
  );
};

/**
 * full width email input
 */
export const EmailInput = (props) => {
  return (
    <GeneralTextInput {...props} type="email" />
  );
};

/**
 * full width password input
 */
export const PasswordInput = (props) => {
  return (
    <GeneralTextInput {...props} type="password" />
  );
};
