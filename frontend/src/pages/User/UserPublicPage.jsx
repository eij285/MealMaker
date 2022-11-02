import React from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import { Box, Grid, Typography } from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ExploreLayout from '../../components/Layout/ExploreLayout';
import {
  ErrorAlert,
  FlexColumnNoGap,
  WYSIWYGOutput
} from '../../components/StyledNodes';
import {
  MediumAlternateButton, MediumDefaultButton,
} from '../../components/Buttons';
import {
  UserImg,
  ProfileContainer,
  UserAttribute
} from '../../components/User/UserNodes';
import { backendRequest, tokenToUserId } from '../../helpers';
import { SingleAuthorRecipeItem } from '../../components/Recipe/RecipeItems';
import { SubPageTitle } from '../../components/TextNodes';

function UserPublicPage () {
  const { userId } = useParams();
  const globals = React.useContext(GlobalContext);
  const token = globals.token;
  const [userProfile, setUserProfile] = React.useState({});
  const [recipesList, setRecipesList] = React.useState([]);
  const [responseError, setResponseError] = React.useState('');

  const loadRecipes = () => {
    const reqURL = `/recipes/user/published?user_id=${userId}`;
    backendRequest(reqURL, null, 'GET', null, (data) => {
      setRecipesList([...data.recipes]);
    }, (error) => {
      setResponseError(error);
    });
  };

  const loadProfile = () => {
    const body = {
      id: userId
    };
    backendRequest('/user/get/profile', body, 'POST', token, (data) => {
      // just a word of caution: telling everyone your login email is a good
      // way to get your account hacked (even if it's just what the backend
      // sends back)
      setUserProfile({...data});
      console.log(data);
      loadRecipes();
    }, (error) => {
      setResponseError(error);
    });
  };

  const subscribeToUser = () => {
    const reqURL = `/user/${userProfile.is_subscribed?'unsubscribe':'subscribe'}`;
    const reqMethod = userProfile.is_subscribed ? 'POST' : 'PUT';
    const body = {
      id: userProfile.id
    };
    backendRequest(reqURL, body, reqMethod, token, (data) => {
      // on success toggle userProfile.is_subscribed state
      setUserProfile({
        ...userProfile,
        is_subscribed: !userProfile.is_subscribed
      });
    }, (error) => {
      setResponseError(error);
    });
  };

  React.useEffect(() => {
    loadProfile();
  }, [token, userId]);

  return (
    <ExploreLayout>
      {responseError !== '' &&
      <Box mb={2}>
        <ErrorAlert message={responseError} setMessage={setResponseError} />
      </Box>}
      {Object.keys(userProfile).length > 0 && <ProfileContainer>
      {!isNaN(userId) && parseInt(userId) === tokenToUserId(token) &&
      <Box sx={{position: 'absolute', zIndex: 1, right: 0, top: 0}}>
        <MediumAlternateButton component={RouterLink} to={'/user-profile'}>
          Edit Profile
        </MediumAlternateButton>
      </Box>}
      {userProfile.hasOwnProperty('base64_image') &&
      userProfile.hasOwnProperty('display_name') && <>
      <UserImg src={userProfile.base64_image} alt={userProfile.display_name} />
      <Typography component="h2" variant="h4" fontWeight={600}>
        {userProfile.display_name}
      </Typography>
      </>}
      {userProfile.hasOwnProperty('visibility') &&
      userProfile.visibility === 'public' && <>
      {token && userProfile.hasOwnProperty('is_subscribed') &&
      <MediumAlternateButton onClick={subscribeToUser}>
        {userProfile.is_subscribed && <>Unsubscribe</>}
        {!userProfile.is_subscribed && <>Subscribe</>}
      </MediumAlternateButton>}
      <FlexColumnNoGap>
        {(userProfile.hasOwnProperty('given_names') || 
        userProfile.hasOwnProperty('last_name')) &&
        (userProfile.given_names || userProfile.last_name) &&
        <UserAttribute title="Name" content={
          <>
          {userProfile.hasOwnProperty('pronoun') && userProfile.pronoun &&
          <>{userProfile.pronoun}&nbsp;</>}
          {userProfile.given_names && <>{userProfile.given_names}&nbsp;</>}
          {userProfile.last_name && <>{userProfile.last_name}</>}
          </>
        } />}
        {userProfile.hasOwnProperty('email') && userProfile.email &&
        <UserAttribute title="Email" content={userProfile.email} />}
        {userProfile.hasOwnProperty('country') && userProfile.country &&
        <UserAttribute title="Country" content={userProfile.country} />}
        {userProfile.hasOwnProperty('about') && userProfile.about &&
        <>
          <Typography component="strong" variant="strong" sx={{mt: 2, mb: -1}}>
            About:
          </Typography>
          <WYSIWYGOutput>{userProfile.about}</WYSIWYGOutput>
        </>}
      </FlexColumnNoGap>
      </>}
      </ProfileContainer>}
      {userProfile.hasOwnProperty('visitor_efficiency') &&
      recipesList.length > 0 && <>
      <SubPageTitle>Recipes</SubPageTitle>
      <Grid container spacing={2}>
        {recipesList.map((recipe, index) => (
        <Grid item xl={3} lg={4} md={6} sm={6} xs={12} key={index}>
          <SingleAuthorRecipeItem recipe={recipe}
            level={userProfile.visitor_efficiency} />
        </Grid>))}
      </Grid>
    </>}
    </ExploreLayout>
  );
}

export default UserPublicPage;
