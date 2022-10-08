import React from 'react';
import { Box, Grid, Typography } from '@mui/material';
import styled from '@emotion/styled';
import NotInterestedIcon from '@mui/icons-material/NotInterested';
import ExploreLayout from '../../components/Layout/ExploreLayout';
import { PageTitle } from '../../components/TextNodes';

const NotFoundIcon = styled(NotInterestedIcon)`
  color: #f44336;
  width: 80px;
  height: auto;
`;

function NotFound404Page () {
  return (
    <ExploreLayout>
      <Grid container alignItems="center" justifyContent="center">
        <Box flexDirection="column" textAlign="center">
          <NotFoundIcon />
          <PageTitle>404</PageTitle>
          <Typography>Page Not Found</Typography>
        </Box>
      </Grid>
    </ExploreLayout>
  );
}

export default NotFound404Page;
