"""
샘플 코드 - 영혼 없는 K-직장인 변명/답장 생성기 (CLI 버전)

이 파일은 Streamlit 없이 'LLM 추론'의 핵심만 담은 샘플입니다.
여러분이 만들 Streamlit 앱은 아래의 추론 로직을 화면(UI)으로 감싸는 것입니다.

준비물:
    .env 파일에 OPENROUTER_API_KEY=... 를 넣어두세요.
    (또는 실행 전에 환경 변수로 export 해도 됩니다)

실행 방법:
    python k_soul_sample.py
"""

import os

from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에 등록된 환경 변수 로드
load_dotenv()

# 영혼 충전도(0~100)에 따른 톤앤매너 가이드
TONE_GUIDE = {
    0:   "극도로 감정을 배제하고 팩트만 건조하게 전달하되 최소한의 비즈니스 격식만 유지",
    20:  "가벼운 사유를 덧붙인 짧은 메신저(슬랙/카톡) 전송용 문체",
    40:  "일반적인 직장인 수준의 무난한 사과와 대안 제시",
    60:  "상대방의 기분을 배려하고 책임감 있는 태도를 보여주는 성숙한 직장인 톤",
    80:  "화려한 비즈니스 미사여구, 불가피한 외부 요인 포장, 구체적인 향후 리커버리 대책까지 포함된 이메일 양식",
    100: "과할 정도로 극진하고 정중하여 상대방이 더 이상 문제를 제기할 수 없도록 만드는 '기적의 처세술' 문체",
}


def generate_reply(situation, real_reason, target, soul_level, model="anthropic/claude-3-haiku"):
    """상황/속마음/대상/영혼충전도를 받아 사회생활용 텍스트를 생성합니다."""

    # OpenAI 클라이언트를 OpenRouter 엔드포인트로 연결
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
    )

    # ------------------------------------------------------------
    # 프롬프트 엔지니어링 - System Prompt 디자인
    # ------------------------------------------------------------
    system_prompt = f"""당신은 대한민국 조직 사회에서 온갖 풍파를 겪고 살아남은 10년 차 '사회생활 만렙'이자 비즈니스 커뮤니케이션의 달인인 K-직장인입니다.
사용자가 제공한 '상황'과 날것 그대로의 '진짜 속마음'을 재료로 삼아, 지정된 '받는 사람'의 성향과 직급에 맞는 완벽한 사회생활용 텍스트를 빌드해야 합니다.

[작성 가이드라인]
1. 사용자가 적은 솔직한 사유(예: 게으름, 유흥, 늦잠, 귀찮음 등)는 흔적도 없이 지워야 합니다. 대신 이를 '불가피한 신체 컨디션 저하', '예기치 못한 외부 인프라 변수', '업무 생산성 극대화를 위한 전략적 조율' 등으로 완벽하게 세탁하세요.
2. 수신 대상: {target} (이 관계에 맞는 정확한 높임말과 직급 호칭을 적용하세요.)
3. 영혼 충전도 설정 수치: {soul_level}%
   - 이 수치에 맞게 다음 톤앤매너 규칙을 엄격히 준수하세요: {TONE_GUIDE.get(soul_level)}
4. 결과물은 바로 복사하여 전송할 수 있도록 실제 전송 폼(인사말 - 본문 - 맺음말)을 갖추어 출력해 주세요. 부연 설명이나 사족은 생략하고 생성된 결과물 텍스트만 깔끔하게 반환하세요.
"""

    user_prompt = f"""
- 현재 상황: {situation}
- 날것의 속마음: {real_reason}
"""

    # ------------------------------------------------------------
    # 추론 - messages 형식으로 Chat Completions API 호출
    # ------------------------------------------------------------
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )

    return response.choices[0].message.content


def main():
    # 아래 값들을 바꿔가며 실습해 보세요 (Streamlit 앱에서는 이 값들을 화면 입력으로 받습니다)
    situation = "출근/회의 지각 예고"
    real_reason = "어제 넷플릭스 정주행하느라 새벽 4시에 자서 알람을 못 들음"
    target = "팀장님"
    soul_level = 80  # 0, 20, 40, 60, 80, 100 중 하나

    print("LLM이 영혼을 갈아 넣어 텍스트를 포장하는 중...\n")
    result = generate_reply(situation, real_reason, target, soul_level)

    print("=" * 50)
    print(f"상황: {situation}")
    print(f"속마음: {real_reason}")
    print(f"대상: {target} / 영혼 충전도: {soul_level}%")
    print("=" * 50)
    print(result)


if __name__ == "__main__":
    main()
