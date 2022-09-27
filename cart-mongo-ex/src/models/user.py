

async def create_user(users_collection, user):
    try:
        user = await users_collection.insert_one(user)

        if user.inserted_id:
            user = await get_user_by_id(users_collection, user.inserted_id)
            return user

    except Exception as e:
        print(f'create_user.error: {e}')

async def get_user_by_id(users_collection, _id):
    try:
        user = await users_collection.find_one({'_id': _id})
        return user
    
    except Exception as e:
        print(f'get_user.error: {e}')

async def get_users(users_collection, skip, limit):
    try:
        user_cursor = users_collection.find().skip(int(skip)).limit(int(limit))
        users = await user_cursor.to_list(length=int(limit))
        return users

    except Exception as e:
        print(f'get_users.error: {e}')

async def update_user(users_collection, _id, user_data):
    try:
        data = {k: v for k, v in user_data.items() if v is not None}

        user = await users_collection.update_one(
            {'_id': _id},
            {'$set': data}
        )

        if user.modified_count:
            return True, user.modified_count

        return False, 0
    except Exception as e:
        print(f'update_user.error: {e}')

async def delete_user(users_collection, _id):
    try:
        user = await users_collection.delete_one(
            {'_id': _id}
        )
        if user.deleted_count:
            return {'status': 'User deleted'}
    except Exception as e:
        print(f'delete_user.error: {e}')
