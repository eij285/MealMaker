import React from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import { Avatar, Backdrop, Badge, Box, Button, CardContent, CardHeader, Grid, IconButton, Typography } from '@mui/material';
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
import AddIcon from '@mui/icons-material/Add';
import RemoveIcon from '@mui/icons-material/Remove';
import LocationOnIcon from '@mui/icons-material/LocationOn';

import Card from '@mui/material/Card';

import CloseIcon from '@mui/icons-material/Close';

import { FlexRowWrap, UserImageNameLink } from '../../components/StyledNodes';

function UserPublicPage () {
  const { userId } = useParams();
  const globals = React.useContext(GlobalContext);
  const token = globals.token;
  const [userProfile, setUserProfile] = React.useState({});
  const [recipesList, setRecipesList] = React.useState([]);
  const [responseError, setResponseError] = React.useState('');
  const [isOwnProfile, setIsOwnProfile] = React.useState(false);
  const [open, setOpen] = React.useState(false);

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
      setIsOwnProfile(parseInt(userId) === tokenToUserId(token));
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

    backendRequest(reqURL, body, reqMethod, token, () => {
      loadProfile();
    }, (error) => {
      setResponseError(error);
    });
  };

  const handleClose = () => {
    setOpen(false);
  };
  const handleToggle = () => {
    setOpen(!open);
  };

  React.useEffect(() => {
    loadProfile();
  }, [token, userId]);

  function AvatarWithFolowBadge() {
    return (
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
        invisible={ userId == tokenToUserId(token) }
        overlap='circular'
        sx={{
          "& .MuiBadge-badge": {
            height: 25,
            width: 25,
          }
        }}
      >
        <Avatar src={userProfile.base64_image} alt={userProfile.display_name} sx={{ width: 176, height: 176}}/>
      </Badge>
    );
  }

  function UserProfileInformation() {
    return (
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
    );
  }

  function FollowersButton() {
    return (
      <Button variant="text" onClick={handleToggle} focusRipple={true} >
        <Grid container direction={"column"}>
          <Grid item key="FollowerCount">
            <Typography
              align="center"
              color={"#000000"}
              component="h2"
              variant="h5"
              fontWeight={600}
            >
              { userProfile.num_followers }
            </Typography>
          </Grid>
          <Grid item key="FollowersHeading">
            <Typography
              color={"#000000"}
              component="h2"
              variant="h5"
              fontWeight={300}
              textTransform="none"
            >
              Followers
            </Typography>
          </Grid>
        </Grid>
      </Button>
    )
  }

  function FollowersBackdropCard() {
    return (
      <Backdrop
            sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
            open={open}
            onClick={handleClose}
          >
            <Card sx={{width: 600}} >
              <CardHeader
                action={
                  <IconButton on={handleClose}>
                    <CloseIcon/>
                  </IconButton>
                }
                align="center"
                title={
                  <Typography variant='h4' fontWeight={800}>Followers</Typography>
                } 
              />
              <CardContent>
              <Grid container direction={"column"}>
                {userProfile.followers.map((follower, index) => (
                  <Grid item key={index}>
                    <Button component={RouterLink} to={`/user/${follower.id}`}>
                      <Grid container direction={"row"} spacing={2} alignItems="center">
                        <Grid item key="FollowerImage">
                          <Avatar src={follower.base64_image} sx={{height: 60, width: 60}} />
                        </Grid>
                        <Grid item key="FollowerDisplayName">
                          <Typography
                            color={"#000000"}
                            component="h3"
                            variant="h6"
                            fontWeight={300}
                            textTransform="none"
                          >
                            {follower.display_name}
                          </Typography>
                        </Grid>
                      </Grid>
                    </Button>
                  </Grid>
                ))}
              </Grid>
              </CardContent>
            </Card>
          </Backdrop>
    );
  }

  return (
    <ExploreLayout>
      {responseError !== '' &&
      <Box mb={2}>
        <ErrorAlert message={responseError} setMessage={setResponseError} />
      </Box>}
      {Object.keys(userProfile).length > 0 && <ProfileContainer>
      {!isNaN(userId) && isOwnProfile &&
      <Box sx={{position: 'absolute', zIndex: 1, right: 0, top: 0}}>
        <MediumAlternateButton component={RouterLink} to={'/user-profile'}>
          Edit Profile
        </MediumAlternateButton>
      </Box>}
      <Grid container spacing={30} alignItems="baseline">
        <Grid item key="UserImgAndInfo">
          {userProfile.hasOwnProperty('base64_image') &&
          userProfile.hasOwnProperty('display_name') && <>
          <AvatarWithFolowBadge />
          </>}
          {userProfile.hasOwnProperty('visibility') &&
          userProfile.visibility === 'public' && <>
          <UserProfileInformation />
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
          <FollowersButton />
          <FollowersBackdropCard />
        </Grid>
        <Grid item key="Following">
         <Link href='/following' color={"#000000"} underline="hover">
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
      <Grid container direction={"row"}>
        <IconButton component={RouterLink} to={'/create-recipe'} disableRipple={true} sx={{"&:hover": {color: "#000000"} }}>
          <AddIcon />
        </IconButton>
        <SubPageTitle>Recipes</SubPageTitle>
      </Grid>
      {userProfile.hasOwnProperty('visitor_efficiency') &&
      recipesList.length > 0 && <>
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
