import React from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Grid,
} from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { PageTitle } from '../../components/TextNodes';
import {
  FlexColumn,
  ErrorAlert,
} from '../../components/StyledNodes';

import { backendRequest, initialCookbookData } from '../../helpers';
import {
  CreateEditCookbookForm
} from '../../components/Cookbook/CookbookNodes';

function CreateCookbookPage () {
  // TODO: complete this page
  const token = React.useContext(GlobalContext).token;

  const [responseError, setResponseError] = React.useState('');

  const navigate = useNavigate();

  const createCookbook = (requestBody) => {
    /*backendRequest('/cookbook/create', body, 'POST', token, (data) => {
      const cookbookId = data.body.cookbook_id;
      navigate(`/edit-cookbook/${cookbookId}`);
    }, (error) => {
      setResponseError(error);
    });*/
  };
  
  return (
    <ManageLayout>
      <Grid item xl={6} lg={8} md={10} sm={12} xs={12}>
        <PageTitle>New Cook Book</PageTitle>
        <FlexColumn>
          {responseError !== '' &&
          <ErrorAlert message={responseError} setMessage={setResponseError} />}
          <CreateEditCookbookForm data={initialCookbookData()}
            callFunction={createCookbook} />
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default CreateCookbookPage;
