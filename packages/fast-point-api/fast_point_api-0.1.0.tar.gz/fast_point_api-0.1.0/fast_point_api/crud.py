from uuid import uuid4
from .schemas import BaseCollectionSchema
from .config import CouchDBManager
#import couchdb

# CRUD Genérico
def create_item(db_manager: CouchDBManager, collection_name: str, item: BaseCollectionSchema):
    db = db_manager.get_db(collection_name)
    item_data = item.dict()
    item_data['_id'] = str(uuid4())  # Generar un ID único
    item_data['estado'] = 1         # Por defecto, el documento está activo
    db.save(item_data)
    return item_data


#print("--------------------------------------------------------------------------------------------------------------------------------------------------------")

def get_items(db_manager: CouchDBManager, collection_name: str):
    db = db_manager.get_db(collection_name)
    items = []
    for doc in db.view('_all_docs', include_docs=True):
        if doc['doc'].get('estado') == 1:  # Filtrar solo documentos activos
            items.append(doc['doc'])
    return items


def get_item(db_manager: CouchDBManager, collection_name: str, item_id: str):
    db = db_manager.get_db(collection_name)
    try:
        item = db[item_id]
        if item.get('estado') == 1:  # Solo devolver si está activo
            return item
    except Exception:
        return None


def update_item(db_manager: CouchDBManager, collection_name: str, item_id: str, item_data: dict):
    db = db_manager.get_db(collection_name)
    try:
        item = db[item_id]
        for key, value in item_data.items():
            if key in item:  # Solo actualizar claves existentes
                item[key] = value
        db.save(item)
        return item
    except Exception:
        return None

def deactivate_item(db_manager: CouchDBManager, collection_name: str, item_id: str):
    db = db_manager.get_db(collection_name)
    try:
        item = db[item_id]
        item['estado'] = 0  # Cambiar estado a inactivo
        db.save(item)
        return item
    except Exception:
        return None
