import couchdb
import json

#import os
# Obtener la URL de CouchDB del entorno
#COUCHDB_URL = os.getenv('COUCHDB_URL', 'http://admin:admin@localhost:5984')



class CouchDBManager:
    def __init__(self, connection_url: str):
        self.connection_url = connection_url
        try:
            self.server = couchdb.Server(self.connection_url)
        except Exception as e:
            raise RuntimeError(f"Error al conectar con CouchDB: {e}")



    def get_db(self, db_name: str):
        try:
            if db_name in self.server:
                return self.server[db_name]
            else:
                db = self.server.create(db_name)
                print(f"Base de datos '{db_name}' creada.")
                return db
        except Exception as e:
            raise RuntimeError(f"Error al obtener/crear la base de datos '{db_name}': {e}")



    def get_existing_collections(self):
        try:
            db_names = list(self.server)
            print(f"Bases de datos existentes: {db_names}")
            return db_names
        except Exception as e:
            raise RuntimeError(f"Error al obtener las bases de datos existentes: {e}")



    def delete_collection(self, db_name: str):
        try:
            if db_name in self.server:
                del self.server[db_name]
                print(f"Base de datos '{db_name}' eliminada.")
            else:
                print(f"La base de datos '{db_name}' no existe.")
        except Exception as e:
            raise RuntimeError(f"Error al eliminar la base de datos '{db_name}': {e}")



    def delete_all_collections(self, exclude_system_dbs=True):
        try:
            system_dbs = ["_replicator", "_users"] if exclude_system_dbs else []
            db_names = self.get_existing_collections()

            for db_name in db_names:
                if db_name not in system_dbs:
                    self.delete_collection(db_name)

            print(f"Se eliminaron todas las bases de datos, excepto: {system_dbs}")
        except Exception as e:
            raise RuntimeError(f"Error al eliminar todas las bases de datos: {e}")


'''
/*


import couchdb
import os
import json

# Obtener la URL de CouchDB del entorno
COUCHDB_URL = os.getenv('COUCHDB_URL', 'http://admin:admin@localhost:5984')

def setup_db(collection_name: str):
    try:
        # Conectarse al servidor CouchDB
        couch = couchdb.Server(COUCHDB_URL)
        
        # Acceder a la db del parametro
        try:
            db = couch[collection_name]
        except couchdb.http.ResourceNotFound:
            # Si no existe, crearla
            db = couch.create(collection_name)
            print(f"Base de datos '{collection_name}' creada.")
        
        return db
    
    except couchdb.http.ServerError as e:
        print(f"Error de conexión con CouchDB: {e}")
        raise

    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")
        raise

#-----------------------------------------------------------------------------------#

def get_existing_collections():
    try:
        # Conectarse al servidor CouchDB
        couch = couchdb.Server(COUCHDB_URL)
        
        response = couch.resource.get('_all_dbs')
        response_body = response[2].read().decode('utf-8')
        db_names = json.loads(response_body)
        print(db_names)

        return db_names
    
    except couchdb.http.ServerError as e:
        print(f"Error al conectar con CouchDB: {e}")
        return []

    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")
        return []
    


def delete_single_collection(collection_name: str):
    try:
        # Conectarse al servidor CouchDB
        couch = couchdb.Server(COUCHDB_URL)
        
        # Obtener todas las bases de datos existentes
        db_names = get_existing_collections()

        if collection_name in db_names:
            try:
                couch.delete(collection_name)
                print(f"Base de datos '{collection_name}' eliminada.")
            except couchdb.http.ResourceNotFound:
                print(f"La base de datos '{collection_name}' no se pudo encontrar para eliminar.")
        else:
            print(f"La base de datos '{collection_name}' no existe.")

    except couchdb.http.ServerError as e:
        print(f"Error al conectar con CouchDB: {e}")

    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")


def delete_all_collections():
    try:
        # Conectarse al servidor CouchDB
        couch = couchdb.Server(COUCHDB_URL)
        
        # Obtener todas las bases de datos existentes
        db_names = get_existing_collections()

        for db_name in db_names:
            if db_name not in ["_replicator", "_users"]:  # No borrar bases de datos del sistema
                try:
                    couch.delete(db_name)
                    print(f"Base de datos '{db_name}' eliminada.")
                except couchdb.http.ResourceNotFound:
                    print(f"La base de datos '{db_name}' no se pudo encontrar para eliminar.")
    
    except couchdb.http.ServerError as e:
        print(f"Error al conectar con CouchDB: {e}")
    
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")

        



*/
'''