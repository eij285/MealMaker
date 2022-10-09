import React from 'react';
import PropTypes from 'prop-types';
import Layout from './Layout';

function ExploreLayout ({ children }) {
  return (
    <Layout incSearch={true} incButtons={true}>
      {children}
    </Layout>
  );
}

ExploreLayout.propTypes = {
  children: PropTypes.any,
};

export default ExploreLayout;
