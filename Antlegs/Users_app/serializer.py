from rest_framework import serializers
import re
from Authentication.models import User_collection
from bson import ObjectId

class UserManagementSerializer(serializers.Serializer): 
    
    username = serializers.CharField(max_length=150,required=True)
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        
        if not attrs: 
            raise serializers.ValidationError("No data provided")
        
        base_pattern = r"^[A-Za-z][A-Za-z0-9_ ]{2,}$"
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
        if attrs.get('username') and not re.match(base_pattern, attrs['username']):
            raise serializers.ValidationError({"error":"Username must start with a letter, and must be at least 3 characters long."})
        
        elif attrs.get('email') and not re.match(email_pattern, attrs['email']):
            raise serializers.ValidationError("Email is not valid.")
        
        return attrs
    
    def update(self, instance, validated_data):
            
        User_collection.update_one({"_id": ObjectId(instance['_id'])}, {"$set":validated_data})
        return validated_data