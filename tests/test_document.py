from domain.document import Document

def test_create_document():
    doc = Document("d1", "Notes", "Hello", "u1")
    assert doc.get_id() == "d1"
    assert doc.get_title() == "Notes"
    assert doc.read() == "Hello"
    assert doc.get_owner() == "u1"

def test_update_document():
    doc = Document("d1", "Notes", "Old", "u1")
    doc.update_content("New")
    assert doc.read() == "New"
