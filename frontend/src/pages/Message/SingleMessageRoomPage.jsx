import React from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import { Alert, Box, Button, Divider, Drawer, Grid, IconButton, Link, MenuItem, Paper, Select, Slide, Snackbar, Tab, Tabs, TextField, Tooltip, Typography } from '@mui/material';
import styled from '@emotion/styled';
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import ArrowCircleUpIcon from '@mui/icons-material/ArrowCircleUp';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import CancelIcon from '@mui/icons-material/Cancel';
import CloseIcon from '@mui/icons-material/Close';
import SendIcon from '@mui/icons-material/Send';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { backendRequest, shortDateTimeString, tokenToUserId } from '../../helpers';
import {
  ErrorAlert,
  FlexRowHCentred,
  FlexColumn,
  UserPreferencesComponent,
  FlexRowWrapSpaced,
  FlexRowWrap,
} from '../../components/StyledNodes';
import { TextInput } from '../../components/InputFields';
import { MediumBlackText, PageTitle, SmallBlackText, SmallGreyText, SubPageTitle } from '../../components/TextNodes';

const ChatboxContainer = styled(Paper)`
  display: flex;
  flex-direction: column;
  position: relative;
  box-sizing: border-box;
  height: calc(100vh - 130px);
`;

const MessageEditDeleteButton = styled(Button)`
  padding: 0;
  line-height: 1;
  min-width: 0;
`;

const ChatboxHeader = ({roomId, setOpen}) => {
  return (
    <Paper sx={{display: 'flex', justifyContent: 'space-between'}}>
      <Typography component="h2" variant="h6" p={1}>
        Message Room {roomId}
      </Typography>
      <IconButton onClick={() => setOpen(true)} disableRipple={true}>
        <ArrowBackIosIcon />
      </IconButton>
    </Paper>
  );
};

const AlertToast = ({content, setContent, state}) => {
  return (
    <Snackbar
      open={content !== ''}
      onClose={() => setContent('')}
      TransitionComponent={props => <Slide {...props} direction="left" />}
      anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      autoHideDuration={5000}
    >
      <Alert severity={state}>
        {content}
        <IconButton aria-label="close" color="inherit" size="small"
          onClick={() => { setContent(''); }}>
          <CloseIcon fontSize="inherit" />
        </IconButton>
      </Alert>
    </Snackbar>
  );
}

const MessageInputComponent = ({message, setMessage, send, cancel}) => {
  return (
    <Paper sx={{display: 'flex', position: 'relative'}}>
      <IconButton sx={{width: '24px', height: '24px'}} color="error"
        onClick={cancel}>
        <CancelIcon />
      </IconButton>
      <TextField type="text" size="small" multiline fullWidth
        placeholder="Enter your message" value={message}
        onChange={(e) => setMessage(e.target.value)} />
      <IconButton color="info" disabled={message === ''} onClick={send}>
        <SendIcon />
      </IconButton>
    </Paper>
  );
};

const MessageUserLink = ({user}) => {
  let userId;
  if ('member_id' in user) {
    userId = user.member_id;
  } else if ('owner_id' in user) {
    userId = user.owner_id;
  } else if ('user_id' in user) {
    userId = user.user_id;
  } else if ('id' in user) {
    userId = user.id;
  } else {
    userId = -1;
  }
  const to = userId >= 0 ? `/user/${userId}` : '#';
  return (
    <Link component={RouterLink} to={to} sx={{color: 'primary.dark'}}>
      {user.display_name}
    </Link>
  );
};

const MessageDrawer = ({open, setOpen, roomId, roomData}) => {
  const token = React.useContext(GlobalContext).token;
  const userId = tokenToUserId(token);
  const [toastMessage, setToastMessage] = React.useState('');
  const [toastState, setToastState] = React.useState('error');
  const isOwner = roomData.all_owners.filter(
    (owner) => owner.owner_id == userId).length > 0;
  const drawerWidth = 240;
  const headerStyles = {
    fontSize: '1.2em',
    fontWeight: 600
  };
  const userContainerStyles = {
    maxHeight: '25vh',
    overflowY: 'auto'
  };
  const promoteStyles = {
    padding: 0,
    marginLeft: '6px'
  };

  const promoteMemberToOwner = (memberId) => {
    const body = {
      room_id: roomId,
      owner_id_list: [memberId]
    };
    backendRequest('/message-rooms/set-owner', body, 'POST', token, (data) => {},
    (error) => {
      setToastState('error');
      setToastMessage(error);
    });
  };

  const addUserToRoom = (userId) => {
    const body = {
      room_id: roomId,
      member_id_list: [userId]
    };
    backendRequest('/message-rooms/add-member', body, 'POST', token, (data) => {},
    (error) => {
      setToastState('error');
      setToastMessage(error);
    });
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <Drawer
        sx={{
          zIndex: 1,
          width: drawerWidth,
          flexShrink: 0,
          '& .MuiDrawer-paper': {
            width: drawerWidth,
          },
        }}
        variant="persistent"
        anchor="right"
        open={open}
      >
        <Box mt={9}>
          <IconButton onClick={() => setOpen(false)} disableRipple={true}>
            <ArrowForwardIosIcon />
          </IconButton>
        </Box>
        <Divider />
        <Box m={1}>
          <Typography component="h3" sx={headerStyles}>
            Owners
          </Typography>
          <Box ml={2} sx={userContainerStyles}>
            {roomData.all_owners.map((owner, index) => (
            <Box key={index}>
              <MessageUserLink user={owner} />
            </Box>
            ))}
          </Box>
        </Box>
        <Box m={1}>
          <Typography component="h3" sx={headerStyles}>
            Members
          </Typography>
          <Box ml={2} sx={userContainerStyles}>
            {roomData.all_members.filter((member) => {
              return roomData.all_owners.filter((owner) => {
                return owner.owner_id === member.member_id
              }).length === 0
            }).map((member, index) => (
            <Box key={index} sx={{display: 'flex'}}>
              <MessageUserLink user={member} />
              {isOwner &&
              <Tooltip title={`Promote ${member.display_name}`}
                placement="top" arrow>
                <IconButton color="secondary" size="small" sx={promoteStyles}
                  onClick={() => promoteMemberToOwner(member.member_id)}>
                  <ArrowCircleUpIcon />
                </IconButton>
              </Tooltip>}
            </Box>
            ))}
          </Box>
        </Box>
        <Box m={1}>
          <Typography component="h3" sx={headerStyles}>
            Users
          </Typography>
          <Button color="success"
            size="small"
            onClick={() => addUserToRoom(0)}
            sx={{textTransform: 'none'}}
            startIcon={<AddCircleIcon />}>
            Add user(s)
          </Button>
        </Box>
      </Drawer>
      <AlertToast content={toastMessage} setContent={setToastMessage}
        state="error" />
    </Box>
  );
};

