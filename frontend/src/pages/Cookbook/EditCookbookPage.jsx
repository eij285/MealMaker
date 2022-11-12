import React from 'react';
import { Link as RouterLink, useNavigate, useParams } from 'react-router-dom';
import styled from '@emotion/styled';
import {
  Box,
  Button,
  Divider,
  Grid,
} from '@mui/material';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import GlobalContext from '../../utils/GlobalContext';
import ManageLayout from '../../components/Layout/ManageLayout';
import { PageTitle, SubPageTitle } from '../../components/TextNodes';
import {
  ConfirmationDialog,
  FlexColumn,
  FlexRow,
  ErrorAlert,
  SuccessAlert
} from '../../components/StyledNodes';
import { backendRequest, initialCookbookData } from '../../helpers';
import {
  CreateEditCookbookForm
} from '../../components/Cookbook/CookbookNodes';
import {
  CookbookScrollerRecipeItem,
  OwnCookbookRecipeItem
} from '../../components/Recipe/RecipeItems';

const RecipeScroller = styled.div`
  position: relative;
  height: 200px;
  width: 100%;
  overflow-x: scroll;
  background-color: #eeeeee;
`;

const RecipeAdder = ({recipesInCookbook, ownRecipes, setAddRecipeIds}) => {
  const [ids, setIds] = React.useState([]);
  const addSelectedIds = () => {
    if (ids.length > 0) {
      setAddRecipeIds([...ids]);
    }
  };
  const addRemove = (index, isAdd) => {
    const selectedId = ownRecipes[index].recipe_id;
    if (isAdd) {
      if (ids.indexOf(selectedId) === -1) {
        setIds([...ids, selectedId]);
      }
    } else {
      setIds([...ids.filter((id) => id != selectedId)]);
    }
  };
  const innerBoxStyles = {
    display: 'flex',
    columnGap: '10px',
    padding: '10px'
  };
  const recipeStyles = {
    width: '180px',
    overflow: 'hidden'
  };
  return (
    <Box>
      <RecipeScroller>
        <Box sx={innerBoxStyles}>
          {ownRecipes.filter((recipe) => {
            for (let r of recipesInCookbook) {
              if (r.body.recipe_id === recipe.recipe_id) {
                return false;
              }
            }
            return true;
          }).map((recipe, index) => (
          <Box key={index} sx={recipeStyles}>
            <CookbookScrollerRecipeItem data={recipe} index={index}
              addRemove={addRemove} />
          </Box>
          ))}
        </Box>
      </RecipeScroller>
      <Button color="success"
        size="large"
        onClick={addSelectedIds}
        sx={{textTransform: 'none'}}
        startIcon={<AddCircleIcon />}>
        Add to cookbook
      </Button>
    </Box>
  );
};

function EditCookbookPage () {
  const { cookbookId } = useParams();
  const token = React.useContext(GlobalContext).token;

  const [cookbookData, setCookbookData] = React.useState({
    ...initialCookbookData(), cookbookId: parseInt(cookbookId)
  });
  const [recipesInCookbook, setRecipesInCookbook] = React.useState([]);
  const [ownRecipes, setOwnRecipes] = React.useState([]);
  const [addRecipeIds, setAddRecipeIds] = React.useState([]);

  const [responseError, setResponseError] = React.useState('');
  const [responseSuccess, setResponseSuccess] = React.useState('');

  const loadCookbook = () => {
    const body = {
      cookbook_id: cookbookId
    };
    backendRequest('/cookbook/edit', body, 'POST', token, (data) => {
      setCookbookData({
        cookbookId: cookbookId,
        name: data.body.cookbook_name,
        photo: data.body.cookbook_photo,
        description: data.body.cookbook_description,
        cookbookStatus: data.body.cookbook_status,
      });
    }, (error) => {
      setResponseError(error);
    });
  };

  const updateCookbook = (requestBody) => {
    backendRequest('/cookbook/update', requestBody, 'POST', token, (data) => {
      setResponseSuccess('Cookbook Updated Successfully');
    }, (error) => {
      setResponseError(error);
    });
  };

  const loadRecipesInCookbook = () => {
    const body = {
      cookbook_id: cookbookId
    };
    backendRequest('/cookbook/view', body, 'POST', token, (data) => {
      setRecipesInCookbook([...data.body.recipes]);
    }, (error) => {
      setResponseError(error);
    });
  };

  const loadOwnRecipes = () => {
    backendRequest('/recipes/fetch-own', {}, 'POST', token, (data) => {
      setOwnRecipes([...data.body]);
    }, (error) => {
      setResponseError(error);
    });
  };

  // remove recipe from cookbook then reload recipes
  const removeFromCookbook = (index) => {
    const recipeId = recipesInCookbook[index].body.recipe_id;
    const requestBody = {
      cookbook_id: cookbookId,
      recipe_id: recipeId
    };
    backendRequest('/cookbook/remove/recipe', requestBody, 'POST', token, (data) => {
      loadRecipesInCookbook();
      loadOwnRecipes();
    }, (error) => {
      setResponseError(error);
    });
  };

  // when recipes ids to remove change remove one by one, then reload when done
  React.useEffect(() => {
    if (addRecipeIds.length > 0) {
      const requests = [];
      for (let recipeId of addRecipeIds) {
        const requestBody = {
          cookbook_id: cookbookId,
          recipe_id: recipeId
        };
        requests.push(
          backendRequest('/cookbook/add/recipe', requestBody,  'PUT', token,
          (data) => {
            
          })
        );
      }
      Promise.all(requests).then(() => {
        loadRecipesInCookbook();
        loadOwnRecipes();
        setAddRecipeIds([]);
      });
    }
  }, [addRecipeIds]);

  React.useEffect(() => {
    loadCookbook();
    loadRecipesInCookbook();
    loadOwnRecipes();
  }, [cookbookId]);

  return (
    <ManageLayout>
      <Grid item xs={12}>
        <Grid container>
          <Grid item xl={6} lg={8} md={10} sm={12} xs={12}>
            <PageTitle>Edit Cook Book</PageTitle>
            <FlexColumn>
              {responseSuccess !== '' &&
              <SuccessAlert message={responseSuccess} setMessage={setResponseSuccess} />}
              {responseError !== '' &&
              <ErrorAlert message={responseError} setMessage={setResponseError} />}
              <CreateEditCookbookForm data={cookbookData}
                callFunction={updateCookbook} />
            </FlexColumn>
          </Grid>
        </Grid>
        <Divider sx={{mt:4}} />
        <SubPageTitle>Cookbook Recipes</SubPageTitle>
        <RecipeAdder recipesInCookbook={recipesInCookbook}
          ownRecipes={ownRecipes} setAddRecipeIds={setAddRecipeIds} />
        {recipesInCookbook.length > 0 &&
        <Grid container mt={4}>
          {recipesInCookbook.map((recipe, index) => (
            <Grid item xl={3} lg={4} md={6} sm={6} xs={12} key={index}>
              <OwnCookbookRecipeItem data={recipe.body} index={index}
                setRemove={removeFromCookbook} />
            </Grid>))}
        </Grid>}
      </Grid>
    </ManageLayout>
  );
}

export default EditCookbookPage;
