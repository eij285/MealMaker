import React from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import styled from '@emotion/styled';
import { Box, Button, Checkbox, Paper, Rating, Typography } from '@mui/material';
import FoodBankIcon from '@mui/icons-material/FoodBank';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import RemoveCircleIcon from '@mui/icons-material/RemoveCircle';
import {
  FlexRow,
  FlexColumn,
  ImageContainer4by3,
  ResponsiveImage4by3,
  FlexColumnNoGap,
  FlexColumnSpaced,
  UserImageName
} from '../StyledNodes';
import { MediumGreyText, SmallBlackText, SmallGreyText, TextVCentred } from '../TextNodes';
import { RecipePrepartionTime } from './RecipeNodes';
import { SmallDefaultButton } from '../Buttons';
import { getAverageRating } from '../../helpers';
import { CheckBox } from '@mui/icons-material';
 
const RecipeItemActionPanel = styled.div`
  box-shadow: -10px 40px 5px -10px rgba(0,0,0,0.75) inset;
  height: 35px;
  display: flex;
  justify-content: space-between;
  padding: 2px 8px;
  position: absolute;
  z-index: 1;
  top: 0;
  left: 0;
  box-sizing: border-box;
  width: 100%;
`;

const RecipeItemPhoto = ({ src, alt }) => {
  return (<>
    {src && <ResponsiveImage4by3 src={src} alt={`${alt} photo`} />}
    {!src && <ImageContainer4by3><FoodBankIcon/></ImageContainer4by3>}
  </>);
};

const RecipeItemPaper = styled(Paper)`
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
`;

const RecipeItemPaperCursor = styled(RecipeItemPaper)`
  cursor: pointer;
`;

const RecipeItemTextContainer = styled(FlexRow)`
  padding: 4px 8px;
  justify-content: space-between;
`;

const RecipeItemTitle = styled(Typography)`
  font-size: 0.85em;
  color: #ffffff;
  white-space: nowrap;
`;

const RecipeItemActions = styled.div`
  display: flex;
  flex-direction: row;
  height: 24px;
`;

const ActionButton = styled(Button)`
  min-width: 40px;
  padding: 0;
`;

const ViewRecipeButton = styled(SmallDefaultButton)`
  position: absolute;
  bottom: 4px;
  right: 4px;
  opacity: 0.8;
  &:hover {
    opacity: 1;
  }
`;

const RatingStarsColumn = styled(FlexColumnNoGap)`
  height: 32px;
`;

/**
 * Rating summary requires reviews and ratings as atomic values
 */
const RatingSummary = ({data}) => {
  return (
    <FlexColumn>
      <RatingStarsColumn>
        {data.review_cnt > 0 && <>
        <Rating value={parseFloat(data.rating_avg)} precision={0.1} readOnly />
        {data.review_cnt == 1 &&
        <SmallGreyText>{data.rating_avg} (1 review)</SmallGreyText>}
        {data.review_cnt > 1 &&
        <SmallGreyText>
          {data.rating_avg} ({data.review_cnt} reviews)
        </SmallGreyText>}
        </>}
        {data.review_cnt < 1 &&
        <MediumGreyText>No Reviews</MediumGreyText>}
      </RatingStarsColumn>
      <Typography>{data.recipe_name}</Typography>
    </FlexColumn>
  )
};

/**
 * Rating summary requires reviews and ratings as collection (arrays)
 */
const AlternativeRatingSummary = ({data}) => {
  const ratingAvg = getAverageRating(data.reviews);
  const nReviews = data.reviews.length;
  return (
    <RatingStarsColumn>
      {nReviews > 0 && <>
      <Rating value={ratingAvg} precision={0.1} readOnly />
      {nReviews === 1 &&
      <SmallGreyText>{ratingAvg} (1 review)</SmallGreyText>}
      {nReviews > 1 &&
      <SmallGreyText>
        {ratingAvg.toFixed(1)} ({nReviews} reviews)
      </SmallGreyText>}
      </>}
      {nReviews < 1 &&
      <MediumGreyText>No Reviews</MediumGreyText>}
    </RatingStarsColumn>
  );
};

const RecipeItemLikes = ({likesCount}) => {
  return (
    <Box sx={{alignSelf: 'flex-end'}}>
      <TextVCentred><ThumbUpIcon />&nbsp;{likesCount}</TextVCentred>
    </Box>
  );
};

export const OwnRecipeItem = ({data, index, cloneRecipe, setDeleteIndex,
  setDialogOpen, setDeleteDesciption}) => {
  const handleDelete = () => {
    setDeleteIndex(index);
    setDialogOpen(true);
    setDeleteDesciption(data.recipe_name);
  };
  return (
    <RecipeItemPaper>
      <Box sx={{position: 'relative'}}>
        <RecipeItemActionPanel>
          <RecipeItemTitle>{data.cuisine}</RecipeItemTitle>
          <RecipeItemActions>
            <ActionButton color="info" component={RouterLink}
              to={`/edit-recipe/${data.recipe_id}`}>
              <EditOutlinedIcon />
            </ActionButton>
            <ActionButton color="warning" onClick={() => cloneRecipe(index)}>
              <ContentCopyIcon />
            </ActionButton>
            <ActionButton color="error" onClick={handleDelete}>
              <DeleteOutlinedIcon />
            </ActionButton>
          </RecipeItemActions>
        </RecipeItemActionPanel>
        <RecipeItemPhoto src={data.recipe_photo} alt={data.recipe_name} />
        <ViewRecipeButton component={RouterLink} to={`/recipe/${data.recipe_id}`}>
          View Recipe
        </ViewRecipeButton>
      </Box>
      <RecipeItemTextContainer>
        <RatingSummary data={data} />
        <FlexColumnSpaced>
          <SmallGreyText align="right">{data.recipe_status}</SmallGreyText>
          <RecipeItemLikes likesCount={data.likes_cnt} />
        </FlexColumnSpaced>
      </RecipeItemTextContainer>
    </RecipeItemPaper>
  )
};

