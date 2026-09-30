# 🧠 딥러닝(Deep Learning) 핵심 실무 가이드 (Perceptron to Transformer)

> **작성자**: 시니어 개발자  
> **대상**: 딥러닝의 기저 수학과 신경망 동작 메커니즘을 확실하게 정립하고, 현대 생성형 AI(LLM, Vision)의 뼈대를 이해하려는 주니어 개발자  
> **목표**: 단일 퍼셉트론부터 최신 트랜스포머(Transformer) 아키텍처까지 인공신경망의 진화 과정을 한눈에 꿰뚫고, PyTorch 기반 실무 코드를 자유자재로 작성한다.

---

## 1. 퍼셉트론(Perceptron)과 인공신경망의 탄생

### 1.1 단층 퍼셉트론 (Single-Layer Perceptron)
1958년 프랑크 로젠블랫이 고안한 인간 뇌의 뉴런을 모방한 가장 단순한 수학적 모델입니다.
- **구조**: 여러 입력 신호($x_1, x_2, \dots$)에 각각의 중요도인 가중치($w_1, w_2, \dots$)를 곱한 후, 편향($b$)을 더해 임계값을 넘으면 1, 넘지 못하면 0을 출력합니다.
  $$y = f\left(\sum_{i=1}^{n} w_i x_i + b\right)$$

### 1.2 인공지능의 첫 번째 겨울: XOR 문제와 선형 분리의 한계
단층 퍼셉트론은 `AND`, `OR` 연산처럼 직선 하나(선형 분리)로 나눌 수 있는 문제는 쉽게 풀었습니다.  
하지만 **`XOR` 연산(두 입력이 서로 다를 때만 1)**은 직선 하나로 참과 거짓을 나눌 수 없는 치명적인 한계가 있었습니다 (1969년 마빈 민스키의 증명).

```
   [AND 연산 (선형 분리 가능)]             [XOR 연산 (직선 하나로 분리 불가!)]
      X2                                      X2
      ▲                                       ▲
    1 │   ○ (0,1)   ● (1,1)                 1 │   ● (0,1)   ○ (1,1)
      │          ＼ (직선으로 분리)            │          ？
    0 │   ○ (0,0)   ○ (1,0)                 0 │   ○ (0,0)   ● (1,0)
      └──────────────► X1                     └──────────────► X1
        0         1                             0         1
```

---

## 2. 다층 퍼셉트론(MLP)과 비선형 활성화 함수

### 2.1 다층 퍼셉트론 (MLP: Multi-Layer Perceptron)
XOR 문제를 해결한 열쇠는 **입력층과 출력층 사이에 은닉층(Hidden Layer)을 추가**하는 것이었습니다. 은닉층을 여러 개 쌓음으로써 공간을 왜곡하고 휘게 만들어 복잡한 비선형 결정 경계를 그릴 수 있게 되었습니다.

### 2.2 비선형 활성화 함수 (Activation Function)
은닉층을 아무리 수백 개 쌓아도, 각 노드가 단순 선형 결합($W_2(W_1 X + b_1) + b_2 = W_{new} X + b_{new}$)만 수행한다면 이는 결국 하나의 거대한 선형 모델과 동일합니다.  
**신경망에 "비선형성(Non-linearity)"을 불어넣어 무한히 복잡한 함수를 근사할 수 있게 해주는 장치가 바로 활성화 함수**입니다.

