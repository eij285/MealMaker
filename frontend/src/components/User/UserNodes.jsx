import React from 'react';
import styled from '@emotion/styled';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import { Typography } from '@mui/material';

const UserImgContainer = styled.div`
  display: flex;
  position: relative;
  flex-direction: row;
  justify-content: center;
  height: 25vh;
  & img, & svg {
    height: 100%;
    width: auto;
    object-fit: contain;
  }
`;

/**
 * User image component
 */
export const UserImg = ({src, alt}) => {
  return (
    <UserImgContainer>
      {src && <img src={src} alt={alt} />}
      {!src && <AccountCircleIcon />}
    </UserImgContainer>
  );
};

export const ProfileContainer = styled.div`
  position: relative;
  display: flex;
  flex-direction: column;
  row-gap: 20px;
  align-items: center;
`;

export const UserAttribute = ({title, content}) => {
  const typoStyle = {
    display: 'flex',
    columnGap: '8px'
  };
  return (
    <Typography component="p" variant="p" sx={typoStyle}>
      <Typography component="strong" variant="strong">
        {title}:
      </Typography>
      <Typography component="span" variant="span">
        {content}
      </Typography>
    </Typography>
  );
};