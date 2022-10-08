import React from 'react';
import PropTypes from 'prop-types';
import Layout from './Layout';
import { Grid, Card, CardContent } from '@mui/material';

function AuthLayout ({ children }) {

  return (
    <Layout>
      <Grid
        container
        justifyContent="center"
        alignContent="center"
        sx={{minHeight: '100%' }}
      >
        <Grid item xl={3} lg={4} md={6} sm={8} xs={12}>
          <Card>
            <CardContent>
              {children}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Layout>
  );
}

AuthLayout.propTypes = {
  children: PropTypes.any,
};

export default AuthLayout;
