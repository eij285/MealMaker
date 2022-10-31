from backend_helper import *
from difflib import SequenceMatcher

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
    search_term_array = breakdown_string_to_array(search_term)
    similarity = []
    for i in range(0, len(target)):
        # target_array = word array of first item of target
        target_array = breakdown_string_to_array(target[i])
        ratio = 0.0
        for target_word in target_array:
            if target_word in search_term_array:
                ratio += 1
        ratio /= (len(target_array) * len(search_term_array))
        similarity.append(ratio)
    return similarity

def check_similarity(search_term, target):
    search_term_array = breakdown_string_to_array(search_term)
    similarity = []
    for i in range(0, len(target)):
        # target_array = word array of first item of target
        target_array = breakdown_string_to_array(target[i])
        ratio = 0.0
        for target_word in target_array:
            for search_term_word in search_term_array:
                ratio += SequenceMatcher(None, target_word, search_term_word).ratio()
        ratio /= (len(target_array) * len(search_term_array))
        similarity.append(ratio)
    return similarity

def search(search_term):
    recipes_db = fetch_database("recipes")
    recipe_ingredient_db = fetch_database("recipe_ingredients")
    all_titles = recipes_db['recipe_name']
    all_ingredients = recipe_ingredient_db['ingredients']
    all_cuisine = recipes_db['cuisine']
    all_id = recipes_db['recipe_id']
    title_similarity = check_similarity(search_term, all_titles)
    ingredient_match = check_similarity_exact(search_term, all_ingredients)
    cuisine_similarity = check_similarity(search_term, all_cuisine)
    similarity = {}
    for i in range(0, len(title_similarity)):
        similarity["similarity"].append(title_similarity[i] + ingredient_match[i] + cuisine_similarity[i])
        similarity["id"].append(all_id[i])
    
    similarity = sorted(similarity.items(), key = lambda kv : kv[1])
    return similarity
        
    
    