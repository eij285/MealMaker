import backend_helper

def create_room(member_id_list, token):
    """create a new room and return the room id

    Args:
        owner_id (int): id of owner of the room
        member_id_list (list): a list of member id to add into room
        
    Returns:
        if error:
            return {
                'status_code': int,
                'error': string,
            }
        if success:
            return {
                'status_code': int,
                'body': {
                    'room_id': int
                },
            }
    """
    # token validation
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
    
    try:
        query = ("INSERT INTO message_rooms (room_name) VALUES ('Room1') RETURNING room_id")
        cur.execute(query)
        conn.commit()
        room_id = cur.fetchone()[0]
        add_owner_to_room(room_id, [user_id], token)['status_code']
        add_member_to_room(room_id, member_id_list, token)['status_code']
        cur.close()
        conn.close()
        return {
            'status_code': 200,
            'body': {
                'room_id': room_id
            }
        }
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': 'Fail to create room'
        }
    
def add_owner_to_room(room_id, owner_id_list, token):
    """add owners to room

    Args:
        room_id (int): id of room to add member into
        owner_id_list (list): a list of owner id to add into room
    
    Return:
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
    
    if len(owner_id_list) == 0:
        return {
            'status_code': 400,
            'error': 'No owner found',
        }
        
    conn = backend_helper.connect()
    cur = conn.cursor()
    
    # token validation
    if token is not None:
        user_id = backend_helper.verify_token(token)
        if not user_id:
            conn.close()
            cur.close()
            return {
                'status_code': 401,
                'error': "Invalid token"
            }
        try:
            query = ("SELECT owner_id FROM message_room_owners WHERE room_id = %s")
            cur.execute(query, (str(room_id)))
            list = cur.fetchall()
            owner_list = []
            for i in list:
                owner_list.append(i[0])
            if user_id not in owner_list and len(owner_list) != 0:
                conn.close()
                cur.close()
                return {
                    'status_code': 400,
                    'error': "Access denied"
                }
        except:
            pass
    
    # Check if owner already an owner of the room
    try:
        query = ("SELECT owner_id FROM message_room_owners WHERE room_id = %s")    
        cur.execute(query, (str(room_id),))
        out = cur.fetchall()
        existing_owner = []
        for elem in out:
            existing_owner.append(elem[0])
        new_owner = []
        for owner in owner_id_list:
            if owner not in existing_owner:
                new_owner.append(owner)
        if len(new_owner) == 0:            
            conn.close()
            cur.close()
            return {
                'status_code':400,
                'error': 'owner already in the group'
            }
    except:
        pass
        
    try:
        for owner in owner_id_list:
            query = ("INSERT INTO message_room_owners (room_id, owner_id) VALUES (%s, %s)")
            cur.execute(query, (room_id, owner))
            conn.commit()
        cur.close()
        conn.close()

        # check if owner a member of room
        query = ("SELECT member_id FROM message_room_members WHERE room_id = %s AND member_id = %s")
        cur.execute(query, (room_id, user_id))
        out = cur.fetchone()[0]
        print(out)
        return {
            'status_code': 200,
            'body': None,
        }
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': 'Failed to add member to room',
        }

    
    
def add_member_to_room(room_id, member_id_list, token):
    """add owners to room

    Args:
        room_id (int): id of room to add member into
        owner_id_list (list): a list of owner id to add into room
        
    Return:
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
    
    if len(member_id_list) == 0:
        return {
            'status_code': 400,
            'error': 'No member found',
        }
    
    conn = backend_helper.connect()
    cur = conn.cursor()
        
    # token validation
    if token is not None:
        user_id = backend_helper.verify_token(token)
        if not user_id:
            conn.close()
            cur.close()
            return {
                'status_code': 401,
                'error': "Invalid token"
            }
        try:
            query = ("SELECT owner_id FROM message_room_owners WHERE room_id = %s")
            cur.execute(query, (room_id,))
            list = cur.fetchall()
            owner_list = []
            for i in list:
                owner_list.append(i[0])
            if user_id not in owner_list and len(owner_list ) != 0:
                conn.close()
                cur.close()
                return {
                    'status_code': 400,
                    'error': "Access denied"
                }
        except:
            pass
    
    # Check if member already in the room
    try:
        query = ("SELECT member_id FROM message_room_members WHERE room_id = %s")    
        cur.execute(query, (room_id,))
        out = cur.fetchall()
        existing_member = []
        for elem in out:
            existing_member.append(elem[0])
        new_member = []
        for member in member_id_list:
            if member not in existing_member:
                new_member.append(member)
        if len(new_member) == 0 and len(member_id_list) != 0:
            return {
                'status_code':400,
                'error': 'members already in the group'
            }
    except:
        pass
    try:
        for member in member_id_list:
            query = ("INSERT INTO message_room_members (room_id, member_id) VALUES (%s, %s)")
            cur.execute(query, (room_id, member))
            conn.commit()
        cur.close()
        conn.close()
        return {
            'status_code': 200,
            'body': None,
        }
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': 'Failed to add member to room',
        }