| 활성화 함수 | 수식 및 특징 | 단점 / 실무 평가 |
| :--- | :--- | :--- |
| **Sigmoid** | $\sigma(z) = \frac{1}{1 + e^{-z}}$ (출력: 0~1) | 입력이 크거나 작으면 미분값이 0이 되는 **기울기 소실(Vanishing Gradient)** 발생 $\rightarrow$ 은닉층 사용 금지, 이진 분류 출력층에만 사용 |
| **Tanh** | $\tanh(z) = \frac{e^z - e^{-z}}{e^z + e^{-z}}$ (출력: -1~1) | 중심이 0(Zero-centered)이라 시그모이드보단 낫지만, 여전히 양 끝단에서 기울기 소실 발생 |
| **ReLU** | $f(z) = \max(0, z)$ | **(현대 딥러닝의 기본 표준)** 연산이 단순하고 양수 영역에서 기울기가 항상 1이므로 기울기 소실 완벽 해결 |
| **Leaky ReLU** | $f(z) = \max(0.01z, z)$ | 음수 영역에서 뉴런이 영구히 죽는 "Dying ReLU" 현상을 방지하기 위해 작은 음수 기울기 허용 |
| **GELU** | $z \cdot \Phi(z)$ (가우시안 오차 선형 유닛) | 입력값을 확률적으로 드롭아웃시키는 효과. **BERT, GPT 등 최신 Transformer/LLM의 표준** |

---

## 3. 딥러닝 학습 메커니즘 4단계 심층 해부

```
  ┌──────────────┐      ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
  │  1. 순전파   │ ──►  │ 2. 손실 계산 │ ──►  │  3. 역전파   │ ──►  │  4. 최적화   │
  │(Forward Pass)│      │(Loss Compute)│      │ (Backprop)   │      │(Optimization)│
  └──────────────┘      └──────────────┘      └──────────────┘      └──────────────┘
    예측값 산출             오차 크기 측정        기울기(Gradient)      가중치(W) 수정
                                                 역방향 전파           (Adam 등)
```

### 3.1 순전파 (Forward Propagation)
- 입력 데이터가 각 레이어를 거치며 선형 변환($Z = W \cdot X + b$)과 비선형 활성화($A = f(Z)$)를 거쳐 최종 출력층까지 전달되어 예측값 $\hat{y}$를 생성하는 과정.

### 3.2 손실 계산 (Loss Function)
정답 $y$와 모델의 예측값 $\hat{y}$의 차이를 단일 스칼라 숫자로 수치화합니다.
- **회귀 문제**: 평균제곱오차 (**MSE: Mean Squared Error**)
  $$MSE = \frac{1}{N} \sum (y - \hat{y})^2$$
- **이진 분류 문제**: 이진 교차 엔트로피 (**BCE: Binary Cross-Entropy**)
  $$BCE = -\frac{1}{N} \sum [y \log(\hat{y}) + (1-y) \log(1-\hat{y})]$$
- **다중 클래스 분류 문제**: 범주형 교차 엔트로피 (**CCE: Categorical Cross-Entropy**)
  $$CCE = -\sum y_i \log(\hat{y}_i)$$

### 3.3 역전파 (Backpropagation)
- **개념**: "최종 손실(Loss)을 줄이려면 신경망 수억 개의 가중치 중 어떤 녀석을 얼마나 수정해야 하는가?"를 수학적으로 계산하는 알고리즘.
- **원리**: 미적분의 **연쇄 법칙(Chain Rule)**을 사용하여 출력층에서부터 거꾸로 은닉층, 입력층 방향으로 거슬러 올라가며 각 가중치에 대한 손실 함수의 편미분값(Gradient, $\frac{\partial Loss}{\partial W}$)을 계산합니다.
- **기울기 소실(Vanishing Gradient)**: 층이 너무 깊어지면 역전파 과정에서 작은 소수점(0.2, 0.1 등)이 계속 곱해져 입력층 쪽으로 갈수록 기울기가 0에 수렴하여 학습이 멈추는 현상 (ReLU, Residual Connection, LayerNorm 등으로 극복).

### 3.4 최적화 (Optimization) 알고리즘의 진화

기울기(Gradient)를 구했다면, 그 반대 방향으로 가중치를 업데이트해야 합니다.

```
경사하강법 (GD) ──► 확률적 경사하강법 (SGD) ──► Momentum (관성 부여)
                                               │
                                               ▼
                              RMSProp (보폭 적응) ──► Adam (Momentum + RMSProp)
```

