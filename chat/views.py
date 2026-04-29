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



RUNPOT_URL = "https://ruqmxrcp2wvlx8-8000.proxy.runpod.net"
API_SECRET_KEY = os.getenv("RUNPOT_API_KEY", "7759e342f8e33b061b680498d30d42b6873a21d1cacd060c0a4258d26eaa94ab")

@csrf_exempt
#chat_with_agent
def api_chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST만 허용"}, status=405)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': "JSON 형식 오류"}, status=400)
    

    def stream_generator():
        print(f"Sending request to RunPod: {RUNPOT_URL}/run-agent")
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
            print(f"Response status: {response.status_code}")

    return StreamingHttpResponse(
        stream_generator(),
        content_type = "text/event-stream"
    )


def chat_page(request):
    return render(request, 'chat/chat.html')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Chat
import json

@csrf_exempt # 테스트를 위해 CSRF 보안을 잠시 해제 (실무에선 토큰 사용 권장)
def save_chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body) # 프론트에서 보낸 JSON 파싱
        
        # RDS에 저장
        chat = Chat.objects.create(
            query=data.get('query'),
            messages=data.get('messages') # 리스트 형태 그대로 저장
        )
        
        return JsonResponse({"status": "success", "id": chat.id})





"""

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



RUNPOT_URL = "https://ruqmxrcp2wvlx8-8000.proxy.runpod.net"
API_SECRET_KEY = os.getenv("RUNPOT_API_KEY", "7759e342f8e33b061b680498d30d42b6873a21d1cacd060c0a4258d26eaa94ab")

@csrf_exempt
#chat_with_agent
def api_chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST만 허용"}, status=405)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': "JSON 형식 오류"}, status=400)
    

    def stream_generator():
            full_response = "" # Track the response to save it later
            with httpx.Client(timeout=120.0) as client:
                with client.stream(...) as response:
                    for line in response.iter_lines():
                        if line:
                            # Process line...
                            # Extract the token from JSON and add to full_response
                            # yield line
            
            # After the loop finishes, save to the JSONField model
            Chat.objects.create(
                query=data.get("task"),
                messages=[
                    {"role": "user", "content": data.get("task")},
                    {"role": "assistant", "content": full_response}
                ]
            )

    def chat_page(request):
        return render(request, 'chat/chat.html')
"""


