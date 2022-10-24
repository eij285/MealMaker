import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import styled from '@emotion/styled';
import {
  Alert,
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  IconButton,
  Link,
  Paper,
  Rating,
  Typography
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { MediumDefaultButton, MediumAlternateButton } from './Buttons';
import { SmallBlackText } from './TextNodes';

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

export const FlexRowWrapSpaced = styled(FlexRowWrap)`
  justify-content: space-between;
`;

export const ImageContainer = styled.div`
  position: relative;
  & img, & svg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
`;

export const ImageContainer4by3 = styled(ImageContainer)`
  padding-bottom: 75%;
`;

export const ImageContainerSquare = styled(ImageContainer)`
  padding-bottom: 100%;
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

const UserNameText = styled(Typography)`
  color: #333333;
  align-self: center;
  padding-left: 4px;
`;

export const UserImageName = ({ src, name }) => {
  return (
    <Box sx={{display: 'flex', color: '#000000'}}>
      <Box sx={{width: '32px'}}>
        <ImageContainerSquare>
          {src && <img src={src} alt={name} />}
          {!src && <AccountCircleIcon />}
        </ImageContainerSquare>
      </Box>
      <UserNameText>{name}</UserNameText>
    </Box>
  );
};

export const UserImageNameLink = ({ src, name, to }) => {
  return (
    <Link component={RouterLink} to={to} sx={{textDecoration: 'none'}}>
      <UserImageName src={src} name={name} />
    </Link>
  )
};

/**
 * Confirmation dialog to prevent accidental destructive actions such as content
 * deletion
 */
export const ConfirmationDialog = ({ title, description, acceptContent,
  rejectContent, openState, setOpenState, execOnAccept }) => {
  return (
    <Dialog
      open={openState}
      onClose={() => setOpenState(false)}
      aria-labelledby="confirmation-dialog-title"
      aria-describedby="confirmation-dialog-description"
    >
      <DialogTitle id="confirmation-dialog-title">
        {title}
      </DialogTitle>
      <DialogContent>
        <DialogContentText id="confirmation-dialog-description">
          {description}
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <MediumDefaultButton onClick={() => execOnAccept()}>
          {acceptContent}
        </MediumDefaultButton>
        <MediumAlternateButton onClick={() => setOpenState(false)} autoFocus>
          {rejectContent}
        </MediumAlternateButton>
      </DialogActions>
    </Dialog>
  );
};
