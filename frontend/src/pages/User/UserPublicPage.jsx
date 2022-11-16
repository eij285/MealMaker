import React from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import { Avatar, Backdrop, Badge, Box, Button, CardContent, CardHeader, Divider, Grid, IconButton, List, ListItem, ListItemAvatar, ListItemText, Typography } from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ExploreLayout from '../../components/Layout/ExploreLayout';
import {
  ErrorAlert,
  FlexColumnNoGap,
  WYSIWYGOutput
} from '../../components/StyledNodes';
import { MediumAlternateButton } from '../../components/Buttons';
import {
  UserImg,
  ProfileContainer,
  UserAttribute
} from '../../components/User/UserNodes';
import { backendRequest, tokenToUserId } from '../../helpers';
import { SingleAuthorRecipeItem } from '../../components/Recipe/RecipeItems';
import { SubPageTitle } from '../../components/TextNodes';
import { CookbookItem } from '../../components/Cookbook/CookbookItems';


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
  const [cookbooksList, setCookbooksList] = React.useState([]);
  const [responseError, setResponseError] = React.useState('');
  const [isOwnProfile, setIsOwnProfile] = React.useState(false);
  const [followersBackdrop, setFollowersBackdrop] = React.useState(false);
  const [followingBackdrop, setFollowingBackdrop] = React.useState(false);

  const loadRecipes = () => {
    const reqURL = `/recipes/user/published?user_id=${userId}`;
    backendRequest(reqURL, null, 'GET', null, (data) => {
      setRecipesList([...data.recipes]);
    }, (error) => {
      setResponseError(error);
    });
  };

  const loadCookbooks = () => {
    const reqURL = `/cookbooks/user/published?user_id=${userId}`;
    backendRequest(reqURL, null, 'GET', null, (data) => {
      setCookbooksList([...data.cookbooks]);
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
      loadCookbooks();
      setIsOwnProfile(parseInt(userId) === tokenToUserId(token));
    }, (error) => {
      console.log(error);
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

  const handleCloseFollowersBackdrop = () => {
    setFollowersBackdrop(false);
  };
  const handleToggleFollowersBackdrop = () => {
    setFollowersBackdrop(!followersBackdrop);
  };

  const handleCloseFollowingBackdrop = () => {
    setFollowingBackdrop(false);
  }
  const handleToggleFollowingBackdrop = () => {
    setFollowingBackdrop(!followingBackdrop);
  }

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
      <Button
        variant="text"
        onClick={handleToggleFollowersBackdrop}
        focusRipple={true}
        sx={{ mt: 3 }}
      >
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
            open={followersBackdrop}
            onClick={handleCloseFollowersBackdrop}
          >
            <Card sx={{ maxHeight: 600, width: 600}}>
              <CardHeader
                action={
                  <IconButton on={handleCloseFollowersBackdrop}>
                    <CloseIcon/>
                  </IconButton>
                }
                align="center"
                title={
                  <Typography variant='h4' fontWeight={800}>Followers</Typography>
                } 
              />
              <Divider />
              <CardContent>
                <List>
                  {userProfile.followers.map((follower, index) => (
                    <ListItem>
                      <Button component={RouterLink} to={`/user/${follower.id}`}>
                        <ListItemAvatar sx={{ mx: 2 }}>
                          <Avatar
                            src={follower.base64_image}
                            sx={{height: 60, width: 60}} />
                        </ListItemAvatar>
                      </Button>
                      <ListItemText primary={follower.display_name} />
                    </ListItem>
                  ))}
                </List>
              </CardContent>
            </Card>
          </Backdrop>
    );
  }

  function FollowingButton() {
    return (
      <Button
        variant="text"
        onClick={handleToggleFollowingBackdrop}
        focusRipple={true}
        sx={{ mt: 3 }}
      >
        <Grid container direction={"column"}>
          <Grid item key="FollowingCount">
            <Typography
              align="center"
              color={"#000000"}
              component="h2"
              variant="h5"
              fontWeight={600}
            >
              { userProfile.num_following }
            </Typography>
          </Grid>
          <Grid item key="FollowingHeading">
            <Typography
              color={"#000000"}
              component="h2"
              variant="h5"
              fontWeight={300}
              textTransform="none"
            >
              Following
            </Typography>
          </Grid>
        </Grid>
      </Button>
    )
  }

  function FollowingBackdropCard() {
    return (
      <Backdrop
            sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }}
            open={followingBackdrop}
            onClick={handleCloseFollowingBackdrop}
          >
            <Card sx={{ maxHeight: 600, width: 600}}>
              <CardHeader
                action={
                  <IconButton on={handleCloseFollowingBackdrop}>
                    <CloseIcon/>
                  </IconButton>
                }
                align="center"
                title={
                  <Typography variant='h4' fontWeight={800}>Following</Typography>
                } 
              />
              <Divider />
              <CardContent>
                <List>
                  {userProfile.following.map((following, index) => (
                    <ListItem
                      secondaryAction={
                        <Button
                          variant="outlined"
                          color="error"
                          onClick={subscribeToUser}
                        >
                          Unfollow
                        </Button>
                      }
                    >
                      <Button component={RouterLink} to={`/user/${following.id}`}>
                        <ListItemAvatar sx={{ mx: 2 }}>
                          <Avatar
                            src={following.base64_image}
                            sx={{height: 60, width: 60}} />
                        </ListItemAvatar>
                      </Button>
                      <ListItemText primary={following.display_name} />
                    </ListItem>
                  ))}
                </List>
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
          <FollowingButton />
          <FollowingBackdropCard />
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
      {cookbooksList.length > 0 && <>
      <SubPageTitle>Cook Books</SubPageTitle>
      <Grid container spacing={2}>
        {cookbooksList.map((cookbook, index) => (
        <Grid item xl={3} lg={4} md={6} sm={6} xs={12} key={index}>
          <CookbookItem cookbook={cookbook} />
        </Grid>))}
      </Grid>
      <Grid container direction={"row"}>
        
      </Grid>
    
    </>}
    </ExploreLayout>
  );
}

export default UserPublicPage;
