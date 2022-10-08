import React from 'react';
import styled from '@emotion/styled';
import { TextField, InputAdornment, IconButton } from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';

const TextInputBlock = styled(TextField)`
  display: block;
`;

/**
 * full width form input
 */
export const GeneralTextInput = (props) => {
  return (
    <TextInputBlock {...props} variant="outlined" size="medium" fullWidth />
  );
};

/**
 * full width text input
 */
export const TextInput = (props) => {
  return (
    <GeneralTextInput {...props} type="text" />
  );
};

/**
 * full width email input
 */
export const EmailInput = (props) => {
  return (
    <GeneralTextInput {...props} type="email" />
  );
};

/**
 * full width password input
 */
export const PasswordInput = (props) => {
  const [viewPassword, setViewPassword] = React.useState(false);
  return (
    <GeneralTextInput {...props}
      type={viewPassword ? 'text' : 'password'}
      InputProps={{
        endAdornment: (
          <InputAdornment position="end">
            <IconButton
              aria-label="toggle password visibility"
              onClick={() => setViewPassword(!viewPassword)}
            >
              {viewPassword ? <VisibilityOff /> : <Visibility />}
            </IconButton>
          </InputAdornment>
        )
      }}
    />
  );
};
