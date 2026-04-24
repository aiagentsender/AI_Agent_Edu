# app.py
import streamlit as st
import random

st.set_page_config(page_title="Persona Chatbot (Offline)", layout="wide")

st.title("🧠 Persona 기반 챗봇_UI_LLM 없음")


# =========================
# 🔽 [추가] Persona 목록 정의
# =========================
PERSONAS = {
    "IT 강사": {"style": "초보자에게 쉽게 설명", "tone": "친절하고 부드러운 설명"},
    "까칠한 시니어 개발자": {
        "style": "핵심만 짧게 설명",
        "tone": "직설적이고 건조한 말투",
    },
    "친구 같은 조언자": {"style": "편하게 설명", "tone": "친근하고 가벼운 말투"},
}


# =========================
# 🔽 Sidebar에서 Persona 선택 UI
# =========================
st.sidebar.title("⚙️ 설정")
selected_persona = st.sidebar.radio(
    "페르소나 선택", list(PERSONAS.keys()), horizontal=True
)

current_persona = PERSONAS[selected_persona]

# 선택된 Persona 정보 출력 (선택 확인용)
st.sidebar.write(f"스타일: {current_persona['style']}")
st.sidebar.write(f"톤: {current_persona['tone']}")


# =========================
# 간단한 룰 기반 응답 생성
# =========================
def generate_response(user_input, persona):
    user_input = user_input.lower()

    # 기본 응답 로직
    if "python" in user_input:
        base_response = "Python은 문법이 쉬워서 입문자에게 아주 좋은 언어입니다 😊"

    elif "llm" in user_input or "ai" in user_input:
        base_response = (
            "LLM은 대규모 데이터를 학습해서 자연어를 이해하고 생성하는 모델입니다."
        )

    elif "streamlit" in user_input:
        base_response = "Streamlit은 데이터 앱을 빠르게 만들 수 있는 Python 기반 UI 프레임워크입니다."

    elif "안녕" in user_input or "hello" in user_input:
        base_response = "안녕하세요! 무엇이 궁금하신가요? 😊"

    elif "?" in user_input:
        base_response = "좋은 질문이에요! 조금 더 구체적으로 설명해드릴게요."

    else:
        fallback = [
            "조금 더 자세히 설명해 주시겠어요?",
            "좋은 질문이에요 😊",
            "그 부분은 중요한 개념입니다!",
            "초보자 관점에서 쉽게 설명해드릴게요.",
        ]
        base_response = random.choice(fallback)

    # =========================
    # Persona 스타일 적용
    # =========================
    if selected_persona == "IT 강사":
        return f"📘 [강사] {base_response}"

    elif selected_persona == "까칠한 시니어 개발자":
        return f"😐 핵심만 말할게. {base_response}"

    elif selected_persona == "친구 같은 조언자":
        return f"😄 야 이거 쉽게 말하면~ {base_response}"

    return base_response


# =========================
# 세션 상태 (Memory)
# =========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =========================
# 채팅 UI 출력
# =========================
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# =========================
# 사용자 입력
# =========================
user_input = st.chat_input("질문을 입력하세요")

if user_input:
    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.write(user_input)

    # 🔽 [수정] Persona 전달
    response = generate_response(user_input, current_persona)

    # 챗봇 응답 출력
    with st.chat_message("assistant"):
        st.write(response)

    # 히스토리 저장
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": response})