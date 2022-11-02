import React from 'react';
import { Box, Grid, Tab, Tabs } from '@mui/material';
import GlobalContext from '../utils/GlobalContext';
import ExploreLayout from '../components/Layout/ExploreLayout';
import { backendRequest } from '../helpers';
import { ErrorAlert, FlexRowHCentred, FlexColumn } from '../components/StyledNodes';
import { PageTitle } from '../components/TextNodes';
import { HomePageRecipeItem } from '../components/Recipe/RecipeItems';

const SingleFeed = ({recipes, level}) => {
  return (
    <Grid>
      <Grid container spacing={2}>
        {recipes.map((recipe, index) => (
        <Grid item xl={3} lg={4} md={6} sm={6} xs={12} key={index}>
          <HomePageRecipeItem recipe={recipe} level={level} />
        </Grid>))}
      </Grid>
    </Grid>
  );
};

function HomePage () {
  const token = React.useContext(GlobalContext).token;

  // bloated app: backend routes return way more data than what's needed
  const [trending, setTrending] = React.useState([]);
  const [subsFeed, setSubsFeed] = React.useState([]);
  const [discover, setDiscover] = React.useState([]);

  const [tabValue, setTabValue] = React.useState(0);
  const [tabLabels, setTabLabels] = React.useState(['Trending']);
  const [dropDown, setDropDown] = React.useState([]);

  const [responseError, setResponseError] = React.useState('');

  const loadTrending = () => {
    backendRequest('/feed/trending', null, 'GET', null, (data) => {
      setTrending([...data.body]);
    }, (error) => {
      setResponseError(error);
    });
  };

  const loadSubsFeed = () => {
    backendRequest('/feed/subscription', {}, 'POST', token, (data) => {
      console.log(data);
      setSubsFeed([...data.body]);
      setTabLabels(['Subscribed', 'Discover']);
      setDropDown(['For You', 'Trending']);
    }, (error) => {
      setResponseError(error);
    });
  };

  const loadDiscover = () => {
    backendRequest('/feed/discover', {}, 'POST', token, (data) => {
      setDiscover([...data.body]);
    }, (error) => {
      setResponseError(error);
    });
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  React.useEffect(() => {
    loadTrending();
    if (token) {
      loadSubsFeed();
      loadDiscover();
    }
  }, [token]);

  return (
    <ExploreLayout>
      <FlexColumn>
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
        <Box sx={{ width: '100%', bgcolor: 'background.paper' }}>
          <Tabs value={tabValue} onChange={handleTabChange} centered>
            {tabLabels.map((value, index) => (
              <Tab key={index} label={value} />
            ))}
          </Tabs>
        </Box>
        {trending.length > 0 && subsFeed.length < 1 && discover.length < 1 &&
        <SingleFeed recipes={trending} level="Intermediate" />}
      </FlexColumn>
    </ExploreLayout>
  );
}

export default HomePage;
