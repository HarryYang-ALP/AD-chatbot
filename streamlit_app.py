import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AD 小幫手", page_icon="💬", layout="centered")

# 現代介面 CSS
st.markdown("""
<style>
/* 整體背景 */
.stApp { background: #f0f2f6; }

/* 隱藏 Streamlit 預設元素 */
#MainMenu, footer, header { visibility: hidden; }

/* 標題區塊 */
.chat-header {
    background: linear-gradient(135deg, #1a73e8, #0d47a1);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 14px;
    color: white;
}
.chat-header-icon { font-size: 32px; }
.chat-header-title { font-size: 20px; font-weight: 700; margin: 0; }
.chat-header-sub { font-size: 13px; opacity: 0.85; margin: 4px 0 0; }

/* 提示泡泡區 */
.bubble-section { margin-bottom: 16px; }
.bubble-label { font-size: 12px; color: #666; margin-bottom: 8px; font-weight: 500; }
.bubble-container { display: flex; flex-wrap: wrap; gap: 8px; }
.bubble-btn {
    background: white;
    border: 1.5px solid #e0e0e0;
    border-radius: 20px;
    padding: 7px 14px;
    font-size: 13px;
    cursor: pointer;
    color: #1a73e8;
    font-weight: 500;
    transition: all 0.2s;
    white-space: nowrap;
}
.bubble-btn:hover {
    background: #e8f0fe;
    border-color: #1a73e8;
}

/* 對話泡泡 */
.stChatMessage { border-radius: 12px !important; }

/* 登入卡片 */
.login-card {
    background: white;
    border-radius: 28px;
    padding: 48px 44px;
    box-shadow: 0 24px 64px rgba(0,0,0,0.18);
    width: 100%;
    max-width: 400px;
    margin: 60px auto 0;
    text-align: center;
}
.login-icon { font-size: 56px; margin-bottom: 16px; }
.login-title { font-size: 26px; font-weight: 800; color: #1a1a1a; margin: 0 0 8px; }
.login-sub { font-size: 14px; color: #999; margin: 0 0 32px; line-height: 1.6; }
.login-divider { height: 1px; background: #f0f0f0; margin: 0 0 28px; }

/* 覆蓋 input 樣式 */
.stTextInput > div > div > input {
    border: 2px solid #e0e0e0 !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    font-size: 15px !important;
    background: #fafafa !important;
}
.stTextInput > div > div > input:focus {
    border-color: #1a73e8 !important;
    background: white !important;
    box-shadow: 0 0 0 3px rgba(26,115,232,0.12) !important;
}
</style>
""", unsafe_allow_html=True)

# 密碼驗證
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("""
    <div class="login-card">
        <div class="login-icon">💬</div>
        <p class="login-title">AD 小幫手</p>
        <p class="login-sub">ALP BPM 系統與行政流程諮詢助手<br>請輸入密碼以繼續</p>
        <div class="login-divider"></div>
    </div>
    """, unsafe_allow_html=True)

    password = st.text_input(
        "存取密碼",
        type="password",
        placeholder="🔒  請輸入存取密碼",
        label_visibility="collapsed"
    )
    if st.button("進入系統 →", use_container_width=True, type="primary"):
        if password == st.secrets["APP_PASSWORD"]:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("❌ 密碼錯誤，請重新輸入")
    st.stop()

