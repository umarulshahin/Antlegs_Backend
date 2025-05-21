from django.db import models
from DB_connection import db
# Create your models here.
from pymongo import errors

User_collection = db["CustomUser"]

try: 
    
    User_collection.create_index([("email", 1)], unique=True)

except errors.operationFailure as e:
    print(f"Error creating index: {e}")
    
    
class UserInstance:
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.username = user_data.get("username")
        self.email = user_data.get("email")