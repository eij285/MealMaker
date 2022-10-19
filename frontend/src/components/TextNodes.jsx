import React from 'react';
import { Link, Typography } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import styled from '@emotion/styled';


const PageTitleBase = styled(Typography)`
  font-weight: 600;
  margin: 20px 0;
`;

/**
 * page title text block
 */
export const PageTitle = (props) => {
  return (
    <PageTitleBase {...props} component="h2" variant="h4" />
  );
};

export const CentredPageTitle = (props) => {
  return (
    <PageTitle {...props} align="center" />
  );
};

/**
 * sub page title h3 element
 */
 export const SubPageTitle = (props) => {
  return (
    <PageTitleBase {...props} component="h3" variant="h5" />
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

export const TextVCentred = styled(Typography)`
  white-space: nowrap;
  display: flex;
  flex-direction: column;
  justify-content: center;
`;

export const SmallGreyText = styled(Typography)`
  font-size: 0.8em;
  color: #888888;
`;
