import React from 'react';
import styled from '@emotion/styled';
import { Button } from '@mui/material';

/**
 * default button type
 */
export const LargeDefaultButton = (props) => {
  const buttonStyles = {
    borderRadius: '25px',
    minWidth: '220px'
  };
  return (
    <Button {...props}
      color="primary"
      variant="contained"
      size="large"
      sx={ buttonStyles } />
  );
};

/**
 * submit button using default button styling
 */
export const LargeSubmitButton = (props) => {
  return (
    <LargeDefaultButton {...props} type="submit" />
  );
};