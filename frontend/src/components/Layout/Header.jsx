import React from 'react';
import PropTypes from 'prop-types';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { AppBar, Box, InputAdornment, Link, TextField, Toolbar, Typography } from '@mui/material';
import { HeaderButton } from '../../components/Buttons';
import LoginIcon from '@mui/icons-material/Login';
import LogoutIcon from '@mui/icons-material/Logout';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SearchIcon from '@mui/icons-material/Search';
import GlobalContext from '../../utils/GlobalContext';
import { backendRequest } from '../../helpers';

const LogoutButton = () => {
  const globals = React.useContext(GlobalContext);
  const token = globals.token;
  const logout = globals.logout;
  const navigate = useNavigate();

  const userLogout = (e) => {
    e.preventDefault();
    if (token) {
      // send to backend
      backendRequest('/auth/logout', {}, 'POST', token, (data) => {});
      logout();
    }
    navigate('/');
  };

  return (
    <HeaderButton onClick={userLogout}>
      <LogoutIcon />&nbsp;Log out
    </HeaderButton>
  );
};

const SearchInput = () => {
  const styles = {
    background: "#ffffff",
    borderRadius: '4px',
    padding: 0,
    border: '1px solid #cccccc',
    "& input" : {
      background: "#ffffff",
      padding: '4px 8px',
      borderRadius: 0
    },
    '@media screen and (max-width: 40em)': {
      "& .css-1q6at85-MuiInputBase-root-MuiOutlinedInput-root, & input": {
        paddingLeft: '2px',
      },
      "& .css-ittuaa-MuiInputAdornment-root": {
        margin: 0
      }
    }
  };
  return (
    <TextField type="text" size="small" sx={ styles } placeholder="search"
      InputProps={{
        startAdornment: (
          <InputAdornment position="start">
            <SearchIcon />
          </InputAdornment>
        )
      }} />
  );
};

function Header ({ incSearch, incButtons }) {
  const globals = React.useContext(GlobalContext);
  const token = globals.token;

  const brandStyles = {
    fontWeight: '600',
    textShadow: '2px 1px 2px #000000',
    marginRight: '4px',
    '@media screen and (max-width: 40em)': {
      fontSize: '14pt',
    },
    '@media screen and (max-width: 36em)': {
      fontSize: '10pt',
    }
  };
  const toolbarStyles = {
    flexDirection: 'row',
    justifyContent: 'space-between',
  };
  const boxStyles = {
    display: 'flex',
    flexDirection: 'row',
    columnGap: '10px',
    '@media screen and (max-width: 40em)': {
      columnGap: '4px'
    }
  };
  return (
    <AppBar position="fixed" color="primary">
      <Toolbar variant="dense" sx={ toolbarStyles }>
        <Link
          component={RouterLink}
          to="/"
          underline="none"
        >
          <Typography
            component="h1"
            variant="h4"
            color="white"
            sx={ brandStyles }
          >
            MealMaker
          </Typography>
        </Link>
        <Box sx={ boxStyles }>
          {incSearch && <SearchInput />}
          {incButtons && !token && <>
          <HeaderButton component={RouterLink} to="/login">
            <LoginIcon />&nbsp;Log in
          </HeaderButton>
          <HeaderButton component={RouterLink} to="/signup">
            Sign up
          </HeaderButton>
          </>}
          {incButtons && token && <>
          <HeaderButton component={RouterLink} to="/user-profile">
            <AccountCircleIcon />&nbsp;My Profile
          </HeaderButton>
          <LogoutButton />
          </>}
        </Box>
      </Toolbar>
    </AppBar>
  );
}

Header.propTypes = {
  incSearch: PropTypes.bool,
  incButtons: PropTypes.bool,
};

export default Header;
