from django.urls import path
from core_server.views import AddUser,Login,RFIDView,PosView
urlpatterns = [
    path('adduser', AddUser.as_view()),
    path('login',Login.as_view()),
    path('rfid',RFIDView.as_view()),
    path('pos',PosView.as_view())
]