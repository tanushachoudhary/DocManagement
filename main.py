from domain.user import User
from domain.document import Document
from domain.document_store import DocumentStore
from domain.user_store import UserStore
from data.persistence import (
    save_users, load_users,
    save_documents, load_documents
)

def main():
    """
    The main entry point of the CLI application.
    Initializes stores, loads data, and runs the interaction loop.
    """
    
    # 1. Initialize In-Memory Stores
    user_store = UserStore()
    document_store = DocumentStore()

    # 2. Load Persisted Data (if available)
    # This ensures previous sessions' data is restored on startup.
    load_users(user_store)
    load_documents(document_store)

    # 3. Main Interaction Loop
    while True:
        print("\n--- Document Management System ---")
        print("1. Add user")
        print("2. Delete user")
        print("3. Create document")
        print("4. Read document")
        print("5. Update document")
        print("6. Delete document")
        print("7. List users")
        print("8. Exit")

        choice = input("Choose: ").strip()

        # --- OPTION 1: Add User ---
        if choice == "1":
            uid = input("User ID: ")
            name = input("Name: ")
            try:
                # Attempt to create and store the user
                user_store.add_user(User(uid, name))
                # Persist changes immediately to disk
                save_users(user_store)
                print("User added.")
            except ValueError as e:
                # Handle duplicate IDs
                print(e)

        # --- OPTION 2: Delete User ---
        elif choice == "2":
            uid = input("User ID to delete: ")
            try:
                user_store.remove_user(uid)
                # Update the JSON file after deletion
                save_users(user_store)
                print("User deleted.")
            except KeyError as e:
                print(e)

        # --- OPTION 3: Create Document ---
        elif choice == "3":
            doc_id = input("Document ID: ")
            title = input("Title: ")
            content = input("Content: ")
            owner = input("Owner ID: ")

            # Validation: Ensure the owner actually exists
            if not user_store.user_exists(owner):
                print("Error: User does not exist. Cannot assign document.")
                continue

            document_store.add_document(
                Document(doc_id, title, content, owner)
            )
            save_documents(document_store)
            print("Document created.")

        # --- OPTION 4: Read Document ---
        elif choice == "4":
            doc_id = input("Document ID: ").strip()
            try:
                document = document_store.get_document(doc_id)
                print("\n--- Document Content ---")
                print(document.read())
                print("------------------------")
            except KeyError:
                print("Document not found.")

        # --- OPTION 5: Update Document ---
        elif choice == "5":
            doc_id = input("Document ID: ")
            content = input("New content: ")
            try:
                document_store.update_document(doc_id, content)
                save_documents(document_store)
                print("Document updated.")
            except KeyError:
                print("Document not found.")

        # --- OPTION 6: Delete Document ---
        elif choice == "6":
            doc_id = input("Document ID: ")
            try:
                document_store.remove_document(doc_id)
                save_documents(document_store)
                print("Document deleted.")
            except KeyError:
                print("Document not found.")

        # --- OPTION 7: List Users ---
        elif choice == "7":
            print("\n--- Registered Users ---")
            for u in user_store.list_users():
                print(f"ID: {u.get_id()} | Name: {u.get_name()}")

        # --- OPTION 8: Exit ---
        elif choice == "8":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()