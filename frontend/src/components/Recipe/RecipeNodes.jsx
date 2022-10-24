import React from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import styled from '@emotion/styled';
import { Box, Button, IconButton, Paper, Rating, Tooltip, Typography } from '@mui/material';
import FoodBankIcon from '@mui/icons-material/FoodBank';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbUpOutlinedIcon from '@mui/icons-material/ThumbUpOutlined';
import { FlexRow, FlexRowWrapSpaced, FlexColumn } from '../StyledNodes';
import { MediumGreyText, TextVCentred } from '../TextNodes';
import { getAverageRating } from '../../helpers';

const RecipeImgContainer = styled.div`
  display: flex;
  flex-direction: row;
`;

export const RecipeImg = ({src, alt}) => {
  return (
    <RecipeImgContainer>
      {src && <img src={src} alt={alt} />}
      {!src && <FoodBankIcon/>}
    </RecipeImgContainer>
  );
};

export const RecipeRating = ({reviews}) => {
  const [avgRating, setAvgRating] = React.useState(0);
  React.useEffect(() => {
    setAvgRating(getAverageRating(reviews));
  }, [reviews]);
  return (
    <Box sx={{ alignSelf: 'center' }}>
      {typeof reviews === typeof [] && <>
        {reviews.length < 1 && <MediumGreyText>No Reviews</MediumGreyText>}
        {reviews.length > 0 && <>
        <Rating value={avgRating} precision={0.5} readOnly />
        <MediumGreyText>
          {avgRating.toFixed(1)}&nbsp;
          ({reviews.length}&nbsp;
          {reviews.length !== 1 && <span>reviews</span>}
          {reviews.length === 1 && <span>review</span>})
        </MediumGreyText>
        </>}
      </>}
    </Box>
  );
};

export const RecipeLikes = ({likesObject, likeRecipe}) => {
  return (
    <>
    {typeof likesObject === typeof {} &&
    <Tooltip title="Like Recipe" placement="top" arrow>
      <IconButton color="info" onClick={likeRecipe}>
        {likesObject.has_liked && <ThumbUpIcon />}
        {!likesObject.has_liked && <ThumbUpOutlinedIcon />}
        &nbsp;{likesObject.likes_count}
      </IconButton>
    </Tooltip>}
    </>
  );
};
