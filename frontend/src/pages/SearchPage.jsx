import React from 'react';
import { useParams } from 'react-router-dom';
import GlobalContext from '../utils/GlobalContext';
import ExploreLayout from '../components/Layout/ExploreLayout';
import { backendRequest } from '../helpers';
import {
  ErrorAlert,
  FlexColumn,
  UserPreferencesComponent
} from '../components/StyledNodes';
import { PageTitle } from '../components/TextNodes';

function SearchPage () {
  const { query } = useParams();
  const searchQuery = typeof query !== 'undefined' ? query : '';

  const token = React.useContext(GlobalContext).token;

  const [recipes, setRecipes] = React.useState([]);
  const [responseError, setResponseError] = React.useState('');

  const loadResults = () => {
    const body = {
      search_term: searchQuery
    }
    // FIX BACKEND: why do you need to be authenticated to search???
    backendRequest('/search', body, 'POST', token, (data) => {
      setRecipes([...data.body]);
      console.log(data.body);
    }, (error) => {
      setResponseError(error);
    });
  };

  React.useEffect(() => {
    loadResults();
  });

  return (
    <ExploreLayout>
      <UserPreferencesComponent />
      <PageTitle>Search: {searchQuery}</PageTitle>
      <FlexColumn>
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />} 
      </FlexColumn>
    </ExploreLayout>
  );
}

export default SearchPage;
