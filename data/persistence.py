import json
import os
from domain.user import User
from domain.document import Document

# ---------------------------------------------------------
# CONSTANTS & SETUP
# ---------------------------------------------------------

# Determine the project's base directory to ensure file paths work
# regardless of where the script is run from.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Define the paths for our JSON storage files
USERS_FILE = os.path.join(DATA_DIR, "users.json")
DOCS_FILE = os.path.join(DATA_DIR, "documents.json")

# Ensure the 'data' directory exists; create it if it doesn't.
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------------------------------------
# USER PERSISTENCE FUNCTIONS
# ---------------------------------------------------------

def save_users(user_store):
    """
    Serializes all users from the UserStore and saves them to a JSON file.
    
    Args:
        user_store (UserStore): The object containing all current User instances.
    """
    # Convert User objects into a list of dictionaries (JSON-serializable format)
    data = [
        {"id": u.get_id(), "name": u.get_name()}
        for u in user_store.list_users()
    ]
    
    # Write the data to the file with indentation for readability
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_users(user_store):
    """
    Reads the users JSON file and repopulates the UserStore.
    
    Args:
        user_store (UserStore): The object where loaded Users will be added.
    """
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
        
        # Iterate through the loaded data and recreate User objects
        for item in data:
            user_store.add_user(User(item["id"], item["name"]))
            
    except FileNotFoundError:
        # If the file doesn't exist yet (first run), just ignore it.
        pass


# ---------------------------------------------------------
# DOCUMENT PERSISTENCE FUNCTIONS
# ---------------------------------------------------------

def save_documents(document_store):
    """
    Serializes all documents from the DocumentStore and saves them to a JSON file.
    
    Args:
        document_store (DocumentStore): The object containing all Document instances.
    """
    data = []
    # Access the private dictionary _documents directly (or use a getter if available)
    for doc in document_store._documents.values():
        data.append({
            "id": doc.get_id(),
            "title": doc.get_title(),
            "content": doc.read(),
            "owner": doc.get_owner()
        })
        
    with open(DOCS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_documents(document_store):
    """
    Reads the documents JSON file and repopulates the DocumentStore.
    
    Args:
        document_store (DocumentStore): The object where loaded Documents will be added.
    """
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
        # If the file doesn't exist yet, ignore it.
        pass