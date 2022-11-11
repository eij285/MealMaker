import React from 'react';
import { Box, Divider, Grid, MenuItem, Select, Tab, Tabs } from '@mui/material';
import styled from '@emotion/styled';
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
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import { LargeDefaultButton, LeftAlignedButton, LeftAlignMedButton } from '../../components/Buttons';

const ButtonContainer = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  column-gap: 20px;
  row-gap: 20px;
`;

function MessageRoomsPage () {
  const token = React.useContext(GlobalContext).token;
  const [responseError, setResponseError] = React.useState('');

  return (
    <ManageLayout>
      <Grid item xl={8} lg={12} xs={12}>
        <PageTitle>Message Rooms</PageTitle>
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
        <FlexColumn>
          <LeftAlignedButton>Create Room</LeftAlignedButton>
          <Divider />
          <Box>
            <SubPageTitle>Owner</SubPageTitle>
            <ButtonContainer>
              <LeftAlignMedButton>Room 1</LeftAlignMedButton>
              <LeftAlignMedButton>Room 2</LeftAlignMedButton>
              <LeftAlignMedButton>Room 3</LeftAlignMedButton>
              <LeftAlignMedButton>Room 4</LeftAlignMedButton>
              <LeftAlignMedButton>Room 5</LeftAlignMedButton>
              <LeftAlignMedButton>Room 6</LeftAlignMedButton>
              <LeftAlignMedButton>Room 7</LeftAlignMedButton>
              <LeftAlignMedButton>Room 8</LeftAlignMedButton>
            </ButtonContainer>
          </Box>
          <Divider />
          <Box>
            <SubPageTitle>Member</SubPageTitle>
            <ButtonContainer>
              <LeftAlignMedButton>Room 9</LeftAlignMedButton>
              <LeftAlignMedButton>Room 10</LeftAlignMedButton>
              <LeftAlignMedButton>Room 11</LeftAlignMedButton>
              <LeftAlignMedButton>Room 12</LeftAlignMedButton>
              <LeftAlignMedButton>Room 13</LeftAlignMedButton>
              <LeftAlignMedButton>Room 14</LeftAlignMedButton>
              <LeftAlignMedButton>Room 15</LeftAlignMedButton>
              <LeftAlignMedButton>Room 16</LeftAlignMedButton>
            </ButtonContainer>
          </Box>
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default MessageRoomsPage;
