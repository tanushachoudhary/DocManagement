class User:
    """
    Represents a user in the system.
    Stores basic user information like ID and name.
    """
    def __init__(self, user_id: str, name: str):
        self._user_id = user_id  # Unique identifier for the user (private)
        self._name = name        # The user's name (private)
        
    def get_id(self) -> str:
        """Returns the user's unique ID."""
        return self._user_id   
    
    def get_name(self) -> str:
        """Returns the user's name."""
        return self._name