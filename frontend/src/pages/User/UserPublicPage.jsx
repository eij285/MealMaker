import React from 'react';
import { useNavigate, useParams, Link as RouterLink } from 'react-router-dom';
import {
  Box,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Typography,
} from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ExploreLayout from '../../components/Layout/ExploreLayout';
import { CentredElementsForm } from '../../components/Forms';
import { PageTitle, SubPageTitleNoMargins } from '../../components/TextNodes';
import {
  ErrorAlert,
  FlexColumn,
  FlexRow,
  FlexRowWrapSpaced,
  UserImageNameLink,
  WYSIWYGOutput
} from '../../components/StyledNodes';
import {
  MediumAlternateButton,
  RightAlignMedButton,
  SmallAlternateButton
} from '../../components/Buttons';
import {
  UserImg,
  ProfileContainer
} from '../../components/User/UserNodes';
import { backendRequest, tokenToUserId } from '../../helpers';

function UserPublicPage () {
  const { userId } = useParams();
  const globals = React.useContext(GlobalContext);
  const token = globals.token;
  const [userProfile, setUserProfile] = React.useState({});

  const loadProfile = () => {
    const body = {
      id: userId
    };
    backendRequest('/user/get/profile', body, 'POST', token, (data) => {
      setUserProfile(data);
      console.log(data);
    }, (error) => {
      console.log(error);
      //setResponseError(error);
    });
  };

  React.useEffect(() => {
    loadProfile();
  }, [token, userId]);

  return (
    <ExploreLayout>
      {Object.keys(userProfile).length > 0 && <ProfileContainer>
      {!isNaN(userId) && parseInt(userId) === tokenToUserId(token) &&
      <Box sx={{position: 'absolute', zIndex: 1, right: 0, top: 0}}>
        <MediumAlternateButton component={RouterLink} to={`/user-profile`}>
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
      </ProfileContainer>}
    </ExploreLayout>
  );
}

export default UserPublicPage;
