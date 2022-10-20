import React from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import styled from '@emotion/styled';
import { Button, Paper, Rating, Typography } from '@mui/material';
import FoodBankIcon from '@mui/icons-material/FoodBank';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DeleteOutlinedIcon from '@mui/icons-material/DeleteOutlined';
import { FlexRow, FlexColumn, ImageContainer4by3, ResponsiveImage4by3 } from '../StyledNodes';
import { SmallGreyText, TextVCentred } from '../TextNodes';

const RecipeItemActionPanel = styled.div`
  box-shadow: -10px 40px 5px -10px rgba(0,0,0,0.75) inset;
  height: 35px;
  display: flex;
  justify-content: space-between;
  padding: 2px 8px;
  position: absolute;
  z-index: 1;
  top: 0;
  left: 0;
  box-sizing: border-box;
  width: 100%;
`;

const RecipeItemPhoto = ({ src, alt }) => {
  return (<>
    {src && <ResponsiveImage4by3 src={src} alt={`${alt} photo`} />}
    {!src && <ImageContainer4by3><FoodBankIcon/></ImageContainer4by3>}
  </>);
};

const RecipeItemPaper = styled(Paper)`
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
`;

const RecipeItemTextContainer = styled(FlexRow)`
  padding: 4px 8px;
  justify-content: space-between;
`;

const RecipeItemTitle = styled(Typography)`
  font-size: 0.85em;
  color: #ffffff;
  white-space: nowrap;
`;

const RecipeItemActions = styled.div`
  display: flex;
  flex-direction: row;
  height: 24px;
`;

const ActionButton = styled(Button)`
  min-width: 40px;
  padding: 0;
`;

export const OwnRecipeItem = ({data, token, refresh}) => {
  return (
    <RecipeItemPaper>
      <RecipeItemActionPanel>
        <RecipeItemTitle>{data.cuisine}</RecipeItemTitle>
        <RecipeItemActions>
          <ActionButton color="info" component={RouterLink}
            to={`/edit-recipe/${data.recipe_id}`}>
            <EditOutlinedIcon />
          </ActionButton>
          <ActionButton color="warning">
            <ContentCopyIcon />
          </ActionButton>
          <ActionButton color="error">
            <DeleteOutlinedIcon />
          </ActionButton>
        </RecipeItemActions>
      </RecipeItemActionPanel>
      <RecipeItemPhoto src={data.recipe_photo} alt={data.recipe_name} />
      <RecipeItemTextContainer>
        <FlexColumn>
          <Rating value={4.5} precision={0.5} readOnly />
          <Typography>{data.recipe_name}</Typography>
        </FlexColumn>
        <FlexColumn>
          <SmallGreyText align="right">{data.recipe_status}</SmallGreyText>
          <TextVCentred><ThumbUpIcon />{10}</TextVCentred>
        </FlexColumn>
      </RecipeItemTextContainer>
    </RecipeItemPaper>
  )
};
