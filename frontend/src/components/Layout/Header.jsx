import React from 'react';
import PropTypes from 'prop-types';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  AppBar,
  Box,
  IconButton,
  InputAdornment,
  TextField,
  Toolbar,
  Typography
} from '@mui/material';
import { HeaderButton } from '../../components/Buttons';
import LoginIcon from '@mui/icons-material/Login';
import PersonAddIcon from '@mui/icons-material/PersonAdd';
import LogoutIcon from '@mui/icons-material/Logout';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import SearchIcon from '@mui/icons-material/Search';
import GlobalContext from '../../utils/GlobalContext';
import { backendRequest } from '../../helpers';
import Logo from '../../assets/chef-hat.png'

const HeaderButtonTypo = ({children}) => {
  const styles = {
    paddingLeft: '6px',
    '@media screen and (max-width: 40em)': {
      display: 'none'
    }
  };
  return (
    <Typography sx={ styles } component="span" variant="span">
      {children}
    </Typography>
  );
};

const LogoutButton = () => {
  const globals = React.useContext(GlobalContext);
  const token = globals.token;
  const logout = globals.logout;
  const navigate = useNavigate();

  const userLogout = (e) => {
    e.preventDefault();
    if (token) {
      // send to backend
      backendRequest('/auth/logout', {}, 'POST', token, (data) => {
        logout();
        navigate('/');
      }, (error) => {
        logout();
        navigate('/');
      });
    }
  };

  return (
    <HeaderButton onClick={userLogout}>
      <LogoutIcon />
      <HeaderButtonTypo>Log out</HeaderButtonTypo>
    </HeaderButton>
  );
};

const SearchInput = () => {
  const navigate = useNavigate();
  const styles = {
    background: '#ffffff',
    borderRadius: '4px',
    padding: 0,
    border: '1px solid #cccccc',
    '& input' : {
      background: '#ffffff',
      padding: '8px',
      borderRadius: 0
    },
    '@media screen and (max-width: 40em)': {
      '& .MuiInputBase-root, & input': {
        paddingLeft: '2px',
      },
      '& .css-ittuaa-MuiInputAdornment-root': {
        margin: 0
      }
    },
    '@media screen and (min-width: 60em)': {
      '& input': {
        minWidth: '300px'
      },
    }
  };

  const placeHold = window.innerWidth > 800 ? 'What would you like to cook?'
    : 'search';

  return (
    <TextField type="text" size="small" sx={ styles } placeholder={placeHold}
      InputProps={{
        startAdornment: (
          <InputAdornment position="start">
            <SearchIcon />
          </InputAdornment>
        )
      }} onKeyPress={(e) => {
        if (e.key === 'Enter') {
          navigate(`/search/${encodeURIComponent(e.target.value)}`);
        }
      }} />
  );
};

function BrandingComponent() {
  const brandStyles = {
    fontWeight: '300',
    marginRight: '4px',
    padding: 0,
    '& img': {
      width: '40px',
      height: 'auto',
    },
    '&:hover .MuiTypography-span': {
      color: '#000000',
    },
    '@media screen and (max-width: 46em)': {
      fontSize: '14pt',
    },
    '@media screen and (max-width: 46em)': {
      fontSize: '12pt',
    },
    '@media screen and (max-width: 36em)': {
      fontSize: '10pt',
      display: 'flex',
      flexDirection: 'column',
      '& img': {
        width: '32px',
      },
      '& .MuiTypography-span': {
        lineHeight: 0.75
      }
    }
  };

  return (
    <IconButton component={RouterLink} to="/" sx={brandStyles}
      disableRipple={true}>
      <img src={Logo} alt="Meal Maker logo" />
      <Typography variant="span" component="span">Meal Maker</Typography>
    </IconButton>
  );
};

function Header ({ incSearch, incButtons }) {
  const globals = React.useContext(GlobalContext);
  const token = globals.token;
  const cartItems = globals.cartItems;

  const toolbarStyles = {
    flexDirection: 'row',
    justifyContent: 'space-between',
  };
  const boxStyles = {
    display: 'flex',
    flexDirection: 'row',
    columnGap: '10px',
  };

  return (
    <AppBar position="fixed" color="default" sx={{zIndex: 1000}}>
      <Toolbar variant="dense" sx={ toolbarStyles }>
        <BrandingComponent />
        {incSearch && <SearchInput />}
        <Box sx={ boxStyles }>
          {incButtons && !token && <>
          <HeaderButton component={RouterLink} to="/login">
            <LoginIcon />
            <HeaderButtonTypo>Log in</HeaderButtonTypo>
          </HeaderButton>
          <HeaderButton component={RouterLink} to="/signup">
            <PersonAddIcon />
            <HeaderButtonTypo>Sign up</HeaderButtonTypo>
          </HeaderButton>
          </>}
          {incButtons && token && <>
          <HeaderButton component={RouterLink} to="/cart">
            <ShoppingCartIcon />
            <Typography component="span" variant="span">
              {cartItems.length}
            </Typography>
          </HeaderButton>
          <HeaderButton component={RouterLink} to="/dashboard">
            <AccountCircleIcon />
            <HeaderButtonTypo>Dashboard</HeaderButtonTypo>
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
