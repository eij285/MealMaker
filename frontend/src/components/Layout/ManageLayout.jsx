import React from 'react';
import PropTypes from 'prop-types';
import Layout from './Layout';

function ManageLayout ({ children }) {
  return (
    <Layout>
      {children}
    </Layout>
  );
}

ManageLayout.propTypes = {
  children: PropTypes.any,
};

export default ManageLayout;
