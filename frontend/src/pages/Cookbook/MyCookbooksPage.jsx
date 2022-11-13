import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Divider,
  Grid,
  Typography,
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
import { backendRequest } from '../../helpers';
import { OwnCookbookItem } from '../../components/Cookbook/CookbookItems';

function MyCookbooksPage () {
  // TODO: complete this page
  const token = React.useContext(GlobalContext).token;
  const [ownCookbooks, setOwnCookbooks] = React.useState([]);

  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [deleteIndex, setDeleteIndex] = React.useState(-1);
  const [deleteDescription, setDeleteDesciption] = React.useState('');

  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const loadCookbooks = () => {
    backendRequest('/cookbook/fetch-own', {}, 'POST', token, (data) => {
      setOwnCookbooks([...data.body]);
    }, (error) => {
      setResponseError(error);
    });
  };

  const deleteCookbook = () => {
    const cookbookId = ownCookbooks[deleteIndex].cookbook_id;
    const body = {
      cookbook_id: cookbookId
    };
    backendRequest('/cookbook/delete', body, 'POST', token, (data) => {
      loadCookbooks();
      setResponseSuccess(
        `Successfully deleted cookbook (cookbook id: ${data.body.cookbook_id})`);
    }, (error) => {
      setResponseError(error);
    });
    setDialogOpen(false);
  };

  const publishToggle = (index) => {
    const cookbookId = ownCookbooks[index].cookbook_id;
    const isPublished = ownCookbooks[index].cookbook_status === 'published';
    const reqURL = isPublished ? '/cookbook/unpublish' : '/cookbook/publish';
    const body = {  
      cookbook_id: cookbookId
    };
    backendRequest(reqURL, body, 'PUT', token, (data) => {
      loadCookbooks();
    }, (error) => {
      setResponseError(error);
    });
  };

  React.useEffect(() => {
    loadCookbooks();
  }, [token]);

  React.useEffect(() => {
    if (!dialogOpen) {
      setDeleteIndex(-1);
    }
  }, [dialogOpen, deleteIndex]);

  return (
    <ManageLayout>
      <Grid item xs={12}>
        <PageTitle>My Cook Books</PageTitle>
        <FlexColumn>
          {responseSuccess !== '' &&
          <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
          {responseError !== '' &&
          <ErrorAlert message={responseError} setMessage={setResponseError} />}
          <Box>
            <Typography>Published:
              {ownCookbooks.filter((c) => c.cookbook_status === 'published').length}
            </Typography>
            <Typography>Total: {ownCookbooks.length}</Typography>
            <Typography>Followed: {1}</Typography>
          </Box>
          <FlexRow>
            <LeftAlignedButton component={RouterLink} to="/create-cookbook">
              Create New Cook Book
            </LeftAlignedButton>
          </FlexRow>
          <Grid container spacing={2}>
            {ownCookbooks.length > 0 && ownCookbooks.map((cookbook, index) => (
            <Grid item xl={3} lg={4} md={6} sm={6} xs={12} key={index}>
              <OwnCookbookItem
                data={cookbook} index={index} setDeleteIndex={setDeleteIndex}
                setDialogOpen={setDialogOpen}
                setDeleteDesciption={setDeleteDesciption}
                publishToggle={publishToggle} />
            </Grid>))}
          </Grid>
          <Divider />
          <PageTitle>Followed Cook Books</PageTitle>
        </FlexColumn>
      </Grid>
      <ConfirmationDialog title="Confirm deletion of:"
        description={deleteDescription}
        acceptContent="Delete" rejectContent="Cancel" openState={dialogOpen}
        setOpenState={setDialogOpen} execOnAccept={deleteCookbook} />
    </ManageLayout>
  );
}

export default MyCookbooksPage;
