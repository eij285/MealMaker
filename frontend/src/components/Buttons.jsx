import React from 'react';
import styled from '@emotion/styled';
import { Button } from '@mui/material';

const LargeButton = (props) => {
  const styles = {
    borderRadius: '25px',
    minWidth: '220px'
  };
  return (
    <Button {...props} variant="contained" size="large" sx={ styles } />
  );
};

const SmallButton = (props) => {
  const styles = {
    borderRadius: '20px',
    minWidth: '50px'
  };
  return (
    <Button {...props} variant="contained" size="small" sx={ styles } />
  );
};

/**
 * default button type
 */
export const LargeDefaultButton = (props) => {
  return (
    <LargeButton {...props} color="primary" />
  );
};

/**
 * default small button type
 */
export const SmallDefaultButton = (props) => {
  return (
    <SmallButton {...props} color="primary" />
  );
};

export const HeaderButton = (props) => {
  const styles = {
    borderRadius: '20px',
    whiteSpace: 'nowrap',
    '@media screen and (max-width: 40em)': {
      fontSize: '6pt',
      padding: '4px 6px',
      minWidth: 0,
      '& svg': {
        maxWidth: '10px'
      }
    }
  };
  return (
    <Button {...props} variant="contained" size="small" color="secondary" sx={ styles } />
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