export const OwnCookbookRecipeItem = ({data, index, setRemove}) => {
  return (
    <RecipeItemPaper>
      <Box sx={{position: 'relative'}}>
        <RecipeItemActionPanel>
          <RecipeItemTitle>{data.cuisine}</RecipeItemTitle>
          <RecipeItemActions>
            <ActionButton color="error" onClick={() => setRemove(index)}>
              <RemoveCircleIcon />
            </ActionButton>
          </RecipeItemActions>
        </RecipeItemActionPanel>
        <RecipeItemPhoto src={data.recipe_photo} alt={data.recipe_name} />
      </Box>
      <RecipeItemTextContainer>
        <FlexColumnSpaced>
          <AlternativeRatingSummary data={data} />
          <Typography>{data.recipe_name}</Typography>
        </FlexColumnSpaced>
        <FlexColumnSpaced>
          <SmallGreyText align="right">{data.recipe_status}</SmallGreyText>
          <RecipeItemLikes likesCount={data.likes.likes_count} />
        </FlexColumnSpaced>
      </RecipeItemTextContainer>
    </RecipeItemPaper>
  )
};

export const CookbookScrollerRecipeItem = ({data, index, addRemove}) => {
  const isDraft = data.recipe_status === 'draft';
  let containerStyles = {};
  if (isDraft) {
    containerStyles = {
      '&::before': {
        content: '""',
        display: 'block',
        position: 'absolute',
        height: '100%',
        width: '100%',
        backgroundColor: 'rgba(0,0,0,0.5)'
      }
    };
  }
  return (
    <RecipeItemPaper sx={containerStyles}>
      <Box sx={{position: 'relative', height: '160px', overflow: 'hidden'}}>
        <RecipeItemActionPanel>
          <Typography sx={{color: '#ffffff', lineHeight: 1, fontSize: '8pt'}}>
            {data.cuisine}<br/>
            ({data.recipe_status})
          </Typography>
          <Checkbox disabled={isDraft}
            onChange={(e) => addRemove(index, e.target.checked)} />
        </RecipeItemActionPanel>
        <RecipeItemPhoto src={data.recipe_photo} alt={data.recipe_name} />
        <SmallBlackText align="left">{data.recipe_name}</SmallBlackText>
      </Box>
    </RecipeItemPaper>
  )
};

export const SingleAuthorRecipeItem = ({recipe, level}) => {
  const navigate = useNavigate();
  return (
    <RecipeItemPaperCursor
      onClick={() => navigate(`/recipe/${recipe.recipe_id}`)}>
      <Box sx={{position: 'relative'}}>
        <RecipeItemActionPanel>
          <RecipeItemTitle>{recipe.cuisine}</RecipeItemTitle>
        </RecipeItemActionPanel>
        <RecipeItemPhoto src={recipe.recipe_photo} alt={recipe.recipe_name} />
      </Box>
      <RecipeItemTextContainer>
        <RatingSummary data={recipe} />
        <FlexColumnSpaced>
          <RecipePrepartionTime hours={recipe.preparation_hours}
            minutes={recipe.preparation_minutes}
            level={level} useSmall={true} />
          <RecipeItemLikes likesCount={recipe.likes_cnt} />
        </FlexColumnSpaced>
      </RecipeItemTextContainer>
    </RecipeItemPaperCursor>
  )
};


const RecipeRatingNameAuthor = ({data}) => {
  return (
    <FlexColumn>
      <AlternativeRatingSummary data={data} />
      <Typography>{data.recipe_name}</Typography>
      <UserImageName src={data.author_image} name={data.author_display_name} />
    </FlexColumn>
  )
};

export const RecipeItem = ({recipe, level}) => {
  const navigate = useNavigate();
  return (
    <RecipeItemPaperCursor
      onClick={() => navigate(`/recipe/${recipe.recipe_id}`)}>
      <Box sx={{position: 'relative'}}>
        <RecipeItemActionPanel>
          <RecipeItemTitle>{recipe.cuisine}</RecipeItemTitle>
        </RecipeItemActionPanel>
        <RecipeItemPhoto src={recipe.recipe_photo} alt={recipe.recipe_name} />
      </Box>
      <RecipeItemTextContainer>
        <RecipeRatingNameAuthor data={recipe} />
        <FlexColumnSpaced>
          <RecipePrepartionTime hours={recipe.preparation_hours}
            minutes={recipe.preparation_minutes}
            level={level} useSmall={true} />
          <RecipeItemLikes likesCount={recipe.likes.likes_count} />
        </FlexColumnSpaced>
      </RecipeItemTextContainer>
    </RecipeItemPaperCursor>
  );
};
