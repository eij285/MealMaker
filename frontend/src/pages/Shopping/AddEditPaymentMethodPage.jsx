import React from 'react';
import { useParams } from 'react-router-dom';
import { Box, Button, Grid } from '@mui/material';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { backendRequest } from '../../helpers';
import { ErrorAlert, FlexColumn, FlexRow, SuccessAlert } from '../../components/StyledNodes';
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import { TextInput } from '../../components/InputFields';
import { CentredElementsForm } from '../../components/Forms';
import { LeftAlignedSubmitButton } from '../../components/Buttons';

function AddEditPaymentMethodPage () {
  // TODO: complete this page
  const { methodId } = useParams();
  const isEdit = typeof methodId !== 'undefined' && !isNaN(methodId);

  const token = React.useContext(GlobalContext).token;

  const [cardholderName, setCardholderName] = React.useState('');
  const [cardholderNameMessage, setCardholderNameMessage] = React.useState('');
  const [cardNumber, setCardNumber] = React.useState('');
  const [cardNumberMessage, setCardNumberMessage] = React.useState('');
  const [expirationDate, setExpirationDate] = React.useState('');
  const [expirationDateMessage, setExpirationDateMessage] = React.useState('');
  const [cvv, setCvv] = React.useState('');
  const [cvvMessage, setCvvMessage] = React.useState('');
  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const addOrUpdatePayment = (e) => {
    e.preventDefault();
    const reqUrl = `/shopping/${isEdit ? 'update': 'add'}-payment-method`;
    const body = {};
    /*backendRequest('/shopping/add-payment-method', body, 'POST', token, (data) => {
      const cookbookId = data.body.cookbook_id;
      setResponseSuccess('Cookbook Updated Successfully');
    }, (error) => {
      setResponseError(error);
    });*/
  };

  React.useEffect(() => {

  }, [token]);

  return (
    <ManageLayout>
      <Grid item xl={4} lg={6} md={8} sm={12} xs={12}>
        <PageTitle>{isEdit ? 'Edit' : 'Add'} Payment Method</PageTitle>
        {responseSuccess !== '' &&
        <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
        {responseError !== '' &&
        <ErrorAlert message={responseError} setMessage={setResponseError} />}
        <CentredElementsForm noValidate onSubmit={addOrUpdatePayment}>
            <TextInput
              label="Cardholder Name"
              required
              value={cardholderName}
              onChange={(e) => setCardholderName(e.target.value)}
              onBlur={(e) =>
                setCardholderNameMessage(
                  e.target.value?'':'Cardholder name required')}
              error={cardholderNameMessage !== ''}
              helperText={cardholderNameMessage}
            />
            <TextInput
              label="Card Number"
              required
              value={cardNumber}
              onChange={(e) => setCardNumber(e.target.value)}
              onBlur={(e) =>
                setCardNumberMessage(e.target.value?'':'Card number required')}
              error={cardNumberMessage !== ''}
              helperText={cardNumberMessage}
            />
            <TextInput
              label="Expiration Date"
              required
              value={expirationDate}
              onChange={(e) => setExpirationDate(e.target.value)}
              onBlur={(e) =>
                setExpirationDateMessage(
                  e.target.value?'':'Expiration date required')}
              error={expirationDateMessage !== ''}
              helperText={expirationDateMessage}
            />
            <TextInput
              label="CVV"
              required
              value={cvv}
              onChange={(e) => setCvv(e.target.value)}
              onBlur={(e) => setCvvMessage(e.target.value?'':'CVV required')}
              error={cvvMessage !== ''}
              helperText={cvvMessage}
            />
            <FlexRow>
              <LeftAlignedSubmitButton>
                {isEdit ? 'Update' : 'Add'} Payment Method
              </LeftAlignedSubmitButton>
            </FlexRow>
          </CentredElementsForm>
      </Grid>
    </ManageLayout>
  );
}

export default AddEditPaymentMethodPage;
