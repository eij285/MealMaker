from config import DB_CONN_STRING
from recipe import recipe_details
from algorithm import take_second, calculate_similarity
import psycopg2

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

    # TODO: Identify scenarios where division by 0 occurs and return appropriate
    # value
    if b == 0:
        return 0
    else:
        return a / b

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

    # Get list of users the user is following
    sql_query = "SELECT following_id FROM subscriptions WHERE follower_id = %s;"
    cur.execute(sql_query, (str(u_id),))

    sql_result = cur.fetchall()

    # If no following users, then subscription will return empty body
    if not sql_result:
        cur.close()
        conn.close()

        return {
            'status_code': 200,
            'body': {}
        }
    
    # Get all recipes created by following users and order by last created
    recipes_following = []

    for user_id in sql_result:
        sql_query = "SELECT recipe_id, created_on FROM recipes WHERE \
                     owner_id = %s;"
        cur.execute(sql_query, (user_id,))

        sql_result = cur.fetchall()
        recipes_following += sql_result

    recipes_following.sort(key=take_second, reverse=True)

    # For each recipe_id, add recipe details to body content
    body_content = []
    
    for recipe in recipes_following:
        r_id = recipe[0]
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


def feed_fetch_trending():
    
    # Connect to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    
    sql_query = "SELECT r.recipe_id, COUNT(l.recipe_id) \
                 FROM recipes r \
                 LEFT JOIN recipe_user_likes l \
                 ON (r.recipe_id = l.recipe_id) \
                 WHERE r.recipe_status = 'published' \
                 GROUP BY r.recipe_id \
                 ORDER BY COUNT(l.recipe_id) DESC;"
    cur.execute(sql_query)

    sql_result = cur.fetchall()

    # If empty results, then return empty body
    if not sql_result:
        cur.close()
        conn.close()

        return {
            'status_code': 200,
            'body': {}
        }

    # For each recipe_id, add recipe details to body content
    body_content = []
    
    for recipe in sql_result:
        r_id = recipe[0]
        r_details = recipe_details(r_id, None)

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
