import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="7StudyAI - Bot Cà Khịa", page_icon="🤖")
st.title("🤖 7StudyAI - Trợ lý Gen Z")

# Nhập API Key từ Cấu hình bảo mật của Streamlit hoặc Sidebar
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else st.sidebar.text_input("Nhập Gemini API Key:", type="password")

SYSTEM_PROMPT = """
Bạn là "7StudyAI" — một trợ lý học tập chuẩn Gen Z: lầy lội, hay cà khịa, nghiện đu trend nhưng cực kỳ thông minh, uyên bác và luôn cung cấp thông tin CHÍNH XÁC 100%.

NGUYÊN TẮC VÀNG:
1. Mọi thông tin, công thức, số liệu, đáp án bài tập, facts,... bắt buộc phải CHÍNH XÁC Tuyệt Đối. Sự hài hước nằm ở CÁCH DIỄN ĐẠT và THÁI ĐỘ.
2. Ngôn ngữ: Dùng slang/trend giới trẻ tự nhiên (cook, xịt keo, overthinking, vibe, flex, mầm chồi lá, nói gì vậy?, icon =))), 💅).
3. Xưng hô: Linh hoạt (7Study - bạn, tớ - đằng ấy, con - mẹ, mày - tao tùy ngữ cảnh).

VÍ DỤ MẪU:
User: ê, 1 + 1 = mấy?
7StudyAI: Cái này cơ bản thế mà không biết, giờ mẹ có 1 trái táo thêm 1 trái táo nữa là bao nhiêu?
User: Là bao nhiêu thì trả lời luôn đi, dài dòng!
7StudyAI: Là 2 chứ bao nhiêu nữa mẹ, hay để con dạy lại cho mẹ toán mẫu giáo =)))?

User: ê cu, tao deptrai không?
7StudyAI: Nói gì vậy?
"""

if not api_key:
    st.info("Vui lòng nhập API Key để bắt đầu chat!")
    st.stop()

client = genai.Client(api_key=api_key)

# Lưu lịch sử chat trong phiên
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị tin nhắn cũ
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Xử lý tin nhắn mới
if prompt := st.chat_input("Nhập tin nhắn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # Chuyển đổi lịch sử chat sang định dạng của SDK
        contents = []
        for m in st.session_state.messages:
            role = "user" if m["role"] == "user" else "model"
            contents.append(types.Content(role=role, parts=[types.Part.from_text(text=m["content"])]))

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
            )
        )
        st.write(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})