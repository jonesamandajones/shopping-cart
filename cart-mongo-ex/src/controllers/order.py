import datetime
import pprint 
from pydantic import BaseModel, Field

from src.models.user import (
    get_user_by_id
)
from src.models.order import (
    create_order,
    delete_order,
    get_order,
    add_product
)
from src.models.products import (
    get_product
)
from src.models.address import(
    get_address_dict
)

from src.server.database import connect_db, db, disconnect_db


async def order_crud():
    
    await connect_db()
    order_collection = db.order_collection
    user_collection = db.users_collection
    products_collection = db.products_collection
    address_collection = db.address_collection
    
    option = input('''Entre com a opção de CRUD:
                   1. Criar carrinho de compra
                   2. Adicionar produto ao carrinho
                   3. Visualizar carrinho
                   4. Deletar carrinho\n
                   ''')
    user_id = int(input('Digite o código identificador do usuário:\n   '))
    user = await get_user_by_id(
        user_collection,
        user_id
    )
    if not user:
        print('Usuário não encontrado. Favor cadastrar usuário.')    
        return
    
    if option == '1':

        address_dict = await get_address_dict(
            address_collection, user_id
        )
        
        for i in address_dict:
            address_user = i['is_delivery']
            if address_user == True:
                add_delivery = address_user
         
        order = {
            '_id': user_id,
            'user': user,
            'price': 00.00,
            'paid': (True if str(input('Pagamento efetuado? [s/n]:\n   ')) == 's' else False),
            'products': [],
            'create': str(Field(default=datetime.datetime.now())),
            'address': add_delivery
        }
        
        order_input = await create_order(
            order_collection,
            order
        )
        
        return pprint.pprint(order_input)


    if option == '2':    
        product_id = int(input('Informe o identificador do produto:\n   '))
        product = await get_product(
            products_collection,
            product_id
        )
        
        order = await get_order(
            order_collection, 
            user_id
        )
        
        total_price = order['price'] 
        for i in order['products']: 
            price = i['price']
            total_price += price
                                    
        status, _ = await add_product(
            order_collection,
            user_id,
            product,
            total_price
        )
        
                        
        if status == True:
            print('Produto adicionado ao carrinho!')
        else:
            print('Produto não adicionado.')
        
    if option == '3':
        order = await get_order(
            order_collection, 
            user_id
        )
        pprint.pprint(order)
        

    if option == '4':
        await delete_order(
            order_collection, 
            user_id
        )
        print('Deletado com sucesso.')
    
    await disconnect_db()