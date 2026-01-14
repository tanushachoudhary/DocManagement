# This is a domain model class that represents a document with properties
# for identification, ownership, content and methods to access and
# modify the content

class Document: 
    #constructor that initializes a Document obj with an ID, title, content and owner ID
    #stores all values as private attributes
    def __init__ (self, doc_id:str, title:str, content:str, owner_id :str):
        self._doc_id = doc_id  # document's id (private)
        self._title = title    # document's title (private)
        self._content = content # document's content (private)
        self._owner_id  = owner_id  # document's owner id (private)

    #getter method that returns the document's ID
    def get_id(self) -> str:
        return self._doc_id

    #getter method that returns the document's title
    def get_title(self) -> str:
        return self._title

    #getter method that returns the document's owner ID
    def get_owner(self) -> str:
        return self._owner_id

    #returns the document's content/text
    def read(self) -> str:
        return self._content

    #updates the document's content with new text, modifies internal _content attribute
    def update_content(self, new_content: str) -> None:
        self._content = new_content

    
    