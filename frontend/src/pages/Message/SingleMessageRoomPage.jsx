import React from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import { Box, Button, Divider, Drawer, Grid, IconButton, MenuItem, Paper, Select, Tab, Tabs, TextField, Typography } from '@mui/material';
import styled from '@emotion/styled';
import ArrowBackIosIcon from '@mui/icons-material/ArrowBackIos';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import CancelIcon from '@mui/icons-material/Cancel';
import SendIcon from '@mui/icons-material/Send';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { backendRequest, filterRecipes } from '../../helpers';
import {
  ErrorAlert,
  FlexRowHCentred,
  FlexColumn,
  UserPreferencesComponent,
  FlexRowWrapSpaced,
  FlexRowWrap,
} from '../../components/StyledNodes';
import { TextInput } from '../../components/InputFields';
import { MediumBlackText, PageTitle, SmallBlackText, SubPageTitle } from '../../components/TextNodes';

const ChatboxContainer = styled(Paper)`
  display: flex;
  flex-direction: column;
  position: relative;
  box-sizing: border-box;
  height: calc(100vh - 130px);
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

const MessageDrawer = ({open, setOpen, users, setUsers}) => {
  const drawerWidth = 240;
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
      </Drawer>
    </Box>
  );
}

function SingleMessageRoomPage () {
  const { roomId } = useParams();
  const token = React.useContext(GlobalContext).token;
  const [responseError, setResponseError] = React.useState('');
  const [openDrawer, setOpenDrawer] = React.useState(false);
  const [message, setMessage] = React.useState('');
  const [users, setUsers] = React.useState([]);
  const [editMessageId, setEditMessageId] = React.useState(-1);

  const cancelMessage = () => {
    setMessage('');
  };

  const sendMessage = () => {
    setMessage('');
  };

  return (
    <ManageLayout>
      <Grid item xl={8} lg={12} xs={12}>
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
        <ChatboxContainer>
          <ChatboxHeader roomId={roomId} setOpen={setOpenDrawer} />
          <Box sx={{flex: 1, backgroundColor: '#eeeeee'}}>

          </Box>
          <MessageInputComponent message={message} setMessage={setMessage}
            send={sendMessage} cancel={cancelMessage} />
        </ChatboxContainer>
        <MessageDrawer open={openDrawer} setOpen={setOpenDrawer} />
      </Grid>
    </ManageLayout>
  );
}

export default SingleMessageRoomPage;
