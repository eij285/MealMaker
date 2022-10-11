import React from 'react';
import { Link, Typography } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import styled from '@emotion/styled';

/**
 * page title text block
 */

export const PageTitle = (props) => {
  const PageTitleBase = styled(Typography)`
    font-weight: 600;
    margin: 20px 0;
  `;
  return (
    <PageTitleBase {...props} component="h2" variant="h4" />
  );
};

export const CentredPageTitle = (props) => {
  return (
    <PageTitle {...props} align="center" />
  );
};


export const CustomLink = (props) => {
  const LinkBase = styled(Link)`
    font-weight: 500;
  `;
  return (
    <LinkBase {...props} component={RouterLink} underline="always" />
  );
};