import React from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import styled from '@emotion/styled';
import { Box, Button, Paper, Rating, Typography } from '@mui/material';
import FoodBankIcon from '@mui/icons-material/FoodBank';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import {
  FlexRow,
  FlexColumn,
  ImageContainer4by3,
  ResponsiveImage4by3,
  FlexColumnNoGap,
  FlexColumnSpaced,
  UserImageName
} from '../StyledNodes';
import { MediumGreyText, SmallGreyText, TextVCentred } from '../TextNodes';
import { RecipePrepartionTime } from './RecipeNodes';
import { SmallDefaultButton } from '../Buttons';
import { getAverageRating } from '../../helpers';
 
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


const HomePageRatingNameAuthor = ({data}) => {
  const ratingAvg = getAverageRating(data.reviews);
  const nReviews = data.reviews.length;
  return (
    <FlexColumn>
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
      <Typography>{data.recipe_name}</Typography>
      <UserImageName src={data.author_image} name={data.author_display_name} />
    </FlexColumn>
  )
};

export const HomePageRecipeItem = ({recipe, level}) => {
  return (
    <RecipeItemPaperCursor>
      <Box sx={{position: 'relative'}}>
        <RecipeItemActionPanel>
          <RecipeItemTitle>{recipe.cuisine}</RecipeItemTitle>
        </RecipeItemActionPanel>
        <RecipeItemPhoto src={recipe.recipe_photo} alt={recipe.recipe_name} />
      </Box>
      <RecipeItemTextContainer>
        <HomePageRatingNameAuthor data={recipe} />
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