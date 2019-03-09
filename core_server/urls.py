from django.urls import path
from core_server.views import AddUser,Login,RFIDView,PosView,TransactAPI,TransactDetails,SpendingRuleAPI
urlpatterns = [
    path('adduser', AddUser.as_view()),
    path('login',Login.as_view()),
    path('rfid',RFIDView.as_view()),
    path('pos',PosView.as_view()),
    path('transact',TransactAPI.as_view()),
    path('txn_details',TransactDetails.as_view()),
    path('srules',SpendingRuleAPI.as_view())
]