1. **SGD (Stochastic Gradient Descent)**: 전체 데이터가 아닌 미니 배치(Mini-batch)만으로 빠르게 기울기를 계산하여 업데이트.
2. **Momentum**: 과거의 관성(속도)을 기억하여 안장점(Saddle Point)과 협곡을 빠르게 탈출.
3. **RMSProp**: 많이 변화한 파라미터는 보폭을 줄이고, 덜 변화한 파라미터는 보폭을 넓히는 적응형 학습률(Adaptive Learning Rate).
4. **Adam (Adaptive Moment Estimation)**: **(실무 점유율 90% 이상의 사실상 표준)** Momentum의 방향성과 RMSProp의 적응형 보폭을 모두 결합하여 어떤 문제에서든 안정적이고 빠른 수렴을 제공.

---

## 4. 대표 아키텍처 4대장 심층 해부

### 4.1 CNN (Convolutional Neural Network) - 이미지/공간 데이터의 정복자
기존 MLP에 2D 이미지를 1차원으로 펴서 넣으면 픽셀 간의 공간적 인접성(Spatial Information)이 완전히 파괴됩니다. CNN은 이를 방지하기 위해 탄생했습니다.

```
[입력 이미지]        [합성곱 필터 (Kernel)]          [피처 맵 (Feature Map)]
 3x3 픽셀              2x2 필터                       2x2 특징 맵
 [ 1  2  3 ]           [ 1  0 ]         합성곱 연산     [ 3   7 ]
 [ 0  1  4 ]     *     [ 0  1 ]      ───────────────►  [ 4   8 ]
 [ 5  3  2 ]
```

* **합성곱(Convolution)**: 이미지 위를 작은 필터(Kernel: $3\times3$, $5\times5$)가 슬라이딩하면서 국소적인 특징(선, 코너, 질감)을 추출.
* **패딩(Padding)**: 외곽에 0을 채워 출력 피처맵의 크기가 줄어드는 것을 방지(`padding='same'`).
* **스트라이드(Stride)**: 필터가 한 번에 이동하는 보폭 크기.
* **풀링(Pooling)**: 중요한 특징만 남기고 가로세로 크기를 압축(주로 `MaxPool2d` 사용)하여 연산량 감소 및 위치 불변성 확보.

---

### 4.2 RNN (Recurrent Neural Network) - 순차/시계열 데이터의 시작
자연어, 주가, 음성처럼 **"앞뒤 순서가 중요한 시퀀스(Sequence) 데이터"**를 다루기 위해 자기 자신을 순환하는 구조를 가집니다.

* **은닉 상태 (Hidden State, $h_t$)**: $t$ 시점의 입력 $x_t$와 이전 시점의 기억 $h_{t-1}$을 함께 입력받아 새로운 기억 $h_t$를 갱신합니다.
* **치명적 한계 (장기 의존성 문제, Long-Term Dependency)**:
  - 문장이 조금만 길어져도(50단어 이상) 시간 축을 따라 역전파(BPTT)가 진행되면서 기울기가 소실되거나 폭발하여, **문장 앞부분의 정보를 완전히 잊어버리는 치명적 기억 상실증**에 걸립니다.

---

### 4.3 LSTM (Long Short-Term Memory) - 장기 기억의 보존
RNN의 장기 기억 상실증을 해결하기 위해 1997년 제프리 힌튼 제자 슈미트후버가 고안한 모델입니다.  
컨베이어 벨트처럼 정보를 온전히 전달하는 **셀 상태(Cell State, $C_t$)**를 두고, 이를 3개의 게이트(Gate)로 정밀 제어합니다.

```
                    ┌─────────────────────────┐
      Cell State:   │ Ct-1 ──────────[x]──────(+)────────► Ct
                    │                 ▲        ▲
                    │          ┌──────┘        │
      Hidden State: │ ht-1 ──┬─┴─┐      ┌──────┴─┐
                    │        │ f │      │ i │ C~ │    [o] ──► ht
                    │        └───┘      └────────┘     ▲
      Input:        │  xt ───┴──────────┴──────────────┘
                    └─────────────────────────┘
```

