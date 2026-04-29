from django.urls import path
from .views import chat_view, api_chat
# from .views import send_msg, msg_list

urlpatterns = [
    path('', chat_view, name="chat"), 
    path('api/', api_chat, name="api_chat"), 
]