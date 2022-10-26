import React from 'react';
import styled from '@emotion/styled';
import { Box, IconButton, Rating, Tooltip, Typography } from '@mui/material';
import FoodBankIcon from '@mui/icons-material/FoodBank';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import ThumbUpOutlinedIcon from '@mui/icons-material/ThumbUpOutlined';
import ThumbDownOutlinedIcon from '@mui/icons-material/ThumbDownOutlined';
import GlobalContext from '../../utils/GlobalContext';
import { ErrorAlert, FlexColumn, FlexColumnNoGap, FlexColumnVCentred, FlexRow, FlexRowNoGap, UserImageNameLink } from '../StyledNodes';
import {
  MediumGreyText,
  MediumBlackText,
  SmallBlackText,
  SmallGreyText,
  SubPageTitle,
  SubPageTitleNoMargins
} from '../TextNodes';
import { TextInput } from '../InputFields';
import { backendRequest, shortDateString, tokenToUserId } from '../../helpers';
import { LeftAlignedButton, LeftAlignMedButton, LeftAltMedButton } from '../Buttons';

const loadReviews = (recipeId, token, setReviews, setError) => {
  const body = {
    recipe_id: recipeId
  };
  const reqURL = '/reviews/all-for-recipe' + (token ? '' : `?recipe_id=${recipeId}`);
  const reqMethod = token ? 'POST' : 'GET';
  backendRequest(reqURL, body, reqMethod, token, (data) => {
    setReviews([...data.reviews])
  }, (error) => {
    setError(error);
  });
};

const CreateReviewComponent = ({recipeId, setReviews, setShow, setError, token}) => {
  const [rating, setRating] = React.useState(3);
  const [comment, setComment] = React.useState('');
  const handleSubmit = () => {
    const body = {
      recipe_id: recipeId,
      rating: rating,
      comment: comment
    };
    backendRequest('/review/create', body, 'POST', token, (data) => {
      loadReviews(recipeId, token, setReviews, setError);
    }, (error) => {
      setError(error);
    });
  };

  const handleCancel = () => {
    setComment('');
    setRating(3);
    setShow(false);
  };
  return (
    <FlexColumn>
      <FlexRow>Rating: 
        <Rating value={rating} onChange={(e, val) => setRating(val)}/>
      </FlexRow>
      <TextInput
        label="Comment"
        multiline
        minRows={2}
        value={comment}
        onChange={(e) => setComment(e.target.value)}
      />
      <FlexRow>
        <LeftAlignMedButton onClick={handleSubmit}>Submit</LeftAlignMedButton>
        <LeftAltMedButton onClick={handleCancel}>Cancel</LeftAltMedButton>
      </FlexRow>
    </FlexColumn>
  );
};

const SingleReview = ({review}) => {
  return (
    <FlexRow>
      <FlexColumnNoGap>
        <UserImageNameLink src={review.user_image} name={review.display_name}
          to={`/user/${review.user_id}`} />
        <SmallGreyText>
          Reviewed: {shortDateString(review.created_on)}
        </SmallGreyText>
        <Rating value={review.rating} readOnly />
        <MediumBlackText>{review.comment}</MediumBlackText>
      </FlexColumnNoGap>
      <FlexColumnVCentred>
        <FlexRow>
          <IconButton>
            {(review.cur_user_vote === '' || review.cur_user_vote === false) &&
            <ThumbUpOutlinedIcon />}
            {review.cur_user_vote === true &&
            <ThumbUpIcon />}
            &nbsp;{review.upvote_count}
          </IconButton>
          <IconButton>
            {(review.cur_user_vote === '' || review.cur_user_vote === true) &&
            <ThumbDownOutlinedIcon />}
            {review.cur_user_vote === false &&
            <ThumbDownIcon />}
            &nbsp;{review.downvote_count}
          </IconButton>
        </FlexRow>
      </FlexColumnVCentred>
    </FlexRow>
  );
};

function RecipeReviews ({recipeId, recipeData}) {
  const token = React.useContext(GlobalContext).token;
  const userId = tokenToUserId(token);

  const userIsAuthor = recipeData.user_is_author;
  const authorImage = recipeData.author_image;
  const authorDisplayName = recipeData.author_display_name;
  const [reviewsData, setReviewsData] = React.useState([...recipeData.reviews]);
  const [showCreateReview, setShowCreateReview] = React.useState(false);
  const [userHasReviewed, setUserHasReviewed] = React.useState(false);
  const [responseError, setResponseError] = React.useState('');

  //console.log(reviewsData);
  
  /*React.useEffect(() => {
    if (userId !== -1) {

    }
  }, [reviewsData]);*/

  return (
    <FlexColumn>
      <SubPageTitleNoMargins>Reviews</SubPageTitleNoMargins>
      {responseError !== '' &&
      <ErrorAlert message={responseError} setMessage={setResponseError} />}
      {userId !== -1 && !showCreateReview &&
      <LeftAlignedButton onClick={() => setShowCreateReview(true)}>
        Create Review
      </LeftAlignedButton>}
      {showCreateReview && <CreateReviewComponent
        recipeId={recipeId} setReviews={setReviewsData}
        setShow={setShowCreateReview} setError={setResponseError}
        token={token} />}
      {reviewsData.length > 0 &&
      <FlexColumn>
      {reviewsData.map((review, index) => (
        <SingleReview review={review} key={index} />
      ))}
      </FlexColumn>}
    </FlexColumn>
  );
};

export default RecipeReviews;
