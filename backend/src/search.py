from backend_helper import *
from difflib import SequenceMatcher
from operator import itemgetter
from recipe import recipe_fetch_ingredients

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
    for elem in target:
        if elem is not None:
            for elem2 in elem:
                # target_array = word array of first item of target
                target_array = breakdown_string_to_array(elem)
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

def search(search_term, token):
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
    
    
    if not verify_token(token):
        return {
            'status_code': 401,
            'error': "Invalid token"
        }
    
    if not token:
        return {
            'status_code': 401,
            'error': "No token"
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
            print(ingredients)
            temp=None
            for ingredient in ingredients:
                temp = []
                temp.append(ingredient['ingredient_name'])
            all_ingredients.append(temp)
            
        # Fetch ingredient not working
        title_similarity = check_similarity(search_term, all_titles)
        ingredient_match = check_similarity_exact(search_term, all_ingredients)
        cuisine_similarity = check_similarity(search_term, all_cuisine)
        output = []
        
        fetch_recipe_by_id(all_id[0])
        
        for i in range(0, len(title_similarity)):
            similarity = {}
            similarity["similarity"] = (title_similarity[i] + ingredient_match[i] + cuisine_similarity[i])
            similarity["id"] = (all_id[i])
            if similarity["similarity"] > 0.2:
                output.append(similarity)
        
        sorted_dict = sorted(output, key=itemgetter('similarity'), reverse=True) 
        out_recipe = []
        conn = connect()
        cur = conn.cursor()
        output = []
        for i in sorted_dict:
            id = i["id"]
            
            # fetch recipe
            query = ("""SELECT * FROM recipes WHERE id = %s""")
            cur.execute(query, (id,))
            out_recipe = cur.fetchone()
            
            # fetch review count
            query = ("""
                SELECT COUNT(*) FROM recipe_reviews
                WHERE recipe_id = %s
                """)
            cur.execute(query, (id,))
            review_count = cur.fetchone()
            
            # fetch ratings
            query = ("""
                SELECT rating FROM recipe_reviews
                WHERE recipe_id = %s
                """)
            cur.execute(query, (id,))
            rating_all = cur.fetchall()
            rating_avg = sum(rating_all) / review_count
            
            # fetch likes
            query = ("""
                SELECT COUNT(*) FROM recipe_user_likes
                WHERE recipe_id = %s
                """)
            cur.execute(query, (id,))
            like_count = cur.fetchone()
            
            # fetch user
            query = ("""
                SELECT display_name, base64_image FROM users
                WHERE id = %s
                """)
            cur.execute(query, (out_recipe[1],))
            out = cur.fetchone()
            owner_name = out[0]
            owner_image = out[1]
            
            out = {
                'recipe_id': id,
                'recipe_name': out_recipe[2],
                'recipe_photo': out_recipe[4],
                'created_on': str(out_recipe[7]),
                'preparation_hours': out_recipe[9],
                'preparation_minutes':out_recipe[10],
                'cuisine': out_recipe[16],
                'breakfast': out_recipe[17],
                'lunch': out_recipe[18],
                'dinner': out_recipe[19],
                'snack': out_recipe[20],
                'vegetarian': out_recipe[21],
                'vegan': out_recipe[22],
                'kosher': out_recipe[23],
                'halal': out_recipe[24],
                'dairy_free': out_recipe[25],
                'gluten_free': out_recipe[26],
                'nut_free': out_recipe[27],
                'egg_free': out_recipe[28],
                'shellfish_free': out_recipe[29],
                'soy_free': out_recipe[30],
                'review_cnt': review_count,
                'rating_avg': rating_avg,
                'likes_cnt': like_count,
                'owner_display_name': owner_name,
                'owner_image': owner_image
            }
            output.append(out)
    
        return{
            'status_code': 200,
            'body': output
        }
    except:
        return {
            'status_code': 400,
            'error': "cannot find ingredients"
        }

        
