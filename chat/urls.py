from django.urls import path
from .views import chat_view
# from .views import send_msg, msg_list

urlpatterns = [
    # path('', chat, name="chat"), 
    path('', chat_view, name="chat"), 
    # path('post_list', post_list, name="post_list"), 
    # path('create', send_msg, name="send_msg"), 
]