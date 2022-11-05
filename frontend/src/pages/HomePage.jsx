import React from 'react';
import { Box, Grid, MenuItem, Select, Tab, Tabs } from '@mui/material';
import GlobalContext from '../utils/GlobalContext';
import ExploreLayout from '../components/Layout/ExploreLayout';
import { backendRequest, filterRecipes } from '../helpers';
import {
  ErrorAlert,
  FlexRowHCentred,
  FlexColumn,
  UserPreferencesComponent,
} from '../components/StyledNodes';
import { RecipeItem } from '../components/Recipe/RecipeItems';

const SingleFeed = ({recipes}) => {
  return (
    <Grid>
      <Grid container spacing={2}>
        {recipes.map((recipe, index) => (
        <Grid item xl={3} lg={4} md={6} sm={6} xs={12} key={index}>
          <RecipeItem recipe={recipe} />
        </Grid>))}
      </Grid>
    </Grid>
  );
};

function HomePage () {
  const globals = React.useContext(GlobalContext);
  const token = globals.token;
  const userPreferences = globals.userPreferences;

  const [allTrending, setAllTrending] = React.useState([]);
  const [allSubsFeed, setAllSubsFeed] = React.useState([]);
  const [allDiscover, setAllDiscover] = React.useState([]);

  const [filteredTrending, setFilteredTrending] = React.useState([]);
  const [filteredSubsFeed, setFilteredSubsFeed] = React.useState([]);
  const [filteredDiscover, setFilteredDiscover] = React.useState([]);

  const [tabValue, setTabValue] = React.useState('Subscribed');
  const [dropdown, setDropdown] = React.useState('For You');

  const [responseError, setResponseError] = React.useState('');

  const loadTrending = () => {
    backendRequest('/feed/trending', null, 'GET', null, (data) => {
      const body = data.body;
      if (Array.isArray(body) && body.length > 0) {
        setAllTrending([...body]);
        filterRecipes(userPreferences, [...body], setFilteredTrending);
      }
    }, (error) => {
      setResponseError(error);
    });
  };

  const loadSubsFeed = () => {
    backendRequest('/feed/subscription', {}, 'POST', token, (data) => {
      const body = data.body;
      if (Array.isArray(body) && body.length > 0) {
        setAllSubsFeed([...body]);
        filterRecipes(userPreferences, [...body], setFilteredSubsFeed);
      }
    }, (error) => {
      setResponseError(error);
    });
  };

  const loadDiscover = () => {
    backendRequest('/feed/discover', {}, 'POST', token, (data) => {
      const body = data.body;
      if (Array.isArray(body) && body.length > 0) {
        setAllDiscover([...body]);
        filterRecipes(userPreferences, [...body], setFilteredDiscover);
      }
    }, (error) => {
      setResponseError(error);
    });
  };

  React.useEffect(() => {
    loadTrending();
    if (token) {
      loadSubsFeed();
      loadDiscover();
    }
  }, [token]);

  React.useEffect(() => {
    filterRecipes(userPreferences, allTrending, setFilteredTrending);
    if (token) {
      filterRecipes(userPreferences, allSubsFeed, setFilteredSubsFeed);
      filterRecipes(userPreferences, allDiscover, setFilteredDiscover);
    }
  }, [userPreferences]);

  return (
    <ExploreLayout>
      <UserPreferencesComponent />
      <FlexColumn>
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
        <Box sx={{ width: '100%', bgcolor: 'background.paper' }}>
          {!token &&
          <Tabs value="Trending"
            textColor="secondary" indicatorColor="secondary" centered>
            <Tab label="Trending" value="Trending" />
          </Tabs>}
          {token && <>
          <Tabs value={tabValue} onChange={(e, newVal) => setTabValue(newVal)}
            textColor="secondary" indicatorColor="secondary" centered>
            <Tab label="Subscribed" value="Subscribed" />
            <Tab label="Discover" value="Discover" />
          </Tabs>
          <FlexRowHCentred>
            <Select size="small" sx={{mt: 2}} disabled={tabValue==='Discover'}
              value={dropdown} onChange={(e) => setDropdown(e.target.value)}>
              <MenuItem value="For You">For You</MenuItem>
              <MenuItem value="Trending">Trending</MenuItem>
            </Select>
          </FlexRowHCentred>
        </>}
        </Box>
        {(!token || dropdown === 'Trending') &&
        <SingleFeed recipes={filteredTrending} />}
        {token && tabValue === 'Subscribed' && dropdown === 'For You' &&
        <SingleFeed recipes={filteredSubsFeed} />}
        {token && tabValue === 'Discover' &&
        <SingleFeed recipes={filteredDiscover} />}
      </FlexColumn>
    </ExploreLayout>
  );
}

export default HomePage;
