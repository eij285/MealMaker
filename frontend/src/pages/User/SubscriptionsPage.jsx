import React from 'react';
import {
  Grid, IconButton, Tooltip,
} from '@mui/material';
import RemoveCircleIcon from '@mui/icons-material/RemoveCircle';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import {
  ErrorAlert, FlexColumn, FlexRow, FlexRowVCentred, UserImageNameLink
} from '../../components/StyledNodes';
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import { backendRequest } from '../../helpers';

function SubscriptionsPage () {
  const token = React.useContext(GlobalContext).token;
  const [followings, setFollowings] = React.useState([]);
  const [followMessage, setFollowMessage]  = React.useState('');
  const [responseError, setResponseError] = React.useState('');

  const loadSubscriptions = () => {
    backendRequest('/user/get/subscriptions', {}, 'POST', token, (data) => {
      setFollowings([...data.followings]);
      const nSubs = data.followings.length;
      setFollowMessage(
        nSubs > 0 ? `Following ${nSubs} contributor${nSubs>1?'s':''}` :
          'Currently no followings'
      );
    }, (error) => {
      setResponseError(error);
    });
  };

  React.useEffect(() => {
    loadSubscriptions();
  }, [token]);

  return (
    <ManageLayout>
      <Grid item xl={4} lg={6} md={8} sm={10} xs={12}>
        <PageTitle>Subscriptions</PageTitle>
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
        {followMessage !== '' && <SubPageTitle>{followMessage}</SubPageTitle>}
        <FlexColumn>
        {followings.map((following, index) => (
          <FlexRowVCentred>
            <UserImageNameLink key={index} src={following.base64_image}
            name={following.display_name} to={`/user/${following.id}`} />
            <Tooltip title="Unsubscribe" placement="right">
              <IconButton color="error">
                <RemoveCircleIcon />
              </IconButton>
            </Tooltip>
          </FlexRowVCentred>
        ))}
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default SubscriptionsPage;
