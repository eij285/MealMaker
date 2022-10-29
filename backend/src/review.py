import psycopg2
from backend_helper import verify_token
from config import DB_CONN_STRING

def review_details(recipe_id, auth_user_id):
    """
    Returns the review details
    """
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        reviews_list = []
        query = ("""
            SELECT u.id, u.display_name, u.base64_image, u.visibility,
            r.review_id, r.rating, r.comment, r.reply, r.created_on
            FROM users u JOIN recipe_reviews r ON (u.id = r.user_id)
            WHERE r.recipe_id = %s
            """)
        cur.execute(query, (recipe_id,))
        sql_result = cur.fetchall()
        reviews_list = []
        votes_query = ("""
            SELECT COUNT(*) FROM recipe_reviews_votes
            WHERE review_id = %s AND is_upvote = %s
            """)
        user_vote = ("""
            SELECT is_upvote FROM recipe_reviews_votes
            WHERE review_id = %s AND user_id = %s
            """)
        for review in sql_result:
            user_id, display_name, user_image, user_visibility, review_id, \
                rating, comment, reply, created_on = review
            
            cur.execute(votes_query, (review_id, True))
            upvotes, = cur.fetchone()

            cur.execute(votes_query, (review_id, False))
            downvotes, = cur.fetchone()

            if auth_user_id:
                cur.execute(user_vote, (review_id, auth_user_id))
                vote_result = cur.fetchone()
                if vote_result is not None:
                    cur_user_vote, = vote_result
                else:
                    cur_user_vote = None
            else:
                cur_user_vote = None
            
            reviews_list.append({
                'user_id': user_id,
                'display_name': display_name,
                'user_image': user_image,
                'user_visibility': user_visibility,
                'review_id': review_id,
                'rating': rating,
                'comment': comment if comment else '',
                'reply': reply if reply else '',
                'created_on': str(created_on),
                'upvote_count': upvotes,
                'downvote_count': downvotes,
                'cur_user_vote': cur_user_vote if cur_user_vote is not None else ''
            })
            

        cur.close()
        conn.close()
    except:
        cur.close()
        conn.close()
        raise Exception
    return reviews_list

def reviews_all_for_recipe(recipe_id, token):
    """
    Get all public user reviews for recipe
    """
    if not recipe_id:
        return {
            'status_code': 400,
            'error': "Bad Request"
        }
    # Start connection to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
    try:
        if token:
            query = "SELECT id FROM users WHERE token = %s"
            cur.execute(query, (str(token),))
            user_id, = cur.fetchone()
        else:
            user_id = None
        query = ("""
            SELECT COUNT(*) FROM recipes r JOIN users u ON (u.id = r.owner_id)
            WHERE r.recipe_id = %s AND
            (u.id = %s OR r.recipe_status = 'published')
        """)
        cur.execute(query, (recipe_id, user_id if user_id else -1))
        recipe = cur.fetchone()
        if not recipe:
            raise Exception
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 404,
            'error': "recipe does not exist"
        }

    try:
        return {
            'status_code':200,
            'reviews': review_details(recipe_id, user_id)
        }

    except:
        return {
            'status_code': 400,
            'error': "failed to fetch reviews for recipe"
        }

def review_create(recipe_id, rating, comment, token):
    """
    Create a review for a recipe. Recipe can only be reviewed by authenticated
    however recipe author cannot review own recipe.
    """
    # error if no token
    if not token:
        return {
            'status_code': 401,
            'error': "No token"
        }
    
    if not verify_token(token):
        return {
            'status_code': 401,
            'error': "Invalid token"
        }
    
    # Start connection to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    try:
        query = "SELECT id FROM users WHERE token = %s"
        cur.execute(query, (str(token),))
        user_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "recipe review requires login"
        }

    try:
        query = "SELECT owner_id FROM recipes WHERE recipe_id = %s"
        cur.execute(query, (recipe_id, ))
        owner_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find recipe id"
        }

    if user_id == owner_id:
        return {
            'status_code':400,
            'error': "recipe author cannot review own recipe"
        }

    try:
        query = ("""
            SELECT COUNT(*) FROM recipe_reviews
            WHERE recipe_id = %s AND user_id = %s
            """)
        cur.execute(query, (recipe_id, user_id))
        if cur.fetchone()[0] > 0:
            raise Exception
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "you have already reviewed this recipe"
        }

    try:
        query = ("""
            INSERT INTO recipe_reviews(recipe_id, user_id, rating, comment)
            VALUES (%s, %s, %s, %s) RETURNING review_id
            """)
        cur.execute(query, (recipe_id, user_id, rating, comment))
        conn.commit()
        review_id, = cur.fetchone()
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 201,
            'body': {
                'review_id': review_id
            }
        }
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "failed to create review"
        }

def review_delete(review_id, token):
    """
    Delete a review for a recipe. Only reviewer can delete review, however
    recipe author can indirectly delete review by deleting recipe due to
    the relational structure of records.
    """
    # error if no token
    if not token:
        return {
            'status_code': 401,
            'error': "No token"
        }
    
    if not verify_token(token):
        return {
            'status_code': 401,
            'error': "Invalid token"
        }
    
    # Start connection to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    try:
        query = "SELECT id FROM users WHERE token = %s"
        cur.execute(query, (str(token),))
        user_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "recipe review deletion requires login"
        }

    try:
        query = "SELECT user_id FROM recipe_reviews WHERE review_id = %s"
        cur.execute(query, (review_id, ))
        reviewer_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find review id"
        }

    if user_id != reviewer_id:
        return {
            'status_code':400,
            'error': "only reviewer can delete own reviews"
        }

    try:
        query = "DELETE FROM recipe_reviews WHERE review_id = %s"
        cur.execute(query, (review_id,))
        conn.commit()
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 200,
            'body': {}
        }
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "failed to delete review"
        }

