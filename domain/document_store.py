# This is a repository/storage class that manages a collection of documents
# providing CRUD operations(Create, Read, Update, Delete) and the ability
# to query documents by owner

class DocumentStore:
    # constructor that initializes the DocumentStore with an empty dictionary(documents) to # store documents
    def __init__(self):
        self._documents = {}

    #adds a document to the store by storing it in the dictionary with doc's ID as the key
    def add_document(self, document):
        self._documents[document.get_id()] = document

    # retrieves a doc by its ID
    def get_document(self, doc_id):
        if doc_id not in self._documents:
            raise KeyError("Document not found")
        return self._documents[doc_id]

    # updates a doc's content by calling update_content() with new content
    def update_document(self, doc_id, new_content):
        document = self.get_document(doc_id)
        document.update_content(new_content)

    # deletes a document by its ID
    def remove_document(self, doc_id):
        if doc_id not in self._documents:
            raise KeyError("Document not found")
        del self._documents[doc_id]

    # returns list of all documents owned by specific user by filtering through all stored 
    # docs and matching their owner ID
    def get_documents_by_user(self, user_id):
        return [
            doc for doc in self._documents.values()
            if doc.get_owner() == user_id
        ]
