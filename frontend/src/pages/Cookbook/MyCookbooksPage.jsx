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
import { MediumBlackText, PageTitle } from '../../components/TextNodes';
import {
  ConfirmationDialog,
  FlexColumn,
  FlexRow,
  ErrorAlert,
  SuccessAlert
} from '../../components/StyledNodes';
import { LeftAlignedButton } from '../../components/Buttons';
import { backendRequest } from '../../helpers';
import { OwnCookbookItem, CookbookItem } from '../../components/Cookbook/CookbookItems';

function MyCookbooksPage () {
  // TODO: complete this page
  const token = React.useContext(GlobalContext).token;
  const [ownCookbooks, setOwnCookbooks] = React.useState([]);
  const [followedCookbooks, setFollowedCookbooks] = React.useState([]);
  const [followingCookbooks, setFollowingCookbooks] = React.useState([]);

  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [deleteIndex, setDeleteIndex] = React.useState(-1);
  const [deleteDescription, setDeleteDesciption] = React.useState('');

  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const loadCookbooks = () => {
    backendRequest('/cookbook/fetch-own', {}, 'POST', token, (data) => {
      setOwnCookbooks([...data.body]);
      setFollowedCookbooks([...data.body.filter((c) => c.follower_count > 0)]);
    }, (error) => {
      setResponseError(error);
    });
  };

  const loadFollowingCookbooks = () => {
    backendRequest('/cookbooks/following', {}, 'POST', token, (data) => {
      setFollowingCookbooks([...data.cookbooks]);
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
    loadFollowingCookbooks();
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
            <Typography>Followed: {followedCookbooks.length}</Typography>
            <Typography>Following: {followingCookbooks.length}</Typography>
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
          <Grid container spacing={2}>
            {followedCookbooks.length > 0 &&
            followedCookbooks.map((cookbook, index) => (
            <Grid item xl={3} lg={4} md={6} sm={6} xs={12} key={index}>
              <CookbookItem cookbook={cookbook} showAuthor={false} />
            </Grid>))}
            {followedCookbooks.length < 1 &&
            <Grid item xs={12}>
              <MediumBlackText>No Followed Cookbooks</MediumBlackText>
            </Grid>}
          </Grid>
          <Divider />
          <PageTitle>Following Cook Books</PageTitle>
          <Grid container spacing={2}>
            {followingCookbooks.length > 0 &&
            followingCookbooks.map((cookbook, index) => (
            <Grid item xl={3} lg={4} md={6} sm={6} xs={12} key={index}>
              <CookbookItem cookbook={cookbook} showAuthor={true} />
            </Grid>))}
            {followingCookbooks.length < 1 &&
            <Grid item xs={12}>
              <MediumBlackText>Not Following Any Cookbooks</MediumBlackText>
            </Grid>}
          </Grid>
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
