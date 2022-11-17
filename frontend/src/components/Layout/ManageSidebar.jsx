import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Divider,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import MuiDrawer from '@mui/material/Drawer';
import { styled } from '@mui/material/styles';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import AccountBoxIcon from '@mui/icons-material/AccountBox';
import SettingsIcon from '@mui/icons-material/Settings';
import FoodBankIcon from '@mui/icons-material/FoodBank';
import MenuBookIcon from '@mui/icons-material/MenuBook';
import { Restaurant } from '@mui/icons-material';
import SpeedIcon from '@mui/icons-material/Speed';
import StoreIcon from '@mui/icons-material/Store';

const drawerWidth = 240;

const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: 'hidden',
});

const closedMixin = (theme) => ({
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: 'hidden',
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up('sm')]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
});

const SidebarToggle = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'flex-end',
  marginTop: '50px',
  padding: theme.spacing(0, 1),
}));

const Sidebar = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    width: drawerWidth,
    maxWidth: '100vw',
    flexShrink: 0,
    whiteSpace: 'nowrap',
    boxSizing: 'border-box',
    zIndex: 0,
    ...(open && {
      ...openedMixin(theme),
      '& .MuiDrawer-paper': openedMixin(theme),
    }),
    ...(!open && {
      ...closedMixin(theme),
      '& .MuiDrawer-paper': closedMixin(theme),
    }),
  }),
);

const SidebarItemContainer = styled(ListItem, {
  shouldForwardProp: (prop) => prop !== 'active' })(({ active }) => ({
    display: 'block',
    padding: 0,
    borderBottomWidth: '1px',
    borderBottomStyle: 'solid',
    borderBottomColor: active ? '#000000' : '#cccccc',
    '& .MuiListItemIcon-root svg': {
      color: active ? '#000000' : '#888888'
    },
    '& .MuiTypography-root': {
      color: active ? '#000000' : '#888888',
      fontWeight: 600
    }
}));

const SidebarItemButton = styled(ListItemButton, {
  shouldForwardProp: (prop) => prop !== 'open' })(({ open }) => ({
    minHeight: 48,
    justifyContent: open ? 'initial' : 'center',
    columnGap: '12px',
    px: 2.5,
  }),
);

const SidebarItemIcon = styled(ListItemIcon, {
  shouldForwardProp: (prop) => prop !== 'open' })(({ open }) => ({
    minWidth: 0,
    mr: open ? 3 : 'auto',
    justifyContent: 'center',
  }),
);

const SidebarItemText = styled(ListItemText, {
  shouldForwardProp: (prop) => prop !== 'open' })(({ open }) => ({
    display: open ? 'block' : 'none',
  }),
);

const SidebarItem = ({to, text, open, icon}) => {
  let activeItem = false;
  const wholeUrlPath = window.location.pathname;
  const urlParts = wholeUrlPath.split('/');
  const urlPath = '/' + (urlParts.length >= 2 ? urlParts[1] : '');
  const pageChildren = {
    '/dashboard': ['/subscriptions', '/subscribers'],
    '/my-recipes': ['/create-recipe', '/edit-recipe'],
    '/user-profile': ['/update-password'],
    '/message-rooms': ['/message-room'],
    '/my-cookbooks': ['/create-cookbook', '/edit-cookbook'],
    '/manage-shopping': ['/add-payment-method', '/edit-payment-method'],
  };
  if (to === wholeUrlPath) {
    activeItem = true;
  } else if (pageChildren.hasOwnProperty(to) &&
    pageChildren[to].includes(urlPath)) {
    activeItem = true;
  }

  return (
    <SidebarItemContainer component={RouterLink} to={to} active={activeItem}>
      <SidebarItemButton open={open}>
        <SidebarItemIcon open={open}>
          {icon}
        </SidebarItemIcon>
        <SidebarItemText primary={text} open={open} />
      </SidebarItemButton>
    </SidebarItemContainer>
  );
};

export default function ManageSidebar() {
  const [open, setOpen] = React.useState(window.innerWidth > 600);

  return (
    <Sidebar variant="permanent" open={open}>
      <SidebarToggle>
        <IconButton onClick={() => setOpen(!open)}>
          {open ? <ChevronLeftIcon /> : <ChevronRightIcon />}
        </IconButton>
      </SidebarToggle>
      <Divider />
      <List sx={{ paddingTop: 0 }}>
        <SidebarItem to="/manage-shopping" text="Shopping" open={open} icon={<StoreIcon />} />
        <SidebarItem to="/user-profile" text="User Profile" open={open} icon={<AccountBoxIcon />} />
        <SidebarItem to="/user-preferences" text="Settings" open={open} icon={<SettingsIcon />} />
      </List>
    </Sidebar>
  );
}
