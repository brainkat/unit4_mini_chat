from django.urls import path
from .views import send_msg, msg_list

urlpatterns = [
    # path('', chat, name="chat"), 
    path('', msg_list, name="chat"), 
    # path('post_list', post_list, name="post_list"), 
    path('create', send_msg, name="send_msg"), 
]