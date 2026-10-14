HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Transformer Serve</title>
<style>
  * { box-sizing: border-box; }
  html, body {
    margin: 0; padding: 0; height: 100%;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    background: #1a1a1a;
    color: #ececec;
  }
  body { display: flex; flex-direction: column; height: 100vh; overflow: hidden; }

  header {
    padding: 14px 24px;
    border-bottom: 1px solid #2a2a2a;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-shrink: 0;
    background: #1a1a1a;
  }
  header .left { display: flex; align-items: center; gap: 12px; }
  .dot { width: 9px; height: 9px; border-radius: 50%; background: #555; flex-shrink: 0; transition: background .3s, box-shadow .3s; }
  .dot.ok { background: #4caf50; box-shadow: 0 0 8px #4caf5099; }
  .dot.bad { background: #e05d44; box-shadow: 0 0 8px #e05d4499; }
  header h1 { font-size: 15px; margin: 0; font-weight: 600; letter-spacing: .2px; }
  header .model { font-size: 11.5px; color: #8a8a8a; margin-top: 1px; }
  header a { color: #d97757; text-decoration: none; font-size: 12.5px; font-weight: 500; }
  header a:hover { text-decoration: underline; }

  .body-wrap { flex: 1; display: flex; overflow: hidden; }
  .scroll-area { flex: 1; overflow-y: auto; display: flex; justify-content: center; }
  main {
    max-width: 700px; width: 100%;
    padding: 24px 20px 12px;
    display: flex; flex-direction: column; gap: 14px;
  }

  .params {
    display: flex; gap: 24px; background: #1f1f1f;
    border: 1px solid #2a2a2a; border-radius: 10px;
    padding: 12px 16px; flex-wrap: wrap;
  }
  .param { display: flex; flex-direction: column; gap: 6px; flex: 1; min-width: 160px; }
  .param label { font-size: 12px; color: #aaa; display: flex; justify-content: space-between; }
  .param label b { color: #d97757; font-weight: 600; }
  input[type="range"] {
    -webkit-appearance: none; height: 4px; border-radius: 2px;
    background: #333; accent-color: #d97757;
  }

  .thread { display: flex; flex-direction: column; gap: 14px; padding-bottom: 16px; }
  .row { display: flex; }
  .row.user { justify-content: flex-end; }
  .row.model { justify-content: flex-start; }
  .bubble {
    padding: 11px 15px; border-radius: 14px; font-size: 14.5px;
    line-height: 1.6; white-space: pre-wrap; max-width: 82%;
  }
  .bubble.user { background: #d97757; color: #1a1a1a; font-weight: 500; border-bottom-right-radius: 4px; }
  .bubble.model { background: #262626; border: 1px solid #303030; border-bottom-left-radius: 4px; }
  .bubble.model.placeholder { color: #999; font-style: italic; }
  .bubble.typing::after { content: '▍'; animation: blink 1s step-start infinite; color: #d97757; }
  @keyframes blink { 50% { opacity: 0; } }

  footer {
    border-top: 1px solid #2a2a2a;
    padding: 14px 20px 18px;
    display: flex; justify-content: center;
    flex-shrink: 0; background: #1a1a1a;
  }
  .input-wrap {
    max-width: 700px; width: 100%;
    display: flex; align-items: flex-end; gap: 10px;
    background: #232323; border: 1px solid #333; border-radius: 14px;
    padding: 8px 8px 8px 16px;
  }
  .input-wrap:focus-within { border-color: #d97757; }
  textarea {
    flex: 1; resize: none; background: transparent; border: none; outline: none;
    color: #eee; font-size: 14.5px; font-family: inherit;
    padding: 8px 0; max-height: 140px; line-height: 1.5;
  }
  button.send {
    background: #d97757; color: #1a1a1a; border: none; border-radius: 10px;
    width: 38px; height: 38px; flex-shrink: 0; font-size: 16px; font-weight: 700;
    cursor: pointer; transition: background .15s, opacity .15s;
  }
  button.send:hover { background: #e28a6b; }
  button.send:disabled { opacity: .4; cursor: not-allowed; }

  ::-webkit-scrollbar { width: 8px; }
  ::-webkit-scrollbar-thumb { background: #333; border-radius: 4px; }
</style>
</head>
<body>

<header>
  <div class="left">
    <span class="dot" id="statusDot"></span>
    <div>
      <h1>Transformer Serve</h1>
      <div class="model" id="modelInfo">loading model info...</div>
    </div>
  </div>
  <a href="https://github.com/ssnym/transformer-serve" target="_blank">Source on GitHub &rarr;</a>
</header>

<div class="body-wrap">
  <div class="scroll-area" id="scrollArea">
    <main>
      <div class="params">
        <div class="param">
          <label>Max new tokens <b id="maxTokVal">100</b></label>
          <input type="range" id="maxTok" min="10" max="300" value="100">
        </div>
        <div class="param">
          <label>Temperature <b id="tempVal">0.60</b></label>
          <input type="range" id="temp" min="0" max="150" value="60">
        </div>
      </div>

      <div class="thread" id="thread">
        <div class="row model">
          <div class="bubble model placeholder">Ask me anything. Set temperature to 0 for deterministic answers.</div>
        </div>
      </div>
    </main>
  </div>
</div>

<footer>
  <div class="input-wrap">
    <textarea id="prompt" placeholder="Message Transformer Serve..." rows="1"></textarea>
    <button class="send" id="sendBtn">&#8593;</button>
  </div>
</footer>

<script>
  const thread = document.getElementById('thread');
  const scrollArea = document.getElementById('scrollArea');
  const promptBox = document.getElementById('prompt');
  const sendBtn = document.getElementById('sendBtn');
  const dot = document.getElementById('statusDot');
  const modelInfo = document.getElementById('modelInfo');
  const maxTok = document.getElementById('maxTok');
  const temp = document.getElementById('temp');
  const maxTokVal = document.getElementById('maxTokVal');
  const tempVal = document.getElementById('tempVal');

  maxTok.oninput = () => maxTokVal.textContent = maxTok.value;
  temp.oninput = () => tempVal.textContent = (temp.value / 100).toFixed(2);

  promptBox.addEventListener('input', () => {
    promptBox.style.height = 'auto';
    promptBox.style.height = Math.min(promptBox.scrollHeight, 140) + 'px';
  });

  async function checkHealth() {
    try {
      const res = await fetch('/health');
      if (!res.ok) throw new Error('bad status');
      const h = await res.json();
      dot.className = 'dot ok';
      modelInfo.textContent =
        h.model_name + ' \\u00b7 ' + h.configured_model_type + ' \\u00b7 ' + h.device_type.toUpperCase();
    } catch (e) {
      dot.className = 'dot bad';
      modelInfo.textContent = 'server unreachable';
    }
  }
  checkHealth();
  setInterval(checkHealth, 30000);

  function addRow(text, who, extraClass) {
    const row = document.createElement('div');
    row.className = 'row ' + who;
    const bubble = document.createElement('div');
    bubble.className = 'bubble ' + who + (extraClass ? ' ' + extraClass : '');
    bubble.textContent = text;
    row.appendChild(bubble);
    thread.appendChild(row);
    scrollArea.scrollTop = scrollArea.scrollHeight;
    return bubble;
  }

      async function send() {
    const text = promptBox.value.trim();
    if (!text) return;
    thread.innerHTML = '';
    addRow(text, 'user');
    const typing = addRow('', 'model', 'typing');
    sendBtn.disabled = true;
    promptBox.value = '';
    promptBox.style.height = 'auto';

    try {
      const res = await fetch('/generate/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: text,
          max_new_tokens: parseInt(maxTok.value),
          temperature: parseFloat(temp.value) / 100,
          do_sample: parseFloat(temp.value) > 0,
        })
      });
      if (!res.ok) throw new Error('HTTP ' + res.status);

      typing.classList.remove('typing');
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        typing.textContent += decoder.decode(value, { stream: true });
        scrollArea.scrollTop = scrollArea.scrollHeight;
      }
    } catch (e) {
      typing.classList.remove('typing');
      typing.textContent = 'Error: could not reach the API. Try again in a moment.';
    }
    sendBtn.disabled = false;
    scrollArea.scrollTop = scrollArea.scrollHeight;
  }

  sendBtn.onclick = send;
  promptBox.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  });
</script>

</body>
</html>
"""