1. **망각 게이트 (Forget Gate, $f_t$)**: 이전 기억 중 버릴 정보의 비율(0~1) 결정.
2. **입력 게이트 (Input Gate, $i_t$ & $\tilde{C}_t$)**: 현재 들어온 새로운 정보 중 기억할 내용을 선별하여 셀 상태에 더함.
3. **출력 게이트 (Output Gate, $o_t$)**: 갱신된 셀 상태를 바탕으로 다음 단계로 내보낼 은닉 상태($h_t$) 결정.
*(참고: GRU는 LSTM의 셀 상태와 은닉 상태를 하나로 통합하여 연산량을 줄인 경량화 버전)*

---

### 4.4 Transformer (트랜스포머) - 현대 AI의 제왕 (LLM의 모태)

2017년 구글의 역사적인 논문 *"Attention Is All You Need"*에서 발표된 구조로, **현재 ChatGPT, Claude, Gemini 등 모든 거대언어모델(LLM)과 최신 Vision 모델의 근간**입니다.

#### 1) 왜 RNN/LSTM을 완전히 대체했는가?
- RNN/LSTM은 순차적으로 단어를 하나씩 읽어야 해서 **GPU를 통한 병렬 연산(Parallelization)이 불가능**했습니다.
- 트랜스포머는 문장 전체를 한 번에 입력받고, 단어들 간의 관계를 단번에 계산하여 **학습 속도와 모델 확장성(Scalability)을 비약적으로 끌어올렸습니다**.

#### 2) Self-Attention의 마법: Query, Key, Value ($Q, K, V$)
문장 안의 각 단어가 문장 내 다른 모든 단어와 얼마나 깊은 연관이 있는지를 계산합니다. (예: "그 동물은 피곤해서 길을 건너지 않았다. **그것(It)**은 너무 지쳤기 때문이다"에서 '그것'이 '동물'을 가리킨다는 것을 Attention이 잡아냄)

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}}\right) V$$

- **Query ($Q$)**: "내가 찾고자 하는 정보의 질문" (검색창 검색어)
- **Key ($K$)**: "각 단어가 가진 식별용 라벨" (동영상 제목/태그)
- **Value ($V$)**: "그 단어가 담고 있는 실제 의미 내용" (동영상 본문 내용)
- **$\sqrt{d_k}$로 나누는 이유 (Scaled)**: 차원이 커질수록 내적 결과값이 너무 커져 Softmax 함수의 미분값이 0에 가까워지는 것을 방지.

#### 3) 트랜스포머의 핵심 구성 요소
- **Multi-Head Attention**: 여러 개의 Attention을 병렬로 수행하여, 문장의 문법적 관계, 의미적 관계, 맥락적 관계를 다양한 각도에서 동시에 포착.
- **Positional Encoding (위치 인코딩)**: 문장을 한 번에 병렬로 집어넣기 때문에 사라진 "단어의 순서 정보"를 삼각함수(Sin/Cos) 좌표로 더해줌.
- **Residual Connection & Layer Normalization**: 수백 개 층을 쌓아도 기울기가 죽지 않도록 스킵 연결과 정규화를 적용.

---

## 5. 실무 PyTorch 구현 예제

### 5.1 CNN 기반 이미지 분류기 표준 구조

```python
import torch
import torch.nn as nn

class ConvNet(nn.Module):
    def __init__(self, num_classes=10):
        super(ConvNet, self).__init__()
        # 특징 추출 블록 (Feature Extractor)
        self.features = nn.Sequential(
            # [Batch, 3, 32, 32] -> [Batch, 32, 32, 32]
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            # [Batch, 32, 32, 32] -> [Batch, 32, 16, 16]
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            # [Batch, 32, 16, 16] -> [Batch, 64, 16, 16]
            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            # [Batch, 64, 16, 16] -> [Batch, 64, 8, 8]
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        # 최종 분류기 (Classifier)
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 8 * 8, 128),
            nn.ReLU(),
            nn.Dropout(p=0.5), # 과적합 방지
            nn.Linear(128, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x
```

