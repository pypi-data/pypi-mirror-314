from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import CouchDBManager
from .endpoints import generar_endpoints_todos
from .schemas import BaseCollectionSchema
from typing import Optional, List, Dict, Type



def ensure_system_dbs(db_manager: CouchDBManager):
    system_dbs = ["_users"] # system_dbs = ["_users", "_replicator"]
    for db_name in system_dbs:
        db_manager.get_db(db_name)



def create_app(
    connection_url: str,
    collection_names: Optional[List[str]] = None,
    models_dict: Optional[Dict[str, Type[BaseCollectionSchema]]] = None,
    cors_origins: Optional[List[str]] = None
) -> FastAPI:

    app = FastAPI()

    # Configuracion de CORS
    cors_origins = cors_origins or ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    db_manager = CouchDBManager(connection_url)

    ensure_system_dbs(db_manager)

    generar_endpoints_todos(app, db_manager, collection_names, models_dict)

    return app

