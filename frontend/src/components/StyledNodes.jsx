import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import styled from '@emotion/styled';
import {
  Alert,
  Box,
  Button,
  Checkbox,
  Container,
  Dialog,
  DialogActions,
  DialogContent,
  DialogContentText,
  DialogTitle,
  Divider,
  Drawer,
  FormControlLabel,
  FormGroup,
  Grid,
  IconButton,
  Link,
  Paper,
  Slider,
  Tooltip,
  Typography
} from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import GlobalContext from '../utils/GlobalContext';
import parse from 'html-react-parser';
import { MediumDefaultButton, MediumAlternateButton } from './Buttons';
import { SubPageTitle } from './TextNodes';
import { CentredElementsForm } from '../components/Forms';

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

export const UserPreferencesComponent = () => {
  const globals = React.useContext(GlobalContext);
  const userPreferences = globals.userPreferences;
  const setUserPreferences = globals.setUserPreferences;

  const boxStyles = {
    position: 'fixed',
    width: '100%',
    left: 0,
    zIndex: 2,
  };
  const btnStyles = {
    alignSelf: 'flex-start',
    marginLeft: '14px',
    padding: 0,
    '&:hover svg': {
      opacity: 0.9
    }
  };

  const openBtnStyles = {
    ...btnStyles,
    top: '-26px',
    position: 'absolute',
    '& svg': {
      width: '48px',
      height: '48px',
      opacity: 0.6,
      marginBottom: '-10px'
    },
  };

  const closeBtnStyles = {
    ...btnStyles,
    position: 'relative',
    height: '32px',
    marginTop: '20px',
    '& svg': {
      width: '48px',
      height: '48px',
      opacity: 0.6,
    },
  };

  const [open, setOpen] = React.useState(false);

  const handlePrefsChange = (e) => {
    const objKey = e.target.name;
    const objValue = e.target.checked;
    setUserPreferences({...userPreferences, [objKey]: objValue});
  };

  const prepTimes = [0, 30, 60, 90, 120, 150, 180, 210];

  const sliderChange = (e, values) => {
    setUserPreferences({
      ...userPreferences,
      minMinutes: values[0],
      maxMinutes: values[1],
    });
  };

  const unspecifiedTimeToggle = (e) => {
    setUserPreferences({
      ...userPreferences,
      showUnspecifiedTime: !userPreferences.showUnspecifiedTime
    });
  };

  const handleCuisineChange = (e) => {
    const objKey = e.target.name;
    const isChecked = e.target.checked;
    if (objKey === 'Unspecified') {
      setUserPreferences({
        ...userPreferences,
        showUnspecifiedCuisines: isChecked
      });
    } else {
      setUserPreferences({
        ...userPreferences,
        cuisines: {
          ...userPreferences.cuisines,
          [`${objKey}`]: isChecked,
        },
      });
    }
  };

  return (
    <Box sx={ boxStyles }>
      <Drawer
        variant="persistent"
        anchor="top"
        open={open}
      >
        <Container maxWidth={false} sx={{pt: 8}}>
          <CentredElementsForm noValidate onChange={handlePrefsChange}>
            <FormGroup>
              <SubPageTitle>Meals</SubPageTitle>
              <FlexRowWrap>
                <FormControlLabel label="Breakfast" control={
                  <Checkbox name="breakfast" checked={userPreferences.breakfast} />} />
                <FormControlLabel label="Lunch" control={
                  <Checkbox name="lunch" checked={userPreferences.lunch} />} />
                <FormControlLabel label="Dinner" control={
                  <Checkbox name="dinner" checked={userPreferences.dinner} />} />
                <FormControlLabel label="Snack" control={
                  <Checkbox name="snack" checked={userPreferences.snack} />} />
              </FlexRowWrap>
            </FormGroup>
            <FormGroup>
              <SubPageTitle>Dietary Needs</SubPageTitle>
              <FlexRowWrap>
                <FormControlLabel label="Vegetarian" control={
                  <Checkbox name="vegetarian" checked={userPreferences.vegetarian} />} />
                <FormControlLabel label="Vegan" control={
                  <Checkbox name="vegan" checked={userPreferences.vegan} />} />
                <FormControlLabel label="Kosher" control={
                  <Checkbox name="kosher" checked={userPreferences.kosher} />} />
                <FormControlLabel label="Halal" control={
                  <Checkbox name="halal" checked={userPreferences.halal} />} />
                <FormControlLabel label="Dairy Free" control={
                  <Checkbox name="dairyFree" checked={userPreferences.dairyFree} />} />
                <FormControlLabel label="Gluten Free" control={
                  <Checkbox name="glutenFree" checked={userPreferences.glutenFree} />} />
                <FormControlLabel label="Nut Free" control={
                  <Checkbox name="nutFree" checked={userPreferences.nutFree} />} />
                <FormControlLabel label="Egg Free" control={
                  <Checkbox name="eggFree" checked={userPreferences.eggFree} />} />
                <FormControlLabel label="Shellfish Free" control={
                  <Checkbox name="shellfishFree" checked={userPreferences.shellfishFree} />} />
                <FormControlLabel label="Soy Free" control={
                  <Checkbox name="soyFree" checked={userPreferences.soyFree} />} />
              </FlexRowWrap>
            </FormGroup>
          </CentredElementsForm>
          <CentredElementsForm noValidate onChange={handleCuisineChange}>
            <FormGroup>
              <SubPageTitle>Cuisines</SubPageTitle>
              <FlexRowWrap>
              {Object.keys(userPreferences.cuisines).map((cuisine, index) => (
                <FormControlLabel key={index} label={`${cuisine}`} control={
                  <Checkbox name={`${cuisine}`}
                    checked={userPreferences.cuisines[`${cuisine}`]} />} />
              ))}
              <Divider orientation="vertical" variant="middle" flexItem />
              <FormControlLabel label="Unspecified" control={
                <Checkbox name="Unspecified"
                  checked={userPreferences.showUnspecifiedCuisines} />} />
              </FlexRowWrap>
            </FormGroup>
          </CentredElementsForm>
          <FlexColumn>
            <SubPageTitle id="preparation-time-range-filter">
              Preparation Time (minutes)
            </SubPageTitle>
            <Grid container columnGap={8} rowGap={2}>
              <Grid item xl={6} lg={6} md={12} sm={12} xs={12}>
                <Slider track={false}
                  aria-labelledby="preparation-time-range-filter"
                  value={[userPreferences.minMinutes, userPreferences.maxMinutes]}
                  min={prepTimes[0]}
                  max={prepTimes[prepTimes.length - 1]}
                  disableSwap
                  marks={prepTimes.map(t => {
                    return {
                      value: t,
                      label: `${t}`
                    }
                  })}
                  onChange={sliderChange}
                />
              </Grid>
              <Grid item xl={4} lg={4} md={12} sm={12} xs={12}>
                <FormControlLabel label="Show Unspecified Time" control={
                  <Checkbox name="showUnspecifiedTime"
                    checked={userPreferences.showUnspecifiedTime}
                    onChange={unspecifiedTimeToggle} />} />
              </Grid>
            </Grid>
          </FlexColumn>
        </Container>
        <Paper component={IconButton} disableRipple={true} sx={ closeBtnStyles }
          onClick={() => setOpen(false)} elevation={3}>
          <ExpandLessIcon />
        </Paper>
      </Drawer>
      {!open &&
      <Paper component={IconButton} disableRipple={true} sx={ openBtnStyles }
        onClick={() => setOpen(true)} elevation={3}>
        <ExpandMoreIcon />
      </Paper>}
    </Box>
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
  // injection, etc). children must be a string else page containing component
  // results in critical error
  return (<>
    {children && typeof variable === 'string' &&
    <WYSIWYGOutputContainer>
      {parse(children)}
    </WYSIWYGOutputContainer>}
    </>);
};
