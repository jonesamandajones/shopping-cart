async def create_order(order_collection, order):
    try:
        order = await order_collection.insert_one(order)

        if order.inserted_id:
            order = await get_order(order_collection, order.inserted_id)
            return order

    except Exception as e:
        print(f'create_order.error: {e}')

async def get_order(orders_collection, user_id):
    try:
        data = await orders_collection.find_one({'_id': user_id})
        if data:
            return data
    except Exception as e:
        print(f'get_order.error: {e}')

async def get_orders(orders_collection, skip, limit):
    try:
        order_cursor = orders_collection.find().skip(int(skip)).limit(int(limit))
        orders = await order_cursor.to_list(length=int(limit))
        return orders

    except Exception as e:
        print(f'get_orders.error: {e}')

async def delete_order(order_items_collection, user_id):
    try:
        user = await order_items_collection.delete_one(
            {'_id': user_id}
        )
        if user.deleted_count:
            return {'status': 'User deleted'}
    except Exception as e:
        print(f'delete_user.error: {e}')

async def add_product(order_collection, user_id, product_data, price_order):
    try:
        product = await order_collection.update_one(
            {'_id': user_id},
            {
                '$push': {'products': product_data},
                '$set': {'price': price_order}
                }
        )

        if product.modified_count:
            return True, product.modified_count

        return False, 0
    except Exception as e:
        print(f'update_product.error: {e}')
        
