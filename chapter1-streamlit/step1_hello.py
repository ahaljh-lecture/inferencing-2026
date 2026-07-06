"""
실습 1-1. 첫 Streamlit 앱
실행:  streamlit run step1_hello.py

브라우저가 자동으로 열립니다. (기본 주소: http://localhost:8501)
코드를 수정하고 저장하면 → 브라우저 우측 상단 'Rerun' 또는 'Always rerun'
"""

import streamlit as st

# 페이지 제목 (브라우저 탭에도 표시됩니다)
st.title("Hello Streamlit! 👋")

# st.write : 뭐든 출력하는 만능 함수 (문자열, 숫자, DataFrame, 차트...)
st.write("HTML, CSS, JavaScript 없이 이 화면이 나왔습니다.")

# 마크다운도 그대로 씁니다
st.markdown("""
### 오늘 우리가 만들 것
- **Page 1** : ML 예측 앱 (개발자 연봉 예측)
- **Page 2** : DL 추론 앱 (Huggingface)
- **Page 3** : LLM 챗봇 (OpenAI API)
""")

st.caption("이 파일이 전부입니다. python 파일 하나 = 웹 앱 하나")
