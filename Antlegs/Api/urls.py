from django.urls import path
from Authentication.views import *
from Authentication.views import CustomTokenObtainPairView
from Users_app.views import *

urlpatterns = [
 
    path('signin/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', custom_token_refresh, name='token_refresh'),
 
    path('signup/', Signup, name='signup'),
    
    path('usermanagement/', UserManagement.as_view(),name='usermanagement'),
]
