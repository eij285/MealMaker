import React from 'react';
import {
  Grid,
} from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import {
  ErrorAlert, FlexRowWrap, UserImageNameLink
} from '../../components/StyledNodes';
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import { backendRequest } from '../../helpers';

function SubscribersPage () {
  const token = React.useContext(GlobalContext).token;
  const [followers, setFollowers] = React.useState([]);
  const [followMessage, setFollowMessage]  = React.useState('');
  const [responseError, setResponseError] = React.useState('');

  const loadSubscribers = () => {
    backendRequest('/user/get/subscribers', {}, 'POST', token, (data) => {
      setFollowers([...data.followers]);
      if (data.visibility === 'public') {
        const nSubs = data.followers.length;
        setFollowMessage(
          nSubs > 0 ? `Have ${nSubs} follower${nSubs>1?'s':''}` :
            'Currently no followers'
        );
      } else {
        setFollowMessage(
          'Your profile is private. A private profile cannot have followers.');
      }
    }, (error) => {
      setResponseError(error);
    });
  };

  React.useEffect(() => {
    loadSubscribers();
  }, [token]);

  return (
    <ManageLayout>
      <Grid item xl={8} lg={12} xs={12}>
        <PageTitle>Subscribers</PageTitle>
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
        {followMessage !== '' && <SubPageTitle>{followMessage}</SubPageTitle>}
        <FlexRowWrap>
        {followers.map((follower, index) => (
          <UserImageNameLink key={index} src={follower.base64_image}
            name={follower.display_name} to={`/user/${follower.id}`} />
        ))}
        </FlexRowWrap>
      </Grid>
    </ManageLayout>
  );
}

export default SubscribersPage;
