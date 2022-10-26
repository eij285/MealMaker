import React from 'react';
import styled from '@emotion/styled';
import { Button } from '@mui/material';

const LargeButton = (props) => {
  const styles = {
    borderRadius: '25px',
    minWidth: '220px',
  };
  return (
    <Button {...props} variant="contained" size="large" sx={ styles } />
  );
};

const MediumButton = (props) => {
  const styles = {
    borderRadius: '25px',
    minWidth: '100px',
    maxHeight: '36px'
  };
  return (
    <Button {...props} variant="contained" size="medium" sx={ styles } />
  );
};

const SmallButton = (props) => {
  const styles = {
    borderRadius: '20px',
    minWidth: '50px',
    maxHeight: '30px'
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
 * alternate button type
 */
export const LargeAlternateButton = (props) => {
  return (
    <LargeButton {...props} color="secondary" />
  );
};

/**
 * default medium button type
 */
 export const MediumDefaultButton = (props) => {
  return (
    <MediumButton {...props} color="primary" />
  );
};

/**
 * default medium button type
 */
 export const MediumAlternateButton = (props) => {
  return (
    <MediumButton {...props} color="secondary" />
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

/**
 * default small button type
 */
 export const SmallAlternateButton = (props) => {
  return (
    <SmallButton {...props} color="secondary" />
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

/**
 * left aligned button
 */
export const LeftAlignedButton = styled(LargeButton)`
  align-self: flex-start;
`;

/**
 * left aligned alternate button
 */
export const LeftAltButton = styled(LargeAlternateButton)`
  align-self: flex-start;
`;

/**
* right aligned button
*/
export const RightAlignedButton = styled(LargeButton)`
  align-self: flex-end;
`;

/*
* right aligned medium button
*/
export const RightAlignMedButton = styled(MediumButton)`
  align-self: flex-end;
`;

/*
* left aligned medium button
*/
export const LeftAlignMedButton = styled(MediumButton)`
  align-self: flex-start;
`;

/*
* left aligned medium button
*/
export const LeftAltMedButton = styled(MediumAlternateButton)`
  align-self: flex-start;
`;


/**
 * left aligned submit button
 */
export const LeftAlignedSubmitButton = styled(LargeSubmitButton)`
  align-self: flex-start;
`;

/**
 * right aligned submit button
 */
export const RightAlignedSubmitButton = styled(LargeSubmitButton)`
  align-self: flex-end;
`;