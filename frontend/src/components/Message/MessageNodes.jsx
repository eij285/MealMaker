import React from 'react';
import { useNavigate, Link as RouterLink } from 'react-router-dom';
import styled from '@emotion/styled';
import {
  Alert,
  Badge,
  Box,
  Button,
  Divider,
  Drawer,
  IconButton,
  Link,
  Paper,
  Popover,
  Select,
  Slide,
  Snackbar,
  TextField,
  Tooltip,
  Typography 
} from '@mui/material';
import AddReactionOutlinedIcon from '@mui/icons-material/AddReactionOutlined';
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import ArrowCircleUpIcon from '@mui/icons-material/ArrowCircleUp';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import CancelIcon from '@mui/icons-material/Cancel';
import CloseIcon from '@mui/icons-material/Close';
import DeleteForeverIcon from '@mui/icons-material/DeleteForever';
import RefreshIcon from '@mui/icons-material/Refresh';
import SendIcon from '@mui/icons-material/Send';
import GlobalContext from '../../utils/GlobalContext';
import { backendRequest, shortDateTimeString, tokenToUserId } from '../../helpers';
import { ConfirmationDialog } from '../../components/StyledNodes';
import { MediumBlackText, SmallGreyText } from '../../components/TextNodes';
const config = require('../../config.json');

export const ChatboxContainer = styled(Paper)`
  display: flex;
  flex-direction: column;
  position: relative;
  box-sizing: border-box;
  height: calc(100vh - 130px);
`;

export const MessageEditDeleteButton = styled(Button)`
  padding: 0;
  line-height: 1;
  min-width: 0;
`;

