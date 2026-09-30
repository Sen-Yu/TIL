# 🤖 머신러닝(Machine Learning) 핵심 실무 가이드 (Zero to Hero)

> **작성자**: 시니어 개발자  
> **대상**: 머신러닝의 핵심 원리를 탄탄히 다지고 실무 정형 데이터(Tabular Data) 및 모델링 파이프라인을 구축하려는 주니어 개발자  
> **목표**: 머신러닝의 동작 원리와 지도·비지도 학습 알고리즘을 수학적/직관적 관점에서 깊이 있게 이해하고, 현업에서 가장 많이 쓰는 알고리즘(XGBoost/LightGBM 등)을 자유자재로 다룬다.

---

## 1. 머신러닝이란 무엇이고 왜 필요한가?

### 1.1 룰 기반(Rule-based) 프로그래밍과의 근본적 차이
전통적인 소프트웨어 개발은 사람이 직접 모든 조건문(`if-else`)을 작성했습니다.  
하지만 복잡한 실세계 문제(예: 고객의 대출 상환 여부, 사기 거래 탐지, 주택 가격 산정)는 고려해야 할 변수(Feature)가 수십~수백 개에 달해 사람이 규칙을 일일이 정의할 수 없습니다.

```
[전통적 개발]: 데이터(Data) + 규칙(Code) ─────────► 결과(Output)
[머신러닝]:   데이터(Data) + 정답(Target/Label) ──► 규칙(Model / 함수 f(x)) 발견!
```

머신러닝의 본질은 **데이터 공간에서 입력 $X$와 출력 $y$ 사이의 관계를 가장 잘 근사하는 최적의 함수 $y = f(X)$를 찾아내는 과정**입니다.

---

## 2. 머신러닝의 3대 학습 유형

```
                             [머신러닝 (ML)]
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
   지도학습 (Supervised)     비지도학습 (Unsupervised)   강화학습 (Reinforcement)
   - 문제와 정답(Label) 제공    - 정답 없이 패턴/군집 발견    - 환경과 상호작용하며 보상 극대화
   - 분류 (Classification)   - 군집화 (Clustering)      - 에이전트, 행동, 보상 메커니즘
   - 회귀 (Regression)       - 차원 축소 (Dimensionality) - 게임 AI, 자율주행, RLHF
```

| 유형 | 데이터 형태 | 대표 과제 | 실무 사례 |
| :--- | :--- | :--- | :--- |
| **지도학습** | 입력 $X$ + 정답 $y$ | 분류, 회귀 | 고객 이탈 예측(분류), 내일의 매출액 예측(회귀) |
| **비지도학습** | 입력 $X$만 존재 | 군집, 차원 축소 | 고객 세그멘테이션, 고차원 데이터 시각화, 이상 거래 탐지 |
| **강화학습** | 상태(S), 행동(A), 보상(R) | 최적 정책(Policy) 학습 | 알파고, 추천 시스템 정책 최적화, LLM 인간 피드백 학습(RLHF) |

---

## 3. 실무 필수 지도학습 알고리즘 심층 해부

### 3.1 선형 회귀 (Linear Regression) & 로지스틱 회귀 (Logistic Regression)

#### 1) 선형 회귀 (Linear Regression)
* **목적**: 독립 변수 $X$와 연속형 종속 변수 $y$ 간의 선형 상관관계를 모델링.
* **수학적 모델**:
  $$\hat{y} = w_1 x_1 + w_2 x_2 + \dots + w_n x_n + b = W^T X + b$$
* **학습 목표**: 예측값과 실제값의 차이인 **잔차제곱합(MSE: Mean Squared Error)**을 최소화하는 최적의 가중치 $W$를 찾음.
* **정규화 모델**:
  - **Ridge (L2 정규화)**: 가중치 제곱합 패널티 추가 ($MSE + \alpha \sum w_i^2$). 가중치를 0에 가깝게 줄여 다중공선성 완화.
  - **Lasso (L1 정규화)**: 가중치 절댓값 패널티 추가 ($MSE + \alpha \sum |w_i|$). 불필요한 특성의 가중치를 완전히 0으로 만들어 자동 특성 선택(Feature Selection) 효과.

