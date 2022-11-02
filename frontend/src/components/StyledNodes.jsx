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
  Tooltip,
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

export const FlexColumnNoGap = styled.div`
  display: flex;
  flex-direction: column;
`;

export const FlexColumnSpaced = styled(FlexColumnNoGap)`
  justify-content: space-between;
`;

export const FlexColumnVCentred = styled(FlexColumnNoGap)`
  justify-content: center;
`;

export const FlexColumn = styled(FlexColumnNoGap)`
  row-gap: 20px;
`;

export const FlexRowNoGap = styled.div`
  display: flex;
  flex-direction: row;
`;

export const FlexRow = styled(FlexRowNoGap)`
  column-gap: 20px;
`;

export const FlexRowVCentred = styled(FlexRow)`
  align-items: center;
`;

export const FlexRowHCentred = styled(FlexRow)`
  justify-content: center;
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

const UserImageNameTooltipInner = React.forwardRef((props, ref) => {
  return (<Box sx={{alignSelf: 'flex-start'}} {...props} ref={ref}>
    <UserImageName src={props.src} name={props.name} />
  </Box>);
});

export const UserImageNameTooltip = ({ src, name, title }) => {
  return (
    <Tooltip title={title} placement="right" arrow>
      <UserImageNameTooltipInner src={src} name={name} />
    </Tooltip>
  )
};

export const UserImageNameControl = ({ src, name, to, visibility }) => {
  return (
    <>
      {visibility === 'public' &&
      <UserImageNameLink src={src} name={name} to={to} />}
      {visibility !== 'public' &&
      <UserImageNameTooltip src={src} name={name}
        title="this is a private profile" />}
    </>
  );
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

const WYSIWYGOutputContainer = styled.section`
  overflow: hidden;
  max-width: 100vw;
  position: relative;
  & * {
    max-width: 100%;
    position: relative;
  }
  blockquote {
    font-style: italic;
  }
  & blockquote::before {
    content: open-quote;
    position: absolute;
    left: -16px;
    top: -10px;
    font-size: 2.4em;
  }
  & table {
    border-collapse: collapse;
  }
  & table th, & table td {
    border: 1px solid #999999;
    padding: 4px 8px;
  }
  & table th {
    border-bottom: 2px solid #999999;
  }
  & a {
    color: #999999;
  }
  & a:active, & a:hover {
    color: #333333;
  }
`;

export const WYSIWYGOutput = ({children}) => {
  // this approach should only be used temporarily until a html parser is added
  // else the website become vulnerable to client-side attacks (e.g. XSS, HTML
  // injection, etc)
  return (
    <WYSIWYGOutputContainer dangerouslySetInnerHTML={{__html: children}} />
  );
};
