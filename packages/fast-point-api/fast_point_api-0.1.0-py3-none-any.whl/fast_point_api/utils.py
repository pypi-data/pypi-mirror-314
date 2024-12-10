from fastapi import HTTPException
import re

# Validar que el nombre de la coleccion
def validate_collection_name(collection_name: str):
    if not collection_name or collection_name.strip() == "":
        raise HTTPException(status_code=400, detail="El nombre de la colección no puede estar vacío o contener solo espacios.")

    pattern = r'^[a-z0-9_-]+$'
    if not re.match(pattern, collection_name):
        raise HTTPException(status_code=400, detail=(
        "El nombre de la colección no es válido. "
        "Se encontraron caracteres no permitidos. "
        "El nombre solo puede contener los siguientes caracteres: "
        "letras minúsculas (a-z), números (0-9), guiones (-) y guiones bajos (_). "
        "Por ejemplo, un nombre válido sería 'mi_coleccion-123'."
    )
)

