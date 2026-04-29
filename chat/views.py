# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Chat, ChatForm

# def msg_list(request):
#     messages = Chat.objects.all().order_by('-created_at')
#     return  render(request, 'chat/chat.html', {'messages': messages})

# def send_msg(request):
#     form = ChatForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         return redirect('chat') #post_list
#     return render(request, 'chat/chat.html', {'form': form})



from django.shortcuts import render, redirect
from .models import Chat, ChatForm

import httpx
import json
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os



def chat_view(request):
    # 1. Handle the Form Submission (POST)
    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chat') # Refresh page to show new message
        else:
            # This will print errors to your terminal to help debug
            print(form.errors) 
    else:
        # 2. Provide a blank form for GET requests
        form = ChatForm()

    # 3. Get all messages to display
    messages = Chat.objects.all().order_by('-created_at')
    
    return render(request, 'chat/chat.html', {
        'messages': messages,
        'form': form
    })



RUNPOT_URL = "https://ruqmxrcp2wvlx8-8000.proxy.runpod.net/"
API_SECRET_KEY = os.getenv("RUNPOT_API_KEY", "7759e342f8e33b061b680498d30d42b6873a21d1cacd060c0a4258d26eaa94ab")

@csrf_exempt
def chat_with_agent(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST만 허용"}, status=405)
    
    try:
        data = json.load(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': "JSON 형식 오류"}, status=400)
    

    def stream_generator():
        with httpx.Client(timeout=120.0) as client:
            with client.stream(
                "POST", f"{RUNPOT_URL}/run-agent",
                headers={
                    "x-api-key": API_SECRET_KEY,
                    "Content-Type": "application/json"
                },
                json={
                    "task":data.get("task", ""),
                    "pdf_path": data.get("pdf_path", ""),
                    "interview_history": data.get("interview_history",[])
                }
            ) as response:
                for line in response.iter_lines():
                    if line and line != "data: [Done]":
                        yield line + "\n"

    return StreamingHttpResponse(
        stream_generator(),
        content_type = "text/event-stream"
    )


def chat_page(request):
    return render(request, 'chat/chat.html')