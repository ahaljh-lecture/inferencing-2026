import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에 등록된 환경 변수 로드
load_dotenv()

# 1. Streamlit 페이지 레이아웃 스타일 설정
st.set_page_config(
    page_title="영혼 없는 K-직장인 변명 생성기",
    page_icon="💼",
    layout="centered"
)

st.title("💼 영혼 없는 K-직장인 변명/답장 생성기")
st.markdown("수강생 실습용: 속마음을 프로페셔널한 비즈니스 텍스트로 필터링하는 단발성 인퍼런스 앱입니다.")

# 2. OpenRouter API Key 및 모델 설정 (사이드바 구성)
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
        "테스트할 LLM 모델 선택",
        options=[
            "anthropic/claude-3-haiku",
            "google/gemini-2.5-flash",
            "qwen/qwen3.6-flash",
            "openai/gpt-4o-mini"
        ],
        index=0,
        help="OpenRouter에서 지원하는 모델 목록입니다. '제공자/모델명' 형식을 따릅니다."
    )
    st.caption("💡 각 모델별로 문체나 뉘앙스가 어떻게 다른지 비교해보세요!")

# 3. 사용자 입력 양식 (Main UI)
st.subheader("📝 1단계: 상황 및 본심 입력")

situation_preset = st.selectbox(
    "어떤 상황인가요? (상황 선택)",
    options=[
        "출근/회의 지각 예고",
        "보고서/업무 마감 지연 양해",
        "갑작스러운 미팅 일정 변경 요청",
        "금요일 퇴근 직전 무리한 업무 요청 거절",
        "연차/휴가 사유 그럴싸하게 꾸미기",
        "직접 입력"
    ]
)

# 직접 입력을 선택한 경우 텍스트 입력창 활성화
if situation_preset == "직접 입력":
    situation = st.text_input("상황을 구체적으로 적어주세요:", placeholder="예: 주말 특근 거절하기")
else:
    situation = situation_preset

real_reason = st.text_area(
    "진짜 속마음 / 날것의 사유 (솔직하게 적을수록 LLM 성능을 체감하기 좋습니다):",
    placeholder="예: 어제 넷플릭스 정주행하느라 새벽 4시에 자서 알람 못 들음 / 주말에 남친이랑 여행 가기로 해서 출근 절대 못함 / 그냥 귀찮음"
)

target = st.selectbox(
    "메시지를 받을 대상 (관계성 설정):",
    options=["팀장님", "경영진", "타 부서 협업 담당자", "외부 클라이언트/고객사"]
)

# 하이퍼파라미터처럼 작동할 '영혼 충전도' 슬라이더 설정
soul_level = st.slider(
    "영혼 충전도 (사회생활 필터 강도)",
    min_value=0,
    max_value=100,
    value=80,
    step=20,
    help="값이 높을수록 미사여구와 재발 방지 대책이 화려해지며, 낮을수록 핵심만 건조하게 전달합니다."
)

# 4. K-직장인 필터 인퍼런스 로직 실행
st.subheader("🚀 2단계: 비즈니스 언어로 인퍼런스")

if st.button("✨ K-직장인 영혼 주입하기", type="primary"):
    if not api_key:
        st.error("OpenRouter API Key가 누락되었습니다. 사이드바 확인이 필요합니다.")
    elif not real_reason.strip():
        st.warning("LLM이 포장할 수 있도록 '진짜 속마음'을 한 줄 이상 입력해주세요.")
    else:
        with st.spinner("LLM이 영혼을 갈아 넣어 텍스트를 포장하는 중..."):
            try:
                # OpenAI 클라이언트를 사용하여 OpenRouter 엔드포인트 호출
                client = OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=api_key,
                    default_headers={
                        "HTTP-Referer": "http://localhost:8501", # 서비스 식별용 (선택)
                        "X-Title": "K-Worker Statement Generator"  # OpenRouter 대시보드 표시용 (선택)
                    }
                )
                
                # 영혼 충전도(슬라이더 값)에 따른 프롬프트 조건 분기 가이드
                tone_guide = {
                    0: "극도로 감정을 배제하고 팩트만 건조하게 전달하되 최소한의 비즈니스 격식만 유지 (예: 사과 및 지각 사실 공지 끝)",
                    20: "가벼운 사유를 덧붙인 짧은 메신저(슬랙/카톡) 전송용 문체",
                    40: "일반적인 직장인 수준의 무난한 사과와 대안 제시",
                    60: "상대방의 기분을 배려하고 책임감 있는 태도를 보여주는 성숙한 직장인 톤",
                    80: "화려한 비즈니스 미사여구, 불가피한 외부 요인 포장, 구체적인 향후 리커버리 대책까지 포함된 이메일 양식",
                    100: "과할 정도로 극진하고 정중하여 상대방이 더 이상 문제를 제기할 수 없도록 만드는 '기적의 처세술' 문체"
                }
                
                # 프롬프트 엔지니어링: System Prompt 디자인
                system_prompt = f"""당신은 대한민국 조직 사회에서 온갖 풍파를 겪고 살아남은 10년 차 '사회생활 만렙'이자 비즈니스 커뮤니케이션의 달인인 K-직장인입니다.
사용자가 제공한 '상황'과 날것 그대로의 '진짜 속마음'을 재료로 삼아, 지정된 '받는 사람'의 성향과 직급에 맞는 완벽한 사회생활용 텍스트를 빌드해야 합니다.

[작성 가이드라인]
1. 사용자가 적은 솔직한 사유(예: 게으름, 유흥, 늦잠, 귀찮음 등)는 흔적도 없이 지워야 합니다. 대신 이를 '불가피한 신체 컨디션 저하', '예기치 못한 외부 인프라 변수', '업무 생산성 극대화를 위한 전략적 조율' 등으로 완벽하게 세탁하세요.
2. 수신 대상: {target} (이 관계에 맞는 정확한 높임말과 직급 호칭을 적용하세요.)
3. 영혼 충전도 설정 수치: {soul_level}%
   - 이 수치에 맞게 다음 톤앤매너 규칙을 엄격히 준수하세요: {tone_guide.get(soul_level)}
4. 결과물은 수강생이 바로 드래그하여 복사할 수 있도록 실제 전송 폼(인사말 - 본문 - 맺음말)을 갖추어 출력해 주세요. 부연 설명이나 사족은 생략하고 생성된 결과물 텍스트만 깔끔하게 반환하세요.
"""

                user_prompt = f"""
- 현재 상황: {situation}
- 날것의 속마음: {real_reason}
"""

                # API Request 호출
                response = client.chat.completions.create(
                    model=selected_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ]
                )
                
                # 응답 데이터 추출 및 출력
                generated_text = response.choices[0].message.content
                
                st.success("🎯 사회생활 필터링 완료!")
                st.code(generated_text, language="markdown")
                
            except Exception as e:
                st.error(f"API 호출 중 에러가 발생했습니다: {e}")