---

### 5.2 Transformer Self-Attention 블록의 수학적 구현

```python
import math
import torch
import torch.nn as nn

class ScaledDotProductAttention(nn.Module):
    def __init__(self, d_k):
        super().__init__()
        self.scale = 1.0 / math.sqrt(d_k)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, Q, K, V, mask=None):
        # 1. Q와 K의 전치 행렬 내적: [Batch, Seq_len, Seq_len]
        scores = torch.matmul(Q, K.transpose(-2, -1)) * self.scale
        
        # 2. 마스킹 (디코더에서 미래 단어 가릴 때 사용)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
            
        # 3. Softmax 확률화
        attn_weights = self.softmax(scores)
        
        # 4. Value와 곱하여 가중합 산출
        output = torch.matmul(attn_weights, V)
        return output, attn_weights
```

---

## 6. 딥러닝 실무 안정화 기법 (과적합 & 학습 불안정 격파)

| 기법 | 동작 원리 | 효과 |
| :--- | :--- | :--- |
| **Dropout** | 학습 시 무작위로 일정 비율(예: 30%)의 뉴런을 꺼버림 | 특정 뉴런에 과도하게 의존하는 공동 적응(Co-adaptation) 방지 |
| **Batch Normalization (BN)** | 미니배치 단위로 평균과 분산을 구해 활성화 값을 정규화 | 주로 **CNN**에서 기울기 소실 방지 및 학습 속도 극대화 |
| **Layer Normalization (LN)** | 각 샘플의 채널/특성 차원 전체에 걸쳐 정규화 수행 | 배치 크기에 구애받지 않으며 **RNN 및 Transformer/LLM의 표준** |
| **Learning Rate Scheduler** | 학습 초기엔 높은 lr로 가다가 점차 lr을 줄임 (Cosine Annealing 등) | 최적의 전역 최솟값(Global Minimum)에 부드럽게 안착 |
| **Early Stopping** | 검증 손실(Validation Loss)이 N회 이상 개선되지 않으면 학습 자동 중단 | 과적합 되기 직전의 최적 모델 체크포인트 자동 보존 |

---

## 7. 주니어가 실무에서 가장 많이 하는 딥러닝 실수 Top 4

1. **학습 모드(`train()`)와 평가 모드(`eval()`) 전환 누락**
   - `model.eval()`을 호출하지 않고 테스트를 돌리면, Dropout과 BatchNorm이 테스트 데이터에도 무작위로 적용되어 추론 결과가 뒤죽박죽이 됩니다.
   - **해결책**: 검증 및 추론 시에는 반드시 `model.eval()`과 `with torch.no_grad():`를 세트로 사용하세요.

2. **CrossEntropyLoss에 Softmax를 이중으로 씌우는 실수**
   - PyTorch의 `nn.CrossEntropyLoss()`는 내부적으로 `LogSoftmax`와 `NLLLoss`를 이미 포함하고 있습니다.
   - 모델 마지막 레이어에 또 `nn.Softmax()`를 넣으면 이중 확률화가 되어 역전파 기울기가 망가집니다.

3. **CUDA Out of Memory (OOM) 발생 시 무작정 GPU 탓하기**
   - 배치 사이즈(Batch Size)가 너무 크거나, 이전 텐서들이 메모리 캐시에서 비워지지 않았기 때문입니다.
   - **해결책**: 배치 사이즈를 반으로 줄이고, `torch.cuda.empty_cache()`를 활용하며, 추론 시에는 불필요한 계산 그래프가 생기지 않도록 `torch.no_grad()`를 감싸세요.

4. **학습률(Learning Rate)을 0.1 같은 큰 값으로 시작해 발산시키는 실수**
   - 일반적인 딥러닝/트랜스포머 실무에서는 `1e-3`($0.001$)이나 `1e-4`($0.0001$), 파인튜닝 시에는 `1e-5` 수준의 미세한 학습률로 시작하는 것이 정석입니다.
