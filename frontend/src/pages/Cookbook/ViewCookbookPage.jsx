import React from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Grid
} from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ExploreLayout from '../../components/Layout/ExploreLayout';
import {
  FlexColumn,
  ErrorAlert,
  FlexRowVCentred,
} from '../../components/StyledNodes';
import { backendRequest } from '../../helpers';
import { AutoStoriesOutlined } from '@mui/icons-material';
import { MediumGreyText, PageTitle } from '../../components/TextNodes';
import { CookbookImg } from '../../components/Cookbook/CookbookNodes';
import { RecipeItem } from '../../components/Recipe/RecipeItems';

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
        <FlexRowVCentred>
          <AutoStoriesOutlined sx={{fontSize: '2.5em'}} />
          <PageTitle>{cookbookData.cookbook_name}</PageTitle>
        </FlexRowVCentred>
        <CookbookImg src={cookbookData.cookbook_photo}
          alt={cookbookData.cookbook_name} />
        <MediumGreyText textAlign="center">
          {cookbookData.cookbook_description}
        </MediumGreyText>
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
