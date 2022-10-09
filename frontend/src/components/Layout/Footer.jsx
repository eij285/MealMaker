import React from 'react';
import { AppBar, Toolbar, Typography } from '@mui/material';

function Footer () {
  return (
    <AppBar
      color="transparent"
      component="footer"
      position="relative"
      sx={{ alignSelf: 'flex-end' }}
    >
      <Toolbar variant="dense">
        <Typography
          component="p"
          color="gray"
        >
          &copy; Code Chefs
        </Typography>
      </Toolbar>
    </AppBar>
  );
}

export default Footer;
