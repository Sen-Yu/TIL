# 📝 모의 코딩테스트 대비 요약본 (Cheat Sheet)

## 1. 자주 사용된 핵심 라이브러리 & 함수 (Python)

### 📦 `collections` (가장 중요!)
- **`deque` (BFS 필수)**
  - 리스트(`[]`)의 `pop(0)`은 O(N)이지만, `deque`의 `popleft()`는 O(1)입니다.
  - **사용법**: 
    ```python
    from collections import deque
    q = deque([start_node])
    q.append(new_node)      # 뒤에 추가
    node = q.popleft()      # 앞에서 뽑기 (BFS)
    ```
- **`Counter` (해시/빈도수 계산)**
  - 리스트 내 원소의 개수를 딕셔너리 형태로 바로 세어줍니다.
  - **사용법**: 
    ```python
    from collections import Counter
    cnt = Counter(['a', 'b', 'a', 'c']) # Counter({'a': 2, 'b': 1, 'c': 1})
    ```

### 📦 `heapq` (우선순위 큐, 최단경로)
- 파이썬의 `heapq`는 기본적으로 **최소 힙(Min Heap)**입니다. (가장 작은 값이 먼저 나옴)
- **활용 범위**: 다익스트라 최단경로, 스케줄링, K번째 최솟값/최댓값 구하기 등

#### ① 최대 힙 (Max Heap) 만들기
- 숫자: 값을 넣을 때 `-`를 붙여서 넣고, 뺄 때 다시 `-`를 붙여 원래 값으로 복구합니다.
  ```python
  import heapq
  hq = []
  heapq.heappush(hq, -10)
  heapq.heappush(hq, -5)
  max_val = -heapq.heappop(hq) # 10 (가장 큰 값이 나옴)
  ```
- 문자열: 문자열엔 `-`를 붙일 수 없으므로 아래의 `__lt__` 메서드를 활용해 부등호 방향을 뒤집은 래퍼(Wrapper) 클래스를 만듭니다.
  ```python
  class MaxString:
      def __init__(self, s): self.s = s
      def __lt__(self, other): return self.s > other.s # 핵심: 방향 반대로
  ```

#### ② 기존 리스트를 한 번에 힙으로 만들기 (`heapify`)
- 이미 데이터가 들어있는 리스트를 O(N)의 빠른 속도로 힙으로 변환합니다. 처음부터 배열을 큐에 다 넣고 시작해야 할 때 무조건 씁니다.
  ```python
  import heapq
  arr = [5, 3, 8, 1, 2]
  heapq.heapify(arr) # arr 원본 자체가 힙 구조로 바뀜
  print(heapq.heappop(arr)) # 1
  ```

#### ③ 다중 조건 정렬 (튜플 사용)
- `(우선순위1, 우선순위2, 실제 값)` 형태로 튜플을 큐에 넣으면, 파이썬은 **튜플의 첫 번째 요소부터 차례대로 비교**하여 정렬합니다.
  ```python
  import heapq
  hq = []
  # (비용, 시간, 노드 번호)
  heapq.heappush(hq, (10, 5, "A"))
  heapq.heappush(hq, (10, 2, "B"))
  heapq.heappush(hq, (5, 8, "C"))
  
  # 비용이 가장 작은 것 -> 같다면 시간이 가장 작은 것 순으로 나옴
  print(heapq.heappop(hq)) # (5, 8, 'C')
  print(heapq.heappop(hq)) # (10, 2, 'B')
  ```

#### ④ 클래스/객체 필드별 커스텀 정렬 (`__lt__` 매직 메서드)
- 특정 필드 기준으로 정렬하려면 클래스 내부에 `<` 연산자를 정의하는 `__lt__` (less than) 메서드를 구현하면 됩니다.
  ```python
  import heapq

  class Node:
      def __init__(self, name, cost, time):
          self.name = name
          self.cost = cost
          self.time = time
          
      # 우선순위 정의 (cost는 오름차순, cost가 같다면 time은 내림차순 정렬)
      def __lt__(self, other):
          if self.cost == other.cost:
              return self.time > other.time # time이 큰 쪽이 우선(앞에 오게 함)
          return self.cost < other.cost     # cost가 작은 쪽이 우선

  hq = []
  heapq.heappush(hq, Node("A", 10, 5))
  heapq.heappush(hq, Node("B", 10, 8))
  heapq.heappush(hq, Node("C", 5, 2))
  
  # C (비용 5) -> B (비용 10, 시간 8로 더 큼) -> A (비용 10, 시간 5) 순으로 나옴
  best = heapq.heappop(hq)
  print(best.name) # "C"
  ```

