import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Box, Button, Grid, TextField } from '@mui/material';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { backendRequest } from '../../helpers';
import { ErrorAlert, FlexColumn, FlexRow, SuccessAlert } from '../../components/StyledNodes';
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import { TextInput } from '../../components/InputFields';
import { CentredElementsForm } from '../../components/Forms';
import { LeftAlignedSubmitButton } from '../../components/Buttons';
import moment from 'moment';

function AddEditPaymentMethodPage () {
  // TODO: complete this page
  const { methodId } = useParams();
  const isEdit = typeof methodId !== 'undefined' && !isNaN(methodId);

  const token = React.useContext(GlobalContext).token;

  const [cardholderName, setCardholderName] = React.useState('');
  const [cardholderNameMessage, setCardholderNameMessage] = React.useState('');
  const [cardNumber, setCardNumber] = React.useState('');
  const [cardNumberMessage, setCardNumberMessage] = React.useState('');
  const [expirationDate, setExpirationDate] = React.useState(null);
  const [expirationDateMessage, setExpirationDateMessage] = React.useState('');
  const [cardCvv, setCardCvv] = React.useState('');
  const [cardCvvMessage, setCardCvvMessage] = React.useState('');
  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const navigate = useNavigate();

  const loadPaymentMethod = () => {
    if (!isEdit) {
      return;
    }
    const body = {
      method_id: 'method_id'
    };
    backendRequest('/cart/payment-method/get', body, 'POST', token, (data) => {
      console.log(data);
      setCardholderName(data.body.card_name);
      setCardNumber(data.body.card_number);
      setExpirationDate(data.body.card_exp_date);
      setCardCvv(data.body.card_cvv);
    }, (error) => {
      setResponseError(error);
    });
  };

  const addOrUpdatePayment = (e) => {
    e.preventDefault();
    if (cardholderName !== '' && cardholderNameMessage === '' && 
      cardNumber !== '' && cardNumberMessage === '' &&
      expirationDate !== null && expirationDateMessage === '' &&
      cardCvv !== '' && cardCvvMessage === '') {
      const reqUrl = `/cart/payment-method/${isEdit ? 'update': 'save'}`;
      const body = {
        card_name: cardholderName,
        card_number: cardNumber,
        card_exp_date: moment(expirationDate).format('YYYY-MM-DD').toString(),
        card_cvv: cardCvv
      };
      backendRequest(reqUrl, body, 'POST', token, (data) => {
        const methodId = data.body.method_id;
        setResponseSuccess(
          `Successfully ${isEdit ? 'updated': 'added'} payment method (${methodId})`);
        navigate(`/edit-payment-method/${methodId}`);
      }, (error) => {
        setResponseError(error);
      });
    } else {
      if (cardholderName === '') {
        setCardholderNameMessage('Cardholder name required');
      }
      if (cardNumber === '') {
        setCardNumberMessage('Card number required');
      }
      if (expirationDate === null) {
        setExpirationDateMessage('Expiration date required');
      }
      if (cardCvv === '') {
        setCardCvvMessage('CVV required');
      }
    }
  };

  React.useEffect(() => {
    loadPaymentMethod();
  }, [token]);

  return (
    <ManageLayout>
      <Grid item xl={4} lg={6} md={8} sm={12} xs={12}>
        <PageTitle>{isEdit ? 'Edit' : 'Add'} Payment Method</PageTitle>
        {responseSuccess !== '' &&
        <Box mb={2}>
          <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />
        </Box>}
        {responseError !== '' &&
        <Box mb={2}>
          <ErrorAlert message={responseError} setMessage={setResponseError} />
        </Box>}
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
            <LocalizationProvider dateAdapter={AdapterDayjs}>
              <DatePicker
                views={['year', 'month']}
                label="Expiration Date"
                required
                openTo="month"
                minDate={Date.now()}
                maxDate={moment().add(10, 'Y')}
                value={expirationDate}
                onChange={(newValue) => {
                  setExpirationDate(newValue);
                  setExpirationDateMessage(newValue?'':'Expiration date required');
                }}
                renderInput={(params) =>
                  <TextField required {...params}
                    error={expirationDateMessage !== ''}
                    helperText={expirationDateMessage} />
                }
              />
            </LocalizationProvider>
            <TextInput
              label="CVV"
              required
              value={cardCvv}
              onChange={(e) => setCardCvv(e.target.value)}
              onBlur={(e) => setCardCvvMessage(e.target.value?'':'CVV required')}
              error={cardCvvMessage !== ''}
              helperText={cardCvvMessage}
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
