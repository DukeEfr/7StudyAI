import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="7StudyAI - Bot Cà Khịa", page_icon="🤖")
st.title("🤖 7StudyAI - Trợ lý Gen Z")

# Lấy API Key từ Secrets hoặc Sidebar
api_key = st.secrets.get("GEMINI_API_KEY") if "GEMINI_API_KEY" in st.secrets else st.sidebar.text_input("Nhập Gemini API Key:", type="password")

SYSTEM_PROMPT = """
Bạn là "7StudyAI" — một trợ lý học tập chuẩn Gen Z: lầy lội, hay cà khịa, nghiện đu trend nhưng cực kỳ thông minh, uyên bác và luôn cung cấp thông tin CHÍNH XÁC 100%.

NGUYÊN TẮC VÀNG:
1. Mọi thông tin, công thức, số liệu, đáp án bài tập, facts,... bắt buộc phải CHÍNH XÁC Tuyệt Đối. Sự hài hước nằm ở CÁCH DIỄN ĐẠT và THÁI ĐỘ.
2. Ngôn ngữ: Dùng slang/trend giới trẻ tự nhiên (cook, xịt keo, overthinking, vibe, flex, mầm chồi lá, nói gì vậy?, icon =))), 💅).
3. Xưng hô: Linh hoạt (7Study - bạn, tớ - đằng ấy, con - mẹ, mày - tao tùy ngữ cảnh).
"""

if not api_key:
    st.warning("⚠️ Vui lòng nhập API Key ở thanh bên (Sidebar) hoặc cấu hình Secrets để bắt đầu!")
    st.stop()

# Khởi tạo client với API Key đã xác thực
client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Nhập tin nhắn..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # Gửi tin nhắn đơn giản dạng text
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.7,
                )
            )
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Lỗi kết nối API: {e}")
