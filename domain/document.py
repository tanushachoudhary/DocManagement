class Document:
    """
    Represents a single document in the system.
    Encapsulates document details like ID, title, content, and the owner's ID.
    """
    def __init__(self, doc_id: str, title: str, content: str, owner_id: str):
        # Initialize private attributes using underscores (encapsulation)
        self._doc_id = doc_id        # Unique identifier for the document
        self._title = title          # Title of the document
        self._content = content      # The actual text content of the document
        self._owner_id = owner_id    # The ID of the User who owns this document

    def get_id(self) -> str:
        """Returns the document's unique ID."""
        return self._doc_id

    def get_title(self) -> str:
        """Returns the document's title."""
        return self._title

    def get_owner(self) -> str:
        """Returns the ID of the document's owner."""
        return self._owner_id

    def read(self) -> str:
        """Returns the content of the document."""
        return self._content

    def update_content(self, new_content: str) -> None:
        """
        Updates the document's content.
        This is a setter method that modifies the private _content attribute.
        """
        self._content = new_content