const CSRF_TOKEN = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
let isLoading = false;

function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendRequest();
  }
}

function addMessage(text, role) {
  const container = document.getElementById('chat-messages');
  const row = document.createElement('div');
  row.className = `msg-row ${role}`;
  const bubble = document.createElement('div');
  bubble.className = `bubble ${role}`;
  bubble.textContent = text;
  row.appendChild(bubble);
  container.appendChild(row);
  container.scrollTop = container.scrollHeight;
  return bubble;
}

function addTypingIndicator() {
  const container = document.getElementById('chat-messages');
  const row = document.createElement('div');
  row.id = 'typing-indicator';
  row.className = 'msg-row assistant';
  row.innerHTML = '<div class="bubble assistant" style="color:#aaa;">입력 중...</div>';
  container.appendChild(row);
  container.scrollTop = container.scrollHeight;
}

function removeTypingIndicator() {
  const el = document.getElementById('typing-indicator');
  if (el) el.remove();
}

async function sendRequest() {
  if (isLoading) return;
  const task = document.getElementById('task-input').value.trim();
  if (!task) return;

  isLoading = true;
  document.getElementById('send-btn').disabled = true;
  document.getElementById('task-input').value = '';

  addMessage(task, 'user');
  addTypingIndicator();

  try {
    const res = await fetch('/chat/api/', {
      // const res = await fetch('/chat/api/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': CSRF_TOKEN
      },
      body: JSON.stringify({
        task: task,
        pdf_path: '',
        interview_history: []
      })
    });

    removeTypingIndicator();

    if (!res.ok) {
      addMessage('오류 ' + res.status, 'assistant');
      return;
    }

    const bubble = addMessage('', 'assistant');
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    const container = document.getElementById('chat-messages');

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      const text = decoder.decode(value);
      for (const line of text.split('\n')) {
        if (line.startsWith('data: ') && line !== 'data: [DONE]') {
          try {
            const data = JSON.parse(line.slice(6));
            if (data.token) {
              bubble.textContent += data.token;
              container.scrollTop = container.scrollHeight;
            }
            if (data.error) bubble.textContent += '\n오류: ' + data.error;
          } catch (e) { }
        }
      }
    }
  } catch (e) {
    removeTypingIndicator();
    addMessage('연결 오류: ' + e.message, 'assistant');
  } finally {
    isLoading = false;
    document.getElementById('send-btn').disabled = false;
  }
}