import React from 'react';
import { Link as RouterLink, useNavigate, useParams } from 'react-router-dom';
import {
  Grid,
} from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { PageTitle } from '../../components/TextNodes';
import {
  ConfirmationDialog,
  FlexColumn,
  FlexRow,
  ErrorAlert,
  SuccessAlert
} from '../../components/StyledNodes';
import { LeftAlignedButton } from '../../components/Buttons';
import { backendRequest, initialCookbookData } from '../../helpers';
import {
  CreateEditCookbookForm
} from '../../components/Cookbook/CookbookNodes';

function EditCookbookPage () {
  // TODO: complete this page
  const { cookbookId } = useParams();
  const token = React.useContext(GlobalContext).token;

  const [cookbookData, setCookbookData] = React.useState({
    ...initialCookbookData(), cookbookId: parseInt(cookbookId)
  });

  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const loadCookbook = () => {
    const body = {
      cookbook_id: cookbookId
    };
    backendRequest('/cookbook/edit', body, 'POST', token, (data) => {
      setCookbookData({
        cookbookId: cookbookId,
        name: data.body.cookbook_name,
        photo: data.body.cookbook_photo,
        description: data.body.cookbook_description,
        cookbookStatus: data.body.cookbook_status,
      });
    }, (error) => {
      setResponseError(error);
    });
  };

  const updateCookbook = (requestBody) => {
    backendRequest('/cookbook/update', requestBody, 'POST', token, (data) => {
      setResponseSuccess('Cookbook Updated Successfully');
    }, (error) => {
      setResponseError(error);
    });
  };

  React.useEffect(() => {
    loadCookbook();
  }, [cookbookId]);

  return (
    <ManageLayout>
      <Grid item xs={12}>
        <PageTitle>Edit Cook Book</PageTitle>
        <FlexColumn>
          {responseSuccess !== '' &&
          <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
          {responseError !== '' &&
          <ErrorAlert message={responseError} setMessage={setResponseError} />}
          <CreateEditCookbookForm data={cookbookData}
            callFunction={updateCookbook} />
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default EditCookbookPage;
