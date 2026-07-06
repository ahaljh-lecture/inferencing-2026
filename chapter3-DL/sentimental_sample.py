"""
샘플 코드 - 문장 감성 분석 (CLI 버전)

이 파일은 Streamlit 없이 '모델 추론'의 핵심만 담은 샘플입니다.
여러분이 만들 Streamlit 앱은 아래의 추론 로직을 화면(UI)으로 감싸는 것입니다.

실행 방법:
    python sentimental_sample.py                       # 미리 준비된 예시 문장들로 실행
    python sentimental_sample.py "이 강의 정말 유익해요!"   # 원하는 문장을 직접 넣어서 실행

처음 실행할 때만 Huggingface에서 모델을 다운로드합니다 (약 500MB, 이후엔 캐시 사용).
"""

import sys

from transformers import pipeline

# 5단계 감성을 보기 좋게 표시하기 위한 매핑
sentiment_display = {
    "Very Negative": ("매우 부정", "😡"),
    "Negative":      ("부정", "🙁"),
    "Neutral":       ("중립", "😐"),
    "Positive":      ("긍정", "🙂"),
    "Very Positive": ("매우 긍정", "🤩"),
}


def load_model():
    """모델을 불러옵니다. Huggingface의 다국어 감성 분석 모델을 사용합니다."""
    return pipeline(
        "text-classification",                                # 태스크 이름
        model="tabularisai/multilingual-sentiment-analysis",  # HF의 모델 주소
        top_k=None,                                           # 5개 클래스 점수를 전부 받기
    )


def analyze(clf, sentence):
    """문장 하나를 추론해서 결과를 출력합니다."""
    # ------------------------------------------------------------
    # 추론 - 문장을 넣으면 감성 점수가 나옵니다
    # ------------------------------------------------------------
    results = clf(sentence)                # [[{'label': 'Positive', 'score': 0.87}, ...]] 5개
    if isinstance(results[0], list):       # transformers 버전에 따라 한 겹 더 싸여 나옵니다
        results = results[0]
    top_result = max(results, key=lambda r: r["score"])

    # ------------------------------------------------------------
    # 출력 - 결과를 보기 좋게
    # ------------------------------------------------------------
    label_ko, emoji = sentiment_display[top_result["label"]]

    print(f"\n입력 문장: {sentence}")
    print(f"분석 결과: {emoji} {label_ko}  (확신도 {top_result['score']:.0%})")

    # 모델이 5개 클래스를 두고 '고민한 흔적'을 그대로 보여줍니다
    print("클래스별 점수:")
    for r in sorted(results, key=lambda r: r["score"], reverse=True):
        label_ko, _ = sentiment_display[r["label"]]
        bar = "█" * int(r["score"] * 20)   # 점수를 막대 그래프처럼 표현
        print(f"  {label_ko:<8} {r['score']:>5.0%} {bar}")

    if top_result["score"] < 0.5:
        print("확신도가 낮네요. 모델도 사람처럼 애매한 문장 앞에선 고민합니다.")


def main():
    print("모델 로딩 중... (처음 한 번만 다운로드합니다)")
    clf = load_model()

    # 명령줄 인자로 문장을 주면 그 문장을, 아니면 예시 문장들을 분석합니다
    if len(sys.argv) > 1:
        sentences = [" ".join(sys.argv[1:])]
    else:
        sentences = [
            "이 강의 정말 유익해요!",
            "점심 메뉴가 좀 아쉬웠다...",
            "그냥 평범한 하루였다.",
        ]

    for sentence in sentences:
        analyze(clf, sentence)


if __name__ == "__main__":
    main()
