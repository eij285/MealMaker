import React from 'react';
import {
  Grid, IconButton, Tooltip,
} from '@mui/material';
import QuestionAnswerIcon from '@mui/icons-material/QuestionAnswer';
import RemoveCircleIcon from '@mui/icons-material/RemoveCircle';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import {
  ConfirmationDialog,
  ErrorAlert,
  FlexColumn,
  FlexRowVCentred,
  SuccessAlert,
  UserImageNameLink
} from '../../components/StyledNodes';
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import { MiniMessageBox } from '../../components/Message/MessageNodes';
import { backendRequest, tokenToUserId } from '../../helpers';

function SubscriptionsPage () {
  const token = React.useContext(GlobalContext).token;
  const [followings, setFollowings] = React.useState([]);
  const [followMessage, setFollowMessage]  = React.useState('');
  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [unsubIndex, setUnsubIndex] = React.useState(-1);
  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');
  const [messageRoomId, setMessageRoomId] = React.useState(-1);

  const updateFollowMessage = (nSubs) => {
    setFollowMessage(
      nSubs > 0 ? `Following ${nSubs} contributor${nSubs>1?'s':''}` :
        'Currently no followings'
    );
  };

  const loadSubscriptions = () => {
    const reqURL = `/user/get/subscriptions?user_id=${tokenToUserId(token)}`;
    backendRequest(reqURL, null, 'GET', null, (data) => {
      setFollowings([...data.followings]);
      updateFollowMessage(data.followings.length);
    }, (error) => {
      setResponseError(error);
    });
  };

  const handleUnsub = (index) => {
    setUnsubIndex(index);
    setDialogOpen(true);
  };

  const genSuccessMessage = (following) => {
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;
    const portno = window.location.port;
    const unsubId = following.id;
    const unsubName = following.display_name;
    return `Successfully unsubscribed from ${unsubName}.
    To resubscribe visit ${protocol}//${hostname}:${portno}/user/${unsubId}`;
  };

  const unsubscribeFromUser = () => {
    if (unsubIndex < 0 || unsubIndex >= followings.length) {
      setResponseError('Invalid subscription');
      return;
    }
    const unsubId = followings[unsubIndex].id;
    const body = {
      id: unsubId
    };
    backendRequest('/user/unsubscribe', body, 'POST', token, (data) => {
      setResponseSuccess(genSuccessMessage(followings[unsubIndex]));
      updateFollowMessage(followings.length - 1);
      setFollowings([...followings.slice(0, unsubIndex),
        ...followings.slice(unsubIndex + 1)]);
    }, (error) => {
      setResponseError(error);
    });
    setDialogOpen(false);
  };

  React.useEffect(() => {
    if (!dialogOpen) {
      setUnsubIndex(-1);
    }
  }, [dialogOpen, unsubIndex]);

  React.useEffect(() => {
    loadSubscriptions();
  }, [token]);

  const messageFollowing = (followingId) => {
    const body = {
      member_id_list: [followingId]
    };
    backendRequest('/message-rooms/create', body, 'POST', token, (data) => {
      setMessageRoomId(data.body.room_id);
    }, (error) => {
      setResponseError(error);
    });
  };

  return (
    <ManageLayout>
      <Grid item xl={4} lg={6} md={8} sm={10} xs={12}>
        <PageTitle>Subscriptions</PageTitle>
        {responseSuccess !== '' &&
        <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
        {followMessage !== '' && <SubPageTitle>{followMessage}</SubPageTitle>}
        <FlexColumn>
        {followings.map((following, index) => (
          <FlexRowVCentred key={index}>
            <UserImageNameLink src={following.base64_image}
            name={following.display_name} to={`/user/${following.id}`} />
            <Tooltip title="Send Message" placement="right">
              <IconButton color="info"
                onClick={() => messageFollowing(following.id)}>
                <QuestionAnswerIcon />
              </IconButton>
            </Tooltip>
            <Tooltip title="Unsubscribe" placement="right">
              <IconButton color="error"
                onClick={() => handleUnsub(index)}>
                <RemoveCircleIcon />
              </IconButton>
            </Tooltip>
          </FlexRowVCentred>
        ))}
        </FlexColumn>
        {messageRoomId >= 0 &&
        <MiniMessageBox roomId={messageRoomId} setRoomId={setMessageRoomId}
          setResponseError={setResponseError} />}
      </Grid>
      <ConfirmationDialog title="Confirm unsubscription from:"
        description={<>{unsubIndex >= 0 && unsubIndex < followings.length &&
          followings[unsubIndex].display_name}</>}
        acceptContent="Unsubscribe" rejectContent="Cancel"
        openState={dialogOpen} setOpenState={setDialogOpen} 
        execOnAccept={unsubscribeFromUser} />
    </ManageLayout>
  );
}

export default SubscriptionsPage;
