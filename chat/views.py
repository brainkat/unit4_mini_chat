from django.shortcuts import render, get_object_or_404, redirect
from .models import Chat, ChatForm

def msg_list(request):
    messages = Chat.objects.all().order_by('-created_at')
    return  render(request, 'chat/chat.html', {'messages': messages})

def send_msg(request):
    form = ChatForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('chat') #post_list
    return render(request, 'chat/chat.html', {'form': form})
