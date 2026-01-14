# provides persistence functionality by saving and loading users and documents to/from JSON file
# allowing data to be stored and retrieved between application runs
import json
import os
from domain.user import User
from domain.document import Document

# sets up file paths for persisting users and documents data, and ensures the data directory # exists before the application tries to save files to it.

# Gets the root project directory by going up two levels from the current file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Constructs the path to the data folder within the project root.
DATA_DIR = os.path.join(BASE_DIR, "data")

# Constructs the full path to data/users.json.
USERS_FILE = os.path.join(DATA_DIR, "users.json")
# Constructs the full path to data/documents.json.
DOCS_FILE = os.path.join(DATA_DIR, "documents.json")

# Creates the data directory if it doesn't already exist. The exist_ok=True parameter 
# prevents errors if the directory already exists.
os.makedirs(DATA_DIR, exist_ok=True)


# serializes all users from the user store to JSON file, extracts each user's ID and name
# converts them to a list of dictionaries and writes them to users.json
def save_users(user_store):
    data = [
        {"id": u.get_id(), "name": u.get_name()}
        for u in user_store.list_users()
    ]
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# deserializes users from the users.json file and loads them into the user store
# reads the JSON file, creates User obj from the data and adds them to the store
# silently handles the case if the file doesn't exist
def load_users(user_store):
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
        for item in data:
            user_store.add_user(User(item["id"], item["name"]))
    except FileNotFoundError:
        pass

# serializes all docs from the document store to a JSON file
# extracts each doc's ID,title,content and owner, converts them to 
# a list of dictionaries and writes them to documents.json
def save_documents(document_store):
    data = []
    for doc in document_store._documents.values():
        data.append({
            "id": doc.get_id(),
            "title": doc.get_title(),
            "content": doc.read(),
            "owner": doc.get_owner()
        })
    with open(DOCS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# deserializes documents from the documents.json file and loads them into the document store
# reads the JSON file, creates Document obj from the data and adds them to the store
# silently handles the case if the file doesn't exist
def load_documents(document_store):
    try:
        with open(DOCS_FILE, "r") as f:
            data = json.load(f)
        for item in data:
            document_store.add_document(
                Document(
                    item["id"],
                    item["title"],
                    item["content"],
                    item["owner"]
                )
            )
    except FileNotFoundError:
        pass
