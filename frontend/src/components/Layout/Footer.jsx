import React from 'react';
import { AppBar, Toolbar, Typography } from '@mui/material';

function Footer () {
  return (
    <AppBar
      component="footer"
      position="relative"
      sx={{ alignSelf: 'flex-end', backgroundColor: 'white', zIndex: 500 }}
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
