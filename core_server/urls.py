from django.urls import path
from core_server.views import AddUser,Login,RFIDView,PosView,TransactAPI,TransactDetails,SpendingRuleAPI,EnableNextTransaction, AddMoney, WriteRFID
urlpatterns = [
    path('adduser', AddUser.as_view()),
    path('login',Login.as_view()),
    path('rfid',RFIDView.as_view()),
    path('pos',PosView.as_view()),
    path('transact',TransactAPI.as_view()),
    path('txn_details',TransactDetails.as_view()),
    path('srules',SpendingRuleAPI.as_view()),
    path('en/<str:secret_no>',EnableNextTransaction.as_view()),
    path('add/<int:amount>',AddMoney.as_view()),
    path('write',WriteRFID.as_view())
]