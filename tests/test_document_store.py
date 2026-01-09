import pytest
from domain.document_store import DocumentStore
from domain.document import Document

def test_add_and_get_document():
    store = DocumentStore()
    doc = Document("d1", "Notes", "Content", "u1")

    store.add_document(doc)
    fetched = store.get_document("d1")

    assert fetched.read() == "Content"

def test_update_document():
    store = DocumentStore()
    doc = Document("d1", "Notes", "Old", "u1")
    store.add_document(doc)

    store.update_document("d1", "New")
    assert store.get_document("d1").read() == "New"

def test_remove_document():
    store = DocumentStore()
    doc = Document("d1", "Notes", "Content", "u1")
    store.add_document(doc)

    store.remove_document("d1")
    with pytest.raises(KeyError):
        store.get_document("d1")

def test_get_documents_by_user():
    store = DocumentStore()
    store.add_document(Document("d1", "A", "x", "u1"))
    store.add_document(Document("d2", "B", "y", "u2"))
    store.add_document(Document("d3", "C", "z", "u1"))

    docs = store.get_documents_by_user("u1")
    assert len(docs) == 2
