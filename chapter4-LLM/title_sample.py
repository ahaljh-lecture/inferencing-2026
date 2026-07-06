"""
샘플 코드 - 돌아온 제목학원 (이미지 → 제목 생성, CLI 버전)

이 파일은 Streamlit 없이 'LLM 추론'의 핵심만 담은 샘플입니다.
여러분이 만들 Streamlit 앱은 아래의 추론 로직을 화면(UI)으로 감싸는 것입니다.

포인트: 텍스트만 다루던 앞의 예제와 달리, 이번엔 '이미지 URL'을 함께 넣습니다.
        (비전을 지원하는 모델이어야 합니다)

준비물:
    .env 파일에 OPENROUTER_API_KEY=... 를 넣어두세요.

실행 방법:
    python title_sample.py                        # 미리 준비된 예시 이미지로 실행
    python title_sample.py "https://.../image.jpg"  # 원하는 이미지 URL로 실행
"""

import inspect
import os
import sys

from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에 등록된 환경 변수 로드
load_dotenv()


def make_title_from_image(image_url, model="openai/gpt-4.1-mini"):
    """이미지 URL을 받아 창의적인 제목을 생성합니다."""

    # OpenAI 클라이언트를 OpenRouter 엔드포인트로 연결
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
    )

    # ------------------------------------------------------------
    # 프롬프트 - 지시 + 예시(few-shot)로 원하는 톤을 학습시킵니다
    # ------------------------------------------------------------
    prompt = inspect.cleandoc('''[지시]
    이미지를 보고 가장 창의적이고 재미있는 제목을 만들어줘. 실제 상황과 반전이 있으면 더 좋아.

    [예시 이미지1]
    스포츠 이벤트를 관람하고 있는 젊은 남성이 있어. 그의 얼굴에서는 눈물이 흐르고 있고, 카메라를 들고 있어. 스포츠를 보며 감동적인 순간을 포착한 것처럼 보여

    [예시 제목1]
    경기 막바지 즈음 누른 버튼이 촬영종료 버튼이 아니라 촬영취소 버튼이었다.

    [예시 이미지2]
    병상에 누워 있는 환자와 그를 둘러싸고 있는 여러 사람이 있어. 환자는 침대에 앉아 있고, 상태는 좋지 않아 보여. 주변 사람 중 한 명은 환자의 손을 잡고 있고, 나머지 사람은 환자를 바라보고 있어.

    [예시 제목2]
    내가 막 잠든 순간에 '임종하셨습니다'라고 한 녀석 누구야?
    ''')

    # ------------------------------------------------------------
    # 추론 - user 메시지 안에 text/image_url 파트를 함께 담아 호출
    # ------------------------------------------------------------
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "너는 창의력이 뛰어난 AI비서야.",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url},
                    },
                ],
            },
        ],
    )

    return response.choices[0].message.content


def main():
    # 명령줄 인자로 이미지 URL을 주면 그 이미지를, 아니면 예시 이미지를 사용합니다
    if len(sys.argv) > 1:
        image_url = sys.argv[1]
    else:
        image_url = (
            "https://mblogthumb-phinf.pstatic.net/20160511_248/easy-drive_1462941604617zF6SX_JPEG/20160511-125800-013.jpg?type=w800"
        )

    print(f"이미지: {image_url}")
    print("제목을 생성하는 중...\n")

    title = make_title_from_image(image_url)

    print("=" * 50)
    print(f"생성된 제목: {title}")
    print("=" * 50)


if __name__ == "__main__":
    main()
