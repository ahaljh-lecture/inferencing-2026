"""
실습(대안). ML 예측 앱 - 내 차 시세 예측
"""

import pickle

import pandas as pd
import streamlit as st

st.title("내 차 시세 예측기")
st.caption("한국 중고차 시장의 경향을 반영한 가상 데이터로 학습한 모델입니다. 결과는 재미로만 봐주세요!")

base_year = 2026

# 브랜드별 판매 차종 (위젯 구성용 - 모델 학습 스크립트와 동일)
brand_car_types = {
    "현대": ["경차", "준중형", "중형", "대형", "SUV", "전기차 전용"],
    "기아": ["경차", "준중형", "중형", "대형", "SUV", "전기차 전용"],
    "제네시스": ["중형", "대형", "SUV"],
    "쉐보레": ["경차", "준중형", "중형", "SUV"],
    "르노코리아": ["준중형", "중형", "SUV"],
    "KG모빌리티": ["중형", "SUV"],
    "BMW": ["준중형", "중형", "대형", "SUV"],
    "벤츠": ["준중형", "중형", "대형", "SUV"],
    "아우디": ["준중형", "중형", "대형", "SUV"],
    "폭스바겐": ["준중형", "중형", "SUV"],
    "볼보": ["중형", "대형", "SUV"],
    "렉서스": ["중형", "대형", "SUV"],
    "테슬라": ["전기차 전용", "SUV"],
    "포르쉐": ["스포츠카", "SUV"],
}


# 모델은 무거우니 한 번만 로드합니다 (st.cache_resource)
@st.cache_resource
def load_model():
    with open("car_model.pkl", "rb") as f:
        return pickle.load(f)


model = load_model()

# ------------------------------------------------------------
# 1. 입력 (Feature) - 위젯으로 받습니다
# ------------------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    brand = st.selectbox("브랜드", list(brand_car_types))
    car_type = st.selectbox("차종", brand_car_types[brand])   # 브랜드에 따라 목록이 바뀝니다!
    year = st.slider("연식", 2008, base_year, 2020)
with col2:
    mileage = st.slider("주행거리 (만km)", 0.0, 30.0, 5.0, step=0.5)
    if car_type == "전기차 전용" or brand == "테슬라":
        fuel = "전기"
        st.selectbox("연료", ["전기"], disabled=True)
    else:
        fuel = st.selectbox("연료", ["가솔린", "디젤", "하이브리드", "LPG"])
    accident = st.radio("사고 이력", ["무사고", "단순수리", "사고이력"], horizontal=True)

# ------------------------------------------------------------
# 2. 예측 - 입력을 DataFrame으로 만들어 model.predict()
# ------------------------------------------------------------
if st.button("시세 예측하기", type="primary"):
    input_df = pd.DataFrame([{
        "브랜드": brand,
        "차종": car_type,
        "연식": year,
        "주행거리_만km": mileage,
        "연료": fuel,
        "사고이력": accident,
    }])
    predicted_price = model.predict(input_df)[0]

    # 신차 상태(올해 연식, 주행 0, 무사고)와 비교해 감가율도 보여줍니다
    new_car_input = input_df.copy()
    new_car_input["연식"], new_car_input["주행거리_만km"], new_car_input["사고이력"] = base_year, 0.0, "무사고"
    new_car_price = model.predict(new_car_input)[0]
    depreciation_rate = (1 - predicted_price / new_car_price) * 100

    # ------------------------------------------------------------
    # 3. 출력 - 결과를 보기 좋게
    # ------------------------------------------------------------
    st.metric("예상 시세", f"{predicted_price:,.0f} 만원",
              delta=f"-{depreciation_rate:.0f}% (신차 대비)", delta_color="inverse")

    if depreciation_rate >= 60:
        st.info("차는 출고되는 순간부터 감가가 시작됩니다. 그래도 추억은 감가되지 않죠.")
    elif brand == "포르쉐":
        st.success("포르쉐는 꿈이 아니라 계획입니다 🏎️")