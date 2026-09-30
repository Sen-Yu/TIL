# 🧠 머신러닝 & 딥러닝 핵심 실무 가이드 (AI 엔지니어링 입문)

> **작성자**: 시니어 개발자  
> **대상**: AI/ML 기초 지식이 필요하거나 현대 AI 서비스(LLM, 추천, 비전 등)의 기저 원리를 이해하고 싶은 주니어 개발자  
> **목표**: 룰 기반 코딩에서 머신러닝, 딥러닝으로 이어지는 패러다임 변화를 체득하고, 학습 메커니즘과 핵심 지표를 실무 수준으로 습득한다.

---

## 1. 패러다임의 진화: 왜 머신러닝과 딥러닝이 필요한가? (Why)

### 1.1 전통적 프로그래밍의 한계
과거의 소프트웨어 개발은 **개발자가 규칙(Rule)을 직접 정의**하는 방식이었습니다:
- "만약 이메일에 '무료', '대출', '당첨'이라는 단어가 3개 이상 들어가면 스팸함으로 보낸다." (`if-else`)
- **문제점**: 스팸 발송자가 "무.료", "대/출"처럼 철자를 바꾸거나 새로운 패턴을 쓰면 규칙이 깨집니다. 사람이 세상의 모든 예외 규칙을 코드로 작성하는 것은 불가능합니다.

### 1.2 패러다임의 전환: 규칙 작성에서 데이터 학습으로

```
[전통적 프로그래밍]
  규칙(Rule / Code) + 데이터(Data) ────────► 결과(Output)

[머신러닝 & 딥러닝]
  데이터(Data) + 결과(Answer / Label) ─────► 규칙(Model / Pattern) 학습!
```

---

## 2. 한눈에 비교하는 3가지 패러다임

| 구분 | 전통적 프로그래밍 | 머신러닝 (Traditional ML) | 딥러닝 (Deep Learning) |
| :--- | :--- | :--- | :--- |
| **문제 해결 방식** | 사람이 직접 로직(`if-else`) 작성 | 사람이 **특징(Feature)**을 추출하고 알고리즘이 패턴 학습 | 컴퓨터가 **특징 추출부터 예측까지 스스로(End-to-End)** 학습 |
| **대표적인 비유** | 요리사가 레시피를 한 줄씩 코딩 | 요리사가 재료의 당도·염도를 측정해 기계에 주면 기계가 맛 판별 | 재료를 통째로 넣으면 거대한 인공두뇌가 맛과 레시피를 알아서 판별 |
| **데이터 요구량** | 데이터 불필요 (로직만 필요) | 수백 ~ 수만 건으로도 우수한 성능 | 수십만 ~ 수천만 건 이상의 빅데이터 필수 |
| **하드웨어 요구사항** | 일반 CPU | 일반 CPU로도 충분 | 대량의 행렬 연산을 위한 **GPU/TPU 필수** |
| **해석 가능성 (XAI)** | 100% 명확 (디버깅 용이) | 높은 편 (어떤 특징이 결과에 영향을 주었는지 확인 가능) | 낮음 (**블랙박스**, 내부 신경망이 너무 복잡하여 원인 규명 어려움) |
| **주요 활용처** | 비즈니스 CRUD 로직 | 고객 이탈 예측, 사기 탐지(FDS), 정형 테이블 데이터 분류 | 이미지 인식, 음성 인식, 자연어 처리(LLM), 생성형 AI |

---

## 3. 머신러닝 (Machine Learning) 완벽 이해

### 3.1 머신러닝의 3대 학습 유형
1. **지도학습 (Supervised Learning) - "문제와 정답을 함께 공부"**
   - **분류 (Classification)**: 범주형 예측 (예: 암 양성/음성 판정, 스팸/정상 메일)
   - **회귀 (Regression)**: 연속된 숫자 예측 (예: 아파트 가격 예측, 내일의 기온 예측)
2. **비지도학습 (Unsupervised Learning) - "정답 없이 데이터의 군집/구조 발견"**
   - **군집화 (Clustering)**: 고객 성향별 그룹핑 (K-Means)
   - **차원 축소 (Dimensionality Reduction)**: 고차원 벡터의 시각화 및 노이즈 제거 (PCA, t-SNE)
3. **강화학습 (Reinforcement Learning) - "보상(Reward)을 최대화하는 방향으로 시행착오 학습"**
   - 알파고(바둑), 자율주행, 게임 AI, LLM 정렬(RLHF)

