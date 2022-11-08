import React from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import { Box, Grid, IconButton, Typography } from '@mui/material';
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


import Link from '@mui/material/Link';
import { Avatar, Badge } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import LocationOnIcon from '@mui/icons-material/LocationOn';

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
      setUserProfile({...data});
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
      <Grid container spacing={30} alignItems="baseline">
        <Grid item key="UserImg">
        {userProfile.hasOwnProperty('base64_image') &&
        userProfile.hasOwnProperty('display_name') && <>
        <Badge 
          anchorOrigin={{
            vertical: "bottom",
            horizontal: "right",
          }}
          badgeContent={
            <IconButton onClick={subscribeToUser}>
              {userProfile.is_subscribed
                ? <RemoveIcon />
                : <AddIcon />
              }
            </IconButton>
          }
          color="primary"
          overlap='circular'
          sx={{
            "& .MuiBadge-badge": {
              height: 25,
              width: 25,

            }
          }}>
          <Avatar src={userProfile.base64_image} alt={userProfile.display_name} sx={{ width: 176, height: 176}}/>
        </Badge>
        </>}
        {userProfile.hasOwnProperty('visibility') &&
        userProfile.visibility === 'public' && <>
        <FlexColumnNoGap>
          {(userProfile.hasOwnProperty('given_names') || 
          userProfile.hasOwnProperty('last_name')) &&
          (userProfile.given_names || userProfile.last_name) &&
          <Typography component="h2" variant="h5" fontWeight={600}>
            {userProfile.given_names && <>{userProfile.given_names}&nbsp;</>}
            {userProfile.last_name && <>{userProfile.last_name}</>}
          </Typography>}

          <Typography color="#707070" > @{userProfile.display_name} </Typography>

          {userProfile.hasOwnProperty('country') && userProfile.country &&
          <><Grid container direction={"row"}>
            <Grid item key="LocationOnIcon">
              <LocationOnIcon sx={{color: "#707070"}} />
            </Grid>
            <Grid item key="Country">
              <Typography color="#707070" > {userProfile.country} </Typography>
            </Grid>
          </Grid>
          </> }
          
          {userProfile.hasOwnProperty('about') && userProfile.about &&
          <>
            <Typography component="strong" variant="strong" sx={{mt: 2, mb: -1}}>
              About:
            </Typography>
            <WYSIWYGOutput>{userProfile.about}</WYSIWYGOutput>
          </>}
        
        </FlexColumnNoGap>
        </>}
        </Grid>
        <Grid item key="Recipes">
          <Typography align="center" component="h2" variant="h5" fontWeight={600}>
            { recipesList.length }
          </Typography>
          <Typography align="center" component="h2" variant="h5" fontWeight={300}>
            Recipes
          </Typography>
        </Grid>
        <Grid item key="Followers">
          <Link href='/subscriptions' color={"#000000"} underline="hover">
            <Typography align="center" component="h2" variant="h5" fontWeight={600}>
              { userProfile.num_followers }
            </Typography>
            <Typography component="h2" variant="h5" fontWeight={300}>
              Followers
            </Typography>
          </Link>
        </Grid>
        <Grid item key="Following">
         <Link href='/subscribers' color={"#000000"} underline="hover">
           <Typography align="center" component="h2" variant="h5" fontWeight={600}>
             { userProfile.num_following }
           </Typography>
           <Typography component="h2" variant="h5" fontWeight={300}>
             Following
           </Typography>
          </Link>
        </Grid>
      </Grid>
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
