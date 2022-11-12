import React from 'react';
import { useParams } from 'react-router-dom';
import { Grid } from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { backendRequest } from '../../helpers';
import {
  ErrorAlert,
} from '../../components/StyledNodes';
import { 
  ChatboxContainer,
  ChatboxHeader,
  MessageDrawer,
  MessageRoomMainComponent
} from '../../components/Message/MessageNodes';
const config = require('../../config.json');

function SingleMessageRoomPage () {
  const { roomId } = useParams();
  const token = React.useContext(GlobalContext).token;
  const [roomData, setRoomData] = React.useState({});
  const [responseError, setResponseError] = React.useState('');
  const [openDrawer, setOpenDrawer] = React.useState(false);

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
    let interval = setInterval(() => loadRoomDetails(), config.POLL_INTERVAL);
    return () => clearInterval(interval);
  });

  return (
    <ManageLayout>
      <Grid item xl={8} lg={12} xs={12}>
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
        {Object.keys(roomData).length > 0 && <>
        <ChatboxContainer>
          <ChatboxHeader roomId={roomId} setOpen={setOpenDrawer} />
          <MessageRoomMainComponent roomId={roomId} roomData={roomData} />
        </ChatboxContainer>
        <MessageDrawer open={openDrawer} setOpen={setOpenDrawer}
          roomId={roomId} roomData={roomData} />
        </>}
      </Grid>
    </ManageLayout>
  );
}

export default SingleMessageRoomPage;