def verify_recipe_owner_for_reply(review_id, token, is_delete):
    """
    Recipe owner/author create/delete reply to review helper function. Note:
    if the reviewer deletes the review it also deletes the reply.
    """
    if not token:
        return {
            'status_code': 401,
            'error': "No token"
        }
    
    if not verify_token(token):
        return {
            'status_code': 401,
            'error': "Invalid token"
        }
    
    # Start connection to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    try:
        query = "SELECT id FROM users WHERE token = %s"
        cur.execute(query, (str(token),))
        user_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        cond_msg = 'delete reply' if is_delete else 'create reply'
        return {
            'status_code': 400,
            'error': f"recipe author must be authenticated to {cond_msg}"
        }

    try:
        query = "SELECT recipe_id FROM recipe_reviews WHERE review_id = %s"
        cur.execute(query, (review_id, ))
        recipe_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find review"
        }

    try:
        query = "SELECT owner_id FROM recipes WHERE recipe_id = %s"
        cur.execute(query, (recipe_id, ))
        owner_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find recipe id"
        }

    cur.close()
    conn.close()
    if user_id != owner_id:
        cond_msg = 'delete' if is_delete else 'create'
        return {
            'status_code':400,
            'error': f"only recipe author can {cond_msg} reply to reviews"
        }
    return True

def review_reply(review_id, reply, token):
    """
    Recipe owner/author reply to existing review. Note: if the reviewer deletes
    the review it also deletes the reply.
    """
    response = verify_recipe_owner_for_reply(review_id, token, False)
    if isinstance(response, dict):
        return response

    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        query = "UPDATE recipe_reviews SET reply = %s WHERE review_id = %s"
        cur.execute(query, (str(reply), review_id))
        conn.commit()
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 200,
            'body': {}
        }
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "failed to reply to review"
        }

def review_reply_delete(review_id, token):
    """
    Recipe owner/author delete reply to existing review.
    """
    response = verify_recipe_owner_for_reply(review_id, token, False)
    if isinstance(response, dict):
        return response
    
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
        query = ("""
            UPDATE recipe_reviews SET reply = NULL WHERE review_id = %s
            """)
        cur.execute(query, (review_id,))
        conn.commit()
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 200,
            'body': {}
        }
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "failed to delete reply to review"
        }

def review_vote(review_id, is_upvote, token):
    """
    Allow users (including recipe author) to upvote and downvote reviews (as
    helpful or unhelpful, respetively). Reviewer cannot upvote or downvote own
    reviews.
    """
    # error if no token
    if not token or not verify_token(token):
        return {
            'status_code': 401,
            'error': "upvoting or downvoting a review requires login"
        }
    
    # Start connection to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    try:
        query = "SELECT id FROM users WHERE token = %s"
        cur.execute(query, (str(token),))
        user_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "upvoting or downvoting a review requires login"
        }

    try:
        query = "SELECT user_id FROM recipe_reviews WHERE review_id = %s"
        cur.execute(query, (review_id, ))
        reviewer_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find review id"
        }

    # seems a bit egotistical to vote for own review
    if user_id == reviewer_id:
        return {
            'status_code':400,
            'error': "user cannot upvote or downvote own review"
        }

    try:
        query = ("""
            SELECT vote_id, is_upvote FROM recipe_reviews_votes
            WHERE review_id = %s AND user_id = %s
            """)
        cur.execute(query, (review_id, user_id))
        vote_result = cur.fetchone()
        if vote_result:
            vote_id, curr_is_upvote = vote_result
            # if same vote as previous user has chosen to remove vote
            if is_upvote == curr_is_upvote:
                query = "DELETE FROM recipe_reviews_votes WHERE vote_id = %s"
                cur.execute(query, (vote_id,))
                conn.commit()
            else:
                # if different vote to previous, update vote
                query = ("""
                    UPDATE recipe_reviews_votes SET is_upvote = %s
                    WHERE vote_id = %s
                    """)
                cur.execute(query, (is_upvote, vote_id))
                conn.commit()
        else:
            # user has not voted, or has removed vote
            query = ("""
                INSERT INTO recipe_reviews_votes(review_id, user_id, is_upvote)
                VALUES (%s, %s, %s)
                """)
            cur.execute(query, (review_id, user_id, is_upvote))
            conn.commit()

        votes_query = ("""
            SELECT COUNT(*) FROM recipe_reviews_votes
            WHERE review_id = %s AND is_upvote = %s
            """)
        user_vote_query = ("""
            SELECT is_upvote FROM recipe_reviews_votes
            WHERE review_id = %s AND user_id = %s
        """)
        cur.execute(votes_query, (review_id, True))
        upvote_count, = cur.fetchone()
        cur.execute(votes_query, (review_id, False))
        downvote_count, = cur.fetchone()
        cur.execute(user_vote_query, (review_id, user_id))
        cur_user_vote = cur.fetchone()
        return {
            'status_code': 200,
            'body': {
                'upvote_count': upvote_count,
                'downvote_count': downvote_count,
                'cur_user_vote': '' if cur_user_vote is None else cur_user_vote[0]
            }
        }
        
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "problem voting for review"
        }