import React from 'react';
import { Box, Grid, Typography } from '@mui/material';
import styled from '@emotion/styled';
import BlockIcon from '@mui/icons-material/Block';
import ExploreLayout from '../../components/Layout/ExploreLayout';
import { PageTitle } from '../../components/TextNodes';

const ForbiddenIcon = styled(BlockIcon)`
  color: #f44336;
  width: 80px;
  height: auto;
`;

function Forbidden403Page () {
  return (
    <ExploreLayout>
      <Grid container alignItems="center" justifyContent="center">
        <Box flexDirection="column" textAlign="center">
          <ForbiddenIcon />
          <PageTitle>403</PageTitle>
          <Typography>Forbidden</Typography>
        </Box>
      </Grid>
    </ExploreLayout>
  );
}

export default Forbidden403Page;
