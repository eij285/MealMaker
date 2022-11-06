import React from 'react';
import styled from '@emotion/styled';
import {
  FormControl,
  InputLabel,
  MenuItem,
  Select,
} from '@mui/material';
import AutoStoriesIcon from '@mui/icons-material/AutoStories';
import { ImageInput, TextInput } from '../../components/InputFields';
import { LeftAlignedSubmitButton } from '../../components/Buttons';
import { CentredElementsForm } from '../../components/Forms';
import { FlexRow } from '../StyledNodes';

export const CreateEditCookbookForm = ({data, callFunction}) => {
  const [cookbookName, setCookbookName] = React.useState('');
  const [cookbookNameMessage, setCookbookNameMessage] = React.useState('');
  const [cookbookPhoto, setCookbookPhoto] = React.useState('');
  const [description, setDescription] = React.useState('');
  const [descriptionMessage, setDescriptionMessage] = React.useState('');
  const [cookbookStatus, setCookbookStatus] = React.useState('draft');

  const createEditCookbook = (e) => {
    e.preventDefault();
    if (cookbookName !== '' && cookbookNameMessage === '' && 
        description !== '' && descriptionMessage === '') {
      const body = {
        ...(data.cookbookId >= 0 && {cookbook_id: data.cookbookId}),
        name: cookbookName,
        description: description,
        photo: cookbookPhoto,
        cookbook_status: cookbookStatus,
      };
      callFunction(body);
    } else {
      setCookbookNameMessage(cookbookName?'':'Cook Book name required');
      setDescriptionMessage(description?'':'Cook Book description required');
    }
  }

  React.useEffect(() => {
    setCookbookName(data.name);
    setCookbookPhoto(data.photo);
    setDescription(data.description);
    setCookbookStatus(data.cookbook_status);
  }, [data]);

  return (
    <CentredElementsForm noValidate onSubmit={createEditCookbook}>
      <TextInput
        label="Cook Book Name"
        required
        value={cookbookName}
        onChange={(e) => setCookbookName(e.target.value)}
        onBlur={(e) =>
          setCookbookNameMessage(e.target.value?'':'Cook Book name required')}
        error={cookbookNameMessage !== ''}
        helperText={cookbookNameMessage}
      />
      <ImageInput elementTitle="Cook Book Photo" icon={AutoStoriesIcon}
        image={cookbookPhoto} setImage={setCookbookPhoto} />
      <TextInput
        label="Description"
        required
        multiline
        minRows={5}
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        onBlur={(e) =>
          setDescriptionMessage(e.target.value?'':'Cook Book description required')}
        error={descriptionMessage !== ''}
        helperText={descriptionMessage}
      />
      <FlexRow>
        <FormControl>
          <InputLabel id="recipe-status">Status</InputLabel>
          <Select labelId="recipe-status" label="Status"
            sx={{ width: '150px' }}
            value={cookbookStatus}
            onChange={(e) => setCookbookStatus(e.target.value)}>
            <MenuItem value="draft">draft</MenuItem>
            <MenuItem value="published">published</MenuItem>
          </Select>
        </FormControl>
      </FlexRow>
      <FlexRow>
        <LeftAlignedSubmitButton>
          Create Cook Book
        </LeftAlignedSubmitButton>
      </FlexRow>
    </CentredElementsForm>
  );
};