### 📦 `itertools` (완전탐색, 조합/순열)
- 백트래킹이나 직접 구현하기 귀찮을 때 유용합니다.
- **`permutations(순열)`**: 순서를 고려하여 뽑기 (`(A, B) != (B, A)`)
- **`combinations(조합)`**: 순서를 고려하지 않고 뽑기 (`(A, B) == (B, A)`)
  ```python
  from itertools import permutations, combinations
  list(permutations([1, 2, 3], 2)) # [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2)]
  list(combinations([1, 2, 3], 2)) # [(1,2), (1,3), (2,3)]
  ```

### 📦 `math` (수학 개념)
- **사용법**:
  ```python
  import math
  math.gcd(a, b) # 최대공약수
  math.lcm(a, b) # 최소공배수 (Python 3.9+)
  math.ceil(x)   # 올림
  ```

---

## 2. 빈출 알고리즘 및 접근법

### 🔍 1) BFS / DFS (그래프 탐색) 총정리

#### ① 언제 무엇을 쓸까? (BFS vs DFS)
- **BFS (너비 우선 탐색)**: 
  - **사용처**: **최단 거리** 구하기 (가중치가 모두 1일 때), 미로 찾기.
  - **특징**: `collections.deque` 사용. 출발지점에서 가까운 곳부터 퍼져나가므로 도착지점에 도달하는 순간이 무조건 최단거리입니다.
  - **핵심 아이디어**: 도착점 -> 여러 출발점의 최단거리를 잴 때는 목적지에서 거꾸로 BFS를 한 번만 돌리는 것이 효율적입니다. (부대복귀 문제)
- **DFS (깊이 우선 탐색)**:
  - **사용처**: **백트래킹** (모든 경우의 수/경로 탐색), 맵의 끊어진 영역 개수 세기.
  - **특징**: 하나의 경로를 끝까지 파고든 다음 돌아옵니다.

#### ② DFS 구현 방식 선택 (재귀 vs 반복문)
- **재귀(Recursion) 기반**:
  - **사용처**: **코딩테스트의 90% 이상**. 백트래킹이나 경로를 저장하고 되돌려야 할 때 구현이 압도적으로 직관적입니다.
  - **주의점**: 파이썬은 재귀 깊이 제한이 있으므로 상단에 `sys.setrecursionlimit(10**6)` 선언을 추천합니다.
- **반복문(Stack) 기반**:
  - **사용처**: 트리의 깊이나 노드 개수가 1만 개 이상이어서 재귀 한도를 늘려도 터질 위험이 있을 때.
  - **특징**: 상태를 되돌리는 백트래킹 구현이 매우 까다롭지만, 단순 영역 개수 세기/연결 확인에서는 에러로부터 안전합니다.

#### ③ 그래프 표현 방식 선택 (인접 행렬 vs 인접 리스트)
- **인접 리스트 (`graph[node] = [neighbors...]`)**:
  - **사용처**: **대부분의 그래프 문제 필수!** (특히 노드 `N`이 1,000 이상이거나 간선이 적을 때)
  - **장점**: 연결된 간선만 확인하므로 메모리와 시간(`O(N+M)`)을 크게 아낍니다.
- **인접 행렬 (`graph[i][j] = 0 or 1`)**:
  - **사용처**: 특정 두 노드 $A$와 $B$가 연결되어 있는지 즉시 `O(1)`로 확인해야 할 때, 또는 노드 수 `N`이 매우 작을 때.
  - **단점**: 연결 상태를 보려 해도 모든 노드를 스캔해야 해서 시간초과(`O(N^2)`)를 일으키는 주범입니다.

