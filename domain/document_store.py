class DocumentStore:
    """
    Manages the collection of Document objects.
    Acts as a simple in-memory database for documents.
    """
    def __init__(self):
        # A dictionary to store documents, mapping doc_id -> Document object
        self._documents = {}

    def add_document(self, document):
        """Adds a document to the store."""
        # Note: In a real system, you might check if the ID exists first (like in UserStore)
        self._documents[document.get_id()] = document

    def get_document(self, doc_id):
        """
        Retrieves a Document object by its ID.
        Raises a KeyError if the document is not found.
        """
        if doc_id not in self._documents:
            raise KeyError("Document not found")
        return self._documents[doc_id]

    def update_document(self, doc_id, new_content):
        """
        Updates the content of a specific document.
        First retrieves the document, then calls its update_content method.
        """
        document = self.get_document(doc_id)
        document.update_content(new_content)

    def remove_document(self, doc_id):
        """
        Removes a document from the store.
        Raises a KeyError if the document does not exist.
        """
        if doc_id not in self._documents:
            raise KeyError("Document not found")
        del self._documents[doc_id]

    def get_documents_by_user(self, user_id):
        """
        Returns a list of all documents owned by a specific user.
        Iterates through all documents to find matches (linear search).
        """
        return [
            doc for doc in self._documents.values()
            if doc.get_owner() == user_id
        ]