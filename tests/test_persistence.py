import json
from domain.user import User
from domain.document import Document
from domain.document_store import DocumentStore
from data.persistence import save_users, load_users, save_documents, load_documents

def test_user_persistence(tmp_path, monkeypatch):
    users_file = tmp_path / "users.json"

    monkeypatch.setattr(
        "data.persistence.USERS_FILE",
        str(users_file)
    )

    from domain.user_store import UserStore
    store = UserStore()
    store.add_user(User("u1", "Alice"))

    save_users(store)

    new_store = UserStore()
    load_users(new_store)

    assert len(new_store.list_users()) == 1
    assert new_store.get_user("u1").get_name() == "Alice"


def test_document_persistence(tmp_path, monkeypatch):
    docs_file = tmp_path / "documents.json"

    monkeypatch.setattr(
        "data.persistence.DOCS_FILE",
        str(docs_file)
    )

    store = DocumentStore()
    store.add_document(Document("d1", "Notes", "Hello", "u1"))

    save_documents(store)

    new_store = DocumentStore()
    load_documents(new_store)

    doc = new_store.get_document("d1")
    assert doc.read() == "Hello"
