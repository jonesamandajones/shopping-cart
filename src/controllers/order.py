import datetime
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

from src.server.database import connect_db, db, disconnect_db


async def order_crud():
    
    await connect_db()
    order_collection = db.order_collection
    user_collection = db.users_collection
    products_collection = db.products_collection
    
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
        
        order = {
            '_id': user_id,
            'user': user,
            'price': 'R$00.00',
            'paid': (True if str(input('Pagamento efetuado? [s/n]:\n   ')) == 's' else False),
            'products': [],
            'create': str(Field(default=datetime.datetime.now())),
            'address': 'endereço de entrega'
        }
        order_input = await create_order(
            order_collection,
            order
        )
        return order_input

    if option == '2':    
        product_id = int(input('Informe o identificador do produto:\n   '))
        product = await get_product(
            products_collection,
            product_id
        )
               
        status, count = await add_product(
            order_collection,
            user_id,
            product
        )
        print(status, count)
        
        
    if option == '3':
        order = await get_order(
            order_collection, 
            user_id
        )
        print(order)
        

    if option == '4':
        await delete_order(
            order_collection, 
            user_id
        )
        print('Deletado com sucesso.')
    
    await disconnect_db()