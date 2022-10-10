import React from 'react';
import PropTypes from 'prop-types';
import Layout from './Layout';
import ManageSidebar from './ManageSidebar';
import { Box } from '@mui/material';

function ManageLayout ({ children }) {
  return (
    <Layout incSearch={true} incButtons={true}>
      <ManageSidebar />
      <Box sx={{ p: 2 }}>
        {children}
      </Box>
    </Layout>
  );
}

ManageLayout.propTypes = {
  children: PropTypes.any,
};

export default ManageLayout;
