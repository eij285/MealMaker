import React from 'react';
import styled from '@emotion/styled';
import { Alert, Box, IconButton, Paper, Rating, Typography } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

const CustomAlert = ({props, status, message, setMessage}) => {
  return (
    <Alert {...props} severity={status} action={
      <IconButton aria-label="close" color="inherit" size="small"
        onClick={() => { setMessage(''); }}>
        <CloseIcon fontSize="inherit" />
      </IconButton>}>
      {message}
    </Alert>
  );
};

export const ErrorAlert = ({props, message, setMessage}) => {
  return (
    <CustomAlert {...props} status="error" message={message}
      setMessage={setMessage} />
  );
};

export const SuccessAlert = ({props, message, setMessage}) => {
  return (
    <CustomAlert {...props} status="success" message={message}
      setMessage={setMessage} />
  );
};

export const FlexColumn = styled.div`
  display: flex;
  flex-direction: column;
  row-gap: 20px;
`;

export const FlexRow = styled.div`
  display: flex;
  flex-direction: row;
  column-gap: 20px;
`;

export const FlexRowWrap = styled(FlexRow)`
  flex-wrap: wrap;
`;

export const ImageContainer4by3 = styled.div`
  position: relative;
  padding-bottom: 75%;
  & img, & svg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
`;

/**
 * responsive image using a 4 by 3 aspect ration
 */
 export const ResponsiveImage4by3 = ({ src, alt }) => {
  return (
    <ImageContainer4by3>
      <img src={src} alt={alt} />
    </ImageContainer4by3>
  );
};
