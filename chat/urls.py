# from django.urls import path
# from .views import chat_view, api_chat

# urlpatterns = [
#     path('', chat_view, name="chat"), 
#     path('api/', api_chat, name="api_chat"), 
# ]

from django.urls import path
from .views import api_chat, save_chat_api, chat_view
from . import views

urlpatterns = [
    path('', chat_view, name="chat"), 
    path('api/', api_chat, name="api_chat"), 
    path('api/save-chat/', views.save_chat_api),
]