def delete_room(token, room_id):
    """delete an existing message room

    Args:
        token (JWT): for authentication
        room_id (int): id of room to be deleted

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
    # token validation
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
    
    try:
        # check if user_id is owner of the room
        query = ("SELECT owner_id FROM message_room_owners WHERE room_id = %s")
        cur.execute(query, (room_id,))
        out = cur.fetchall()
        owner_id_list = []
        for elem in out:
            owner_id_list.append(elem[0])
        if user_id not in owner_id_list:
            cur.close()
            conn.close()
            return {
                'status_code': 400,
                'error': 'Access Denied'
            }
        
        # deleting room if user is an owner
        query = ("DELETE FROM message_rooms WHERE room_id = %s")
        cur.execute(query, (room_id,))
        conn.commit()
        cur.close()
        conn.close()
        return {
            'status_code': 200,
            'body': None
        }
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': 'Failed to delete room'
        }
    
    
def fetch_room_details(room_id, token):
    """fetch details of a specified room

    Args:
        room_id (int): room info to be fetched
        token (JWT): for authentication

    Returns:
        {
            'status_code': int,
            'body': {
                'all_messages': [
                        {
                            'message_id': int, 
                            'message_content': str, 
                            'is_edited': boolean, 
                            'is_deleted': boolean, 
                            'time_sent': DateTime, 
                            'sender_id': int,
                            'room_id': int,
                        },
                    ],
                'all_emojis': [
                  {
                      'emoji_char': CHAR,
                      'reactor_id': int,
                      'message_id': int
                  }  
                ],
                'all_members': [
                    {
                        'member_id': int,
                        'display_name': str
                    }
                ],
                'all_owners': [
                    {
                        'owner_id': int
                        'display_name': str
                    },
                ]
                }
            ]
        }
    """
    # token validation
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
    
    # Fetch all owner id
    query = ("""SELECT owner_id FROM message_room_owners WHERE room_id = %s""")
    cur.execute(query, (str(room_id),))
    all_owner_id = cur.fetchall()
    all_owner = []
    for e in all_owner_id:
        query = ("SELECT display_name FROM users WHERE id = %s")
        cur.execute(query, (e[0],))
        name = cur.fetchone()[0]
        all_owner.append({
            'owner_id': e[0],
            'display_name': name
        })

    # Fetch all member id
    query = ("""SELECT member_id FROM message_room_members WHERE room_id = %s""")
    cur.execute(query, (str(room_id),))
    all_member_id = cur.fetchall()
    all_member = []
    for e in all_member_id:
        query = ("SELECT display_name FROM users WHERE id = %s")
        cur.execute(query, (e[0],))
        name = cur.fetchone()[0]
        all_member.append({
            'member_id': e[0],
            'display_name': name
        })
    
    # Fetch all messages
    all_messages = backend_helper.fetch_all_with_condition("messages", "room_id", room_id)
    all_emojis = backend_helper.fetch_database("message_emojis")
    all_emoji_message_id = []
    for emoji in all_emojis:
        all_emoji_message_id.append(emoji['message_id'])
    output = {}
    output['all_members'] = all_member
    output['all_owners'] = all_owner
    output['all_messages'] = all_messages
    output['all_emojis'] = all_emojis
    return{
        'status_code': 200,
        'body': output
    }
    
def fetch_user_rooms(token):
    """fetch room where user is in

    Args:
        token (JWT): for authentication

    Returns:
        {
            'status_code': int,
            'body': [
                {
                    'is_owner': boolean,
                    'room_id': int
                },
            ]
        }
    """
    # token validation
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
    
    try:
        # fetch all room where user is owner
        query = ("SELECT room_id FROM message_room_owners WHERE owner_id = %s")
        cur.execute(query, (user_id,))
        out = cur.fetchall()
        room_list = []
        dic = {}
        for elem in out:
            dic['room_id'] = elem[0]
            dic['is_owner'] = True
            room_list.append(dic)
            dic = {}
        # fetch all room where user is member
        query = ("SELECT room_id FROM message_room_members WHERE member_id = %s")
        cur.execute(query, (user_id,))
        out = cur.fetchall()
        dic = {}
        for elem in out:
            dic['room_id'] = elem[0]
            dic['is_owner'] = False
            room_list.append(dic)
            dic = {}
        return {
            'status_code': 200,
            'body': room_list
        }
    except:
        cur.close()
        conn.close()
        return {
            'status_code': 400,
            'error': 'Failed to delete room'
        }
        
        
        
if __name__ == "__main__":
    backend_helper.database_reset()
    backend_helper.database_populate()
    # backend_helper.fetch_database("users")