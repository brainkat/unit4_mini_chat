from django.db import models
from django import forms

class Chat(models.Model):
    query = models.TextField()
    messages = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['query', 'messages']

# messages = [
#   {"role": "system", "content": "You are a helpful baking assistant."},
#   {"role": "user", "content": "How do I bake a sourdough bread?"},
#   {"role": "assistant", "content": "First, you need a bubbly starter..."}
# ]

# from django.db import models
# from django import forms

# class Chat(models.Model):
#     query = models.TextField()
#     messages = models.JSONField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     @classmethod
#     def add_chat(cls, query, message_list):
#         """
#         메시지 리스트를 받아서 바로 DB(RDS)에 저장하는 헬퍼 메서드
#         """
#         return cls.objects.create(query=query, messages=message_list)

#     def str(self):
#         return f"{self.query[:20]} ({self.created_at})"