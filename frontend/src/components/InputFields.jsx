import React from 'react';
import styled from '@emotion/styled';
import { Button, Grid, TextField, InputAdornment, IconButton, FormControl, Typography } from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import AutorenewIcon from '@mui/icons-material/Autorenew';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import RemoveCircleIcon from '@mui/icons-material/RemoveCircle';
import { imageToBase64 } from '../helpers';
import { FlexColumn, FlexRow } from './StyledNodes';
import { SubPageTitle } from '../components/TextNodes';

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


/**
 * full width numeric input
 */
 export const NumericInput = (props) => {
  return (
    <GeneralTextInput {...props} type="number" />
  );
};

export const NarrowNumericInput = styled(NumericInput)`
  @media screen and (min-width: 40em) {
    width: 100px;
  }
`;

const imageUpload = async (files, setImage) => {
  if (files.length !== 1) {
    return;
  }
  const imageData = await imageToBase64(files[0]);
  setImage(imageData);
};


export const ImageInput = ({elementTitle, icon, image, setImage}) => {

  const CustomIcon = styled(icon)`
    font-size: 12em;
    max-width: 100%;
  `;

  const CustomImg = styled.img`
    max-width: 100%;
    max-height: 200px;
    width: auto;
    height: auto;
  `;

  const ImgButton = styled(Button)`
    & input {
      display: none;
    }
  `;

  const TypoIcon = styled(Typography)`
    text-transform: none;
    color: #000000;
    & * {
      display: inline;
      vertical-align: middle;
    }
  `;

  return (
    <FormControl>
      <Grid container spacing={3}>
        <Grid item md={4} sm={5} xs={6}>
          {!image && <CustomIcon/>}
          {image && <CustomImg src={image} alt={`${elementTitle} photo`} />}
        </Grid>
        <Grid item>
          <FlexColumn>
            <SubPageTitle>Recipe Photo</SubPageTitle>
            <FlexRow>
              <ImgButton component="label">
                <input
                  type="file"
                  accept=".jpg, .jpeg, .png"
                  onChange={(e) => imageUpload(e.target.files, setImage)}
                />
                {image && <TypoIcon><AutorenewIcon/> Replace Image</TypoIcon>}
                {!image && <TypoIcon><AddCircleIcon /> Add Image</TypoIcon>}
              </ImgButton>
              <ImgButton component="label" onClick={() => setImage('')}>
                {image && <TypoIcon><RemoveCircleIcon/> Remove Image</TypoIcon>}
              </ImgButton>
            </FlexRow>
          </FlexColumn>
        </Grid>
      </Grid>
    </FormControl>
  )
};
