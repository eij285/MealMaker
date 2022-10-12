from recipe import create_recipe, edit_recipe, fetch_all_recipe, publish_recipe
from auth import auth_register
from backend_helper import *

def test_create_recipe():
    try:
        create_user_database()
        create_recipe_database()
    except:
        remove_user_database()
        remove_recipe_database()
        create_user_database()
        create_recipe_database()
    out = auth_register("Person1", "person1@email.com", "Password123#")
    token = out['body']['token']
    out = create_recipe("Recipe 1", "Description 1", "Method 1", 1, "Draft", token)
    assert out['status_code'] >= 200
    all_recipes = fetch_database('recipe')
    assert len(all_recipes) == 1
    recipe = all_recipes[0]
    assert recipe['recipe_name'] == 'Recipe 1'
    assert recipe['recipe_description'] == 'Description 1'
    assert recipe['methods'] == 'Method 1'
    assert recipe['portion_size'] == 1
    assert recipe['recipe_status'] == 'Draft'
    print("All tests passed!!!")

def test_create_multiple_recipe():
    return


def test_edit_recipe():
    create_user_database()
    create_recipe_database()
    token = auth_register("Person1", "person1@email.com", "Password123#")['body']['token']
    out = create_recipe("Recipe1", "Description 1", "Method 1", 1, "Draft", token)
    recipe_id = out['body']['recipe_id']

    out = edit_recipe("New Recipe 1", "New Description 1", "New Method 1", 4, recipe_id, "Public")
    assert out['status_code'] == 200
    
        
    
    


if __name__ == "__main__":
    test_create_recipe()
    
    