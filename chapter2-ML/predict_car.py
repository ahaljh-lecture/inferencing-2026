"""
샘플 코드. 학습된 모델로 중고차 시세 예측하기 (CLI 버전)

Streamlit 같은 화면 없이, 코드 안에 입력값을 직접 넣어서 예측 결과를 출력합니다.
모델 추론의 핵심 흐름(모델 로드 → 입력 만들기 → predict → 결과 출력)만 담았습니다.

실행:  python predict_car.py
"""

import pickle

import pandas as pd

base_year = 2026

# ------------------------------------------------------------
# 1. 모델 로드 - 저장해 둔 pickle 파일을 그대로 불러옵니다
# ------------------------------------------------------------
with open("car_model.pkl", "rb") as f:
    model = pickle.load(f)

# ------------------------------------------------------------
# 2. 입력 (Feature) - 예측하고 싶은 차량 정보를 직접 채웁니다
#    이 값들을 바꿔가며 예측 결과가 어떻게 달라지는지 확인해 보세요.
# ------------------------------------------------------------
brand = "현대"          # 브랜드
car_type = "SUV"        # 차종
year = 2020             # 연식
mileage = 5.0           # 주행거리 (만km)
fuel = "가솔린"          # 연료 (가솔린, 디젤, 하이브리드, 전기, LPG)
accident = "무사고"      # 사고 이력 (무사고, 단순수리, 사고이력)

# 모델은 DataFrame 형태의 입력을 받습니다 (학습할 때와 컬럼명이 같아야 합니다!)
input_df = pd.DataFrame([{
    "브랜드": brand,
    "차종": car_type,
    "연식": year,
    "주행거리_만km": mileage,
    "연료": fuel,
    "사고이력": accident,
}])

# ------------------------------------------------------------
# 3. 예측 - model.predict() 호출
# ------------------------------------------------------------
predicted_price = model.predict(input_df)[0]

# 신차 상태(올해 연식, 주행 0, 무사고)와 비교해 감가율도 계산해 봅니다
new_car_input = input_df.copy()
new_car_input["연식"] = base_year
new_car_input["주행거리_만km"] = 0.0
new_car_input["사고이력"] = "무사고"
new_car_price = model.predict(new_car_input)[0]
depreciation_rate = (1 - predicted_price / new_car_price) * 100

# ------------------------------------------------------------
# 4. 출력 - 결과를 보기 좋게 터미널에 찍습니다
# ------------------------------------------------------------
print("=" * 40)
print(f" 브랜드   : {brand}")
print(f" 차종     : {car_type}")
print(f" 연식     : {year}년")
print(f" 주행거리 : {mileage}만km")
print(f" 연료     : {fuel}")
print(f" 사고이력 : {accident}")
print("-" * 40)
print(f" 예상 시세 : {predicted_price:,.0f} 만원")
print(f" 감가율    : {depreciation_rate:.0f}% (신차 대비)")
print("=" * 40)
