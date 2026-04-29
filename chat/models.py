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