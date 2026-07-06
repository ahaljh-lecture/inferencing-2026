"""
실습 1-4. 멀티페이지 앱 뼈대 - 오늘의 최종 결과물이 담길 그릇
실행:  streamlit run Home.py

규칙은 하나뿐:
  Home.py 옆에 pages/ 폴더를 만들고 .py 파일을 넣으면
  → 사이드바에 페이지 메뉴가 자동으로 생깁니다.
  파일명 앞의 "1_", "2_" 숫자는 메뉴 순서입니다.

이후 실습이 끝날 때마다 pages/ 안의 파일을 완성해 나갑니다.
"""

import streamlit as st

st.set_page_config(page_title="나만의 AI 데모 앱", page_icon="🤖")

st.title("🤖 나만의 AI 데모 앱")
st.caption("Inferencing 서비스 개발 실습 - 모델은 달라도 패턴은 같습니다: 입력 → 모델 → 출력")

st.markdown("""
| 페이지 | 모델 | 어디서 오나 | 실습 |
|---|---|---|---|
| 1. ML 연봉 예측 | scikit-learn | pickle 파일 | 실습 2 |
| 2. DL 감성 분석 | Transformer | Huggingface | 실습 3 |
| 3. LLM 챗봇 | GPT | OpenAI API | 실습 4 |

👈 왼쪽 사이드바에서 페이지를 골라보세요. 지금은 공사 중이지만,
강의가 끝나면 **3개 모델을 서비스하는 웹 앱**이 완성됩니다!
""")

st.info("참고: 최신 공식 권장 방식은 st.Page + st.navigation 이지만, "
        "이 강의에서는 더 간단한 pages/ 폴더 방식을 사용합니다.")