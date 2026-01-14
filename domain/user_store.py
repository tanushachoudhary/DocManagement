# This is a repository/storage class similar to document store but for managing users 
# provides CRUD operations and user lookup functionaltiy
class UserStore:
    # initializes UserStore with an empty dictionary to store users
    def __init__(self):
        self._users = {}

    # adds a new user to the store
    def add_user(self, user):
        if user.get_id() in self._users:
            raise ValueError("User already exists.")
        self._users[user.get_id()] = user

    # retrieves a user by their ID
    def get_user(self, user_id):
        if user_id not in self._users:
            raise KeyError("User not found.")
        return self._users[user_id]

    # checks if a user with given ID exists
    def user_exists(self, user_id):
        return user_id in self._users

    # returns list of all users currently stored in the store
    def list_users(self):
        return list(self._users.values())
    
    # deletes a user from the store by their ID
    def remove_user(self, user_id):
        if user_id not in self._users:
            raise KeyError("User not found.")
        del self._users[user_id]
