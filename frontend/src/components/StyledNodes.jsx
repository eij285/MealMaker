import React from 'react';
import styled from '@emotion/styled';
import { Alert, IconButton } from '@mui/material';
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