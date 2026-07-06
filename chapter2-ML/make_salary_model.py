"""
개발자 연봉 예측 모델 만들기 (강사용)
- 현실적인 분포의 가상 데이터를 생성하고 (salary_data.csv)
- RandomForest 회귀 모델을 학습해서 pickle로 저장합니다 (salary_model.pkl)

실행:  python make_salary_model.py
"""

import pickle

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

rng = np.random.default_rng(42)
N = 3000

# ---------------------------------------------------------------
# 1. 가상 데이터 생성 (실제 개발자 연봉 통계의 대략적인 경향을 반영)
# ---------------------------------------------------------------
job_roles = ["백엔드", "프론트엔드", "풀스택", "모바일", "데이터 분석가",
             "데이터 엔지니어", "ML 엔지니어", "DevOps/인프라", "QA"]
role_premium = {"백엔드": 350, "프론트엔드": 250, "풀스택": 300, "모바일": 280,
                "데이터 분석가": 250, "데이터 엔지니어": 500, "ML 엔지니어": 750,
                "DevOps/인프라": 450, "QA": 100}

languages = ["Python", "Java", "JavaScript/TypeScript", "C/C++", "C#",
             "Go", "Kotlin", "SQL", "기타"]
language_premium = {"Python": 150, "Java": 100, "JavaScript/TypeScript": 80,
                    "C/C++": 180, "C#": 60, "Go": 250, "Kotlin": 180, "SQL": 30, "기타": 0}

education_levels = ["고졸", "학사", "석사", "박사"]
education_premium = {"고졸": 0, "학사": 150, "석사": 400, "박사": 750}

company_sizes = ["스타트업 (~50명)", "중소기업 (50~300명)", "중견기업 (300~1000명)", "대기업 (1000명~)"]
company_size_premium = {"스타트업 (~50명)": 0, "중소기업 (50~300명)": 200,
                        "중견기업 (300~1000명)": 550, "대기업 (1000명~)": 1000}

df = pd.DataFrame({
    "years_experience": rng.integers(0, 26, N),
    "job_role": rng.choice(job_roles, N),
    "main_language": rng.choice(languages, N),
    "education": rng.choice(education_levels, N, p=[0.08, 0.62, 0.25, 0.05]),
    "company_size": rng.choice(company_sizes, N, p=[0.25, 0.30, 0.25, 0.20]),
})

salary = (
    3200                                              # 신입 기본
    + 900 * np.sqrt(df["years_experience"])           # 경력 (체감 곡선)
    + df["job_role"].map(role_premium)
    + df["main_language"].map(language_premium)
    + df["education"].map(education_premium)
    + df["company_size"].map(company_size_premium)
    # ML 엔지니어 + 석/박사 시너지
    + np.where((df["job_role"] == "ML 엔지니어") & df["education"].isin(["석사", "박사"]), 400, 0)
    + rng.normal(0, 450, N)                           # 개인차 (noise)
)
df["salary"] = salary.round(-1).clip(2800, 20000).astype(int)

df.to_csv("salary_data.csv", index=False, encoding="utf-8-sig")
print(f"데이터 생성 완료: salary_data.csv ({len(df)}건)")
print(df.head(), "\n")

# ---------------------------------------------------------------
# 2. 학습 / 평가 데이터 분리  ←  강의 슬라이드 "모델이 잘 맞는지 어떻게 알까?"
# ---------------------------------------------------------------
X = df.drop(columns=["salary"])
y = df["salary"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ---------------------------------------------------------------
# 3. 모델 학습 (전처리 + 모델을 Pipeline 하나로)
# ---------------------------------------------------------------
model = Pipeline([
    ("preprocess", ColumnTransformer([
        ("categorical", OneHotEncoder(handle_unknown="ignore"),
         ["job_role", "main_language", "education", "company_size"]),
    ], remainder="passthrough")),
    ("model", RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42)),
])
model.fit(X_train, y_train)

# ---------------------------------------------------------------
# 4. 평가 - 본 적 없는 데이터로 시험 보기
# ---------------------------------------------------------------
pred = model.predict(X_test)
print(f"평가 데이터 MAE : {mean_absolute_error(y_test, pred):,.0f}만원")
print(f"평가 데이터 R²  : {r2_score(y_test, pred):.3f}")

# ---------------------------------------------------------------
# 5. pickle로 저장 - 이 파일을 수강생에게 배포합니다
# ---------------------------------------------------------------
with open("salary_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("모델 저장 완료: salary_model.pkl")