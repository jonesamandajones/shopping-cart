
async def get_address_record(addresss_collection, user_id):
    try:
        data = await addresss_collection.find_one({'_id': user_id})
        if data:
            return data
    except Exception as e:
        print(f'get_address.error: {e}')

async def create_address_record(address_collection, address):
    try:
        address = await address_collection.insert_one(address)

        if address.inserted_id:
            address = await get_address(address_collection, address.inserted_id)
            return address

    except Exception as e:
        print(f'create_address.error: {e}')

async def get_address(addresss_collection, address_id):
    try:
        data = await addresss_collection.find_one({'_id': address_id})
        if data:
            return data
    except Exception as e:
        print(f'get_address.error: {e}')

async def get_address_list(addresss_collection, skip, limit):
    try:
        address_cursor = addresss_collection.find().skip(int(skip)).limit(int(limit))
        addresss = await address_cursor.to_list(length=int(limit))
        return addresss

    except Exception as e:
        print(f'get_address.error: {e}')

async def get_address_record_by_id(address_collection, address_record_id):
    address = await address_collection.find_one({'_id': address_record_id})
    return address

async def get_address_by_id(address_collection, address_id):
    address = await address_collection.find_one({'_id': address_id})
    return address

async def add_address(address_collection, user_id, address_data):
    try:
        address = await address_collection.update_one(
            {'_id': user_id},
            {'$push': {f'address': address_data}}
        )

        if address.modified_count:
            return True, address.modified_count

        return False, 0
    except Exception as e:
        print(f'update_address.error: {e}')

async def update_address(address_collection, user_id, index, address_data):
    try:
        data = {k: v for k, v in address_data.items() if v is not None}

        address = await address_collection.update_one(
            {'_id': user_id},
            {'$set': {f'address.{index}.{list(data.keys())[0]}': data[list(data.keys())[0]]}}
        )

        if address.modified_count:
            return True, address.modified_count

        return False, 0
    except Exception as e:
        print(f'update_address.error: {e}')

async def delete_address(address_collection, user_id, index, address):
    try:
        address = await address_collection.update_one(
            {'_id': user_id},
            {'$pull': {'address': address}}
        )
        if address.modified_count:
            return {'status': 'address deleted'}
    except Exception as e:
        print(f'delete_product.error: {e}')

async def get_address_for_delivery(address_collection):
    address = await address_collection.find_one({'is_delivery': True})
    return address