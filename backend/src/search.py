from backend_helper import *
from difflib import SequenceMatcher
from operator import itemgetter
from recipe import recipe_fetch_ingredients, recipe_details

def breakdown_string_to_array(search_term):
    word = []
    str = ""
    for i in range(0, len(search_term)):
        str = str + search_term[i:i+1]
        if search_term[i:i+1] == " ":
            word.append(str[:-1])
            str = ""
    word.append(str)
    return word

def check_similarity_exact(search_term, target):
    """check the number of exact terms matching between search_term and target

    Args:
        search_term (string): search term from user
        target (list): a list of ingredients in string

    Returns:
        similarity (list): a list of ratio
    """

    search_term_array = breakdown_string_to_array(search_term)
    similarity = []
    for elem in target:
        if elem is not None:
            for elem2 in elem:
                # target_array = word array of first item of target
                target_array = breakdown_string_to_array(elem2)
                ratio = 0.0
                for target_word in target_array:
                    if target_word in search_term_array:
                        ratio += 1
            ratio /= (len(target_array) * len(search_term_array))
            similarity.append(ratio)
        else:
            similarity.append(0)
    return similarity

def check_similarity(search_term, target):
    
    search_term_array = breakdown_string_to_array(search_term)
    similarity = []
    for elem in target:
        if elem is not None:
            # target_array = word array of first item of target
            target_array = breakdown_string_to_array(elem)
            ratio = 0.0
            for target_word in target_array:
                for search_term_word in search_term_array:
                    ratio += SequenceMatcher(None, target_word, search_term_word).ratio()
            ratio /= (len(target_array) * len(search_term_array))
            similarity.append(ratio)
        else:
            similarity.append(0)
    return similarity

def search(search_term):
    """search for recipes based on search_term, with a cutoff of anything with less than 20% similarity not returned

    Args:
        search_term (string): term to be used to search for ingredients
        token       (string): token used for validation

    Returns:
        list of pydict: a list of pydict ordered by most similar to search term
            {
                'recipe_id':,
                'recipe_name':,
                'recipe_photo':,
                'created_on': str(),
                'preparation_hours':,
                'preparation_minutes':,
                'cuisine':,
                'breakfast':,
                'lunch':,
                'dinner':,
                'snack':,
                'vegetarian':,
                'vegan':,
                'kosher':,
                'halal':,
                'dairy_free':,
                'gluten_free':,
                'nut_free':,
                'egg_free':,
                'shellfish_free':,
                'soy_free':,
                'review_cnt':,
                'rating_avg':,
                'likes_cnt':,
                'owner_display_name':,
                'owner_image':
            }
        for datatype, refer to schema.sql
    """
    
    if search_term == "":
        return{
            'status_code': 200,
            'body': []
        }
    
    try:        
        recipes_db = fetch_database("recipes")
        all_titles = []
        all_ingredients = []
        all_cuisine = []
        all_id = []
        
        for recipe in recipes_db:
            all_cuisine.append(recipe['cuisine'])
            all_id.append(recipe['recipe_id'])
            all_titles.append(recipe['recipe_name'])
            ingredients = recipe_fetch_ingredients(recipe['recipe_id'])

            temp=[]
            for ingredient in ingredients:
                temp.append(ingredient['ingredient_name'])
            all_ingredients.append(temp)
        # Fetch ingredient not working
        title_similarity = check_similarity(search_term, all_titles)
        ingredient_match = check_similarity_exact(search_term, all_ingredients)
        cuisine_similarity = check_similarity(search_term, all_cuisine)
        output = []
        for i in range(0, len(title_similarity)):
            similarity = {}            
            similarity["similarity"] = (title_similarity[i] + ingredient_match[i] + cuisine_similarity[i])
            similarity["id"] = (all_id[i])            
            if similarity["similarity"] > 0.2:
                output.append(similarity)
        
        sorted_dict = sorted(output, key=itemgetter('similarity'), reverse=True) 
        output = []
        for i in sorted_dict:
            id = i["id"]
            out = recipe_details(id, None)['body']
            output.append(out)
        
        return{
            'status_code': 200,
            'body': output
        }
    except:
        return {
            'status_code': 400,
            'error': "cannot find any results"
        }

        
