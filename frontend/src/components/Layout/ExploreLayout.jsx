import React from 'react';
import PropTypes from 'prop-types';
import { Container } from '@mui/material';
import Layout from './Layout';

function ExploreLayout ({ children }) {
  return (
    <Layout incSearch={true} incButtons={true}>
      <Container maxWidth="xl">
        {children}
      </Container>
    </Layout>
  );
}

ExploreLayout.propTypes = {
  children: PropTypes.any,
};

export default ExploreLayout;