#### 2) 로지스틱 회귀 (Logistic Regression)
* **목적**: 이름은 '회귀'지만 **이진 분류(Binary Classification)**를 수행하는 핵심 알고리즘.
* **동작 원리**: 선형 회귀 결과($z = W^T X + b$)를 0과 1 사이의 확률값으로 변환하기 위해 **시그모이드 함수(Sigmoid Function)**를 통과시킵니다.
  $$\sigma(z) = \frac{1}{1 + e^{-z}}$$
* **손실 함수**: **이진 교차 엔트로피(Binary Cross-Entropy / Log Loss)**를 최소화하도록 경사하강법으로 학습.
* **실무 특징**: 연산이 매우 가볍고, 각 특성(Feature)의 회귀 계수(Odds Ratio)를 통해 **"어떤 변수가 예측에 긍정적/부정적 영향을 미쳤는지 명확하게 설명(Explainable)"**할 수 있어 금융/의료계의 베이스라인 모델로 필수 사용됩니다.

---

### 3.2 결정 트리 (Decision Tree)
* **멘탈 모델**: 스무고개 놀이. 데이터를 가장 잘 순수하게(Pure) 나누는 질문을 재귀적으로 찾아 트리를 분기.
* **분기 기준 (불순도 지표)**:
  - **지니 계수 (Gini Impurity)**: $1 - \sum p_i^2$. 0에 가까울수록 순수함(한 클래스만 모임). Scikit-Learn의 기본값.
  - **엔트로피 (Entropy / Information Gain)**: $-\sum p_i \log_2(p_i)$. 정보의 무질서도 측정.
* **장점**: 스케일링/정규화 같은 전처리가 거의 필요 없고 직관적임.
* **치명적 단점**: 트리가 깊어지면 학습 데이터를 통째로 외워버리는 **과적합(Overfitting)**에 극도로 취약함 $\rightarrow$ 이를 해결하기 위해 **앙상블(Ensemble)**이 탄생!

---

### 3.3 앙상블 기법 (Ensemble): 배깅(Bagging) vs 부스팅(Boosting)

앙상블은 여러 개의 약한 학습기(Weak Learner: 주로 얕은 결정 트리)를 결합하여 단일 모델보다 훨씬 강력하고 일반화된 예측기를 만드는 기술입니다.

```
[배깅 (Bagging - 병렬 학습)]
  데이터셋 ──► 부트스트랩 샘플 1 ──► 트리 1 ──┐
          ──► 부트스트랩 샘플 2 ──► 트리 2 ──┼──► 투표(Voting) / 평균(Averaging)
          ──► 부트스트랩 샘플 N ──► 트리 N ──┘

[부스팅 (Boosting - 순차적 학습)]
  데이터셋 ──► 트리 1 ──(오차 계산)──► 트리 2 (오차 집중) ──(오차 계산)──► 트리 N ──► 최종 가중합
```

#### 1) 랜덤 포레스트 (Random Forest - 배깅의 대표)
* **원리**: 데이터를 복원 추출(Bootstrap Sampling)하여 수백 개의 서로 다른 결정 트리를 병렬로 훈련한 뒤, 결과를 다수결 투표(분류) 또는 평균(회귀)으로 종합.
* **특성 무작위성(Feature Randomness)**: 분기 시 전체 특성이 아닌 무작위로 선택된 일부 특성($\sqrt{N}$)만 고려하여 트리들 간의 상관관계를 낮춤(분산 감소 $\rightarrow$ 과적합 방어력 최상).

#### 2) 부스팅 3대장 (Boosting - 실무 머신러닝의 절대 강자)
이전 트리가 틀린 오차(Residual)를 다음 트리가 집중적으로 보정해 나가는 순차적 학습 방식입니다.

