import React from 'react';
import PropTypes from 'prop-types';
import Layout from './Layout';

function ExploreLayout ({ children }) {
  return (
    <Layout>
      {children}
    </Layout>
  );
}

ExploreLayout.propTypes = {
  children: PropTypes.any,
};

export default ExploreLayout;
