import psycopg2
from backend_helper import verify_token
from config import DB_CONN_STRING

def notification_send(reciever_id, content, sender_id, sender_name):
    """Send a notification from an authorised user
    Note: this function is for internal use only.
    
    Args:
        reciever_id     (Integer): id of user to notify
        content         (String): notification content
        sender_id       (Integer): id of sender
        sender_name     (Integer): name of sender
        
    Returns:
        Status 201 - notification sent successfully
        Status 400 - failure to send notification
        Status 500 - server error (failure to connect to database)
    """
    # Start connection to database
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
        cur = conn.cursor()
    except:
        return {
            'status_code': 500,
            'error': 'Unable to connect to database'
        }

    # Add new notification
    try:
        query = ("""
            INSERT INTO notifications
            (reciever_id, notification_content, sender_id, sender_name)
            VALUES (%s, %s, %s, %s)
            RETURNING notification_id
            """)
        cur.execute(query, (reciever_id, content, sender_id, sender_name))
        conn.commit()
        notification_id, = cur.fetchone()
        # Close connection
        cur.close()
        conn.close()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "failed to send notification"
        }
    return {
        'status_code': 201,
        'body': {
            'notification_id': notification_id
        }
    }


def notification_auth_send(reciever_id, content, token):
    """Send a notification from an authorised user to designated user
    
    Args:
        reciever_id     (Integer): id of user to notify
        content         (String): notification content
        token           (String): token of authenticated user
        
    Returns:
        Status 201 - recipe created successfully, returning body (dict)
                     containing recipe_id (Integer)
        Status 400 - failure to create recipe
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
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
        query = ("SELECT id, display_name FROM users WHERE token = %s")
        cur.execute(query, (str(token),))
        sender_id, sender_name = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find user id"
        }
    
    return notification_send(reciever_id, content, sender_id, sender_name)


def notification_send_unauth(reciever_id, content, sender_name):
    """Send a notification from a user identified by sender_name to designated
    user. Note: this function should not be associated with a URL path as it
    leaves the user vulnerable to getting notifications from anonymous users.
    It should only be used for trusted services that don't have a user id.
    E.g. system services or error notifications.
    
    Args:
        reciever_id     (Integer): id of user to notify
        content         (String): notification content
        sender_name     (Integer): name of sender or service
        
    Returns:
        Status 201 - notification sent successfully
        Status 400 - failure to send notification
        Status 500 - server error (failure to connect to database)
    """
    sender_name_modified = sender_name if sender_name else 'anon'
    return notification_send(reciever_id, content, -1, sender_name_modified)


def notifications_fetch_all(token):
    """Fetch all notifications for user identified by token
    
    Args:
        token           (String): token of authenticated user
        
    Returns:
        Status 200 - successful return of notifications for user
                notifications (list of dict)
                        notification_id         (Integer)
                        notification_content    (String)
                        sender_id               (Integer): (-1 if invalid user)
                        sender_name             (String)
                        time_sent               (String)

        Status 400 - failure to fetch notifications
        Status 401 - invalid or no token
        Status 500 - server error (failure to connect to database)
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
        query = ("SELECT id FROM users WHERE token = %s")
        cur.execute(query, (str(token),))
        reciever_id, = cur.fetchone()
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find user id"
        }
    try:
        query = ("""
            SELECT notification_id, notification_content, sender_id,
            sender_name, time_sent
            FROM notifications
            WHERE reciever_id = %s
        """)
        cur.execute(query, (reciever_id,))
        results = cur.fetchall()
        notifications_list = []
        for one_notification in results:
            notifications_list.append({
                'notification_id': one_notification[0],
                'notification_content': one_notification[1],
                'sender_id': one_notification[2],
                'sender_name': one_notification[3],
                'time_sent': str(one_notification[4])
            })
        
    except:
        # Close connection
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': "cannot find notifications"
        }

    return {
        'status_code': 200,
        'notifications': notifications_list
    }
