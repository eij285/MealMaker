import React from 'react';
import { useParams } from 'react-router-dom';
import GlobalContext from '../utils/GlobalContext';
import ExploreLayout from '../components/Layout/ExploreLayout';
import { backendRequest } from '../helpers';

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
    }, (error) => {
      setResponseError(error);
    });
  };

  React.useEffect(() => {
    loadResults();
  }, [searchQuery]);

  return (
    <ExploreLayout>
      Search Page {searchQuery}
    </ExploreLayout>
  );
}

export default SearchPage;
