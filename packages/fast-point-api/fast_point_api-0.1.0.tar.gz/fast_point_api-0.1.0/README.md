# Fast Point API

Fast Point API is a framework for building APIs using FastAPI. It provides dynamic collection management and currently integrates with CouchDB. Future updates may include support for additional databases. This package is designed to simplify the creation of APIs for managing collections and CRUD operations.

---

## Features
- Automatically generates CRUD endpoints for collections.
- Manages collections in a CouchDB instance, with potential future updates to support other databases.
- Defines data structures using Pydantic schemas.

---

## Installation
Install the package via pip:
```bash
pip install fast-point-api
```

---

## Getting Started
Here's a quick example to set up your API:

### Example Code
```bash
from fast_point_api.app_factory import create_app
from fast_point_api.schemas import PizzaModel, DrinkModel

# Define custom models
class MyModel(PizzaModel):
    extra_field: str

# CouchDB connection URL
connection_url = "http://admin:admin@localhost:5984"

# Define collections and models
collections = {
    "pizzas": PizzaModel,
    "bebidas": DrinkModel,
}

# Create the FastAPI app
app = create_app(connection_url=connection_url, models_dict=collections)
```

Run your app:
```bash
uvicorn main:app --reload
```

Visit the interactive API docs at `http://127.0.0.1:8000/docs`.

---

## CouchDB Manager Example
The `CouchDBManager` class simplifies database management. Here's how to use it:

```bash
from fast_point_api.config import CouchDBManager

# Initialize CouchDBManager
manager = CouchDBManager(connection_url="http://admin:admin@localhost:5984")

# Get existing collections
collections = manager.get_existing_collections()
print(f"Existing collections: {collections}")

# Create or get a database
db = manager.get_db("example_db")

# Delete a specific collection
manager.delete_collection("example_db")

# Delete all collections (excluding system databases)
manager.delete_all_collections(exclude_system_dbs=True)
```

---

## CRUD Operations Example
This package includes generic CRUD operations that you can use directly:

```bash
from fast_point_api.schemas import PizzaModel
from fast_point_api.crud import create_item, get_items, update_item

# Example Pizza data
pizza = PizzaModel(
    name="Pepperoni",
    description="Classic Pepperoni Pizza",
    ingredients="Tomato, Cheese, Pepperoni",
    size="Large",
    price=15.99,
    is_vegetarian=False,
)

# Create a new item
new_item = create_item(manager, "pizzas", pizza)
print(f"Created item: {new_item}")

# Retrieve all items
items = get_items(manager, "pizzas")
print(f"Items: {items}")

# Update an item
updated_data = {"price": 12.99}
updated_item = update_item(manager, "pizzas", new_item["_id"], updated_data)
print(f"Updated item: {updated_item}")
```

---

## Configuration
### CouchDB Setup
Ensure you have CouchDB running. You can use Docker to start an instance:
```bash
docker run -d -p 5984:5984 -e COUCHDB_USER=admin -e COUCHDB_PASSWORD=admin couchdb
```

---

## API Endpoints
The package automatically generates CRUD endpoints for each collection. For example, for a collection named `pizzas`:
- `POST /pizzas/` - Create a new item.
- `GET /pizzas/` - Get all items.
- `GET /pizzas/{item_id}` - Get a single item by ID.
- `PUT /pizzas/{item_id}` - Update an item by ID.
- `DELETE /pizzas/{item_id}` - Deactivate an item by ID.

Additionally, generic endpoints are available at `/generic/{collection_name}/`.

---

## Dependencies
This package requires:
- **FastAPI**
- **CouchDB**
- **Uvicorn**
- **Pydantic**

Refer to `requirements.txt` for the full list of dependencies.

---

## License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## Contributing
Contributions are welcome! Feel free to fork the repository and submit pull requests.

---

## Contact
Author: **MaynerAC**  
Email: **mayneranahuacoaquira@gmail.com**  
GitHub: [maynerac](https://github.com/maynerac)
