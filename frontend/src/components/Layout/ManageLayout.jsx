import React from 'react';
import PropTypes from 'prop-types';
import Layout from './Layout';
import ManageSidebar from './ManageSidebar';
import { Box, Grid } from '@mui/material';

function ManageLayout ({ children }) {
  return (
    <Layout incSearch={true} incButtons={true}>
      <ManageSidebar />
      <Box sx={{ p: 2, flex: 1 }}>
        <Grid container>
          {children}
        </Grid>
      </Box>
    </Layout>
  );
}

ManageLayout.propTypes = {
  children: PropTypes.any,
};

export default ManageLayout;
