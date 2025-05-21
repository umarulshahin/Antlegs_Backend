from rest_framework import serializers
import re
from .models import User_collection
from django.utils import timezone
from django.contrib.auth.hashers import make_password,check_password
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.Serializer): 
    
    _id = serializers.CharField(read_only=True)
    username = serializers.CharField(max_length=150,required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, max_length=150, required=True)
    is_active = serializers.BooleanField(default=True)
    created_at = serializers.DateTimeField(default=timezone.now)
    
    def validate(self, attrs):
        
        if not attrs: 
            raise serializers.ValidationError("No data provided")
        
        base_pattern = r"^[A-Za-z][A-Za-z0-9_ ]{2,}$"
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        password_pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$'

        if not re.match(base_pattern, attrs['username']):
            raise serializers.ValidationError({"error":"Username must start with a letter, and must be at least 3 characters long."})
        
        elif not re.match(email_pattern, attrs['email']):
            raise serializers.ValidationError("Email is not valid.")
        
        elif User_collection.find_one({"email": attrs['email']}):
            raise serializers.ValidationError({"error":"Email already exists."})
        
        elif not re.match(password_pattern, attrs['password']):
            raise serializers.ValidationError({"error":"Password must be at least 8 characters long, contain at least one uppercase letter, one number, and one special character."})
        
        return attrs    
    def create(self, validated_data):
        
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['created_at'] = timezone.now()
        validated_data['is_active'] = True
        
        result = User_collection.insert_one(validated_data)
        validated_data['_id'] = str(result.inserted_id)
        return validated_data
    
    
    
class CustomTokenObtainPairSerializer(serializers.Serializer):
    
    username_field = 'email'
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True,required=True)
    
    def validate(self, attrs):
        
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email is None or password is None:
            raise serializers.ValidationError({"error":"Email and password are required."})
        
        user = User_collection.find_one({"email": email})
        if user is None: 
            raise serializers.ValidationError({"error":"User with this email does not exist."})
        
        if not check_password(password, user.get('password'),""): 
            raise serializers.ValidationError({"error":"Password is incorrect."})
        
        
        token = RefreshToken()
        token['user_id'] = str(user['_id'])
        token['username'] = user.get('username')
        
        return {
            'token' : {"refresh": str(token),
                      "access": str(token.access_token)},
            
            'userdata' : {
                'username' : user.get('username'),
                'id' : str(user['_id']),
            }
        }
        
            