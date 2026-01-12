class UserStore:
    """
    Manages the collection of User objects.
    Acts as a simple in-memory database for users.
    """
    def __init__(self):
        # A dictionary to store users, mapping user_id -> User object
        self._users = {}

    def add_user(self, user):
        """
        Adds a new user to the store.
        Raises a ValueError if a user with the same ID already exists.
        """
        if user.get_id() in self._users:
            raise ValueError("User already exists.")
        self._users[user.get_id()] = user

    def get_user(self, user_id):
        """
        Retrieves a User object by their ID.
        Raises a KeyError if the user is not found.
        """
        if user_id not in self._users:
            raise KeyError("User not found.")
        return self._users[user_id]

    def user_exists(self, user_id):
        """Returns True if the user exists in the store, False otherwise."""
        return user_id in self._users

    def list_users(self):
        """Returns a list of all User objects currently in the store."""
        return list(self._users.values())

    def remove_user(self, user_id):
        """
        Removes a user from the store by their ID.
        Raises a KeyError if the user does not exist.
        """
        if user_id not in self._users:
            raise KeyError("User not found.")
        del self._users[user_id]