### 3.2 실무 필수 머신러닝 알고리즘 Top 3
- **선형 / 로지스틱 회귀 (Linear / Logistic Regression)**: 베이스라인 모델로 가장 먼저 테스트하는 가볍고 해석력 높은 모델.
- **결정 트리 / 랜덤 포레스트 (Decision Tree / Random Forest)**: `if-then` 질문을 계층적으로 던지는 트리 기반 앙상블 모델.
- **XGBoost / LightGBM**: 캐글(Kaggle)과 실무 테이블형 데이터(Tabular Data)에서 가장 강력한 성능을 내는 부스팅(Boosting) 알고리즘.

---

## 4. 딥러닝 (Deep Learning) 완벽 이해

### 4.1 멘탈 모델: 인공신경망 (Artificial Neural Network)
사람의 뇌세포(뉴런)가 신호를 받아 다음 뉴런으로 전달하는 구조를 수학적으로 모방했습니다:
- **입력층 (Input Layer)**: 데이터가 들어오는 곳 (예: 픽셀 값)
- **은닉층 (Hidden Layer)**: 데이터의 추상적인 특징을 추출하는 층 (이 층이 깊으면 "Deep" Learning)
- **출력층 (Output Layer)**: 최종 예측 값 (예: 고양이일 확률 98%)

```
  [입력층]           [은닉층 (Deep Layers)]          [출력층]
    X1 ───(가중치 W)───► [ ○ ] ───► [ ○ ] ───► [ 고양이 (0.98) ]
    X2 ───(가중치 W)───► [ ○ ] ───► [ ○ ] ───► [ 강아지 (0.02) ]
```

### 4.2 딥러닝이 동작하는 4단계 핵심 메커니즘
1. **순전파 (Forward Propagation)**: 입력 데이터를 받아 가중치($W$)와 곱하고 활성화 함수를 거쳐 최종 예측값을 계산합니다.
2. **손실 계산 (Loss Function)**: 정답(Label)과 모델의 예측값 사이의 오차(Loss)를 계산합니다 (예: MSE, Cross-Entropy).
3. **역전파 (Backpropagation)**: 오차를 출력층에서부터 거꾸로 전파하며 미분(Gradient)을 계산하여 "어떤 가중치가 오차에 얼마나 기여했는가"를 측정합니다.
4. **최적화 (Optimizer)**: 경사하강법(Gradient Descent) 기반 알고리즘(주로 **Adam**)을 통해 오차를 줄이는 방향으로 가중치를 업데이트합니다.

### 4.3 대표적인 딥러닝 아키텍처 계보
- **CNN (Convolutional Neural Network)**: 이미지/공간 데이터 특화 (필터를 통해 이미지의 윤곽선, 질감 등 공간적 특징 추출).
- **RNN / LSTM**: 시계열/순차적 데이터 특화 (과거 정보를 기억하는 루프 구조, 장기 기억 소실 문제 존재).
- **Transformer (트랜스포머)**: **현대 모든 AI(ChatGPT, Claude, BERT 등)의 근간**. Attention 메커니즘을 통해 문장 전체의 단어 간 연관성을 병렬로 단번에 파악.

---

## 5. 실무 표준 코드 예제

### 5.1 머신러닝 파이프라인 예제 (Scikit-Learn 기반 붓꽃 품종 분류)

```python
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 1. 데이터 로드 및 분리 (데이터 누수 방지를 위해 반드시 학습/테스트 분리)
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42, stratify=iris.target
)

# 2. 전처리 (정규화 / 스케일링)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # 주의: test셋에는 fit을 절대 호출하지 않음!

# 3. 모델 정의 및 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# 4. 평가
predictions = model.predict(X_test_scaled)
print(classification_report(y_test, predictions, target_names=iris.target_names))
```

---

### 5.2 딥러닝 신경망 정의 및 학습 루프 (PyTorch 표준 패턴)

