from .users import users_crud
from .address import address_crud
from .products import products_crud
from .order import order_crud

from src.server.database import connect_db, db, disconnect_db


async def menu_crud():
    
    await connect_db()
    order_collection = db.order_collection
    user_collection = db.users_collection
            
    option =  input(f'''Seja bem-vinda(o)!!
                    
                    Informe a seguir a opção desejada:
                    1. CRUD Usuários
                    2. CRUD Endereços
                    3. CRUD Produtos
                    4. CRUD Carrinho
                    ''')
    
    if option == '1':
        await users_crud()
        
    if option == '2':
        await address_crud()
        
    if option == '3':
        await products_crud()
    
    if option == '4':
        await order_crud()
  
 
    await disconnect_db()
