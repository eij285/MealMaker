import React from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import { Box, Divider, Grid } from '@mui/material';
import styled from '@emotion/styled';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { backendRequest } from '../../helpers';
import { ErrorAlert, FlexColumn } from '../../components/StyledNodes';
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import { LeftAlignedButton, LeftAlignMedButton } from '../../components/Buttons';

const ButtonContainer = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  column-gap: 20px;
  row-gap: 20px;
`;

const MessageRoomButton = ({roomInfo}) => {
  return (
    <LeftAlignMedButton component={RouterLink}
    to={`/message-room/${roomInfo.room_id}`}>
      Room {roomInfo.room_id}
    </LeftAlignMedButton>
  );
};

function MessageRoomsPage () {
  const token = React.useContext(GlobalContext).token;
  const [messageRooms, setMessageRooms] = React.useState([]);
  const [responseError, setResponseError] = React.useState('');
  const navigate = useNavigate();

  const createRoom = () => {
    const body = {
      member_id_list: []
    };
    backendRequest('/message-rooms/create', body, 'POST', token, (data) => {
      navigate(`/message-room/${data.body.room_id}`);
    }, (error) => {
      setResponseError(error);
    });
  };

  const loadRooms = () => {
    backendRequest('/message-rooms', {}, 'POST', token, (data) => {
      setMessageRooms([...data.body]);
    }, (error) => {
      setResponseError(error);
    });
  };

  React.useEffect(() => {
    loadRooms();
  }, [token]);

  return (
    <ManageLayout>
      <Grid item xl={8} lg={12} xs={12}>
        <PageTitle>Message Rooms</PageTitle>
        {responseError !== '' &&
        <Box mb={2}>
          <ErrorAlert message={responseError} setMessage={setResponseError} />
        </Box>}
        <FlexColumn>
          <LeftAlignedButton onClick={createRoom}>
            Create Room
          </LeftAlignedButton>
          <Divider />
          <Box>
            <SubPageTitle>Owner</SubPageTitle>
            <ButtonContainer>
            {messageRooms.filter(room => room.is_owner).map((room, index) => (
              <MessageRoomButton key={index} roomInfo={room} />
            ))}
            </ButtonContainer>
          </Box>
          <Divider />
          <Box>
            <SubPageTitle>Member</SubPageTitle>
            <ButtonContainer>
            {messageRooms.filter(room => !room.is_owner).map((room, index) => (
              <MessageRoomButton key={index} roomInfo={room} />
            ))}
            </ButtonContainer>
          </Box>
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default MessageRoomsPage;
