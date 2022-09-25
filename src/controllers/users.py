from pymongo import ASCENDING
from src.models.user import (
    create_user,
    get_user_by_id,
    update_user,
    delete_user,
    get_users
)
from src.server.database import connect_db, db, disconnect_db

#######################################################################
################################ CRUD #################################
#######################################################################

async def users_crud():
    registration = input(
        """ Entre com a opção de CRUD:
          
                   1. Criar usuário
                   2. Buscar usuário pelo seu identificador (id)
                   3. Atualizar usuário
                   4. Deletar usuário
                   5. Visualizar todos os usuários \n"""
    )
    await connect_db()
    users_collection = db.users_collection

################################# Criar usuário ##################################

    if registration == '1':
        user_id = int(input('Determine o código identificador do usuário:  '))
        user = {
                '_id':  user_id,
                'name': str(input('Nome do usuário:\n   ')),
                'email': str(input('Email:\n   ')),
                'password': str(input('Senha de acesso:\n   ')),
                'is_active': True if str(input('Usuário ativo? [s/n]\n   ')) == 's' else False,
                'is_admin': True if str(input('Definir como adminstrador? [s/n]\n   ')) == 's' else False
        }
        user_input = await create_user(
            users_collection,
            user
        )
        print(user_input)

################################# Buscar usuário ##################################         
            
    elif registration == '2':
        user_id = int(input('Digite o código identificador do usuário:\n   '))
        user = await get_user_by_id(
            users_collection,
            user_id
        )
        print(user)

################################# Atualizar usuário ##################################        
        
    elif registration == '3':
        user_id = int(input('Digite o identificador (id) do usuário:   '))
        user = await get_user_by_id(
            users_collection,
            user_id
        )
        mod_registration = (
            input(f'''O usuário requerido foi: {user} \n
                    Para modificar seu nome, digite 1
                    Para modificar seu email, digite 2
                    Para modificar a senha, digite 3
                    Para definir como ativo ou intativo, digite 4 
                    Para definir como administrador, digite 5 \n'''))
                        
        if mod_registration == '1':
            user_data = {
                'nome': str(input('Novo nome:   '))
            }
            is_updated, numbers_updated = await update_user(
                users_collection,
                user_id,
                user_data
            )
            if is_updated:
                print(f"Atualização realizada com sucesso, número de documentos alterados {numbers_updated}")
            else:
                print("Atualização falhou!")         
        if mod_registration == '2':
            user_data = {
            'email': str(input('Novo email:   '))
        }
        if mod_registration == '3':
            user_data = {
            'password': str(input('Nova senha:   '))
        }
        if mod_registration == '4':
            user_data = {
            'is_active': True if str(input('Usuário ativo? [s/n]:   ')) == 's' else False
        }
        if mod_registration == '5':
            user_data = {
            'is_admin': True if str(input('Usuário é administrador? [s/n]:   ')) == 's' else False
        }                  
    
    ################################# Deletar usuário ##################################
      
    elif registration == '4':
        user_id = int(input('Digite o identificador (id) do usuário:   '))
        user = await get_user_by_id(
            users_collection,
            user_id
        )
        result = await delete_user(
            users_collection,
            user_id
        )
        print(result)

################################# Listar usuários ##################################        
        
    elif registration == '5':
        users = await get_users(
            users_collection,
            skip=0,
            limit=5
        )
        print(users)

    await disconnect_db()
