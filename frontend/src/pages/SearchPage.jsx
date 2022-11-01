import React from 'react';
import { useParams } from 'react-router-dom';
import ExploreLayout from '../components/Layout/ExploreLayout';

function SearchPage () {
  const { query } = useParams();
  const searchQuery = typeof query !== 'undefined' ? query : '';
  return (
    <ExploreLayout>
      Search Page {searchQuery}
    </ExploreLayout>
  );
}

export default SearchPage;
