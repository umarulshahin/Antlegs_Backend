# Users_app/authentication.py

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from django.conf import settings
from Authentication.models import User_collection
from bson import ObjectId


class MongoJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # Return None to allow other authenticators or anonymous access

        token = auth_header.split(' ')[1]

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token.')

        id = payload.get('user_id')
        
        if not id:
            raise AuthenticationFailed('Email not in token.')
        user_data = User_collection.find_one({'_id': ObjectId(id)})

        if not user_data:
            raise AuthenticationFailed('User not found.')       

        class MongoUser:
            def __init__(self, data):
                self.email = data.get('email')
                self.id = str(data.get('_id'))
                self.is_authenticated = True

        return (MongoUser(user_data), token)