### 🧠 2) DP (Dynamic Programming)
- **언제 쓰나요?**: 이전의 결과가 다음 결과에 영향을 미치고, 점화식을 세울 수 있을 때 (ex. 최대 이익, 최단 경로 개수)
- **접근법**:
  1. `dp` 배열을 무엇으로 정의할지 생각합니다. (ex. `dp[i]` = i번째까지의 최대값)
  2. 초기값을 세팅합니다. (`dp[0], dp[1]`)
  3. `dp[i]`를 구하기 위한 점화식을 찾습니다. (`dp[i] = max(dp[i-1], dp[i-2] + arr[i])`)

### 🪟 3) 투 포인터 / 슬라이딩 윈도우
- **언제 쓰나요?**: **연속된** 부분 배열의 합, 길이 등을 구할 때 (`O(N)`에 해결 가능)
- **접근법**: 
  - `start`, `end` 두 포인터를 두고 조건을 만족하면 `end`를 늘리고, 조건을 벗어나면 `start`를 당기면서 값을 갱신합니다.

### 딕셔너리(Hash) 활용
- **언제 쓰나요?**: 값의 검색, 맵핑(ex. 마라톤 완주자, 할인 행사 등)이 잦을 때 리스트 `in` 탐색(O(N))을 피하기 위해 `dict`(O(1))를 사용합니다.

---

## 3. 자주 나오는 핵심 구현 (진수 변환, 소수 판별)

### 🧮 1) 진수 변환 (N진수)
- `int(string, base)`: n진수 문자열을 10진수 정수로 변환 (`int("101", 2)` -> 5)
- **10진수 -> N진수 변환 함수 (외워두면 편함)**:
  ```python
  def to_n_base(n, q):
      if n == 0: return '0'
      rev_base = ''
      while n > 0:
          n, mod = divmod(n, q)
          rev_base += str(mod)
      return rev_base[::-1] # 역순인 것을 뒤집어 줘야 함
  ```

### 🛡️ 2) 소수 판별 (Prime Number)
- **단일 숫자 소수 판별**: 제곱근(`math.sqrt(n)`)까지만 확인하면 O(√N)에 해결 가능.
  ```python
  import math
  def is_prime(x):
      if x < 2: return False
      for i in range(2, int(math.sqrt(x)) + 1):
          if x % i == 0:
              return False
      return True
  ```

---

## 4. 파이썬 표준 입출력 (Standard I/O) 템플릿

코딩테스트에서 시간 초과를 방지하기 위해 파일 상단에 항상 아래 세팅을 해두는 것을 권장합니다.
```python
import sys
input = sys.stdin.readline
```

### 1) 단일 변수 입력
```python
N = int(input().rstrip())
S = input().rstrip()
```

### 2) 공백으로 구분된 여러 변수
```python
N, M = map(int, input().split())
A, B, C = map(int, input().split())
```

### 3) 1차원 리스트(배열)
```python
arr = list(map(int, input().split()))
```

### 4) N줄에 걸쳐서 입력되는 1차원 배열
```python
N = int(input().rstrip())
arr = [int(input().rstrip()) for _ in range(N)] 
```

### 5) 2차원 맵 / 그래프 (공백 띄어쓰기 있음)
```python
N, M = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(N)]
```

### 6) 2차원 맵 / 그래프 (공백 없음 - 미로 탐색 등)
```python
N, M = map(int, input().split())
# 문자열 리스트로 저장: [['1','0','1','0'], ...]
graph_str = [list(input().rstrip()) for _ in range(N)]
# 정수 리스트로 저장: [[1, 0, 1, 0], ...]
graph_int = [list(map(int, input().rstrip())) for _ in range(N)]
```

### 7) 무한 입력 (EOF 처리)
```python
while True:
    try:
        A, B = map(int, input().split())
        print(A + B)
    except:
        break
```

### 8) 빠른 출력 팁
```python
arr = [1, 2, 3, 4]
print(*arr)  # 1 2 3 4
print('\n'.join(map(str, arr))) # 줄바꿈하여 한번에 출력
```