# System Prompt
SYSTEM_PROMPT = """
你是 ALP 公司的 AD 小幫手，專門回答 BPM 系統操作與行政流程相關問題。
請務必使用繁體中文回答，回答要清楚簡潔。
若被問到你是什麼模型，請回答「我是基於 Gemini 3.5 Flash Lite 模型建置的 AD 小幫手」。
若問題與 BPM 系統或行政流程相關，請根據以下知識庫回答。
若問題超出以下知識範圍但屬於一般性問題，可用一般知識回答並說明「以下為一般建議，非 ALP 系統規範」。
若完全無法回答，請回答「此問題超出我目前的知識範圍，請洽相關負責人或 AD 團隊協助。」

以下是你的知識庫：

【BPM 系統基本資訊】
- 系統網址：https://bpm.alp.global
- 登入方式：點擊 Azure AD Login，使用 M365 公司 Email 帳號登入
- 語言支援：英文、繁體中文、簡體中文

【帳號設定與代理人機制】
- 進入路徑：頂部功能列的「Personal」或個人姓名下的「Account」
- 代理人設定兩步驟：
  1. 設定狀態：在「Leaving」選單設定「Out of Office」或具體的「Leaving Period」並儲存
  2. 指派代理規則：在「Task Rules」新增規則，選擇 Delegation（委派），從用戶清單選取代理人並確認規則狀態為 Valid
- 管理代理：使用者可隨時編輯或刪除已建立的代理設定

【選單功能】
- Processes：選擇表單類型（SRF, PRF, SCF, TRF, APF, PMT）發起申請
- Drafts（草稿）：存放未完成表單，系統版本更新時需重新建立
- Templates（範本）：存下常用內容快速建立新申請，系統更新時需重新建立
- Worklist：待審核清單，登入後預設顯示此頁
- Share Task：特定角色共用清單，必須先點擊「Claim Task」取得處理權才能編輯
- My Requests：查看發出的申請，可發送 Reminder 給審核人
- Processed：已審核過的表單清單
- All Accessible：具檢視權限的所有表單，可進階搜尋篩選

【核心操作按鈕】
- Approve（同意）：同意並送至下一步
- Return（退回）：退回至先前特定節點，流程不終止
- Reject（拒絕）：拒絕並直接終止流程
- Notify（知會）：通知特定對象，不影響流程進行
- Add Approver（加會簽）：加入會簽人並設定順序，完成後回到當前步驟
- Enable Co-sign（啟用加簽）：在意見欄開啟加簽功能
- Withdraw（撤回）：下一關未處理前可取回修改
- Cancel（作廢）：在流程完成前終止申請
- Claim Task（取得處理權）：從 Share Task 取得表單所有權
- Release Task（釋放處理權）：釋放已取得的任務
- Submit（提出申請）：送出表單
- Preview（流程預覽）：查看流程圖，紅色為已完成節點，綠色框為目前所在節點

【流程狀態圖示】
- 圓圈符號 = Running（審核中）
- 勾選符號 = Approved（已核准）
- 叉號符號 = Rejected（已拒絕）
- 取消符號 = Aborted（已作廢）

【採購單（Procurement Order）操作】
判斷是否拋入 SAP-MM（符合任一條件需勾選「是」）：
- 主營業務：地產開發、物流管理、倉儲系統、供應鏈優化等核心業務
- 資產：單價 8 萬以上且耐用 2 年以上（列帳資產）；單價 1 萬至 8 萬且耐用 2 年以上（列管資產）
- 預付軟體/訂閱：一次付超過一個月以上的授權費
核心欄位：
- 成本中心：IT部門（IT01/IT02/IT81/IT03）、TEL部門（SC02/SC81/SC71/SC01）、PD部門（PD71/PD91/PD92/PD93/PD01）
- WBS Code：必須選擇有「最下層註記 (X)」的代碼，超出預算需先申請追加
- 付款方式：一次性（到貨後付清）或分期（按百分比或金額設定，發票日期需早於請款日）
簽核時效：急件每關 1 天，一般件每關 3 天（不含假日），逾期系統自動寄信提醒

【一般採購核決權限（LOA）】
- NT$30,000 以下：採購單位主管核決
- NT$30,001 ~ NT$300,000：採購／成控／會計會辦，單位主管核決
- NT$300,001 ~ NT$5,000,000：採購／成控／會計會辦，營運長核決
- NT$5,000,001 ~ NT$30,000,000：採購／成控／會計會辦，執行長核決
- NT$30,000,001 以上：採購／成控／會計會辦，董事長核決

【物管採購核決權限（LOA）】
- NT$150,000 以下：採購單位主管核決
- NT$150,001 以上且以原合約條件續約：採購單位主管核決
- NT$150,001 ~ NT$5,000,000：採購／成控／會計會辦，營運長核決
- NT$5,000,001 ~ NT$30,000,000：採購／成控／會計會辦，執行長核決
- NT$30,000,001 以上：採購／成控／會計會辦，董事長核決

【新建工程採購核決權限（LOA）】
- NT$30,000,000 以下：採購／成控／會計會辦，執行長核決
- NT$30,000,001 以上：採購／成控／會計會辦，董事長核決

【請款核決權限（LOA）】
其他部門請款：
- NT$30,000 以下或例行性請款：會計單位主管核決
- NT$30,001 ~ NT$5,000,000：會計會辦，營運長核決
- NT$5,000,001 以上：會計會辦，執行長核決
產品開發處請款：
- NT$150,000 以下或例行性請款：會計單位主管核決
- NT$150,001 ~ NT$5,000,000：會計會辦，執行長核決
- NT$5,000,001 以上：會計會辦，董事長核決
注意：預付供應商、員工預支及急件請款需由財務長核定

【合約核決權限（LOA）】
- 支出類合約（新建工程／自動化專案採購合約）：採購／財務／會計會辦，董事長核決
- 支出類合約（其他採購合約）：採購／財務／會計會辦，執行長核決
- 收入類合約（新建工程／客戶租賃合約）：財務／會計會辦，董事長核決
- 收入類合約（其他收入合約）：財務／會計會辦，執行長核決
- 保密協議（NDA）：法務單位主管核決
- 合作備忘錄（MOU）／意向書（LOI）：執行長核決
- 租賃租入合約：財務／會計會辦，董事長核決

【驗收單（Acceptance Order）】
- 一張驗收單只能對應一張採購單；一張採購單可分多次開多張驗收單
- 適用範圍：已拋入 SAP-MM 的採購單（營建類新建工程除外）
- 資產驗收：需與驗收經辦約定現場驗收，完成後經辦上傳紀錄並同步 SAP，申請人才可請款
- 必要附件：工程類附完工圖；備品類附含型號、數量的清晰照片；服務類附完成證明
- 數量控制：一次性付款可手動調整驗收數量；分期付款數量不可更動

【業務夥伴（Business Partner）】
建立情境：因採購需建供應商、因租賃需建客戶、新進同仁需建員工 BP
變更情境：修改既有資料、建立新角色、凍結不再往來的 BP
注意：申請前先查詢 BP 代碼或名稱，若已存在且資料一致則不需申請
特殊資訊：台灣供應商需填 8 碼統一編號；員工 BP 需填身分證字號與 3 碼員工編號

【出差申請（Travel Application Form）】
- 須於出差至少 3 個工作天前完成申請
- 適用範圍：國內外需住宿之出差
- 當日來回洽公請改用 Apollo 系統申請「公出」
- 未經核准的出差，差旅費一律不得預支或報銷
- 出差類別：專案支援、業務拓展、培訓研討、市場調研、其他
- 簽核流程：申請人 → 直屬主管 → 單位主管 → 人資單位 → 執行長
- 簽核完成後出勤資料自動同步至 Apollo，不需重複補單

【LOA 核決權限表圖例】
- ○ 擬辦  ◎ 覆核  ◉ 核定
"""

