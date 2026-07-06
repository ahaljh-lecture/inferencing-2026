import inspect
import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에 등록된 환경 변수 로드
load_dotenv()


def make_title_from_image(image_url, api_key, model):
    # OpenAI 클라이언트를 OpenRouter 엔드포인트로 연결
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "http://localhost:8501",  # 서비스 식별용 (선택)
            "X-Title": "Title Generator",              # OpenRouter 대시보드 표시용 (선택)
        },
    )

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

    # OpenRouter는 Chat Completions API 호환 → messages 형식으로 호출합니다.
    # 이미지는 user 메시지 안에 text/image_url 파트로 함께 담습니다.
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

    result = response.choices[0].message.content
    print(result)

    return result


st.title("돌아온 제목학원 by OpenRouter")

# API Key 및 모델 설정 (사이드바 구성 - 옆 페이지와 동일한 패턴)
api_key_env = os.environ.get("OPENROUTER_API_KEY")

with st.sidebar:
    st.header("⚙️ API 및 모델 설정")

    # 환경 변수에 키가 없으면 화면에서 직접 입력받도록 처리 (실습 편의성)
    if not api_key_env:
        api_key = st.text_input("OpenRouter API Key 입력", type="password")
    else:
        st.success("환경 변수에서 API Key를 로드했습니다.")
        api_key = api_key_env

    selected_model = st.selectbox(
        "제목 생성에 사용할 LLM 모델 선택",
        options=[
            "openai/gpt-4.1-mini",
            "openai/gpt-4o-mini",
            "anthropic/claude-3-haiku",
        ],
        index=0,
        help="이미지 입력(비전)을 지원하는 모델이어야 합니다. '제공자/모델명' 형식을 따릅니다.",
    )

image_url = st.text_input("Enter image URL:")
if image_url:
    try:
        st.image(image_url, caption="Image")

        if st.button("제목을 만들어줘!"):
            if not api_key:
                st.error("OpenRouter API Key가 누락되었습니다. 사이드바를 확인해주세요.")
            else:
                with st.spinner("제목을 생성하는 중..."):
                    new_title = make_title_from_image(image_url, api_key, selected_model)
                    st.subheader(new_title)
    except Exception:
        st.error("Error: Invalid image URL")