export const ChatboxHeader = ({roomId, setOpen}) => {
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

export const AlertToast = ({content, setContent, state}) => {
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

export const MessageInputComponent = ({message, setMessage, send, cancel}) => {
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

export const MessageUserLink = ({user}) => {
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

export const MessageDrawer = ({open, setOpen, roomId, roomData}) => {
  const token = React.useContext(GlobalContext).token;
  const userId = tokenToUserId(token);
  const [toastMessage, setToastMessage] = React.useState('');
  const [users, setUsers] = React.useState([]);
  const [toastState, setToastState] = React.useState('error');
  const [dialogOpen, setDialogOpen] = React.useState(false);
  const navigate = useNavigate();
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

  const addUsersToRoom = (e) => {
    e.preventDefault();
    let member_id_list = [];
    const userOpts = e.target.users;
    for (let user of userOpts) {
      if (user.selected) {
        member_id_list.push(parseInt(user.value));
      }
    }
    const body = {
      room_id: roomId,
      member_id_list: member_id_list
    };
    backendRequest('/message-rooms/add-member', body, 'POST', token, (data) => {
      setToastState('success');
      setToastMessage(`Added ${member_id_list.length} users to room`);
    },
    (error) => {
      setToastState('error');
      setToastMessage(error);
    });
  };

  const getUsers = () => {
    backendRequest('/user/get/users', {}, 'POST', token, (data) => {
      setUsers([...data.body]);
    },
    (error) => {
      setToastState('error');
      setToastMessage(error);
    });
  };

  const deleteMessageRoom = () => {
    const body = {
      room_id: roomId,
    };
    backendRequest('/message-rooms/delete', body, 'POST', token, (data) => {
      navigate('/message-rooms');
    },
    (error) => {
      setDialogOpen(false);
      setToastState('error');
      setToastMessage(error);
    });
  };

  React.useEffect(() => {
    getUsers();
  }, [token]);

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
        {isOwner &&
        <Box sx={{display: 'flex', justifyContent: 'flex-end'}}>
          <Tooltip title="Delete Message Room" placement="left" arrow>
            <IconButton color="error" size="small"
              onClick={() => setDialogOpen(true)}>
              <DeleteForeverIcon />
            </IconButton>
          </Tooltip>
        </Box>}
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
            <Tooltip title="refresh" placement="right" arrow>
              <IconButton color="success" size="small" onClick={getUsers}>
                <RefreshIcon />
              </IconButton>
            </Tooltip>
          </Typography>
          <form onSubmit={addUsersToRoom}>
            <Select
              name="users"
              multiple
              native
              fullWidth
              inputProps={{
                id: 'users-select-multiple-native',
              }}>
              {users.filter((user) => {
                if (roomData.all_owners.filter((owner) => 
                  owner.owner_id === user.id).length > 0) {
                  return false;
                }
                if (roomData.all_members.filter((member) => 
                  member.member_id === user.id).length > 0) {
                  return false;
                }
                return true;
              }).map((user, index) => (
                <option key={index} value={user.id}>
                  {user.display_name}
                </option>
              ))}
            </Select>
            <Button color="success"
              size="small"
              type="submit"
              sx={{textTransform: 'none'}}
              startIcon={<AddCircleIcon />}>
              Add user(s)
            </Button>
          </form>
        </Box>
      </Drawer>
      <AlertToast content={toastMessage} setContent={setToastMessage}
        state={toastState} />
      <ConfirmationDialog
        title="Are you sure you want to delete this message room?"
        description="Note: this cannot be undone"
        acceptContent="Delete" rejectContent="Cancel" openState={dialogOpen}
        setOpenState={setDialogOpen} execOnAccept={deleteMessageRoom} />
    </Box>
  );
};

export const MessageReactions = ({reactions}) => {
  let reactsCounter = {};
  for (let r of reactions) {
    if (r.emoji_utf8 in reactsCounter) {
      reactsCounter[`${r.emoji_utf8}`]++;
    } else {
      reactsCounter[`${r.emoji_utf8}`] = 1;
    }
  }
  return (
    <Box>
      {Object.keys(reactsCounter).map((emoji, index) => (
        <Badge key={index} badgeContent={reactsCounter[`${emoji}`]}
          color="info" sx={{margin: '12px 6px'}}>
          <Typography component="span" fontSize={24}
              dangerouslySetInnerHTML={{__html: `${emoji}`}} />
        </Badge>
      ))}
    </Box>
  );
};

export const MessageReactSelector = ({messageId, reaction, setToastMessage,
  token}) => {
  const [anchorEl, setAnchorEl] = React.useState(null);
  const curReactChar = reaction.length > 0 ? reaction[0].emoji_utf8 : '';

  const emojiContainerStyles = {
    display: 'flex',
    flexDirection: 'row',
    flexWrap: 'wrap',
    width: '222px',
    height: '200px'
  };
  
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const open = Boolean(anchorEl);
  const id = open ? 'simple-popover' : undefined;

  const reactToMessage = (reactChar) => {
    const body = {
      message_id: messageId,
      react_char: reactChar
    };
    backendRequest('/message/react', body, 'POST', token, (data) => {},
    (error) => { setToastMessage(error); });
  };
  
  return (
    <Box>
      <IconButton aria-describedby={id} size="small" onClick={handleClick}>
        <AddReactionOutlinedIcon />
      </IconButton>
      <Popover
        id={id}
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: 'bottom',
          horizontal: 'left',
        }}>
        <Box sx={emojiContainerStyles}>
        {config.EMOJIS.map((emoji, index) => (
          <Button key={index} size="small" sx={{minWidth: '44px'}}
            onClick={() => reactToMessage(emoji)} variant="contained"
            color={curReactChar === emoji ? 'info' : 'inherit'}>
            <Typography component="span"
              dangerouslySetInnerHTML={{__html: `${emoji}`}} />
          </Button>
        ))}
        </Box>
      </Popover>
    </Box>
  );
};

export const MessageRoomMainComponent = ({roomId, roomData}) => {
  const token = React.useContext(GlobalContext).token;
  const userId = tokenToUserId(token);
  const [toastMessage, setToastMessage] = React.useState('');
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

  return (<>
    {Object.keys(roomData).length > 0 && <>
    <Box sx={{flex: 1, backgroundColor: '#eeeeee', overflowY: 'auto'}}>
      <Box>
      {roomData.all_messages.map((msg, index) => (
        <Box key={index} mt={2} mb={2} p={1} flexDirection="column"
          textAlign={msg.sender_id === userId ? 'right' : 'left'}>
          {msg.is_deleted &&
          <MediumBlackText>
            This message has been deleted
          </MediumBlackText>}
          {!msg.is_deleted && <>
          {idToUserName(msg.sender_id)}
          <SmallGreyText>
            {shortDateTimeString(msg.time_sent)}
            {msg.is_edited && <> (edited)</>}
          </SmallGreyText>
          <Typography>{msg.message_content}</Typography>
          <MessageReactions reactions={roomData.all_emojis.filter(
              (emoji) => emoji.message_id === msg.message_id)} />
          {msg.sender_id !== userId &&
          <MessageReactSelector
            messageId={msg.message_id}
            reaction={roomData.all_emojis.filter(
              (emoji) => emoji.message_id === msg.message_id &&
              emoji.reactor_id === userId)}
            setToastMessage={setToastMessage} token={token} />}
          </>}
          {msg.sender_id === userId && 
          <Box display="flex" flexDirection="row"
            justifyContent="flex-end" columnGap={2}>
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
        </Box>
      ))}
      </Box>
    </Box>
    <MessageInputComponent message={message} setMessage={setMessage}
    send={sendMessage} cancel={cancelMessage} />
    <AlertToast content={toastMessage} setContent={setToastMessage}
        state="error" />
    </>}
  </>);
};

export const MiniChatboxContainer = styled(Paper)`
  display: flex;
  position: fixed;
  bottom: 50px;
  right: 8px;
  flex-direction: column;
  box-sizing: border-box;
  height: 300px;
  width: 200px;
  @media (min-width: 960px) and (min-height: 560px) {
    height: 400px;
    width: 300px;
  }
  @media (min-width: 1280px) and (min-height: 800px) {
    height: 500px;
    width: 400px;
  }
`;

export const MiniChatboxHeader = ({roomId, setRoomId}) => {
  return (
    <Paper sx={{display: 'flex', justifyContent: 'space-between'}}>
      <Link component={RouterLink} to={`/message-room/${roomId}`}
        color="primary.dark" p={1}>
        continue in room {roomId}
      </Link>
      <IconButton onClick={() => setRoomId(-1)} size="small">
        <CloseIcon color="error" />
      </IconButton>
    </Paper>
  );
};

export const MiniMessageBox = ({roomId, setRoomId, setResponseError}) => {
  const token = React.useContext(GlobalContext).token;
  const [roomData, setRoomData] = React.useState({});
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

  React.useEffect(() => {
    if (roomId >= 0) {
      let interval = setInterval(() => loadRoomDetails(), config.POLL_INTERVAL);
      return () => clearInterval(interval);
    }
  });

  return (<>
    {roomId >= 0 && Object.keys(roomData).length > 0 &&
    <MiniChatboxContainer>
      <MiniChatboxHeader roomId={roomId} setRoomId={setRoomId} />
      <MessageRoomMainComponent roomId={roomId} roomData={roomData} />
    </MiniChatboxContainer>}
  </>);
};
