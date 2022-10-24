import React from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import styled from '@emotion/styled';
import { Box, Button, IconButton, Paper, Rating, Tooltip, Typography } from '@mui/material';
import FoodBankIcon from '@mui/icons-material/FoodBank';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import ThumbUpOutlinedIcon from '@mui/icons-material/ThumbUpOutlined';
import { FlexRow, FlexRowWrapSpaced, FlexColumn } from '../StyledNodes';
import { MediumGreyText, SmallBlackText, SmallGreyText, TextVCentred } from '../TextNodes';
import {
  ImageInput,
  TextInput,
  NumericInput,
  NarrowNumericInput
} from '../../components/InputFields';
import { formatNutrient, getAverageRating } from '../../helpers';
const config = require('../../config.json');

const RecipeImgContainer = styled.div`
  display: flex;
  position: relative;
  flex-direction: row;
  justify-content: center;
  height: 33vh;
  & img, & svg {
    height: 100%;
    width: auto;
    object-fit: contain;
  }
`;

export const RecipeImg = ({src, alt}) => {
  return (
    <RecipeImgContainer>
      {src && <img src={src} alt={alt} />}
      {!src && <FoodBankIcon/>}
    </RecipeImgContainer>
  );
};

export const RecipeRating = ({reviews}) => {
  const [avgRating, setAvgRating] = React.useState(0);
  React.useEffect(() => {
    setAvgRating(getAverageRating(reviews));
  }, [reviews]);
  return (
    <Box sx={{ alignSelf: 'center' }}>
      {typeof reviews === typeof [] && <>
        {reviews.length < 1 && <MediumGreyText>No Reviews</MediumGreyText>}
        {reviews.length > 0 && <>
        <Rating value={avgRating} precision={0.5} readOnly />
        <MediumGreyText>
          {avgRating.toFixed(1)}&nbsp;
          ({reviews.length}&nbsp;
          {reviews.length !== 1 && <span>reviews</span>}
          {reviews.length === 1 && <span>review</span>})
        </MediumGreyText>
        </>}
      </>}
    </Box>
  );
};

export const RecipeLikes = ({likesObject, likeRecipe}) => {
  return (
    <>
    {typeof likesObject === typeof {} &&
    <Tooltip title="Like Recipe" placement="top" arrow>
      <IconButton color="info" onClick={likeRecipe}>
        {likesObject.has_liked && <ThumbUpIcon />}
        {!likesObject.has_liked && <ThumbUpOutlinedIcon />}
        &nbsp;{likesObject.likes_count}
      </IconButton>
    </Tooltip>}
    </>
  );
};


const RecipeInfoPanelContainer = styled(FlexRowWrapSpaced)`
  border: 1px solid #333333;
  padding: 8px;
  row-gap: 20px;
  align-items: center;
`;

const NutritionText = ({topVal, bottomVal, units}) => {
  return (
    <Box sx={{textAlign: 'center'}}>
      <Typography>{topVal}</Typography>
      <Typography>{bottomVal}</Typography>
    </Box>
  );
};

const PreparationTimeText = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: center;
`;

const RecipePrepartionTimeText = React.forwardRef((props, ref) => {
  //  Spread the props to the underlying DOM element.
  return (<div {...props} ref={ref}>
    <Typography>
      {props.hours > 0 && `${props.hours}hrs`}&nbsp;
      {props.minutes > 0 && `${props.minutes}mins`}
    </Typography>
    <SmallGreyText>{props.level}</SmallGreyText>
  </div>
  );
});

const RecipePrepartionTime = ({hours, minutes, level}) => {
  let totalMinutes = 0;
  let ttMsg = '';
  if (hours !== null) {
    totalMinutes = hours * 60;
    ttMsg = `${hours}hrs`;
  }
  if (minutes !== null) {
    totalMinutes += minutes;
    ttMsg += `${ttMsg?' ':''}${minutes}mins`;
  }
  if (level === config.EFFICIENCY[2]) {
    totalMinutes /= config.EFFICIENCY_CONV;
  } else if (level === config.EFFICIENCY[0]) {
    totalMinutes /= config.EFFICIENCY_CONV;
  }
  totalMinutes = Math.round(totalMinutes);
  const customHours = parseInt(totalMinutes / 60);
  const customMinutes = totalMinutes - (customHours * 60);
  hours !== null && minutes !== null && (ttMsg += ` @ Intermediate Efficiency`);

  return (
    <FlexRow>
      <AccessTimeIcon sx={{fontSize: '3em'}} />
      <PreparationTimeText>
        {hours !== null && minutes !== null && level !== config.EFFICIENCY[1] &&
        <Tooltip title={ttMsg} placement="top" arrow>
          <RecipePrepartionTimeText hours={customHours} minutes={customMinutes}
            level={level} />
        </Tooltip>}
        {hours !== null && minutes !== null && level === config.EFFICIENCY[1] &&
        <RecipePrepartionTimeText hours={customHours} minutes={customMinutes}
          level={level} />}
        {hours === null && minutes === null &&
        <Typography>Unspecified Preparation Time</Typography>}
      </PreparationTimeText>
    </FlexRow>
  );
};

const RecipeTags = ({data}) => {
  let tags = [];
  data.vegetarian && tags.push('Vegetarian');
  data.vegan && tags.push('Vegan');
  data.kosher && tags.push('Halal');
  data.dairy_free && tags.push('Dairy Free');
  data.gluten_free && tags.push('Gluten Free');
  data.nut_free && tags.push('Nut Free');
  data.egg_free && tags.push('Egg Free');
  data.shellfish_free && tags.push('Shellfish Free');
  data.soy_free && tags.push('Gluten Free');
  return (
    <SmallBlackText>
      {tags.join(', ')}
    </SmallBlackText>
  );
};

export const RecipeInfoPanel = ({data, currData, setServings}) => {
  const reqImperial = data.units === 'Imperial';
  const energy = formatNutrient(currData.energy, false, reqImperial);
  const protein = formatNutrient(currData.protein, true, reqImperial);
  const carbohydrates = formatNutrient(currData.carbohydrates, true, reqImperial);
  const fats = formatNutrient(currData.fats, true, reqImperial);
  return (
    <RecipeInfoPanelContainer>
      <FlexRow>
        <NumericInput
          label="Servings"
          sx={{ width: '100px' }}
          value={data.servings}
          onChange={(e) =>
            setServings(e.target.value ? `${parseInt(e.target.value)}`: '')}
        />
        <NutritionText topVal="Energy" bottomVal={energy} />
        <NutritionText topVal="Protein" bottomVal={protein} />
        <NutritionText topVal="Carbs" bottomVal={carbohydrates} />
          <NutritionText topVal="Fats" bottomVal={fats} />
      </FlexRow>
      <RecipePrepartionTime hours={data.preparation_hours}
        minutes={data.preparation_minutes} level={data.efficiency} />
      <RecipeTags data={data} />
    </RecipeInfoPanelContainer>
  );
};
