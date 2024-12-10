from fastapi import HTTPException
from typing import Optional, List, Dict, Type
from .schemas import BaseCollectionSchema
from .crud import create_item, get_items, get_item, update_item, deactivate_item
from .utils import validate_collection_name
from .config import CouchDBManager



# Función generadora para todos los endpoints
def generar_endpoints_todos(app, db_manager: CouchDBManager, collection_names: Optional[List[str]] = None, models_dict: Optional[Dict[str, Type[BaseCollectionSchema]]] = None):
    if models_dict:
        collection_names = list(models_dict.keys())
    else:
        collection_names = collection_names or db_manager.get_existing_collections()

    models_dict = models_dict or {}

    for collection_name in collection_names:
        model = models_dict.get(collection_name, BaseCollectionSchema)
        generar_endpoints(app, db_manager, collection_name, model)



# Función generadora para endpoints genéricos
def generar_endpoints_genericos(app, db_manager: CouchDBManager, tag_name: str = "Todos"):

    # Rutas genéricas para cualquier colección
    @app.post("/generic/{collection_name}/", tags=[tag_name])
    async def create_new_item(collection_name: str, item: BaseCollectionSchema):
        validate_collection_name(collection_name)
        return create_item(db_manager, collection_name, item)

    @app.get("/generic/{collection_name}/", tags=[tag_name])
    async def get_all_items(collection_name: str):
        validate_collection_name(collection_name)
        return get_items(db_manager, collection_name)

    @app.get("/generic/{collection_name}/{item_id}", tags=[tag_name])
    async def get_single_item(collection_name: str, item_id: str):
        validate_collection_name(collection_name)
        item = get_item(db_manager, collection_name, item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return item

    @app.put("/generic/{collection_name}/{item_id}", tags=[tag_name])
    async def update_single_item(collection_name: str, item_id: str, item: BaseCollectionSchema):
        validate_collection_name(collection_name)
        updated_item = update_item(db_manager, collection_name, item_id, item.dict())
        if not updated_item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return updated_item

    @app.delete("/generic/{collection_name}/{item_id}", tags=[tag_name])
    async def deactivate_single_item(collection_name: str, item_id: str):
        validate_collection_name(collection_name)
        item = deactivate_item(db_manager, collection_name, item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return {"detail": f"{collection_name.capitalize()} desactivado correctamente"}



# Función generadora para endpoints específicos con modelo opcional
def generar_endpoints(app, db_manager: CouchDBManager, collection_name: str, model: Type[BaseCollectionSchema] = None, tag_name: str = None):

    if not collection_name:
        raise HTTPException(status_code=400, detail="El nombre de la colección es obligatorio.")

    tag_name = tag_name or collection_name.capitalize()
    
    model = model or BaseCollectionSchema

    @app.post(f"/{collection_name}/", tags=[tag_name])
    async def create_new_item(item: model):
        validate_collection_name(collection_name)
        return create_item(db_manager, collection_name, item)

    @app.get(f"/{collection_name}/", tags=[tag_name])
    async def get_all_items():
        validate_collection_name(collection_name)
        return get_items(db_manager, collection_name)

    @app.get(f"/{collection_name}/{{item_id}}", tags=[tag_name])
    async def get_single_item(item_id: str):
        validate_collection_name(collection_name)
        item = get_item(db_manager, collection_name, item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return item

    @app.put(f"/{collection_name}/{{item_id}}", tags=[tag_name])
    async def update_single_item(item_id: str, item: model):
        validate_collection_name(collection_name)
        updated_item = update_item(db_manager, collection_name, item_id, item.dict())
        if not updated_item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return updated_item

    @app.delete(f"/{collection_name}/{{item_id}}", tags=[tag_name])
    async def deactivate_single_item(item_id: str):
        validate_collection_name(collection_name)
        item = deactivate_item(db_manager, collection_name, item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return {"detail": f"{collection_name.capitalize()} desactivado correctamente"}





# FUNCION CREAR_BD_COUCHDB() ???
#docker run -d -p 5984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=admin couchdb

# uvicorn api_lugares.main:app --reload
# uvicorn fastapi-couchdb-component.main:app --reload









#-------------------------PROBANDO----------------------------------#

#generar_endpoints_genericos(app)


#generar_endpoints(app,"direcciones",LugarModel)
#generar_endpoints(app,"carros",LugarModel)
#generar_endpoints(app,"peliculas",LugarModel)
#generar_endpoints(app,"pelis",LugarModel,"Movies")


#generar_endpoints_todos(app, collection_names=["pizzas", "bebidas"])


#models_dicta = {"pizzas": PizzaModel, "bebidas": DrinkModel,}
#generar_endpoints_todos(app, models_dict=models_dicta)
#generar_endpoints(app,"pizzas",PizzaModel)
#generar_endpoints(app,"bebidas",DrinkModel)


#pizza_instance = PizzaModel(name="Margarita", description="Deliciosa pizza", ingredients="Tomate, queso", size="Mediana", price=12.99, is_vegetarian=True)
#print(pizza_instance)
#print(pizza_instance.dict())
#print(pizza_instance.__class__)


#generar_endpoints(app, "pizzas", PizzaModel)
#generar_endpoints(app, "bebidas", DrinkModel)



#delete_single_collection("pizzas")
#delete_all_collections()


#generar_endpoints_todos(app)


#collection_nameSs=["pizzas_wdd_s", "bebidAAas"]
#generar_endpoints_todos(app,collection_names=collection_nameSs)


#-----------------------------------------------------------#



'''
/*

from fastapi import FastAPI, HTTPException
from .config import delete_all_collections, delete_single_collection, get_existing_collections, setup_db
from .schemas import BaseCollectionSchema
from fastapi.middleware.cors import CORSMiddleware
from .crud import (
    create_item, get_items, get_item, update_item, deactivate_item
)
import re
from fastapi import HTTPException
from .utils import validate_collection_name

from .schemas import LugarModel, PizzaModel, DrinkModel


#CREARBD FUNCION() ??
#docker run -d -p 5984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=admin couchdb


app = FastAPI()
# uvicorn api_lugares.main:app --reload
# uvicorn fastapi-couchdb-component.main:app --reload


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración inicial (las coleecciones se crea una si no existe)
@app.on_event("startup")
async def setup():
    setup_db("_users")  # Crear cualquier colección aquí
    
    # Obtenemos las colecciones existentes desde la base de datos
    #existing_collections = ["lugares", "categorias", "direcciones"]  # Puedes obtener esto dinámicamente
    existing_collections = get_existing_collections()
'''
'''
    # Registrar dinámicamente los endpoints para cada colección
    for collection_name in existing_collections:
        app.add_api_route(f"/{collection_name}/", get_items_endpoint(collection_name), methods=["GET"], tags=[collection_name.capitalize()])
        app.add_api_route(f"/{collection_name}/", create_item_endpoint(collection_name), methods=["POST"], tags=[collection_name.capitalize()])
        app.add_api_route(f"/{collection_name}/{{item_id}}", get_item_endpoint(collection_name), methods=["GET"], tags=[collection_name.capitalize()])
        app.add_api_route(f"/{collection_name}/{{item_id}}", update_item_endpoint(collection_name), methods=["PUT"], tags=[collection_name.capitalize()])
        app.add_api_route(f"/{collection_name}/{{item_id}}", deactivate_item_endpoint(collection_name), methods=["DELETE"], tags=[collection_name.capitalize()])
        
'''
'''





from typing import Optional, List, Dict, Type
from fastapi import HTTPException
from .schemas import BaseCollectionSchema
from .crud import create_item, get_items, get_item, update_item, deactivate_item
from .utils import validate_collection_name


# Función generadora para todos los endpoints
def generar_endpoints_todos(app: FastAPI, collection_names: Optional[List[str]] = None, models_dict: Optional[Dict[str, Type[BaseCollectionSchema]]] = None):
    if models_dict:
        collection_names = list(models_dict.keys())
    else:
        collection_names = collection_names or get_existing_collections()

    models_dict = models_dict or {}

    for collection_name in collection_names:
        model = models_dict.get(collection_name, BaseCollectionSchema)

        generar_endpoints(app, collection_name, model)




# Función generadora para endpoints genéricos
def generar_endpoints_genericos(app, tag_name: str = "Todos"):
    
    # Rutas genéricas para cualquier colección
    @app.post("/generic/{collection_name}/", tags=[tag_name])
    async def create_new_item(collection_name: str, item: BaseCollectionSchema):
        validate_collection_name(collection_name)  # Validar el nombre de la colección
        return create_item(collection_name, item)

    @app.get("/generic/{collection_name}/", tags=[tag_name])
    async def get_all_items(collection_name: str):
        validate_collection_name(collection_name)  # Validar el nombre de la colección
        return get_items(collection_name)

    @app.get("/generic/{collection_name}/{item_id}", tags=[tag_name])
    async def get_single_item(collection_name: str, item_id: str):
        validate_collection_name(collection_name)  # Validar el nombre de la colección
        item = get_item(collection_name, item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return item

    @app.put("/generic/{collection_name}/{item_id}", tags=[tag_name])
    async def update_single_item(collection_name: str, item_id: str, item: BaseCollectionSchema):
        validate_collection_name(collection_name)  # Validar el nombre de la colección
        updated_item = update_item(collection_name, item_id, item.dict())
        if not updated_item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return updated_item

    @app.delete("/generic/{collection_name}/{item_id}", tags=[tag_name])
    async def deactivate_single_item(collection_name: str, item_id: str):
        validate_collection_name(collection_name)  # Validar el nombre de la colección
        item = deactivate_item(collection_name, item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return {"detail": f"{collection_name.capitalize()} desactivado correctamente"}






from fastapi import HTTPException
from typing import Type

# Función generadora para endpoints específicos con modelo opcional
#def generar_endpoints(app, collection_name: str, model: Type[BaseCollectionSchema] = None, tag_name: str = None):
#
def generar_endpoints(app, collection_name: str, model: Type[BaseCollectionSchema] = None, tag_name: str = None):

    if not collection_name:
        raise HTTPException(status_code=400, detail="El nombre de la colección es obligatorio.")

    tag_name = tag_name or collection_name.capitalize()

    model = model or BaseCollectionSchema

    @app.post(f"/{collection_name}/", tags=[tag_name])
    async def create_new_item(item: model):
        validate_collection_name(collection_name)  # Validar el nombre de la colección
        return create_item(collection_name, item)

    @app.get(f"/{collection_name}/", tags=[tag_name])
    async def get_all_items():
        validate_collection_name(collection_name)  # Validar el nombre de la colección
        return get_items(collection_name)

    @app.get(f"/{collection_name}/{{item_id}}", tags=[tag_name])
    async def get_single_item(item_id: str):
        validate_collection_name(collection_name)  # Validar el nombre de la colección
        item = get_item(collection_name, item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return item

    @app.put(f"/{collection_name}/{{item_id}}", tags=[tag_name])
    async def update_single_item(item_id: str, item: model):
        validate_collection_name(collection_name)  # Validar el nombre de la colección
        updated_item = update_item(collection_name, item_id, item.dict())
        if not updated_item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return updated_item

    @app.delete(f"/{collection_name}/{{item_id}}", tags=[tag_name])
    async def deactivate_single_item(item_id: str):
        validate_collection_name(collection_name)  # Validar el nombre de la colección
        item = deactivate_item(collection_name, item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return {"detail": f"{collection_name.capitalize()} desactivado correctamente"}






#-----------------------------------------------------------#


generar_endpoints_genericos(app)


#generar_endpoints(app,"direcciones",LugarModel)
#generar_endpoints(app,"carros",LugarModel)
#generar_endpoints(app,"peliculas",LugarModel)
#generar_endpoints(app,"pelis",LugarModel,"Movies")



#generar_endpoints_todos(app, collection_names=["pizzas", "bebidas"])


models_dicta = {"pizzas": PizzaModel, "bebidas": DrinkModel,}
#generar_endpoints_todos(app, models_dict=models_dicta)
#generar_endpoints(app,"pizzas",PizzaModel)
#generar_endpoints(app,"bebidas",DrinkModel)



#pizza_instance = PizzaModel(name="Margarita", description="Deliciosa pizza", ingredients="Tomate, queso", size="Mediana", price=12.99, is_vegetarian=True)
#print(pizza_instance)
#print(pizza_instance.dict())
#print(pizza_instance.__class__)

generar_endpoints(app, "pizzas", PizzaModel)
generar_endpoints(app, "bebidas", DrinkModel)






#delete_single_collection("pizzas")
#delete_all_collections()







#generar_endpoints_todos(app)


#collection_nameSs=["pizzas_wdd_s", "bebidAAas"]
#generar_endpoints_todos(app,collection_names=collection_nameSs)


#-----------------------------------------------------------#
















# Funciones auxiliares
def get_items_endpoint(collection_name: str):
    async def endpoint():
        return get_items(collection_name)
    return endpoint

def create_item_endpoint(collection_name: str):
    async def endpoint(item: BaseCollectionSchema):
        return create_item(collection_name, item)
    return endpoint

def get_item_endpoint(collection_name: str):
    async def endpoint(item_id: str):
        item = get_item(collection_name, item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return item
    return endpoint

def update_item_endpoint(collection_name: str):
    async def endpoint(item_id: str, item: BaseCollectionSchema):
        updated_item = update_item(collection_name, item_id, item.dict())
        if not updated_item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return updated_item
    return endpoint

def deactivate_item_endpoint(collection_name: str):
    async def endpoint(item_id: str):
        item = deactivate_item(collection_name, item_id)
        if not item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} no encontrado")
        return {"detail": f"{collection_name.capitalize()} desactivado correctamente"}
    return endpoint





*/
'''


