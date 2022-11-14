import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import styled from '@emotion/styled';
import {
  Avatar,
  Box,
  Button,
  Divider,
  Grid,
  Link,
  Paper,
  Typography,
} from '@mui/material';
import GlobalContext from '../utils/GlobalContext';
import ManageLayout from '../components/Layout/ManageLayout';
import { PageTitle, SmallGreyText, SubPageTitle } from '../components/TextNodes';
import {
  FlexColumn,
  ErrorAlert,
  SuccessAlert
} from '../components/StyledNodes';
import { backendRequest, shortDateTimeString, tokenToUserId } from '../helpers';

const CentredContentContainer = styled(Paper)`
  display: flex;
  box-sizing: border-box;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 12px;
  height: 100%;
`;

const SubsText = styled(CentredContentContainer)`
  text-decoration: none;
  text-align: center;
  font-weight: bold;
`;

const OneNotification = ({data}) => {
  return (
    <Box sx={{display: 'flex', flexDirection: 'column'}}>
      <Box p={1}>
        <Box>
          <Typography component="span">From: </Typography>
          <Link color="primary.dark" component={RouterLink}
            to={data.sender_id >= 0 ? `/user/${data.sender_id}` : '#'}>
            {data.sender_name}
          </Link>
        </Box>
        <SmallGreyText>
          Sent: {shortDateTimeString(data.time_sent)}
        </SmallGreyText>
        <Typography component="p">
          {data.notification_content}
        </Typography>
      </Box>
      <Divider />
    </Box>
  );
};

function DashboardPage () {
  const token = React.useContext(GlobalContext).token;
  const userId = tokenToUserId(token);
  const [userStats, setUserStats] = React.useState({});
  const [notifications, setNotifications] = React.useState([]);
  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const loadUserStats = () => {
    const body = {
      user_id: userId
    };
    backendRequest('/user/stats', body, 'POST', token, (data) => {
      setUserStats({...data.body});
      console.log(data.body);
    }, (error) => {
      setResponseError(error);
    });
  };

  const loadNotifications = () => {
    backendRequest('/notifications/fetch-all', {}, 'POST', token, (data) => {
      setNotifications([...data.notifications]);
    }, (error) => {
      setResponseError(error);
    });
  };

  React.useEffect(() => {
    loadUserStats();
    loadNotifications();
  }, [token]);

  const NotifHeaderStyles = {
    margin: 0,
    fontWeight: 600
  };

  return (
    <ManageLayout>
      <Grid item xs={12}>
        <PageTitle>Dashboard</PageTitle>
        <FlexColumn>
          {responseSuccess !== '' &&
          <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
          {responseError !== '' &&
          <ErrorAlert message={responseError} setMessage={setResponseError} />}
          <Grid container spacing={2}>
            <Grid container spacing={2} item xl={8} lg={6} md={5} sm={4} xs={12}>
              <Grid item xl={6} lg={12} md={12} sm={12} xs={12}>
                <CentredContentContainer
                  component={RouterLink} to={`/user/${userId}`}>
                  <Avatar sx={{ width: 128, height: 128 }} variant="circular" src={userStats.user_image} alt={userStats.display_name} />
                  <SubPageTitle>{userStats.display_name}</SubPageTitle>
                </CentredContentContainer>
              </Grid>
              <Grid item xl={3} lg={6} md={12} sm={12} xs={12}>
                <SubsText component={RouterLink} to="/subscriptions">
                  {userStats.num_followings} Subscriptions
                </SubsText>
              </Grid>
              <Grid item xl={3} lg={6} md={12} sm={12} xs={12}>
                <SubsText component={RouterLink} to="/subscribers">
                  {userStats.num_followers} Subscribers
                </SubsText>
              </Grid>
              <Grid item xs={12}></Grid>
              <Grid item xs={12}></Grid>
            </Grid>
            <Grid item xl={4} lg={6} md={7} sm={8} xs={12}>
              <Paper>
                <Typography component="h2" variant="h5" sx={NotifHeaderStyles}>
                  Notifications
                </Typography>
                {notifications.length < 1 &&
                <Typography>No Notifications</Typography>}
                {notifications.length > 0 &&
                <Box sx={{maxHeight:'calc(100vh - 246px)', overflowY:'auto'}}>
                  <Box>
                  {notifications.map((notif, index) => (
                    <OneNotification key={index} data={notif} />
                  ))}
                  </Box>
                </Box>}
              </Paper>
            </Grid>
          </Grid>
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default DashboardPage;
