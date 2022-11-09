import backend_helper 

def fetch_message(message_id):
    # Database connection
    try:
        conn = backend_helper.connect()
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    try:
        query = ("""SELECT * FROM messages WHERE message_id = %s""")
        cur.execute(query, (str(message_id),))
        out = cur.fetchone()
        cur.close()
        conn.close()
        return {
            'status_code': 200,
            'body': {
                'message_id': out[0],
                                
            }
        }
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': 'Failed to fetch message'
        }
    
def message_send(target_id, content, token):
    """send message to room or user

    Args:
        room_id (int): id of room to send message to
        content (string): message content to send to
        token (JWT): token for authentication

    Returns:
        if error:
            return {
                'status_code': int,
                'error': string,
            }
        if success:
            return {
                'status_code': int,
                'body': None,
            }
    """
    
    # Token validation
    if not token:
        return {
            'status_code': 401,
            'error': "No token"
        }
    
    user_id = backend_helper.verify_token(token)
    if not user_id:
        return {
            'status_code': 401,
            'error': "Invalid token"
        }
    
    
    # Database connection
    try:
        conn = backend_helper.connect()
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
        
    # Send message to room
    try:
        room = backend_helper.fetch_all_with_condition("message_room", "room_id", target_id)
        if room == []:
            return {
                'status_code': 400,
                'error': 'Cannot find room'
            }
        query = ("INSERT INTO messages(message_content, room_id, sender_id) VALUES (%s, %s, %s)")
        cur.execute(query, (content, target_id, user_id))
        conn.commit()
        cur.close()
        conn.close()
        return {
            'status_code': 200,
            'body': {},
        }    
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': 'Cannot send message'
        }

def message_edit(message_id, message_content, token):
    """Edit an existing message if it is the owner

    Args:
        message_id (int): id of message to edit
        message_content (str): content to update message with
        token (JWT): used for authentication

    Returns:
        if error:
            return {
                'status_code': int,
                'error': string,
            }
        if success:
            return {
                'status_code': int,
                'body': None,
            }
    """
    # Token validation
    if not token:
        return {
            'status_code': 401,
            'error': "No token"
        }
    
    user_id = backend_helper.verify_token(token)
    if not user_id:
        return {
            'status_code': 401,
            'error': "Invalid token"
        }
    
    
    # Database connection
    try:
        conn = backend_helper.connect()
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
        
    # Check if requestor is message sender
    message = backend_helper.fetch_all_with_condition("messages", "message_id", message_id)[0]
    if message['sender_id'] != user_id:
        return{
            'status_code': 400,
            'error': 'Access denied'
        }
    
    # If sender want to edit message to empty, system will delete the message
    if message_content == "":
        message_delete(message_id, user_id, token)
    
    try:
        query = ("UPDATE messages SET message_content = %s, is_edited = TRUE WHERE message_id = %s")
        cur.execute(query, (message_content, message_id,))
        conn.commit()
        cur.close()
        conn.close()
        return {
            'status_code': 200,
            'body': {},
        }    
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': 'Fail to edit message'
        }
    
def message_delete(message_id, token):
    """Delete message by changing message to be "this message has been deleted"

    Args:
        message_id (int): id of message to be deleted
        token (JWT): for authentication

    Returns:
        if error:
            return {
                'status_code': int,
                'error': string,
            }
        if success:
            return {
                'status_code': int,
                'body': None,
            }
    """
    # Token validation
    if not token:
        return {
            'status_code': 401,
            'error': "No token"
        }
    
    user_id = backend_helper.verify_token(token)
    if not user_id:
        return {
            'status_code': 401,
            'error': "Invalid token"
        }
    
    
    # Database connection
    try:
        conn = backend_helper.connect()
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }
        
    # Check if requestor is message sender
    message = backend_helper.fetch_all_with_condition("messages", "message_id", message_id)[0]
    if message['sender_id'] != user_id:
        return{
            'status_code': 400,
            'error': 'Access denied'
        }
    
    # Delete message by updating message content to "This message has been deleted"
    try:
        delete_message = "This message has been deleted"
        query = ("UPDATE messages SET message_content = %s, is_deleted = FALSE WHERE message_id = %s")
        cur.execute(query, (delete_message, message_id,))
        conn.commit()
        cur.close()
        conn.close()
        return {
            'status_code': 200,
            'body': {},
        }    
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': 'Fail to delete message'
        }

def message_react(message_id, react_char, token):
    """React to a message, message owner cannot react to their own message

    Args:
        message_id (int): id of message to react to
        react_char (char): reaction as an utf8 char
        token (JWT): for authentication
        
    Returns:
        if error:
            return {
                'status_code': int,
                'error': string,
            }
        if success:
            return {
                'status_code': int,
                'body': None,
            }
    """
    # Token validation
    if not token:
        return {
            'status_code': 401,
            'error': "No token"
        }
    
    user_id = backend_helper.verify_token(token)
    if not user_id:
        return {
            'status_code': 401,
            'error': "Invalid token"
        }
    
    conn = backend_helper.connect()
    cur = conn.cursor()
    
    # Fetch message
    try:
        query = ("SELECT sender_id FROM messages WHERE message_id = %s")
        cur.execute(query, (message_id,))
        owner_id = cur.fetchone()[0]
        # Check if person to react message is the owner of the message
        if owner_id == user_id:
            return{
                'status_code': 400,
                'error': 'Owner cannot react to their own message'
            }
    except:
        return{
            'status_code': 400,
            'error': 'Failed to fetch message'
        }
    
    try:
        query = ("SELECT message_id FROM message_emojis WHERE message_id = %s AND reactor_id = %s")
        cur.execute(query, (message_id, user_id))
        out = cur.fetchone()
        if out is None:
            query = ("INSERT INTO message_emojis(emoji_utf8, message_id, reactor_id) VALUES (%s, %s, %s) ")
        else:
            query = ("UPDATE message_emojis SET emoji_utf8 = %s WHERE message_id = %s AND reactor_id = %s")
        cur.execute(query, (react_char, message_id, user_id))
        cur.commit()
        conn.close()
        cur.close()
        return{
            'status_code': 200,
            'body': None,
        }
    except:
        return{
            'status_code': 400,
            'error': 'Failed to react to message'
        }