import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace

# -------------------------------------------------------------------
# 1. 감정 결과를 한글과 이모지로 매핑하는 딕셔너리
# -------------------------------------------------------------------
EMOTION_KO = {
    'happy': '기쁨 😄',
    'sad': '슬픔 😢',
    'angry': '분노 😡',
    'surprise': '놀람 😲',
    'fear': '두려움 😨',
    'disgust': '불쾌 🤢',
    'neutral': '무표정 😐'
}

# -------------------------------------------------------------------
# 2. Streamlit UI 구성
# -------------------------------------------------------------------
st.title("🎭 오늘의 감정 상태 분석기")

# 입력 방식 선택 (카메라 촬영 / 파일 업로드)
input_method = st.radio(
    "입력 방식을 선택하세요",
    ("📷 카메라 촬영", "📁 파일 업로드"),
    horizontal=True
)

if input_method == "📷 카메라 촬영":
    st.write("웹캠을 보고 가장 자신 있는 표정을 지어보세요!")
    img_file_buffer = st.camera_input("찰칵!")
else:
    st.write("표정이 잘 보이는 얼굴 사진을 업로드해 보세요!")
    img_file_buffer = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

if img_file_buffer is not None:
    # 1. Streamlit 이미지를 OpenCV가 읽을 수 있는 배열(numpy)로 변환
    bytes_data = img_file_buffer.getvalue()
    cv_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    with st.spinner("AI가 표정을 분석 중입니다..."):
        try:
            # 2. DeepFace로 감정 분석 수행 (enforce_detection=True로 얼굴이 없으면 에러 발생)
            # 리스트 형태로 결과가 반환되므로 첫 번째[0] 얼굴 데이터를 사용
            result = DeepFace.analyze(cv_img, actions=['emotion'], enforce_detection=True)
            face_data = result[0]
            
            # 가장 확률이 높은(Dominant) 감정 추출
            dominant_emotion = face_data['dominant_emotion']
            emotion_kr = EMOTION_KO.get(dominant_emotion, dominant_emotion)
            
            # 3. 시각적 재미를 위해 얼굴 영역에 네모 박스 그리기
            region = face_data['region']
            x, y, w, h = region['x'], region['y'], region['w'], region['h']
            
            # 초록색(0, 255, 0) 두께 3의 사각형 그리기
            cv2.rectangle(cv_img, (x, y), (x+w, y+h), (0, 255, 0), 3)
            
            # OpenCV(BGR)를 Streamlit용(RGB)으로 변환하여 화면에 출력
            rgb_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            st.image(rgb_img, caption="얼굴 인식 결과", use_container_width=True)
            
            # 결과 텍스트 출력
            st.success(f"AI가 분석한 현재 감정은... **{emotion_kr}** 입니다!")

            # (선택) 상세 감정 수치 보여주기 - 접었다 펼칠 수 있는 expander 사용
            with st.expander("📊 상세 감정 확률 보기"):
                for emotion, score in face_data['emotion'].items():
                    st.write(f"- {EMOTION_KO.get(emotion, emotion)}: {score:.2f}%")
                    
        except ValueError:
            # 얼굴을 찾지 못해 DeepFace 내부에서 에러가 났을 때의 처리
            st.warning("얼굴을 명확히 찾지 못했습니다. 정면을 잘 보고 다시 찍어주세요!")