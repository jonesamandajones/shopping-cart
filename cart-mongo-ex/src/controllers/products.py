import pprint
from src.models.products import (
    create_product,
    get_product_by_id,
    update_product,
    delete_product,
    get_products
)
from src.server.database import connect_db, db, disconnect_db


async def products_crud():
    option = input(
        """ Entre com a opção de CRUD:
          
                   1. Criar produto
                   2. Buscar produto pelo seu identificador 
                   3. Atualizar produto
                   4. Deletar poduto
                   5. Visualizar todos os produtos \n"""
    )
    
    await connect_db()
    products_collection = db.products_collection
    
    if option == '1':
        # create product
        prod_id = int(input('Determine o código identificador do produto:  '))
        product =  {
            "_id": prod_id,
            'name': str(input('Nome do produto:\n   ')),
            'description': str(input('Descrição do produto:\n   ')),
            'price': float(input('Preço do produto:\n   ')),
            'image': str(input('Imagem do produto:\n   ')),
            }

        product_input = await create_product(
            products_collection,
            product
        )
        pprint.pprint(product_input)
        
    elif option == '2':
        # get product
        prod_id = int(input('Digite o identificador do produto:   '))
        product_input = await get_product_by_id(
            products_collection,
            prod_id
        )
        print(product_input)
    elif option == '3':
        # update
        prod_id = int(input('Digite o identificador (id) do produto:   '))
        product_input = await get_product_by_id(
            products_collection,
            prod_id
        )
        mod_option = (
            input(f'''O produto escolhido foi: {product_input} \n
                    Para modificar o nome, digite 1
                    Para modificar a descrição, digite 2
                    Para modificar o preco, digite 3
                    Para modificar a imagem, digite 4 \n'''))
                        
        if mod_option == '1':
            user_data = {
            'name': str(input('Novo nome:   '))
        }            
        if mod_option == '2':
            user_data = {
            'description': str(input('Nova descrição:   '))
        }
        if mod_option == '3':
            user_data = {
            'price': int(input('Novo preço:   '))
        }
        if mod_option == '4':
            user_data = {
            'image': str(input('Nova imagem:   '))
        }
        
        is_updated, numbers_updated = await update_product(
            products_collection,
            product_input,
            user_data
        )
        
        if is_updated:
            print(f"Atualização realizada com sucesso, número de documentos alterados {numbers_updated}")
        else:
            print("Atualização falhou!")
            
    elif option == '4':
        # delete
        prod_id = int(input('Digite o identificador (id) do produto:   '))
        product_input = await get_product_by_id(
            products_collection,
            prod_id
        )
        
        result = await delete_product(
            products_collection,
            product_input
        )
        pprint.pprint(result)
        
    elif option == '5':
        # pagination
        products = await get_products(
            products_collection,
            skip=0,
            limit=5
        )
        pprint.pprint(products)

    await disconnect_db()
