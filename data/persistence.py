import json
import os
from domain.user import User
from domain.document import Document

# ---------------------------------------------------------
# 1. SETUP FILE PATHS
# ---------------------------------------------------------
# Calculate the absolute path to the project root directory.
# __file__ is the current file (persistence.py).
# dirname() goes up one level. We call it twice to go from:
# data/persistence.py -> data/ -> ProjectRoot/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define the 'data' folder path (ProjectRoot/data)
DATA_DIR = os.path.join(BASE_DIR, "data")

# Define the specific file paths for users and documents
USERS_FILE = os.path.join(DATA_DIR, "users.json")
DOCS_FILE = os.path.join(DATA_DIR, "documents.json")

# Create the data directory if it doesn't exist yet (prevents errors on first run)
os.makedirs(DATA_DIR, exist_ok=True)


# ---------------------------------------------------------
# 2. USER PERSISTENCE (Save/Load Users)
# ---------------------------------------------------------

def save_users(user_store):
    """
    Converts all User objects from the UserStore into a list of dictionaries
    and writes them to 'data/users.json'.
    """
    # specific format: [{"id": "1", "name": "Alice"}, ...]
    data = [
        {"id": u.get_id(), "name": u.get_name()}
        for u in user_store.list_users()
    ]
    
    # Write to file with indentation so it's readable by humans
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_users(user_store):
    """
    Reads 'data/users.json', converts the data back into User objects,
    and adds them to the UserStore.
    """
    try:
        with open(USERS_FILE, "r") as f:
            data = json.load(f)
        
        # Recreate User objects from the loaded data
        for item in data:
            user = User(item["id"], item["name"])
            user_store.add_user(user)
            
    except FileNotFoundError:
        # It's normal for the file to be missing on the very first run.
        # We just do nothing and start with an empty store.
        pass


# ---------------------------------------------------------
# 3. DOCUMENT PERSISTENCE (Save/Load Documents)
# ---------------------------------------------------------

def save_documents(document_store):
    """
    Converts all Document objects from the DocumentStore into a list of dictionaries
    and writes them to 'data/documents.json'.
    """
    data = []
    
    # Accessing the private dictionary _documents to get all items
    # (Note: Ideally, DocumentStore should have a 'get_all_documents()' method)
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
    Reads 'data/documents.json', converts the data back into Document objects,
    and adds them to the DocumentStore.
    """
    try:
        with open(DOCS_FILE, "r") as f:
            data = json.load(f)
            
        # Recreate Document objects from the loaded data
        for item in data:
            doc = Document(
                doc_id=item["id"],
                title=item["title"],
                content=item["content"],
                owner_id=item["owner"]
            )
            document_store.add_document(doc)
            
    except FileNotFoundError:
        # Ignore if file doesn't exist (first run)
        pass