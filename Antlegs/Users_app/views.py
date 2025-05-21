from django.shortcuts import render
from rest_framework.decorators import APIView,permission_classes
from rest_framework.response import Response
from rest_framework import status
from Authentication.models import User_collection
from rest_framework.permissions import IsAuthenticated
from Authentication.serializer import UserSerializer
# Create your views here.

    

class UserManagement(APIView): 
    
    permission_classes = [IsAuthenticated]
    
    def get(self,request): 
        
        try: 
            users = User_collection.find()
            serializer = UserSerializer(users,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e: 
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        