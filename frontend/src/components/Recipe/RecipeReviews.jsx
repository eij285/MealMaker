import React from 'react';
import styled from '@emotion/styled';
import { Box, Button, IconButton, Paper, Rating, Tooltip, Typography } from '@mui/material';
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
import { LeftAlignedButton, LeftAlignMedButton, LeftAltMedButton, LeftAltSmallButton, LeftSmallSubmitButton } from '../Buttons';
import { CentredElementsForm } from '../Forms';

const loadReviews = (recipeId, token, recipeData, setRecipeData, setError) => {
  const body = {
    recipe_id: recipeId
  };
  const reqURL = '/reviews/all-for-recipe' + (token ? '' : `?recipe_id=${recipeId}`);
  const reqMethod = token ? 'POST' : 'GET';
  backendRequest(reqURL, body, reqMethod, token, (data) => {
    setRecipeData({
      ...recipeData, reviews: [...data.reviews]
    });
  }, (error) => {
    setError(error);
  });
};

const CreateReviewComponent = ({recipeId, recipeData, setRecipeData, setShow,
  setError, token}) => {
  const [rating, setRating] = React.useState(3);
  const [comment, setComment] = React.useState('');
  const handleSubmit = () => {
    const body = {
      recipe_id: recipeId,
      rating: rating,
      comment: comment
    };
    backendRequest('/review/create', body, 'POST', token, (data) => {
      loadReviews(recipeId, token, recipeData, setRecipeData, setError);
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

const SingleReview = ({review, recipeData, setRecipeData, index, token}) => {
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

const ReplyButton = (props) => {
  return (
    <Button {...props} sx={{
      textTransform: 'none',
      color: '#333333',
      minWidth: 'auto',
      padding: '4px 0'
    }} />
  )
};

const ReviewReplyContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 10px 0 0 20px;
`;

const ReviewReplyForm = styled.form`
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  row-gap: 10px;
  width: 100%;
`;

const ReviewReplyComponent = ({review, recipeData, setRecipeData, index,
  token}) => {
  const reviewId = review.review_id;
  const userIsAuthor = recipeData.user_is_author;
  const authorId = recipeData.author_id;
  const authorDisplayName = recipeData.author_display_name;
  const authorImage = recipeData.author_image;
  
  const [showReplyForm, setShowReplyForm] = React.useState(false);
  const submitReply = (e) => {
    e.preventDefault();
    const reply = e.target.reply.value;
    const body = {
      review_id: reviewId,
      reply: reply
    };
    backendRequest('/review/reply', body, 'POST', token, (data) => {
      setRecipeData({
        ...recipeData,
        reviews: [...recipeData.reviews.slice(0, index),
          {...review, reply: reply}, ...recipeData.reviews.slice(index + 1)]
      });
      setShowReplyForm(false);
    }, (error) => {
      //setError(error);
      console.log(error);
    });
  };
  const cancelReply = (e) => {
    e.preventDefault();
    e.target.reply.value = '';
    setShowReplyForm(false);
  };

  const deleteReply = (e) => {
    e.preventDefault();
    const reviewId = review.review_id;
    const body = {
      review_id: reviewId
    };
    backendRequest('/review/reply/delete', body, 'POST', token, (data) => {
      setRecipeData({
        ...recipeData,
        reviews: [...recipeData.reviews.slice(0, index),
          {...review, reply: ''}, ...recipeData.reviews.slice(index + 1)]
      });
    }, (error) => {
      //setError(error);
      console.log(error);
    });
  };

  return (
    <ReviewReplyContainer>
      {!showReplyForm && userIsAuthor && review.reply === '' &&
      <ReplyButton onClick={() => setShowReplyForm(true)}>reply</ReplyButton>}
      {!showReplyForm && userIsAuthor && review.reply !== '' && <>
      <ReplyButton onClick={deleteReply}>
        delete reply
      </ReplyButton>
      <UserImageNameLink src={authorImage} name={authorDisplayName}
          to={`/user/${authorId}`} />
      <MediumBlackText>{review.reply}</MediumBlackText>
      </>
      }
      {showReplyForm &&
      <ReviewReplyForm onSubmit={submitReply} onReset={cancelReply}>
        <TextInput
          name="reply"
          label="Reply"
          multiline
          minRows={2}
        />
        <FlexRow>
          <LeftSmallSubmitButton>Submit</LeftSmallSubmitButton>
          <LeftAltSmallButton type="reset">
            Cancel
          </LeftAltSmallButton>
        </FlexRow>
      </ReviewReplyForm>
      }
    </ReviewReplyContainer>
  );
};

function RecipeReviews ({recipeId, recipeData, setRecipeData}) {
  const token = React.useContext(GlobalContext).token;
  const userId = tokenToUserId(token);
  const userIsAuthor = recipeData.user_is_author;
  const [showCreateReview, setShowCreateReview] = React.useState(false);
  const [userHasReviewed, setUserHasReviewed] = React.useState(false);
  const [responseError, setResponseError] = React.useState('');

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
        recipeId={recipeId} recipeData={recipeData} setRecipeData={setRecipeData}
        setShow={setShowCreateReview} setError={setResponseError}
        token={token} />}
      {Object.keys(recipeData).length && recipeData.reviews.length > 0 &&
      <FlexColumn>
      {recipeData.reviews.map((review, index) => (
        <Paper sx={{p: 1}} key={index}>
          <SingleReview review={review} recipeData={recipeData}
            setRecipeData={setRecipeData} index={index} token={token} />
          {userIsAuthor &&
          <ReviewReplyComponent review={review} recipeData={recipeData}
            setRecipeData={setRecipeData} index={index} token={token} />}
          </Paper>))}
          </FlexColumn>}
    </FlexColumn>
  );
};

export default RecipeReviews;
