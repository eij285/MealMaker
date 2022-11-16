import React from 'react';
import PropTypes from 'prop-types';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  AppBar,
  Avatar,
  Box,
  IconButton,
  InputAdornment,
  ListItemIcon,
  ListItemText,
  MenuItem,
  MenuList,
  SpeedDialIcon,
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
import { backendRequest, tokenToUserId } from '../../helpers';
import Logo from '../../assets/chef-hat.png'
import UserProfilePage from '../../pages/User/UserProfilePage';
import Button from '@mui/material/Button';

import SettingsIcon from '@mui/icons-material/Settings';
import Message from '@mui/icons-material/Message';
import Divider from '@mui/material/Divider';
import Menu from '@mui/material/Menu';
import Tooltip from '@mui/material/Tooltip';

import SpeedIcon from '@mui/icons-material/Speed';


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

const SearchInput = () => {
  const navigate = useNavigate();
  const styles = {
    background: '#ffffff',
    borderRadius: '16px',
    padding: 0,
    border: '1px solid #cccccc',
    '& input' : {
      background: '#ffffff',
      padding: '8px',
      borderRadius: 16
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
    <TextField type="text" size="small" sx={ styles } placeholder={placeHold} variant="standard"
      InputProps={{
        disableUnderline: true,
        startAdornment: (
          <InputAdornment position="start" sx={{ml: 2}}>
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
  const logout = globals.logout;
  const navigate = useNavigate();

  const [userAvatar, setUserAvatar] = React.useState('');
  const [responseError, setResponseError] = React.useState('');

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

  const loadUserAvatar = () => {
    const body = {
      user_id: tokenToUserId(token)
    };
    backendRequest('/user/stats', body, 'POST', token, (data) => {
      setUserAvatar(data.body.user_image);
    }, (error) => {
      console.log(tokenToUserId(token));
      console.log(error);
      setResponseError(error);
    });
  };

  React.useEffect(() => {
    loadUserAvatar();
  }, [token]);

  const toolbarStyles = {
    flexDirection: 'row',
    justifyContent: 'space-between',
  };
  const boxStyles = {
    display: 'flex',
    flexDirection: 'row',
    columnGap: '10px',
  };

  const AccountMenu = () => {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const open = Boolean(anchorEl);
    const handleClick = (event) => {
      setAnchorEl(event.currentTarget);
    };
    const handleClose = () => {
      setAnchorEl(null);
    };
    return (
      <React.Fragment>
        <Box sx={{ display: 'flex', alignItems: 'center', textAlign: 'center' }}>
          <Tooltip title="Account settings">
            <IconButton
              onClick={handleClick}
              size="small"
              sx={{ ml: 2 }}
              aria-controls={open ? 'account-menu' : undefined}
              aria-haspopup="true"
              aria-expanded={open ? 'true' : undefined}
            >
              <Avatar sx={{ width: 32, height: 32, background: '#666666'}} />
            </IconButton>
          </Tooltip>
        </Box>
        <Menu
          anchorEl={anchorEl}
          id="account-menu"
          open={open}
          onClose={handleClose}
          onClick={handleClose}
          PaperProps={{
            elevation: 0,
            sx: {
              overflow: 'visible',
              filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
              mt: 1.5,
              '& .MuiAvatar-root': {
                width: 32,
                height: 32,
                ml: -0.5,
                mr: 1,
              },
              '&:before': {
                content: '""',
                display: 'block',
                position: 'absolute',
                top: 0,
                right: 14,
                width: 10,
                height: 10,
                bgcolor: 'background.paper',
                transform: 'translateY(-50%) rotate(45deg)',
                zIndex: 0,
              },
            },
          }}
          transformOrigin={{ horizontal: 'right', vertical: 'top' }}
          anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
        >
          <MenuItem component={RouterLink} to={`/user/${tokenToUserId(token)}`}>
            <Avatar /> Profile
          </MenuItem>
          <MenuItem component={RouterLink} to={'/user-profile'}>
            <ListItemIcon>
              <SpeedIcon />
            </ListItemIcon>
          Dashboard
          </MenuItem>
          <Divider />
          <MenuItem component={RouterLink} to={'/user-preferences'}>
            <ListItemIcon>
              <SettingsIcon />
            </ListItemIcon>
            Settings
          </MenuItem>
          <MenuItem onClick={userLogout}>
            <ListItemIcon>
              <LogoutIcon/>
            </ListItemIcon>
            Logout
          </MenuItem>
        </Menu>
      </React.Fragment>
    );
  }

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
          <Tooltip title="Messages">
            <IconButton
              aria-label="messages"
              component={RouterLink} to="/message-rooms"
              disableRipple={true}
              sx={{'&:hover': {color: '#000000'}}}
            >
              <Message />
            </IconButton>
          </Tooltip>
          <Tooltip title="Shopping cart">
            <IconButton 
              aria-label="shopping cart"
              component={RouterLink} to="/cart"
              disableRipple={true}
              sx={{'&:hover': {color: '#000000'}}}
            >
              <ShoppingCartIcon />
              <Typography component="span" variant="span">
                {cartItems.length}
              </Typography>
            </IconButton>
          </Tooltip>
          <AccountMenu />
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
