import React from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Grid,
  Tooltip
} from '@mui/material';
import AutoStoriesOutlinedIcon from '@mui/icons-material/AutoStoriesOutlined';
import FoodBankIcon from '@mui/icons-material/FoodBank';
import LoyaltyIcon from '@mui/icons-material/Loyalty';
import GlobalContext from '../../utils/GlobalContext';
import ExploreLayout from '../../components/Layout/ExploreLayout';
import {
  FlexColumn,
  ErrorAlert,
  FlexRowVCentred,
  FlexRowWrapSpaced,
  UserImageNameLink,
  FlexRow,
} from '../../components/StyledNodes';
import { backendRequest } from '../../helpers';
import { MediumGreyText, PageTitle, TextVCentred } from '../../components/TextNodes';
import { CookbookImg } from '../../components/Cookbook/CookbookNodes';
import { RecipeItem } from '../../components/Recipe/RecipeItems';
import { RightAlignMedButton, SmallAlternateButton } from '../../components/Buttons';

function ViewCookbookPage () {
  const { cookbookId } = useParams();
  const token = React.useContext(GlobalContext).token;
  const [cookbookData, setCookbookData] = React.useState({});
  const [responseError, setResponseError] = React.useState('');

  const loadCookbook = () => {
    const body = {
      cookbook_id: cookbookId
    };
    const reqURL = '/cookbook/view' + (token ? '' : `?cookbook_id=${cookbookId}`);
    const reqMethod = token ? 'POST' : 'GET';
    backendRequest(reqURL, body, reqMethod, token, (data) => {
      setCookbookData({...data.body});
    }, (error) => {
      setResponseError(error);
    });
  };

  const followCookbook = () => {
    const reqURL = `/cookbook/${cookbookData.is_following?'unsubscribe':'subscribe'}`;
    const reqMethod = cookbookData.is_following ? 'POST' : 'PUT';
    const body = {
      cookbook_id: cookbookId
    };
    backendRequest(reqURL, body, reqMethod, token, (data) => {
      setCookbookData({
        ...cookbookData,
        is_following: !cookbookData.is_following
      });
    }, (error) => {
      setResponseError(error);
    });
  };

  React.useEffect(() => {
    loadCookbook();
  }, [cookbookId, token]);
  
  return (
    <ExploreLayout>
      <FlexColumn>
        {responseError !== '' &&
        <Box mt={2}>
          <ErrorAlert message={responseError} setMessage={setResponseError} />
        </Box>}
        {Object.keys(cookbookData).length > 0 &&<>
        <FlexRowWrapSpaced>
          <FlexRowVCentred>
            <AutoStoriesOutlinedIcon sx={{fontSize: '2.5em'}} />
            <PageTitle>{cookbookData.cookbook_name}</PageTitle>
          </FlexRowVCentred>
          {cookbookData.is_owner &&
          <RightAlignMedButton component={RouterLink}
            to={`/edit-cookbook/${cookbookId}`}>
            Edit Cook Book
          </RightAlignMedButton>}
        </FlexRowWrapSpaced>
        <CookbookImg src={cookbookData.cookbook_photo}
          alt={cookbookData.cookbook_name} />
        <MediumGreyText textAlign="center">
          {cookbookData.cookbook_description}
        </MediumGreyText>
        <FlexRowWrapSpaced>
          {!cookbookData.is_owner &&
          <SmallAlternateButton onClick={followCookbook}>
            {!cookbookData.is_following && <>Follow Cook Book</>}
            {cookbookData.is_following && <>Unfollow Cook Book</>}
          </SmallAlternateButton>}
          <FlexRow>
            <Tooltip title="recipes" placement="top" arrow>
              <TextVCentred>
                <FoodBankIcon />&nbsp;{cookbookData.recipes.length}
              </TextVCentred>
            </Tooltip>
            <Tooltip title="followers" placement="top" arrow>
              <TextVCentred>
                <LoyaltyIcon />&nbsp;{cookbookData.follower_count}
              </TextVCentred>
            </Tooltip>
          </FlexRow>
          <Box>
            <UserImageNameLink src={cookbookData.author_image}
              name={cookbookData.author_display_name}
              to={`/user/${cookbookData.author_id}`} />
          </Box>
        </FlexRowWrapSpaced>
        {cookbookData.recipes &&
        <Grid container spacing={2}>
        {cookbookData.recipes.map((recipe, index) => (
          <Grid item xl={3} lg={4} md={6} sm={6} xs={12} key={index}>
            <RecipeItem recipe={recipe.body} />
          </Grid>))}
        </Grid>}
        </>}
      </FlexColumn>
    </ExploreLayout>
  );
}

export default ViewCookbookPage;
