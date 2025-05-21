from django.urls import path
from Authentication.views import *
from Authentication.views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from Users_app.views import *

urlpatterns = [
 
    path('signin/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
 
    path('signup/', Signup, name='signup'),
    
    path('usermanagement/', UserManagement.as_view(),name='usermanagement'),
]
