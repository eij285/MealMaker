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
    print("All tests under test_create_recipe() passed!!!")

def test_create_multiple_recipe():
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
    out = create_recipe("Recipe 2", "Description 2", "Method 2", 3, "Published", token)
    out = create_recipe("Recipe 3", "Description 3", "Method 3", 5, "Draft", token)
    all_recipes = fetch_database('recipe')
    assert(len(all_recipes)) == 3
    recipe_name = ['Recipe 1', 'Recipe 2', 'Recipe 3']
    recipe_descr = ['Description 1', 'Description 2', 'Description 3']
    recipe_method = ['Method 1', 'Method 2', 'Method 3']
    recipe_portion = [1,3,5]
    recipe_status = ['Draft', 'Published', 'Draft']
    for i, recipe in enumerate(all_recipes):
        assert recipe['recipe_name'] == recipe_name[i]
        assert recipe['recipe_description'] == recipe_descr[i]
        assert recipe['methods'] == recipe_method[i]
        assert recipe['portion_size'] == recipe_portion[i]
        assert recipe['recipe_status'] == recipe_status[i]
    print("All tests under test_create_multiple_recipe() passed!!!")

    
    
def test_edit_recipe():
    try:
        create_user_database()
        create_recipe_database()
    except:
        remove_user_database()
        remove_recipe_database()
        create_user_database()
        create_recipe_database()
    token = auth_register("Person1", "person1@email.com", "Password123#")['body']['token']
    out = create_recipe("Recipe 1", "Description 1", "Method 1", 1, "Draft", token)
    all_recipes = fetch_database('recipe')
    recipe = all_recipes[0]
    assert recipe['recipe_name'] == 'Recipe 1'
    assert recipe['recipe_description'] == 'Description 1'
    assert recipe['methods'] == 'Method 1'
    assert recipe['portion_size'] == 1
    assert recipe['recipe_status'] == 'Draft'
    
    out = edit_recipe("New Recipe 1", "New Description 1", "New Method 1", 4, recipe['recipe_id'], "Published", token)
    all_recipes = fetch_database('recipe')
    recipe = all_recipes[0]
    assert out['status_code'] == 200
    assert recipe['recipe_name'] == "New Recipe 1"
    assert recipe['recipe_description'] == "New Description 1"
    assert recipe['methods'] == 'New Method 1'
    assert recipe['portion_size'] == 4
    assert recipe['recipe_status'] == 'Published'
    print("All tests under test_edit_recipe() passed!!!")

def test_edit_multiple_recipe():
    try:
        create_user_database()
        create_recipe_database()
    except:
        remove_user_database()
        remove_recipe_database()
        create_user_database()
        create_recipe_database()
    token = auth_register("Person1", "person1@email.com", "Password123#")['body']['token']
    create_recipe("Recipe 1", "Description 1", "Method 1", 1, "Draft", token)
    create_recipe("Recipe 2", "Description 2", "Method 2", 3, "Published", token)
    create_recipe("Recipe 3", "Description 3", "Method 3", 5, "Published", token)
    all_recipes = fetch_database('recipe')
    recipe_id_1 = all_recipes[0]['recipe_id']
    recipe_id_2 = all_recipes[2]['recipe_id']
    out = edit_recipe("New Recipe 1", "New Description 1", "New Method 1", 4, recipe_id_1, "Published", token)
    assert out['status_code'] == 200
    out = edit_recipe("New Recipe 3", "New Description 3", "New Method 3", 1, recipe_id_2, "Draft", token)
    assert out['status_code'] == 200
    recipe_name = ['New Recipe 1', 'Recipe 2', 'New Recipe 3']
    recipe_descr = ['New Description 1', 'Description 2', 'New Description 3']
    recipe_method = ['New Method 1', 'Method 2', 'New Method 3']
    recipe_portion = [4,3,1]
    recipe_status = ['Published', 'Published', 'Draft']
    all_recipes = fetch_database('recipe')
    for recipe in all_recipes:
        if recipe['recipe_id'] == recipe_id_1:
            assert recipe['recipe_name'] == recipe_name[0]
            assert recipe['recipe_description'] == recipe_descr[0]
            assert recipe['methods'] == recipe_method[0]
            assert recipe['portion_size'] == recipe_portion[0]
            assert recipe['recipe_status'] == recipe_status[0]
        elif recipe['recipe_id'] == recipe_id_2:
            assert recipe['recipe_name'] == recipe_name[2]
            assert recipe['recipe_description'] == recipe_descr[2]
            assert recipe['methods'] == recipe_method[2]
            assert recipe['portion_size'] == recipe_portion[2]
            assert recipe['recipe_status'] == recipe_status[2]
        else:
            assert recipe['recipe_name'] == recipe_name[1]
            assert recipe['recipe_description'] == recipe_descr[1]
            assert recipe['methods'] == recipe_method[1]
            assert recipe['portion_size'] == recipe_portion[1]
            assert recipe['recipe_status'] == recipe_status[1]
    print("All tests under test_edit_multiple_recipe() passed!!!")

if __name__ == "__main__":
    test_create_recipe()
    test_create_multiple_recipe()
    test_edit_recipe()
    test_edit_multiple_recipe()
    