from recipe import create_recipe, edit_recipe, publish_recipe
from auth import auth_register
from backend_helper import *

def test_create_recipe():
    create_user_database()
    create_recipe_database()
    out = auth_register("Person1", "person1@email.com", "Password123#")
    try:
        token = out['body']['token']
    except:
        print("ERROR")
        remove_user_database()
        remove_recipe_database()
        return

    create_recipe("Recipe1", "Description 1", "Method 1", 1, token)
    print(fetch_recipe_database())
    remove_user_database()
    remove_recipe_database()
    


if __name__ == "__main__":
    test_create_recipe()
    
    