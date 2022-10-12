import React from 'react';
import PropTypes from 'prop-types';
import Layout from './Layout';
import { Grid, Card, CardContent } from '@mui/material';
import { FlexColumn } from '../../components/StyledNodes';

function AuthLayout ({ children }) {

  return (
    <Layout incSearch={false} incButtons={false}>
      <Grid
        container
        justifyContent="center"
        alignContent="center"
      >
        <Grid item xl={3} lg={4} md={6} sm={8} xs={12}>
          <Card>
            <CardContent>
              <FlexColumn>
                {children}
              </FlexColumn>
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
