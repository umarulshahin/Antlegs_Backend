from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from .models import User_collection
from datetime import datetime, timedelta
import jwt
from bson import ObjectId


    
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
# Create your views here.

#....................... User Registration ......................
@api_view(['POST'])
def Signup(request):
    
    data = request.data
    
    
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#....................... Custom Token Generation ......................

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer 
    

def generate_jwt_tokens(user_id):
    access_payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=5),
        "iat": datetime.utcnow()
    }
    refresh_payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow()
    }
    access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access": access_token, "refresh": refresh_token}

#....................... Custom  Refesh Token Generation ......................
@api_view(["POST"])
def custom_token_refresh(request):
    
    refresh_token = request.data.get("refresh")

    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")

        user = User_collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return Response({"detail": "Invalid user"}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate new tokens
        tokens = generate_jwt_tokens(user_id)
        return Response(tokens)
    
    except jwt.ExpiredSignatureError:
        return Response({"detail": "Refresh token expired"}, status=status.HTTP_403_FORBIDDEN)
    except jwt.InvalidTokenError:
        return Response({"detail": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)