from django.shortcuts import render
from rest_framework.decorators import APIView,permission_classes
from rest_framework.response import Response
from rest_framework import status
from Authentication.models import User_collection
from rest_framework.permissions import IsAuthenticated
from Authentication.serializer import UserSerializer
from bson import ObjectId
from .serializer import UserManagementSerializer

# Create your views here.

class UserManagement(APIView): 
    
    permission_classes = [IsAuthenticated]
    
    #....................... GET ALL USERS......................
    def get(self,request): 
        
        try: 
            users = User_collection.find()
            serializer = UserSerializer(users,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e: 
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # ...................... User Updation...................... #
    def patch(self,request): 
        
        data = request.data
        try: 
            
            id = data.get("_id")
            
            if not id: 
                return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User_collection.find_one({"_id": ObjectId(id)})
            
            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserManagementSerializer(user,data=data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
            
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # ...................... User Deletion ...................... #
    def delete(self,request): 
        
        id = request.data.get('id')
        try: 
            
            if not id: 
                return Response({"error": "ID is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User_collection.find_one({"_id": ObjectId(id)})
            if not user: 
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            result = User_collection.delete_one({"_id": ObjectId(id)})
            
            if result.deleted_count == 1:   
                return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to delete user."}, status=status.HTTP_404_NOT_FOUND)
                    
        except Exception as e: 
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)