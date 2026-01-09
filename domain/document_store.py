class DocumentStore:
    def __init__(self):
        self._documents = {}

    def add_document(self, document):
        self._documents[document.get_id()] = document

    def get_document(self, doc_id):
        if doc_id not in self._documents:
            raise KeyError("Document not found")
        return self._documents[doc_id]

    def update_document(self, doc_id, new_content):
        document = self.get_document(doc_id)
        document.update_content(new_content)

    def remove_document(self, doc_id):
        if doc_id not in self._documents:
            raise KeyError("Document not found")
        del self._documents[doc_id]

    def get_documents_by_user(self, user_id):
        return [
            doc for doc in self._documents.values()
            if doc.get_owner() == user_id
        ]
