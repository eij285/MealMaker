from config import DB_CONN_STRING
from recipe import recipe_details
import psycopg2
import math

from pprint import pprint

def take_second(elem):
    return (elem[1])

def estimate_rating(recipe_id, user_id, all_ratings):
    target_recipe_ratings = all_ratings[recipe_id - 1]

    positive_sims = []

    # Loop through all recipes and calculate similarities
    for idx, recipe_ratings in enumerate(all_ratings):
        
        # Skip targeted recipe
        if idx == recipe_id - 1:
            continue

        sim = calculate_similarity(target_recipe_ratings, recipe_ratings)

        # Add to list of positive similarities if similarity is positive
        # (include the actual rating itself)
        if sim > 0:
            positive_sims.append((sim, all_ratings[idx][user_id - 1]))

    # Calculate weighted average
    a, b = 0, 0

    for sim_pair in positive_sims:
        sim, rating = sim_pair
        a += sim * rating
        b += sim

    return a / b

def calculate_similarity(orig_vals, new_vals):
    """Calculates Pearson-correlation similarity for two sets of values
    
    Args:


    Returns:


    """
    # Assert that both are of equal lengths

    # Get mean for both lists (discarding 0's)
    filtered_ov = [x for x in orig_vals if x != 0]
    filtered_nv = [x for x in new_vals if x != 0]

    ov_mean = sum(filtered_ov)/len(filtered_ov)
    nv_mean = sum(filtered_nv)/len(filtered_nv)

    # Compute cosine similarity
    a = 0
    b = 0
    c = 0

    for orig_val, new_val in zip(orig_vals, new_vals):
        ov_vm = 0
        nv_vm = 0

        # Subtracts mean from orig if rating exists
        if orig_val != 0:
            ov_vm = orig_val - ov_mean
        
        # Subtracts mean from new if rating exists
        if new_val != 0:
            nv_vm = new_val - nv_mean

        # Add results to values a, b and c
        a += ov_vm * nv_vm
        b += ov_vm ** 2
        c += nv_vm ** 2

    # Square root b and c, and comute cosine similarity
    b = math.sqrt(b)
    c = math.sqrt(c)

    return a / (b * c)

def feed_fetch_discover(token):

    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    
    # Check that the token corresponds to an active user
    cur.execute("SELECT id FROM users WHERE token = %s;", (token,))

    sql_result = cur.fetchall()
    if not sql_result:
        cur.close()
        conn.close()

        return {
            'status_code': 401,
            'error': 'Token does not correspond to any active user;'
        }
    
    # Get the matching user id from token
    u_id, = sql_result[0]

    # Get largest user_id
    max_uid = 0

    cur.execute("SELECT MAX(user_id) FROM recipe_reviews;")
    sql_result = cur.fetchall()

    if sql_result:
        max_uid, = sql_result[0]
    
    # Get largest recipe_id
    max_rid = 0
    
    cur.execute("SELECT MAX(recipe_id) FROM recipe_reviews;")
    sql_result = cur.fetchall()

    if sql_result:
        max_rid, = sql_result[0]

    # Collect all ratings info from database
    cur.execute("SELECT recipe_id, user_id, rating FROM recipe_reviews;")

    sql_result = cur.fetchall()

    # If empty results, then return empty body
    if not sql_result:
        cur.close()
        conn.close()

        return {
            'status_code': 200,
            'body': {}
        }

    # Otherwise, initialise 2d array with recipes as rows and users as columns
    ratings = [[0 for x in range(max_uid)] for y in range(max_rid)]

    for rating_info in sql_result:
        rid, uid, rating = rating_info
        ratings[rid - 1][uid - 1] = rating
    
    # Check what recipes user has not rated (to be discovered)
    unrated_recipes = []

    for x in range(max_rid):

        # Skip recipe if it is a draft
        sql_query = "SELECT * FROM recipes WHERE recipe_id = %s \
                     AND recipe_status = 'published'"
        cur.execute(sql_query, (x + 1,))

        sql_result = cur.fetchall()
        if not sql_result:
            continue

        if ratings[x][u_id - 1] == 0:
            unrated_recipes.append(x + 1)

    # For each unrated recipe, calculate estimated rating
    estimates = []

    for r_id in unrated_recipes:
        estimates.append((r_id, estimate_rating(r_id, u_id, ratings)))

    # Sort by highest estimate to lowest estimate
    estimates.sort(key=take_second, reverse=True)
    print(estimates)

    # For each recipe_id, add recipe details to body content
    body_content = []
    
    for estimate in estimates:
        r_id = estimate[0]
        r_details = recipe_details(r_id, token)

        # Check that fetching recipe details is successful
        if r_details['status_code'] != 200:
            cur.close()
            conn.close()

            return r_details
        
        # Otherwise add details to body_content
        else:
            body_content.append(r_details['body'])

    return {
        'status_code': 200,
        'body': body_content
    }

def feed_fetch_subscription(token):
    
    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    
    # Check that the token corresponds to an active user
    cur.execute("SELECT id FROM users WHERE token = %s;", (token,))

    sql_result = cur.fetchall()
    if not sql_result:
        cur.close()
        conn.close()

        return {
            'status_code': 401,
            'error': 'Token does not correspond to any active user;'
        }
    
    # Get the matching user id from token
    u_id, = sql_result[0]

    pass

def feed_fetch_trending():
    pass

if __name__ == "__main__":
    pprint(feed_fetch_discover("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoxMiwiZXhwIjoxNjY3OTA2MDE4fQ.v9cREARALjt-Lj6AgyphTKRTCBJCQT393Ct1cozT9Ew"))

