import React from 'react';
import { Grid } from '@mui/material';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { TextInput } from '../../components/InputFields';
import { CentredElementsForm } from '../../components/Forms';
import { PageTitle } from '../../components/TextNodes';
import { FlexColumn } from '../../components/StyledNodes';

function UserPreferencesPage () {
  const token = React.useContext(GlobalContext).token;
  return (
    <ManageLayout>
      <Grid item xl={4} lg={6} md={8} sm={10} xs={12}>
        <PageTitle>User Preferences</PageTitle>
        <FlexColumn>
          <CentredElementsForm noValidate>

          </CentredElementsForm>
        </FlexColumn>
      </Grid>
    </ManageLayout>
  );
}

export default UserPreferencesPage;