```python
import torch
import torch.nn as nn
import torch.optim as optim

# 1. 다층 퍼셉트론(MLP) 신경망 정의
class SimpleClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(SimpleClassifier, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),                       # 비선형성을 부여하는 활성화 함수
            nn.Dropout(p=0.2),               # 과적합 방지
            nn.Linear(hidden_dim, output_dim)
        )

    def forward(self, x):
        return self.network(x)

model = SimpleClassifier(input_dim=10, hidden_dim=64, output_dim=2)

# 2. 손실 함수와 최적화 알고리즘(Optimizer) 설정
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 3. 딥러닝의 표준 학습 루프 (Training Loop)
epochs = 5
for epoch in range(epochs):
    model.train()  # 모델을 훈련 모드로 설정
    
    # 더미 데이터 (실무에서는 DataLoader 사용)
    inputs = torch.randn(32, 10)
    targets = torch.randint(0, 2, (32,))

    optimizer.zero_grad()            # 1) 이전 스텝의 기울기 초기화
    outputs = model(inputs)          # 2) 순전파 (예측)
    loss = criterion(outputs, targets) # 3) 손실 계산
    loss.backward()                  # 4) 역전파 (기울기 계산)
    optimizer.step()                 # 5) 가중치 업데이트

    print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
```

---

## 6. 실무 필수 용어 & 평가 지표 치트시트

### 6.1 핵심 하이퍼파라미터
- **Epoch (에포크)**: 전체 학습 데이터를 모델이 한 번 처음부터 끝까지 다 훑어본 횟수.
- **Batch Size (배치 사이즈)**: 한 번에 메모리에 올려 가중치를 업데이트할 샘플 데이터의 묶음 크기 (예: 32, 64, 128).
- **Learning Rate (학습률, lr)**: 가중치를 얼마나 큰 보폭으로 수정할 것인가를 결정하는 스텝 크기 (너무 크면 발산하고, 너무 작으면 세월아 네월아 걸림).

### 6.2 모델 평가 지표 (혼동 행렬 기반)

| 지표 | 공식 / 개념 | 실무 선택 기준 |
| :--- | :--- | :--- |
| **정확도 (Accuracy)** | 전체 중 맞춘 비율 | 데이터 클래스 비율이 50:50으로 균등할 때만 유효 |
| **정밀도 (Precision)**| 모델이 참이라고 예측한 것 중 진짜 참 | **스팸 필터링**: 정상 메일을 스팸으로 오분류하면 안 될 때 중요 |
| **재현율 (Recall)** | 실제 참인 것 중 모델이 맞춘 비율 | **암 진단, 결함 탐지**: 실제 암 환자를 놓치면 치명적일 때 중요 |
| **F1-Score** | 정밀도와 재현율의 조화 평균 | **데이터가 불균형(Imbalanced)할 때 모델 성능의 척도** |

---

## 7. 주니어가 실무에서 가장 많이 실수하는 4가지와 꿀팁

1. **데이터 누수 (Data Leakage) 발생**
   - `StandardScaler`나 인코딩을 적용할 때 `fit`을 전체 데이터셋에 먼저 해버리고 `train/test`를 쪼개는 치명적인 실수입니다. 이렇게 하면 테스트 셋의 정보(평균, 분산)가 학습에 유출되어 실서버 배포 시 성능이 폭망합니다.
   - **해결책**: 반드시 `train_test_split`을 먼저 한 뒤, **학습 셋(Train)으로만 `fit`하고 테스트 셋(Test)은 오직 `transform`만** 해야 합니다.

2. **과적합(Overfitting) 방치**
   - 모델이 학습 데이터(Train)의 사소한 노이즈까지 외워버려 Train 정확도는 99%인데 실전(Test/Prod)에서는 60%가 나오는 현상입니다.
   - **해결책**: 드롭아웃(Dropout), L2 정규화(Weight Decay), 조기 종료(Early Stopping), 데이터 증강(Augmentation)을 적용하세요.

3. **불균형 데이터에서 'Accuracy(정확도)'만 보고 만족하기**
   - 예를 들어 100건 중 99건이 정상 결제이고 1건만 사기 결제인 데이터라면, 모델이 무조건 "정상"이라고만 답해도 정확도는 99%가 나옵니다.
   - **해결책**: 불균형 데이터에서는 절대 정확도에 속지 말고 **Precision, Recall, F1-Score, PR-AUC**를 평가 척도로 삼아야 합니다.

4. **PyTorch에서 `optimizer.zero_grad()` 누락**
   - PyTorch는 메모리 효율을 위해 미분값(Gradient)을 기본적으로 누적(Accumulate)합니다. 학습 루프 안에서 `zero_grad()`를 호출하지 않으면 이전 배치의 기울기가 계속 더해져 모델 학습이 산으로 갑니다.
   - **해결책**: `outputs = model(inputs)` 또는 `loss.backward()` 직전에 반드시 `optimizer.zero_grad()`를 명시하세요.
