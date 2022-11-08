import React from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import {
  Grid,
} from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ExploreLayout from '../../components/Layout/ExploreLayout';
import {
  FlexColumn,
  ErrorAlert,
} from '../../components/StyledNodes';
import { backendRequest } from '../../helpers';

import NotFound404Page from '../Error/NotFound404Page';

function ViewCookbookPage () {
  const { cookbookId } = useParams();
  const token = React.useContext(GlobalContext).token;
  const [errorStatus, setErrorStatus] = React.useState(0);
  const [responseError, setResponseError] = React.useState('');

  const loadCookbook = () => {
    const body = {
      cookbook_id: cookbookId
    };
    const reqURL = '/cookbook/view' + (token ? '' : `?cookbook_id=${cookbookId}`);
    const reqMethod = token ? 'POST' : 'GET';
    backendRequest(reqURL, body, reqMethod, token, (data) => {
      const body = data.body;
      
    }, (error) => {
      setResponseError(error);
    }, setErrorStatus);
  };

  React.useEffect(() => {
    loadCookbook();
  }, [cookbookId, token]);
  
  return (<>
    {errorStatus === 404 && <NotFound404Page />}
    {errorStatus !== 404 &&
    <ExploreLayout>
      <Grid item xl={6} lg={8} md={10} sm={12} xs={12}>
        <FlexColumn>
          {responseError !== '' &&
          <ErrorAlert message={responseError} setMessage={setResponseError} />}
        </FlexColumn>
      </Grid>
    </ExploreLayout>}
  </>);
}

export default ViewCookbookPage;
