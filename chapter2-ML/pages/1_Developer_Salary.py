"""
실습 2. ML 예측 앱 - 개발자 연봉 예측
"""

import pickle

import pandas as pd
import streamlit as st

st.title("개발자 연봉 예측기")
st.caption("가상 데이터로 학습한 모델입니다. 결과는 재미로만 봐주세요!")


# 모델은 무거우니 한 번만 로드합니다 (st.cache_resource)
@st.cache_resource
def load_model():
    with open("salary_model.pkl", "rb") as f:
        return pickle.load(f)


model = load_model()

# ------------------------------------------------------------
# 1. 입력 (Feature) - 위젯으로 받습니다
# ------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    years_experience = st.slider("경력 연수", 0, 25, 3)
    job_role = st.selectbox("직군", ["백엔드", "프론트엔드", "풀스택", "모바일",
                                    "데이터 분석가", "데이터 엔지니어", "ML 엔지니어",
                                    "DevOps/인프라", "QA"])
    main_language = st.selectbox("주 사용 언어", ["Python", "Java", "JavaScript/TypeScript",
                                             "C/C++", "C#", "Go", "Kotlin", "SQL", "기타"])
with col2:
    education = st.selectbox("최종 학력", ["고졸", "학사", "석사", "박사"], index=1)
    company_size = st.selectbox("회사 규모", ["스타트업 (~50명)", "중소기업 (50~300명)",
                                          "중견기업 (300~1000명)", "대기업 (1000명~)"])

# ------------------------------------------------------------
# 2. 예측 - 입력을 DataFrame으로 만들어 model.predict()
# ------------------------------------------------------------
if st.button("연봉 예측하기", type="primary"):
    input_df = pd.DataFrame([{
        "years_experience": years_experience,
        "job_role": job_role,
        "main_language": main_language,
        "education": education,
        "company_size": company_size,
    }])
    predicted_salary = model.predict(input_df)[0]

    # ------------------------------------------------------------
    # 3. 출력 - 결과를 보기 좋게
    # ------------------------------------------------------------
    st.metric("예상 연봉", f"{predicted_salary:,.0f} 만원",
              delta=f"{predicted_salary - 6000:+,.0f} 만원 (전체 평균 대비)")

    if predicted_salary >= 10000:
        st.balloons()
        st.success("억대 연봉이네요! 축하합니다 🎉")
    else:
        st.info(f"ML 엔지니어로 전직하고 대학원에 가면 얼마가 될까요? 바꿔서 눌러보세요.")