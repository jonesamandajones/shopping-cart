import pprint

from src.models.user import (
    get_user_by_id
)

from src.models.address import (
    add_address,
    create_address_dict,
    get_address_by_id,
    update_address,
    delete_address,
    get_address_dict_by_id,
    get_address_dict
)
from src.server.database import connect_db, db, disconnect_db


async def address_crud():
    user_id = int(input('Informe o identificador do usuário:\n   '))
    
    await connect_db()
    users_collection = db.users_collection
    user = await get_user_by_id(users_collection, user_id)
    
    if not user:
        print('Usuário não encontrado. Favor cadastrar usuário.')    
        return
    
    option = input( 
        """Entre com a opção de CRUD:
          
                   1. Cadastrar endereço
                   2. Buscar endereços do usuário
                   3. Atualizar endereço
                   4. Deletar endereço
                   5. Visualizar todos os endereços \n"""
    )
    
    address_collection = db.address_collection
    
    if option == '1':
        # create address
        
        address_dict = await get_address_dict_by_id(address_collection, user_id)
        add_id = str(input('Informe um título para o endereço (ex.: casa):   '))        
        address = {
                '_id': add_id,
                'street': str(input('Logradouro:\n   ')),
                'cep': str(input('CEP:\n   ')),
                'district': str(input('Bairro:\n   ')),
                'city': str(input('Cidade:\n   ')),
                'state': str(input('Estado:\n   ')),
                'is_delivery': True if str(input('Definir como endereço para entrega? [s/n]\n   ')) == 's' else False
        }
        if not address_dict:
            add_dict = {
                '_id': user_id,
                'address': []
            }
            add_dict['address'].append(address)
            await create_address_dict(
                address_collection,
                add_dict
            )  
        else:
            await add_address(
                address_collection,
                user_id,
                address
            )
            
        
    elif option == '2':
        address = await get_address_by_id(
            address_collection,
            user_id
        )
        pprint.pprint(address)
        
    elif option == '3':
        # update
        add_id = str(input('Informe o título do endereço que deseja:   '))
        address_dict = await get_address_by_id(
            address_collection,
            user_id
        )
        print(address_dict)
        for i, add in enumerate(address_dict['address']):
            if add['_id'] == add_id:
                index = i
        
        mod_option = (
            input(f'''O endereço escolhido foi: {address_dict} \n
                    Para modificar a rua, digite 1
                    Para modificar o CEP, digite 2
                    Para modificar o bairro, digite 3
                    Para modificar a cidade, digite 4 
                    Para modificar o estado, digite 5
                    Para definir como endereço de entrega, digite 6 \n'''))
                        
        if mod_option == '1':
            user_data = {
            'street': str(input('Rua:   '))
        }            
        if mod_option == '2':
            user_data = {
            'cep': str(input('CEP:   '))
        }
        if mod_option == '3':
            user_data = {
            'district': int(input('Bairro:   '))
        }
        if mod_option == '4':
            user_data = {
            'city': str(input('Cidade:   '))
        }
        if mod_option == '5':
            user_data = {
            'state': str(input('Estado:   '))
        }
        if mod_option == '6':
            user_data = {
            'is_delivery': True if str(input('Endereço para entrega? [s/n]:   ')) == 's' else False
        }   
    
        is_updated, numbers_updated = await update_address(
            address_collection,
            user_id,
            index,
            user_data
        )
        
        if is_updated:
            print(f"Atualização realizada com sucesso, número de endereços alterados {numbers_updated}")
        else:
            print("Atualização falhou!")
            
    elif option == '4':
        # delete
        add_id = input('Digite o identificador do endereço que deseja:   ')
        address_dict = await get_address_by_id(
            address_collection,
            user_id
        )
        
        for i, add in enumerate(address_dict['address']):
            if add['_id'] == add_id:
                index = i
                address = add
        
        result = await delete_address(
            address_collection,
            user_id,
            index,
            address
        )
        print(result)
        
    elif option == '5':
        # pagination
        address_dict = await get_address_dict(
            address_collection,
            user_id
        )
        
        pprint.pprint(address_dict['address'])

    await disconnect_db()
