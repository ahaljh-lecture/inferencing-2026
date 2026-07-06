"""
실습 1-2. 기본 입력 위젯 - 입력 → 처리 → 출력 패턴
실행:  streamlit run step2_widgets.py

⭐ Streamlit 핵심 동작 원리 ⭐
위젯을 건드릴 때마다 이 스크립트 "전체"가 위에서 아래로 다시 실행됩니다.
(버튼을 눌러도, 슬라이더를 움직여도!)
"""

import streamlit as st

st.title("개발자 프로필 카드 만들기")
st.caption("입력 → 처리 → 출력. 오늘 하루 종일 반복할 패턴입니다.")

# ------------------------------------------------------------
# 1. 입력 - 위젯으로 받습니다 (위젯의 리턴값 = 현재 입력값)
# ------------------------------------------------------------
name = st.text_input("이름", placeholder="홍길동")

years_experience = st.slider("경력 연수", min_value=0, max_value=25, value=3)

job_role = st.selectbox("직군", ["백엔드", "프론트엔드", "풀스택", "모바일",
                          "데이터 분석가", "데이터 엔지니어", "ML 엔지니어",
                          "DevOps/인프라", "QA"])

interests = st.multiselect("관심 분야 (여러 개 선택)",
                       ["머신러닝", "딥러닝", "LLM", "웹 개발", "데이터 분석"],
                       default=["LLM"])

# 위 코드가 실행되는 순간, 각 변수에는 이미 사용자의 입력값이 들어있습니다.
# 확인해볼까요? (입력을 바꿔보세요 - 즉시 반영됩니다 = 매번 재실행되니까!)
st.write("현재 입력값:", name, "/", years_experience, "년 /", job_role)

# ------------------------------------------------------------
# 2. 처리 & 3. 출력 - 버튼이 눌렸을 때만
# ------------------------------------------------------------
# st.button()은 "이번 재실행이 이 버튼 클릭 때문인가?"를 True/False로 알려줍니다
if st.button("프로필 카드 생성", type="primary"):
    if not name:
        st.error("이름을 입력해주세요!")
    else:
        # (처리) 지금은 문자열 조합이지만,
        #        실습 2부터는 이 자리에 model.predict()가 들어갑니다
        level = "주니어" if years_experience < 3 else ("미들" if years_experience < 8 else "시니어")

        # (출력)
        st.success(f"**{name}** 님은 경력 {years_experience}년의 {level} {job_role} 개발자입니다.")
        if interests:
            st.info(f"관심 분야: {', '.join(interests)} — 오늘 강의에 다 나옵니다 😉")