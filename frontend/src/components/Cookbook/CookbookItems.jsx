import React from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import styled from '@emotion/styled';
import { Box, Button, Paper, Typography } from '@mui/material';
import AutoStoriesIcon from '@mui/icons-material/AutoStories';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import {
  FlexRow,
  ImageContainer4by3,
  ResponsiveImage4by3,
  FlexRowSpaced,
} from '../StyledNodes';
import { SmallAlternateButton, SmallDefaultButton } from '../Buttons';
import { SmallGreyText } from '../TextNodes';

const CookbookItemActions = styled(Paper)`
  padding: 4px 8px;
  position: absolute;
  z-index: 1;
  top: 0;
  right: 0;
  box-sizing: border-box;
  border-bottom-left-radius: 5px;
  background-color: rgba(0,0,0,0.75);
`;

const CookbookItemPhoto = ({ src, alt }) => {
  return (<>
    {src && <ResponsiveImage4by3 src={src} alt={`${alt} photo`} />}
    {!src && <ImageContainer4by3><AutoStoriesIcon/></ImageContainer4by3>}
  </>);
};

const CookbookItemPaper = styled(Paper)`
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
  & .show-on-hover {
    display: none;
  }
  &:hover .show-on-hover {
    display: flex;
  }
`;

const CookbookActionButton = styled(Button)`
  min-width: 40px;
  padding: 0;
`;

const CookbookItemTextContainer = styled(FlexRow)`
  padding: 4px 8px;
  justify-content: space-between;
`;

const CookbookItemPaperCursor = styled(CookbookItemPaper)`
  cursor: pointer;
`;

const CookbookItemBottomPanel = styled(Paper)`
  position: absolute;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  row-gap: 10px;
  width: 100%;
  bottom: 0;
  right: 0;
  padding: 4px 8px 8px;
  background-color: rgba(0,0,0,0.75);
`;

export const OwnCookbookItem = ({data, index, setDeleteIndex, setDialogOpen,
  setDeleteDesciption}) => {
  const handleDelete = () => {
    setDeleteIndex(index);
    setDialogOpen(true);
    setDeleteDesciption(data.cookbook_name);
  };
  return (
    <CookbookItemPaper>
      <Box sx={{position: 'relative'}}>
        <CookbookItemActions elevation={3}>
          <CookbookActionButton color="info" component={RouterLink}
            to={`/edit-cookbook/${data.cookbook_id}`}>
            <EditOutlinedIcon />
          </CookbookActionButton>
          <CookbookActionButton color="error" onClick={handleDelete}>
            <DeleteOutlinedIcon />
          </CookbookActionButton>
        </CookbookItemActions>
        <CookbookItemPhoto src={data.cookbook_photo} alt={data.cookbook_name} />
      </Box>
      <CookbookItemBottomPanel elevation={3}>
        <FlexRowSpaced>
        <Typography color="white">
          {data.cookbook_name}
        </Typography>
        <SmallGreyText>
          {data.cookbook_status}
        </SmallGreyText>
        </FlexRowSpaced>
        <FlexRowSpaced className="show-on-hover">
          <SmallDefaultButton component={RouterLink} to={`/cookbook/${data.cookbook_id}`}>
            View
          </SmallDefaultButton>
          <SmallAlternateButton>
            {data.cookbook_status === 'draft' && <>Publish</>}
            {data.cookbook_status === 'published' && <>Unpublish</>}
          </SmallAlternateButton>
        </FlexRowSpaced>
      </CookbookItemBottomPanel>
    </CookbookItemPaper>
  )
};
