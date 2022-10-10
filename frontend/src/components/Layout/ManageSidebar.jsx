import * as React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { styled } from '@mui/material/styles';
import MuiDrawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import InboxIcon from '@mui/icons-material/MoveToInbox';
import MailIcon from '@mui/icons-material/Mail';

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

const SidebarItemContainer = styled(ListItem)(() => ({
    display: 'block',
    padding: 0,
    borderBottom: '1px solid #cccccc',
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
    color: '#333333'
  }),
);

const SidebarItem = ({to, text, open, icon}) => {
  return (
    <SidebarItemContainer component={RouterLink} to={to}>
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
  const [open, setOpen] = React.useState(false);

  return (
    <Sidebar variant="permanent" open={open}>
      <SidebarToggle>
        <IconButton onClick={() => setOpen(!open)}>
          {open ? <ChevronLeftIcon /> : <ChevronRightIcon />}
        </IconButton>
      </SidebarToggle>
      <Divider />
      <List sx={{ paddingTop: 0 }}>
        <SidebarItem to="/user-profile" text="Update Profile" open={open} icon={<InboxIcon />} />
        <SidebarItem to="#" text="My Recipes" open={open} icon={<InboxIcon />} />
        <SidebarItem to="#" text="Cook Books" open={open} icon={<InboxIcon />} />
        <SidebarItem to="#" text="Subscriptions" open={open} icon={<InboxIcon />} />
        <SidebarItem to="#" text="Subscribers" open={open} icon={<InboxIcon />} />
        <SidebarItem to="#" text="Preferences" open={open} icon={<InboxIcon />} />
        <SidebarItem to="#" text="Messages" open={open} icon={<InboxIcon />} />
        <SidebarItem to="#" text="Shopping" open={open} icon={<InboxIcon />} />
      </List>
    </Sidebar>
  );
}
