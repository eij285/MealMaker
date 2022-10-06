import React from 'react';
import PropTypes from 'prop-types';
import { Link as RouterLink } from 'react-router-dom';
import { AppBar, Link, Toolbar, Typography } from '@mui/material';

function Header ({ incSearch, incButtons }) {
  return (
    <AppBar position="fixed" color="primary">
      <Toolbar variant="dense">
        <Link
          component={RouterLink}
          to="/"
          underline="none"
        >
          <Typography
            component="h1"
            variant="h4"
            color="white"
          >
            MealMaker
          </Typography>
        </Link>
      </Toolbar>
    </AppBar>
  );
}

Header.propTypes = {
  incSearch: PropTypes.bool,
  incButtons: PropTypes.bool,
};

export default Header;