| 알고리즘 | 동작 방식 및 특징 | 실무 평가 |
| :--- | :--- | :--- |
| **XGBoost (Extreme Gradient Boosting)** | - 결측치 자동 처리, 트리 가지치기(Pruning), L1/L2 규제 내장<br>- 병렬 CPU 연산 지원으로 기존 GBM 대비 압도적 속도 개선 | 캐글(Kaggle) 및 실무에서 검증된 정형 데이터의 든든한 기준점 |
| **LightGBM** | - **Leaf-wise(리프 중심)** 트리 분할 방식 (깊이보다 손실을 가장 많이 줄이는 리프 탐색)<br>- 히스토그램 기반 빈(Bin) 분할로 **XGBoost 대비 학습 속도와 메모리 효율이 압도적** | 수십만 행 이상의 대규모 데이터셋에서 1순위로 채택 |
| **CatBoost** | - **범주형(Categorical) 변수**를 원-핫 인코딩 없이 타깃 통계 기반으로 자동 처리<br>- 대칭 트리(Symmetric Tree) 구조로 추론(Serving) 속도가 매우 빠름 | 문자열/범주형 범주가 많은 실무 비즈니스 데이터에 최적 |

---

### 3.4 서포트 벡터 머신 (SVM) & k-최근접 이웃 (KNN)

#### 1) 서포트 벡터 머신 (SVM: Support Vector Machine)
* **핵심 원리**: 두 클래스 사이의 거리인 **마진(Margin)**을 최대화하는 최적의 결정 경계(초평면, Hyperplane)를 찾는 알고리즘.
* **서포트 벡터**: 경계면에 가장 가까이 붙어있는 경계선 결정 데이터 포인트들.
* **커널 트릭 (Kernel Trick)**: 저차원에서 선형 분리가 불가능한 데이터를 고차원 공간으로 매핑(RBF 커널, 다항 커널 등)하여 선형 분리가 가능하게 만드는 수학적 기법.

#### 2) k-최근접 이웃 (KNN: k-Nearest Neighbors)
* **핵심 원리**: 새로운 데이터가 들어왔을 때, 기존 데이터 중 가장 가까운 거리(유클리디안 등)에 있는 $k$개의 이웃을 확인하고 다수결로 판정.
* **특징**: 별도의 학습(Training) 과정이 없고 추론 시점에 거리를 계산하는 게으른 학습(Lazy Learning). 데이터가 많아지면 추론이 느려짐.

---

## 4. 실무 필수 비지도학습 알고리즘 심층 해부

### 4.1 K-Means 클러스터링
* **원리**: 데이터를 사전 정의된 $K$개의 군집(Cluster)으로 묶는 알고리즘.
  1. 무작위로 $K$개의 중심점(Centroid) 선정
  2. 모든 데이터를 가장 가까운 중심점에 할당
  3. 할당된 데이터들의 평균 위치로 중심점 재계산
  4. 중심점이 더 이상 변하지 않을 때까지 2~3 반복
* **최적의 K 찾기**: 군집 내 오차제곱합(Inertia) 감소폭이 완만해지는 지점을 찾는 **엘보우 기법(Elbow Method)**과 **실루엣 점수(Silhouette Score)** 활용.

### 4.2 주성분 분석 (PCA: Principal Component Analysis)
* **원리**: 데이터의 분산(Variance, 정보량)을 가장 잘 보존하는 새로운 축(주성분)을 찾아 고차원 데이터를 저차원으로 축소하는 기법.
* **실무 활용**:
  1. 수백 개의 특성을 2~3개 축으로 축소하여 2D/3D 산점도 시각화
  2. 다중공선성(Multicollinearity) 제거 및 노이즈 필터링
  3. 모델 학습 속도 획기적 단축

---

## 5. 실무 엔드투엔드 파이프라인 코드 (Scikit-Learn & LightGBM)

실무에서는 전처리와 모델 학습을 따로 하지 않고, **`Pipeline`**으로 묶어 데이터 누수를 원천 차단하고 재현성을 확보합니다:

```python
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from lightgbm import LGBMRegressor
from sklearn.metrics import root_mean_squared_error, r2_score

# 1. 데이터 로드
housing = fetch_california_housing(as_frame=True)
X, y = housing.data, housing.target

# 2. 데이터 분리 (반드시 전처리 전에 분리!)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. 전처리 + 모델을 하나의 통합 파이프라인으로 구성
pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),  # 결측치 중앙값 대체
    ('scaler', StandardScaler()),                  # 표준 정규화
    ('model', LGBMRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        random_state=42,
        verbosity=-1
    ))
])

# 4. K-Fold 교차 검증 (Cross-Validation)으로 안정적인 성능 검증
kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=kf, scoring='r2')
print(f"5-Fold CV R2 Score: {np.mean(cv_scores):.4f} (±{np.std(cv_scores):.4f})")

# 5. 최종 학습 및 테스트셋 평가
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

print(f"Test RMSE: {root_mean_squared_error(y_test, y_pred):.4f}")
print(f"Test R2 Score: {r2_score(y_test, y_pred):.4f}")
```

