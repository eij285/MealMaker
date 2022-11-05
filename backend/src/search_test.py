from backend_helper import *
from search import search
from recipe import *
from auth import *

def test_search_simple(search_term):
    create_user_database()
    create_recipe_database()
    create_recipe_ingredient_database()
    create_recipe_reviews_database()
    create_recipe_user_likes_database()
    out = auth_register("Person1", "person1@email.com", "Password123#")
    token = out['body']['token']
    
    recipe_id = create_recipe("Australian Beef", "Description 1", 5, "draft", token)['body']['recipe_id']
    recipe_update_ingredients(recipe_id, [create_ingredient_for_testing("Beef"), create_ingredient_for_testing("salt"), create_ingredient_for_testing("pepper")])
    
    recipe_id = create_recipe("Asian Stir Fry Noodle", "Description 2", 3, "draft", token)['body']['recipe_id']
    recipe_update_ingredients(recipe_id, [create_ingredient_for_testing("noodle"), create_ingredient_for_testing("Chicken"), create_ingredient_for_testing("salf"), create_ingredient_for_testing("pepper"), create_ingredient_for_testing("MSG")])
    
    recipe_id = create_recipe("Banana Cake", "Description 3", 6, "draft", token)['body']['recipe_id']
    recipe_update_ingredients(recipe_id, [create_ingredient_for_testing("Banana"), create_ingredient_for_testing("flour"), create_ingredient_for_testing("sugar"), create_ingredient_for_testing("egg")])
    
    recipe_id = create_recipe("Asian Beef", "Description 4", 3, "draft", token)['body']['recipe_id']
    recipe_update_ingredients(recipe_id, [create_ingredient_for_testing("MSG"), create_ingredient_for_testing("Beef"), create_ingredient_for_testing("onion"), create_ingredient_for_testing("egg"), create_ingredient_for_testing("noodle")])

    out = search(search_term, token)
    print(out)
    
if __name__ == "__main__":
    remove_user_database()
    remove_recipe_database()
    remove_recipe_ingredient_database()
    remove_recipe_reviews_database()
    remove_recipe_user_likes_database()
    test_search_simple("Beef with egg")

    # print(fetch_database("users"))