function SingleMessageRoomPage () {
  const { roomId } = useParams();
  const token = React.useContext(GlobalContext).token;
  const userId = tokenToUserId(token);
  const [roomData, setRoomData] = React.useState({});
  const [responseError, setResponseError] = React.useState('');
  const [toastMessage, setToastMessage] = React.useState('');
  const [openDrawer, setOpenDrawer] = React.useState(false);
  const [message, setMessage] = React.useState('');
  const [editMessageId, setEditMessageId] = React.useState(-1);

  const newMessage = () => {
    const body = {
      message: message,
      room_id: roomId
    };
    backendRequest('/message/send', body, 'POST', token, (data) => {},
    (error) => { setToastMessage(error); });
  };

  const updateMessage = () => {
    const body = {
      message: message,
      message_id: editMessageId
    };
    backendRequest('/message/edit', body, 'POST', token, (data) => {},
    (error) => { setToastMessage(error); });
  };

  const sendMessage = () => {
    if (editMessageId < 0) {
      newMessage();
    } else {
      updateMessage();
    }
    setMessage('');
    setEditMessageId(-1);
  };

  const cancelMessage = () => {
    setMessage('');
    setEditMessageId(-1);
  };

  const deleteMessage = (messageId) => {
    const body = {
      message_id: messageId
    };
    backendRequest('/message/delete', body, 'POST', token, (data) => {},
    (error) => { setToastMessage(error); });
  };

  const loadRoomDetails = () => {
    const body = {
      room_id: roomId
    };
    backendRequest('/message-rooms/fetch-details', body, 'POST', token, (data) => {
      setRoomData({...data.body});
    }, (error) => {
      setResponseError(error);
    });
  };

  const idToUserName = (curUserId) => {
    for (let user of roomData.all_owners) {
      if (user.owner_id === curUserId) {
        return user.display_name;
      }
    }
    for (let user of roomData.all_members) {
      if (user.member_id === curUserId) {
        return user.display_name;
      }
    }
    return 'anon';
  };

  React.useEffect(() => {
    loadRoomDetails();
  }, [roomId]);

  return (
    <ManageLayout>
      <Grid item xl={8} lg={12} xs={12}>
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
        {Object.keys(roomData).length > 0 && <>
        <ChatboxContainer>
          <ChatboxHeader roomId={roomId} setOpen={setOpenDrawer} />
          <Box sx={{flex: 1, backgroundColor: '#eeeeee'}}>
          {roomData.all_messages.map((msg, index) => (
            <Box key={index} mt={2} mb={2} p={1} flexDirection="column"
              textAlign={msg.sender_id === userId ? 'right' : 'left'}>
              {msg.is_deleted && <MediumBlackText>deleted</MediumBlackText>}
              {!msg.is_deleted && <>
              {idToUserName(msg.sender_id)}
              <SmallGreyText>
                {shortDateTimeString(msg.time_sent)}
                {msg.is_edited && <> (edited)</>}
              </SmallGreyText>
              {msg.sender_id === userId && 
              <Box display="flex" flexDirection="row" justifyContent="flex-end"
                columnGap={2}>
                <MessageEditDeleteButton color="secondary"
                  onClick={() => {
                    setEditMessageId(msg.message_id);
                    setMessage(msg.message_content);
                  }}>
                  Edit
                </MessageEditDeleteButton>
                <MessageEditDeleteButton color="secondary"
                  onClick={() => deleteMessage(msg.message_id)}>
                  Delete
                </MessageEditDeleteButton>
              </Box>}
              <Typography>{msg.message_content}</Typography>
              </>}
            </Box>
          ))}
          </Box>
          <MessageInputComponent message={message} setMessage={setMessage}
            send={sendMessage} cancel={cancelMessage} />
        </ChatboxContainer>
        <MessageDrawer open={openDrawer} setOpen={setOpenDrawer}
          roomId={roomId} roomData={roomData} />
        </>}
      </Grid>
      <AlertToast content={toastMessage} setContent={setToastMessage}
        state="error" />
    </ManageLayout>
  );
}

export default SingleMessageRoomPage;