---

## 6. 모델 평가 지표 & 검증 전략 치트시트

### 6.1 분류(Classification) 평가 지표

| 지표 | 공식 | 핵심 의미 및 실전 용도 |
| :--- | :--- | :--- |
| **Accuracy (정확도)** | $\frac{TP+TN}{TP+TN+FP+FN}$ | 전체 중 정답 비율. 클래스 비율이 5:5일 때만 유효. |
| **Precision (정밀도)** | $\frac{TP}{TP+FP}$ | 모델이 양성(1)이라 한 것 중 진짜 양성. **스팸메일, 추천 시스템**에 중요. |
| **Recall (재현율/민감도)**| $\frac{TP}{TP+FN}$ | 실제 양성 중 모델이 탐지해낸 비율. **암 진단, 금융 이상거래(FDS)**에 생명. |
| **F1-Score** | $2 \times \frac{Precision \times Recall}{Precision + Recall}$ | 정밀도와 재현율의 조화평균. **불균형 데이터 평가의 사실상 표준**. |
| **ROC-AUC** | ROC 곡선 아래 면적 (0~1) | 임계값(Threshold) 변화에 무관한 분류기의 판별 잠재력 (0.8 이상 우수). |

### 6.2 회귀(Regression) 평가 지표
- **MAE (Mean Absolute Error)**: 절대 오차의 평균. 이상치(Outlier)에 강건함.
- **MSE / RMSE (Root Mean Squared Error)**: 오차를 제곱하여 평균. 큰 오차에 강한 패널티를 부여하므로 실무에서 기본 채택.
- **R² (결정계수, 0~1)**: 독립변수가 종속변수의 분산을 얼마나 설명하는지 비율 (1에 가까울수록 완벽).

---

## 7. 주니어가 실무에서 가장 많이 하는 실수 Top 4 & 회피법

1. **데이터 누수 (Data Leakage)의 함정**
   - 테스트셋이나 교차검증 폴드(Fold)의 정보가 전처리(스케일러, 인코더, 결측치 대체기)를 통해 모델에 유출되는 현상.
   - **해결책**: 반드시 Scikit-Learn의 `Pipeline`을 사용하여 교차검증 내부에서 폴드별로 `fit`과 `transform`이 독립 수행되도록 설계하세요.

2. **클래스 불균형(Class Imbalance) 방치**
   - 사기 거래 탐지처럼 정상 99.9%, 사기 0.1%인 데이터에서 모델을 돌리면 무조건 "정상"만 뱉는 쓰레기 모델이 나옵니다.
   - **해결책**: 
     - LightGBM/XGBoost의 `scale_pos_weight` 옵션 활용
     - SMOTE(오버샘플링) 적용
     - 평가지표로 Accuracy를 완전히 배제하고 F1-Score / PR-AUC 사용

3. **특성 공학(Feature Engineering) 소홀히 하고 하이퍼파라미터 튜닝만 매달리기**
   - "쓰레기를 넣으면 쓰레기가 나온다 (Garbage In, Garbage Out)". 파라미터 튜닝으로 얻는 성능 향상은 1~2%이지만, 좋은 도메인 특성 하나(날짜에서 요일 추출, 비율 변수 생성 등)가 성능을 10~20% 끌어올립니다.

4. **과적합(Overfitting) 발생 시 모델 복잡도만 올리기**
   - Train 점수는 높은데 Test 점수가 낮다면 모델이 데이터를 외우고 있는 것입니다.
   - **해결책**: 트리의 깊이(`max_depth`)를 줄이고, `min_child_weight`를 높이며, 조기 종료(`early_stopping_rounds`)를 적용하세요.
