import React from 'react';
import PropTypes from 'prop-types';
import { Box } from '@mui/material';
import Header from './Header';
import Footer from './Footer';

function Layout ({ incSearch, incButtons, children }) {
    
  const boxStyles = {
    minHeight: '100vh',
    display: 'flex',
    position: 'relative',
    flexDirection: 'column',
    paddingTop: '48px',
    boxSizing: 'border-box'
  };

  return (
    <Box sx={ boxStyles }>
      <Header incSearch={incSearch} incButtons={incButtons} />
      <Box sx={{ display: 'flex', flex: 1 }}>
        {children}
      </Box>
      <Footer />
    </Box>
  );
}

Layout.propTypes = {
  incSearch: PropTypes.bool,
  incButtons: PropTypes.bool,
  children: PropTypes.any,
};

export default Layout;
