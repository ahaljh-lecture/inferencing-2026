"""
실습 1-3. 화면 구성 + st.cache_resource
실행:  streamlit run step3_layout.py

- st.sidebar : 왼쪽 사이드바 (설정 메뉴 두기 좋음)
- st.columns : 화면을 좌우로 분할
- st.cache_resource : 무거운 객체(모델)는 한 번만 로드 ⭐
"""

import time

import streamlit as st

st.title("화면 구성 & 캐시")


# ------------------------------------------------------------
# st.cache_resource - 오늘 가장 중요한 한 줄
# ------------------------------------------------------------
# 문제: Streamlit은 위젯을 건드릴 때마다 스크립트 전체를 재실행합니다.
#       → 모델 로드(수 초~수십 초)도 매번 다시??
# 해결: @st.cache_resource를 붙이면 최초 1번만 실행하고,
#       그 다음부터는 저장해둔 결과를 재사용합니다.
@st.cache_resource
def load_model():
    time.sleep(3)  # 무거운 모델을 로드하는 척 (실습 2에서는 진짜 pickle.load)
    return "🤖 (3초 걸려 로드된 아주 무거운 모델)"


with st.spinner("모델 로드 중..."):
    model = load_model()

st.write("모델 준비 완료:", model)
st.caption("↑ 아래 위젯들을 아무리 건드려도 3초 로딩은 다시 일어나지 않습니다. "
           "(@st.cache_resource를 주석 처리하고 비교해보세요!)")

st.divider()

# ------------------------------------------------------------
# st.sidebar - 사이드바에 설정 모아두기
# ------------------------------------------------------------
st.sidebar.header("설정")
language = st.sidebar.radio("인사 언어", ["한국어", "English"])
shout = st.sidebar.checkbox("크게 외치기")

# ------------------------------------------------------------
# st.columns - 화면 좌우 분할
# ------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("입력")
    name = st.text_input("이름", value="Streamlit")

with col2:
    st.subheader("출력")
    greeting = f"안녕하세요, {name}님!" if language == "한국어" else f"Hello, {name}!"
    if shout:
        greeting = greeting.upper() + "!!!"
    st.metric("인사말", greeting)