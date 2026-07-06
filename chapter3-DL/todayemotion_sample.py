"""
감정 분석 모델 추론 샘플 코드 (CLI 버전)

DeepFace를 사용해 이미지 파일 속 얼굴의 감정을 분석하는 최소 예제입니다.
Streamlit 같은 UI 없이 터미널에서 바로 실행할 수 있습니다.

사용법:
    python sample_infer.py <이미지_파일_경로>

예시:
    python sample_infer.py my_face.jpg
"""

import sys

from deepface import DeepFace

# -------------------------------------------------------------------
# 감정 결과를 한글과 이모지로 매핑하는 딕셔너리
# -------------------------------------------------------------------
EMOTION_KO = {
    'happy': '기쁨 😄',
    'sad': '슬픔 😢',
    'angry': '분노 😡',
    'surprise': '놀람 😲',
    'fear': '두려움 😨',
    'disgust': '불쾌 🤢',
    'neutral': '무표정 😐',
}


def analyze_emotion(image_path):
    """이미지 파일 경로를 받아 감정 분석 결과를 반환한다."""
    # DeepFace.analyze는 이미지 경로(문자열)를 바로 받을 수 있다.
    # actions=['emotion']으로 감정 분석만 수행한다.
    # 여러 얼굴이 있을 수 있으므로 결과는 리스트로 반환된다.
    results = DeepFace.analyze(
        img_path=image_path,
        actions=['emotion'],
        enforce_detection=True,  # 얼굴을 못 찾으면 에러 발생
    )
    return results


def main():
    # 1. 커맨드라인 인자에서 이미지 경로 읽기
    if len(sys.argv) < 2:
        print("사용법: python sample_infer.py <이미지_파일_경로>")
        sys.exit(1)

    image_path = sys.argv[1]
    print(f"'{image_path}' 이미지를 분석합니다...\n")

    # 2. 감정 분석 수행
    try:
        results = analyze_emotion(image_path)
    except ValueError:
        # 얼굴을 명확히 찾지 못했을 때의 처리
        print("얼굴을 명확히 찾지 못했습니다. 정면이 잘 보이는 사진을 사용해 주세요!")
        sys.exit(1)

    # 3. 감지된 얼굴마다 결과 출력
    for idx, face_data in enumerate(results, start=1):
        dominant_emotion = face_data['dominant_emotion']
        emotion_kr = EMOTION_KO.get(dominant_emotion, dominant_emotion)

        # 얼굴 위치 정보
        region = face_data['region']
        x, y, w, h = region['x'], region['y'], region['w'], region['h']

        print(f"[얼굴 #{idx}] 위치: x={x}, y={y}, w={w}, h={h}")
        print(f"  => 가장 강한 감정: {emotion_kr}\n")

        # 상세 감정 확률 출력
        print("  상세 감정 확률:")
        for emotion, score in face_data['emotion'].items():
            print(f"    - {EMOTION_KO.get(emotion, emotion)}: {score:.2f}%")
        print()


if __name__ == "__main__":
    main()