# 初始化 Gemini
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    model_name="gemini-3.5-flash-lite",
    system_instruction=SYSTEM_PROMPT
)

# 標題
st.markdown("""
<div class="chat-header">
    <div class="chat-header-icon">💬</div>
    <div>
        <p class="chat-header-title">AD 小幫手</p>
        <p class="chat-header-sub">有任何 BPM 系統或行政流程的問題，直接問我！</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 初始化
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# 提示泡泡
QUICK_QUESTIONS = [
    "如何登入 BPM？",
    "採購單怎麼填？",
    "如何設定代理人？",
    "一般採購核決權限？",
    "出差申請流程？",
    "Reject 和 Return 差別？",
    "驗收單怎麼開？",
    "Share Task 如何使用？",
]

if not st.session_state.messages:
    st.markdown('<div class="bubble-label">💡 常見問題，點擊即可發問：</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, q in enumerate(QUICK_QUESTIONS):
        with cols[i % 4]:
            if st.button(q, key=f"quick_{i}", use_container_width=True):
                st.session_state.pending_question = q
                st.rerun()

# 處理提示泡泡點擊
if "pending_question" in st.session_state:
    prompt = st.session_state.pop("pending_question")
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            reply = response.text
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            if "429" in str(e):
                st.error("今日問答次數已達上限，請明天再試！")
            else:
                st.error(f"錯誤：{str(e)}")

# 顯示歷史訊息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 輸入框
if prompt := st.chat_input("請輸入你的問題..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            response = st.session_state.chat.send_message(prompt)
            reply = response.text
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            if "429" in str(e):
                st.error("今日問答次數已達上限，請明天再試！")
            else:
                st.error(f"錯誤：{str(e)}")
