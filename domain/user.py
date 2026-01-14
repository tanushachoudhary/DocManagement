#This is a simple domain model class that represents a user with 
# basic properties and accessor methods to retrieve them.

class User:
    
    # constructor that initializes a User obj with a User ID and name
    # stores both values as private attributes
    def __init__(self, user_id: str, name: str):
        self._user_id = user_id #user's id (private)
        self._name = name #user's name (private)
        
    # getter method that returns the user's ID
    def get_id(self) -> str:
        return self._user_id   
   
    # getter method that returns the user's name
    def get_name(self) -> str:
        return self._name