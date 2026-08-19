import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="AD 小幫手", page_icon="🤖", layout="wide")
st.markdown("<style>#MainMenu,footer,header{visibility:hidden}.block-container{padding:0!important;max-width:100%!important}</style>", unsafe_allow_html=True)

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
APP_PASSWORD = st.secrets["APP_PASSWORD"]
BG = "https://raw.githubusercontent.com/HarryYang-ALP/AD-chatbot/main/background.jpg"
LOGO = "https://raw.githubusercontent.com/HarryYang-ALP/AD-chatbot/main/logo.png"

components.html(f"""
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AD 小幫手</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;height:100vh;overflow:hidden}}

/* ── 登入頁 ── */
#login-page{{
  position:fixed;inset:0;
  background:url('{BG}') center/cover no-repeat;
  display:flex;align-items:center;justify-content:center;
  z-index:100;
}}
#login-page::before{{
  content:'';position:absolute;inset:0;
  background:rgba(0,0,0,0.45);
}}
.login-card{{
  position:relative;
  background:white;border-radius:20px;
  padding:44px 40px 40px;width:380px;
  text-align:center;
  box-shadow:0 20px 60px rgba(0,0,0,0.3);
}}
.login-card img{{width:72px;height:auto;margin-bottom:16px}}
.login-card h1{{font-size:20px;font-weight:700;color:#202124;margin-bottom:6px}}
.login-card p{{font-size:13px;color:#5f6368;margin-bottom:24px}}
.login-divider{{height:1px;background:#e8eaed;margin-bottom:24px}}
.login-card input{{
  width:100%;padding:13px 16px;
  border:1.5px solid #dadce0;border-radius:8px;
  font-size:14px;background:#fafafa;outline:none;
  margin-bottom:12px;transition:border 0.2s,box-shadow 0.2s;
}}
.login-card input:focus{{
  border-color:#1a73e8;background:white;
  box-shadow:0 0 0 3px rgba(26,115,232,0.15);
}}
.login-btn{{
  width:100%;padding:13px;
  background:#1a73e8;color:white;
  border:none;border-radius:8px;
  font-size:14px;font-weight:500;cursor:pointer;
  transition:background 0.2s;
}}
.login-btn:hover{{background:#1557b0}}
.login-error{{color:#d93025;font-size:13px;margin-top:10px;min-height:20px}}

/* ── 聊天頁 ── */
#chat-page{{
  display:none;flex-direction:column;height:100vh;
  background:#f7f8fa;max-width:760px;margin:0 auto;
}}
.chat-header{{
  padding:16px 24px;border-bottom:1px solid #e8eaed;
  background:white;display:flex;align-items:center;gap:12px;
  flex-shrink:0;
}}
.chat-header img{{width:32px;height:auto;object-fit:contain}}
.chat-header-text h2{{font-size:16px;font-weight:600;color:#202124;margin:0}}
.chat-header-text p{{font-size:12px;color:#80868b;margin:0}}

.chat-messages{{
  flex:1;overflow-y:auto;padding:20px 24px;
  display:flex;flex-direction:column;gap:16px;
}}
.msg-row{{display:flex;gap:10px;align-items:flex-start}}
.msg-row.user{{justify-content:flex-end}}
.msg-avatar{{
  width:30px;height:30px;border-radius:50%;
  background:#e8f0fe;display:flex;align-items:center;
  justify-content:center;flex-shrink:0;overflow:hidden;
}}
.msg-avatar img{{width:18px;height:auto;object-fit:contain}}
.msg-bubble{{
  max-width:75%;padding:11px 15px;
  font-size:14px;line-height:1.65;border-radius:0 14px 14px 14px;
  background:#fff;border:1px solid #e8eaed;color:#202124;
}}
.msg-row.user .msg-bubble{{
  background:#e8f0fe;border:none;
  border-radius:14px 0 14px 14px;color:#1a1a1a;
}}

.bubbles-area{{padding:0 24px 12px;flex-shrink:0}}
.bubbles-label{{font-size:11px;color:#80868b;margin-bottom:7px}}
.bubbles-wrap{{display:flex;flex-wrap:wrap;gap:7px}}
.bubble-btn{{
  padding:6px 13px;font-size:13px;
  background:white;border:1px solid #dadce0;
  border-radius:20px;cursor:pointer;color:#1a73e8;
  transition:all 0.15s;white-space:nowrap;
}}
.bubble-btn:hover{{background:#e8f0fe;border-color:#1a73e8}}

.chat-input-area{{
  padding:12px 24px 20px;background:white;
  border-top:1px solid #e8eaed;flex-shrink:0;
}}
.input-wrap{{
  display:flex;align-items:center;gap:10px;
  background:#f7f8fa;border:1px solid #dadce0;
  border-radius:24px;padding:8px 8px 8px 18px;
  transition:border 0.2s,box-shadow 0.2s;
}}
.input-wrap:focus-within{{
  border-color:#1a73e8;background:white;
  box-shadow:0 0 0 2px rgba(26,115,232,0.12);
}}
.input-wrap textarea{{
  flex:1;border:none;background:transparent;
  font-size:14px;resize:none;outline:none;
  max-height:120px;line-height:1.5;
  font-family:inherit;color:#202124;
}}
.send-btn{{
  width:34px;height:34px;border-radius:50%;
  background:#1a73e8;border:none;cursor:pointer;
  display:flex;align-items:center;justify-content:center;
  flex-shrink:0;transition:background 0.2s;
}}
.send-btn:hover{{background:#1557b0}}
.send-btn svg{{width:16px;height:16px;fill:white}}
.typing{{color:#80868b;font-size:13px;padding:4px 0}}

/* 歡迎訊息 */
.welcome-area{{
  padding:32px 24px 8px;text-align:center;
}}
.welcome-area h3{{font-size:22px;font-weight:600;color:#202124;margin-bottom:8px}}
.welcome-area p{{font-size:14px;color:#5f6368}}
</style>
</head>
<body>

<!-- 登入頁 -->
<div id="login-page">
  <div class="login-card">
    <img src="{LOGO}" alt="ALP">
    <h1>AD 小幫手</h1>
    <p>ALP BPM 系統與行政流程諮詢助手</p>
    <div class="login-divider"></div>
    <input type="password" id="pw-input" placeholder="請輸入存取密碼"
      onkeydown="if(event.key==='Enter')doLogin()">
    <button class="login-btn" onclick="doLogin()">登入</button>
    <div class="login-error" id="login-error"></div>
  </div>
</div>

<!-- 聊天頁 -->
<div id="chat-page">
  <div class="chat-header">
    <img src="{LOGO}" alt="ALP">
    <div class="chat-header-text">
      <h2>AD 小幫手</h2>
      <p>有任何 BPM 系統或行政流程問題，直接問我</p>
    </div>
  </div>

  <div class="chat-messages" id="chat-messages">
    <div class="welcome-area">
      <h3>你好！我是 AD 小幫手</h3>
      <p>有任何 BPM 系統或行政流程的問題都可以問我</p>
    </div>
  </div>

  <div class="bubbles-area" id="bubbles-area">
    <div class="bubbles-label">💡 你可以這樣問：</div>
    <div class="bubbles-wrap" id="bubbles-wrap"></div>
  </div>

  <div class="chat-input-area">
    <div class="input-wrap">
      <textarea id="chat-input" rows="1" placeholder="請輸入你的問題..."
        onkeydown="if(event.key==='Enter'&&!event.shiftKey){{event.preventDefault();sendMsg()}}"
        oninput="autoResize(this)"></textarea>
      <button class="send-btn" onclick="sendMsg()">
        <svg viewBox="0 0 24 24"><path d="M2 21l21-9L2 3v7l15 2-15 2z"/></svg>
      </button>
    </div>
  </div>
</div>

<script>
const CORRECT_PW = "{APP_PASSWORD}";
const API_KEY = "{GEMINI_API_KEY}";
const API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key=" + API_KEY;

const SYSTEM_PROMPT = `你是 ALP 公司的 AD 小幫手，專門回答 BPM 系統操作與行政流程相關問題。
請務必使用繁體中文回答，回答要清楚簡潔。
若被問到你是什麼模型，請回答「我是基於 Gemini Flash Lite 模型建置的 AD 小幫手」。
若問題超出知識範圍，請回答「此問題超出我目前的知識範圍，請洽相關負責人或 AD 團隊協助。」

知識庫：
【BPM基本資訊】網址：https://bpm.alp.global / 登入：點 Azure AD Login 用 M365 Email / 語言：英文、繁體中文、簡體中文
【代理人設定】路徑：Personal > Account。步驟1：Leaving 設 Out of Office 並儲存。步驟2：Task Rules 新增 Delegation 規則，選代理人，確認 Valid。
【選單功能】Processes：發起申請 / Drafts：草稿 / Templates：範本 / Worklist：待審核 / Share Task：共用任務需先 Claim Task / My Requests：我的申請 / Processed：已處理 / All Accessible：所有可檢視
【操作按鈕】Approve同意 / Return退回 / Reject拒絕終止 / Notify知會 / Add Approver加會簽 / Withdraw撤回 / Cancel作廢 / Claim Task取得處理權 / Release Task釋放 / Submit送出 / Preview流程圖
【採購單】SAP-MM判定：主營業務、資產(8萬以上耐用2年=列帳;1-8萬耐用2年=列管)、預付軟體超過1個月。欄位：成本中心(IT:IT01/02/81/03, TEL:SC02/81/71/01, PD:PD71/91/92/93/01)、WBS Code選最下層X、付款一次性或分期。急件1天/一般3天。
【一般採購LOA】3萬以下:主管 / 3萬-30萬:採購成控會計+主管 / 30萬-500萬:+營運長 / 500萬-3000萬:+執行長 / 3000萬以上:+董事長
【物管採購LOA】15萬以下:主管 / 15萬+原合約續約:主管 / 15萬-500萬:+營運長 / 500萬-3000萬:+執行長 / 3000萬以上:+董事長
【新建工程LOA】3000萬以下:執行長 / 3000萬以上:董事長
【請款LOA】其他部門:3萬以下主管,3萬-500萬營運長,500萬以上執行長。產品開發:15萬以下主管,15萬-500萬執行長,500萬以上董事長。急件/預付需財務長。
【合約LOA】新建工程採購合約:董事長 / 其他採購合約:執行長 / 新建工程租賃合約:董事長 / 其他收入合約:執行長 / NDA:法務主管 / MOU/LOI:執行長 / 租賃合約:董事長
【驗收單】1驗收對1採購,1採購可多張驗收。需拋SAP-MM(非新建工程)。資產需現場驗收+SAP收貨。附件:工程=完工圖,備品=型號照片,服務=完成證明。一次性可改數量,分期不可。
【業務夥伴】建立:供應商/客戶/員工BP。變更:修改/新角色/凍結。先查詢再申請。台灣供商需統編,員工需身分證+3碼員編。
【出差】3工作天前申請。含住宿才用BPM,當日來回用Apollo公出。未核准不得預支報銷。簽核:申請人>直屬主管>單位主管>人資>執行長。完成後自動同步Apollo。`;

const BUBBLES = {{
  default: ["如何登入 BPM？","採購單怎麼填？","如何設定代理人？","出差申請流程？","核決權限查詢？","驗收單怎麼開？"],
  採購: ["核決權限是多少？","WBS Code 怎麼選？","付款方式有哪些？","如何撤回採購單？"],
  核決: ["一般採購核決？","物管採購核決？","請款核決權限？","合約核決權限？"],
  驗收: ["驗收單附件規定？","驗收單對應規則？","資產驗收流程？"],
  出差: ["出差簽核流程？","當日來回怎麼申請？","差旅費如何報銷？"],
  代理: ["代理人設定步驟？","如何取消代理？","代理期間任務？"],
  登入: ["如何設定代理人？","語言怎麼切換？","Worklist 在哪？","Share Task 怎麼用？"],
}};

let chatHistory = [];

function doLogin() {{
  const pw = document.getElementById('pw-input').value;
  if (pw === CORRECT_PW) {{
    document.getElementById('login-page').style.display = 'none';
    document.getElementById('chat-page').style.display = 'flex';
    renderBubbles('default');
  }} else {{
    document.getElementById('login-error').textContent = '密碼錯誤，請重新輸入';
    document.getElementById('pw-input').value = '';
    document.getElementById('pw-input').focus();
  }}
}}

function renderBubbles(hint) {{
  let set = BUBBLES.default;
  for (const key of Object.keys(BUBBLES)) {{
    if (key !== 'default' && hint.includes(key)) {{ set = BUBBLES[key]; break; }}
  }}
  const wrap = document.getElementById('bubbles-wrap');
  wrap.innerHTML = set.map(q =>
    `<button class="bubble-btn" onclick="sendQuestion('${{q}}')">${{q}}</button>`
  ).join('');
  document.getElementById('bubbles-area').style.display = 'block';
}}

function sendQuestion(q) {{
  document.getElementById('chat-input').value = q;
  sendMsg();
}}

function addMsg(text, isUser) {{
  const msgs = document.getElementById('chat-messages');
  const row = document.createElement('div');
  row.className = 'msg-row' + (isUser ? ' user' : '');

  if (!isUser) {{
    const av = document.createElement('div');
    av.className = 'msg-avatar';
    av.innerHTML = `<img src="{LOGO}" alt="ALP">`;
    row.appendChild(av);
  }}

  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';
  bubble.innerHTML = text.replace(/\\n/g,'<br>');
  row.appendChild(bubble);
  msgs.appendChild(row);
  msgs.scrollTop = msgs.scrollHeight;
  return bubble;
}}

async function sendMsg() {{
  const input = document.getElementById('chat-input');
  const text = input.value.trim();
  if (!text) return;
  input.value = '';
  input.style.height = 'auto';

  document.getElementById('bubbles-area').style.display = 'none';
  addMsg(text, true);

  chatHistory.push({{ role: 'user', parts: [{{ text }}] }});

  const typingRow = document.createElement('div');
  typingRow.className = 'msg-row';
  const av = document.createElement('div');
  av.className = 'msg-avatar';
  av.innerHTML = `<img src="{LOGO}" alt="ALP">`;
  const typing = document.createElement('div');
  typing.className = 'typing';
  typing.textContent = '思考中...';
  typingRow.appendChild(av);
  typingRow.appendChild(typing);
  document.getElementById('chat-messages').appendChild(typingRow);
  document.getElementById('chat-messages').scrollTop = 99999;

  try {{
    const res = await fetch(API_URL, {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{
        system_instruction: {{ parts: [{{ text: SYSTEM_PROMPT }}] }},
        contents: chatHistory
      }})
    }});
    const data = await res.json();
    const reply = data.candidates?.[0]?.content?.parts?.[0]?.text || '抱歉，無法取得回應。';
    typingRow.remove();
    addMsg(reply, false);
    chatHistory.push({{ role: 'model', parts: [{{ text: reply }}] }});
    renderBubbles(text);
  }} catch(e) {{
    typingRow.remove();
    addMsg('發生錯誤，請稍後再試。', false);
  }}
}}

function autoResize(el) {{
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
}}

document.getElementById('pw-input').focus();
</script>
</body>
</html>
""", height=700, scrolling=False)
