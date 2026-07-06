"""
실습 3. DL 추론 앱 - 문장 감성 분석기

실습 2(ML)와 비교하면서 보세요.
- pkl 파일 로드      →  Huggingface에서 모델 다운로드 (pipeline)
- model.predict(입력) →  clf(문장)
- 나머지 패턴(입력 → 추론 → 출력)은 완전히 똑같습니다!
"""

import streamlit as st
from transformers import pipeline

st.title("문장 감성 분석기")
st.caption("Huggingface의 다국어 감성 분석 모델로 문장의 뉘앙스를 읽어봅니다. 한국어도 됩니다!")

# 5단계 감성을 보기 좋게 표시하기 위한 매핑
sentiment_display = {
    "Very Negative": ("매우 부정", "😡"),
    "Negative":      ("부정", "🙁"),
    "Neutral":       ("중립", "😐"),
    "Positive":      ("긍정", "🙂"),
    "Very Positive": ("매우 긍정", "🤩"),
}


# 모델은 무거우니 한 번만 로드합니다 (st.cache_resource - 실습 2와 동일!)
# 처음 실행할 때만 Huggingface에서 모델을 다운로드합니다 (약 500MB, 이후엔 캐시 사용)
@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",                              # 태스크 이름
        model="tabularisai/multilingual-sentiment-analysis",  # HF의 모델 주소
        top_k=None,                                         # 5개 클래스 점수를 전부 받기
    )


with st.spinner("모델 로딩 중... (처음 한 번만 다운로드합니다)"):
    clf = load_model()

# ------------------------------------------------------------
# 1. 입력 - 이번엔 표(Feature)가 아니라 '문장'입니다
# ------------------------------------------------------------
sentence = st.text_area(
    "분석할 문장을 입력하세요",
    placeholder="예) 이 강의 정말 유익해요! / 점심 메뉴가 좀 아쉬웠다...",
    height=100,
)

# ------------------------------------------------------------
# 2. 추론 - 문장을 넣으면 감성 점수가 나옵니다
# ------------------------------------------------------------
if st.button("감성 분석하기", type="primary"):
    if not sentence.strip():
        st.warning("문장을 입력해주세요!")
        st.stop()

    results = clf(sentence)                # [[{'label': 'Positive', 'score': 0.87}, ...]] 5개
    if isinstance(results[0], list):       # transformers 버전에 따라 한 겹 더 싸여 나옵니다
        results = results[0]
    top_result = max(results, key=lambda r: r["score"])

    # ------------------------------------------------------------
    # 3. 출력 - 결과를 보기 좋게
    # ------------------------------------------------------------
    label_ko, emoji = sentiment_display[top_result["label"]]
    st.metric("분석 결과", f"{emoji} {label_ko}", delta=f"확신도 {top_result['score']:.0%}")

    # 모델이 5개 클래스를 두고 '고민한 흔적'을 그대로 보여줍니다
    st.subheader("모델의 속마음 (클래스별 점수)")
    score_table = {sentiment_display[r["label"]][0]: r["score"] for r in results}
    st.bar_chart(score_table)

    if top_result["score"] < 0.5:
        st.info("확신도가 낮네요. 모델도 사람처럼 애매한 문장 앞에선 고민합니다.")