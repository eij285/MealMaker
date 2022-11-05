from backend_helper import *

def filter_by_time(search_result, time_taken):
    """filter search result by time taken

    Args:
        search_result (list): a list of recipe_id
        time_taken (int): number in minutes

    Returns:
        {
            'status_code' (int): code,
            'body' (list): a list of recipe_id
        }
    """
    try:
        recipe_db = fetch_database("recipes")
        output = []
        for recipe in recipe_db:
            if (recipe['preparation_hours'] == None):
                recipe['preparation_hours'] = 0
            if (recipe['preparation_minutes'] == None):
                recipe['preparation_minutes'] = 0
            total_time = recipe['preparation_hours'] * 60 + recipe['preparation_minutes']
            if recipe['id'] in search_result and (0 < total_time <= time_taken) :
                output.append(recipe['id'])
        return{
            'status_code': 200,
            'body': output
        }
    except:
        return{
            'status_code': 400,
            'body': "fail to find any results"
        }
        
def filter_by_ingredients(search_result, ingredient_list):
    """Filter search result by list of ingredients

    Args:
        search_result (list): a list of recipe_id
        ingredient_list (list): a list of ingredient id
    
    Returns:
        {
            'status_code' (int): code,
            'body' (list): a list of recipe_id
        }
    """
    try:
        recipe_ingredient_db = fetch_database("recipe_ingredients")
        output = []
        for recipe in recipe_ingredient_db:
            if recipe['recipe_id'] in search_result and recipe['ingredient_name'] in ingredient_list:
                output.append(recipe['recipe_id'])
        return{
            'status_code': 200,
            'body': output
        }
    except:
        return{
            'status_code': 400,
            'error': "fail to find any results"
        }
    
    
   
def filter_by_cuisine(search_result, cuisine_option):
    """filter search result by cuisine

    Args:
        search_result (list): a list of recipe_id
        cuisine_option (string): a cuisine to be used as filter for search_result
    
    Returns:
        {
            'status_code' (int): code,
            'body' (list): a list of recipe_id
        }
    """
    
    try:
        recipe_ingredient_db = fetch_database("recipe_ingredients")
        output = []
        for recipe in recipe_ingredient_db:
            if recipe['recipe_id'] in search_result and recipe['cuisine'] == cuisine_option:
                output.append(recipe['recipe_id'])
        return{
            'status_code': 200,
            'body': output
        }
    except:
        return{
            'status_code': 400,
            'error': "fail to find any results"
        }
        