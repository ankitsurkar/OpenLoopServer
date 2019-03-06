from django.urls import path
from core_server.views import *
urlpatterns = [path('adduser', AddUser.as_view()),
 path('login',Login.as_view())
]