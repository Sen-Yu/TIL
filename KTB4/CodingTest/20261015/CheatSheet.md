# 📝 코딩테스트 대비 최종 요약본 (Cheat Sheet) - 10.15 최신판

그동안 누적된 문제 풀이(09.30 이전 내용 포함)와 최근 학습하신 **그리디(투 포인터/에이스 전략), 최소 신장 트리(프림/크루스칼/유니온 파인드), 스택 최적화(단조 스택/패턴 폭파), 그리고 코딩테스트 3대 필수 템플릿(다익스트라/이분 탐색/누적 합)**까지 완벽하게 통합한 마스터 요약본입니다. 시험 직전 그대로 복사해서 쓸 수 있도록 모든 코드에 `import`문과 구체적인 템플릿을 포함했습니다.

---

## 1. 파이썬 표준 입출력 (Standard I/O) & 필수 세팅

코딩테스트(백준, 구름, 소프티어 등)에서 직접 입출력을 다룰 때 **시간 초과와 재귀 에러 방지**를 위해 코드 최상단에 무조건 적고 시작하는 2줄입니다.

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**6) # DFS/재귀 사용 시 필수 (기본 1000 제한 해제)
```

### 1) 자주 쓰는 입력 패턴 모음
```python
N = int(input())                          # 단일 정수
S = input().rstrip()                      # 단일 문자열 (개행문자 제거 rstrip 필수!)
A, B, C = map(int, input().split())       # 띄어쓰기 된 여러 정수
arr = list(map(int, input().split()))     # 1차원 정수 리스트
graph = [list(map(int, input().split())) for _ in range(N)] # 2차원 격자 리스트
```

### 2) 무한 입력 (EOF 처리)
```python
while True:
    try:
        A, B = map(int, input().split())
        print(A + B)
    except:
        break
```

### 3) 빠른 출력 팁
출력이 많을 때는 반복문마다 `print()`를 호출하지 말고 모아서 한 번에 출력합니다.
```python
arr = [1, 2, 3, 4]
print(*arr)                     # 언패킹 출력: 1 2 3 4
print('\n'.join(map(str, arr))) # 줄바꿈하여 한 번에 출력 (속도 극대화)
```

---

## 2. 자주 사용된 핵심 라이브러리 & 함수 (Python)

### 📦 `collections` (큐 & 카운팅)
- **`deque` (BFS 필수)**: 리스트의 `pop(0)`은 $O(N)$이지만, `deque`의 `popleft()`는 $O(1)$입니다.
- **`Counter`**: 리스트/문자열 내 원소의 개수를 딕셔너리 형태로 즉시 계산합니다.
- **`defaultdict`**: 존재하지 않는 키를 조회해도 `KeyError` 없이 기본값을 자동 생성합니다.
```python
from collections import deque, Counter, defaultdict

# 1. deque 사용법
q = deque([1, 2, 3])
q.append(4)         # 뒤에 추가
node = q.popleft()  # 앞에서 뽑기 (BFS 핵심, O(1))

# 2. Counter 사용법
cnt = Counter(['a', 'b', 'a', 'c']) 
print(cnt['a'])          # 2
print(cnt.most_common(1)) # 가장 많이 등장한 [('a', 2)]

# 3. defaultdict 사용법 (그래프 인접 리스트 초기화 시 매우 유용)
graph = defaultdict(list)
graph[1].append(2)  # 키 생성 없이 바로 append 가능!
```

### 📦 `heapq` (우선순위 큐, 최단경로, 스케줄링)
파이썬은 기본적으로 **최소 힙(Min Heap)**으로 동작합니다.
```python
import heapq

# 1. 기존 리스트를 힙으로 변환 및 삽입/삭제
arr = [5, 3, 8]
heapq.heapify(arr)           # O(N)으로 한 번에 힙 변환
heapq.heappush(arr, 1)       # 원소 추가
min_val = heapq.heappop(arr) # 1 (가장 작은 값 추출)

# 2. 🔥 상위 K개만 유지하기 (명예의 전당 등)
k = 3
best = []
for score in [10, 50, 20, 40, 30]:
    heapq.heappush(best, score)
    if len(best) > k:
        heapq.heappop(best) # 크기가 k를 넘으면 가장 작은 값 버림
print(best[0]) # 현재 상위 K개 중 최솟값(커트라인) = 30

# 3. 최대 힙 (Max Heap) - 숫자 부호 반전
hq = []
heapq.heappush(hq, -10)
max_val = -heapq.heappop(hq) # 10

# 4. 튜플을 이용한 우선순위 정렬 (비용 순, 정점 번호)
pq = []
heapq.heappush(pq, (cost, next_node)) # 첫 번째 원소(cost)를 기준으로 자동 정렬
```

### 📦 `bisect` (이분 탐색 라이브러리)
정렬된 리스트에서 특정 값의 삽입 위치나 개수를 $O(\log N)$에 찾습니다.
```python
from bisect import bisect_left, bisect_right

arr = [1, 2, 4, 4, 4, 8, 9]
# 1. 값의 위치 찾기
print(bisect_left(arr, 4))   # 2 (값이 처음 나타나는 인덱스)
print(bisect_right(arr, 4))  # 5 (값보다 큰 수가 처음 나타나는 인덱스)

# 2. 특정 범위 [left_val, right_val]에 속하는 데이터 개수 구하기
def count_by_range(a, left_val, right_val):
    return bisect_right(a, right_val) - bisect_left(a, left_val)

print(count_by_range(arr, 4, 4)) # 4의 개수 = 3개
```

### 📦 `itertools` & `math`
```python
from itertools import permutations, combinations, product
import math

# 1. itertools
items = ['A', 'B', 'C']
print(list(permutations(items, 2))) # 순열 (순서 중요): [(A,B), (B,A), ...]
print(list(combinations(items, 2))) # 조합 (순서 무관): [(A,B), (A,C), (B,C)]
print(list(product([1, 2], repeat=2))) # 중복순열: [(1,1), (1,2), (2,1), (2,2)]

# 2. math
print(math.gcd(10, 15))   # 최대공약수 = 5
print(math.lcm(10, 15))   # 최소공배수 = 30 (Python 3.9+)
print(math.comb(5, 2))    # 5C2 조합의 '개수' = 10
print(math.isqrt(17))     # 정수 제곱근(내림) = 4
INF = math.inf            # 무한대 (최솟값 갱신 초기값으로 유용)
```

---

## 3. 빈출 알고리즘 및 핵심 접근법

### 🔍 1) BFS / DFS (그래프 탐색)

#### ① DFS (깊이 우선 탐색) 템플릿
- **사용처**: 백트래킹(모든 경우의 수 탐색), 분리된 영역 개수 세기.
```python
import sys
sys.setrecursionlimit(10**6)

graph = {1: [2, 3], 2: [4], 3: [], 4: []}
visited = set()

# 재귀 템플릿 (90% 이상 사용)
def dfs_recursive(node):
    visited.add(node)
    for next_node in graph[node]:
        if next_node not in visited:
            dfs_recursive(next_node)

# 스택(반복문) 템플릿 (재귀 깊이가 너무 깊어 터질 때 사용)
def dfs_stack(start_node):
    visited = set()
    stack = [start_node]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for next_node in reversed(graph[node]): # 순서 유지를 위해 reversed
                if next_node not in visited:
                    stack.append(next_node)
```

#### ② BFS (너비 우선 탐색) 템플릿
- **사용처**: 모든 간선의 가중치가 동일할 때의 최단 거리, 미로 탈출.
```python
from collections import deque

def bfs(start_node):
    visited = set([start_node])
    q = deque([start_node])
    
    while q:
        node = q.popleft()
        for next_node in graph[node]:
            if next_node not in visited:
                visited.add(next_node)
                q.append(next_node)
```

#### ③ 🔥 방향(코너) 비용이 있는 BFS (경주로 건설)
- 회전할 때 코너 비용(500원)이 드는 등 **"어떤 방향으로 진입했느냐"**에 따라 미래의 최적해가 바뀌는 경우, 2차원 배열 `visited[y][x]`로는 풀 수 없습니다.
- **해결책**: `visited[dir][y][x]` 형태의 3차원 배열을 사용하여 **"진입 방향"별로 최소 비용**을 따로 기록해야 합니다.

---

### 🧠 2) DP (Dynamic Programming)

#### ① Bottom-Up 방식 (반복문 타뷸레이션)
```python
def dp_bottom_up(n, money):
    dp = [0] * n
    dp[0] = money[0]
    dp[1] = max(money[0], money[1])
    
    for i in range(2, n):
        dp[i] = max(dp[i-1], dp[i-2] + money[i])
        
    return dp[n-1]
```

#### ② Top-Down 방식 (재귀 + `lru_cache` 꿀팁)
- 파이썬의 `@lru_cache`를 사용하면 DP 테이블 선언 없이도 결과가 자동 메모이제이션(캐싱)됩니다.
```python
from functools import lru_cache
import sys
sys.setrecursionlimit(10**6)

@lru_cache(maxsize=None)
def dp_top_down(n):
    if n == 0: return money[0]
    if n == 1: return max(money[0], money[1])
    return max(dp_top_down(n-1), dp_top_down(n-2) + money[n])
```

#### ③ 🔥 원형 배열 DP (도둑질)
- 첫 집과 마지막 집이 인접하여 동시에 선택할 수 없을 때, 문제를 2개의 직선 문제로 분할합니다.
```python
def solution_circular_dp(money):
    if len(money) == 3: return max(money)
    n = len(money)
    
    # 1. 첫 번째 집을 무조건 터는 경우 (마지막 집 n-1 제외)
    dp1 = [0] * n
    dp1[0] = dp1[1] = money[0]
    for i in range(2, n - 1):
        dp1[i] = max(dp1[i-1], dp1[i-2] + money[i])
        
    # 2. 첫 번째 집을 절대 안 터는 경우 (마지막 집 포함)
    dp2 = [0] * n
    dp2[0] = 0
    dp2[1] = money[1]
    for i in range(2, n):
        dp2[i] = max(dp2[i-1], dp2[i-2] + money[i])
        
    return max(max(dp1), max(dp2))
```

---

### 🥞 3) 스택(Stack) & 단조 스택(Monotonic Stack) 🔥 [10월 신규]

#### ① 패턴 매칭 및 연속 폭파 스택 (햄버거 만들기)
- **금기사항**: 문자열 슬라이싱 이어붙이기(`s[:l] + s[l+4:]`)는 매번 $O(N)$의 복사 비용이 들어 $O(N^2)$ 시간 초과를 유발합니다.
- **해결책**: 리스트에 순서대로 쌓다가(`append`), 끝부분(`[-4:]`)이 특정 패턴과 일치하면 끝에서만 즉시 제거(`pop` 4회)하여 $O(N)$으로 해결합니다.
```python
def solution_stack_crush(ingredient):
    answer = 0
    stack = []
    for i in ingredient:
        stack.append(i)
        if stack[-4:] == [1, 2, 3, 1]: # 특정 완성 패턴 감지
            answer += 1
            for _ in range(4):
                stack.pop()
    return answer
```

#### ② 단조 스택 (뒤에 있는 큰 수 찾기 / 오큰수)
- 배열 길이가 최대 100만일 때, "나보다 뒤에 있는 수 중 처음으로 나보다 큰 수"를 이중 루프로 찾으면 무조건 시간 초과가 발생합니다.
- **해결책**: 스택에 값이 아니라 **인덱스(`idx`)**를 저장하고, 새 숫자 `n`이 스택의 맨 위 원소보다 크면 `while`문으로 일괄 `pop`하며 정답을 갱신합니다.
```python
def solution_monotonic_stack(numbers):
    answer = [-1] * len(numbers)
    stack = [] # 인덱스를 저장하는 스택
    
    for idx, n in enumerate(numbers):
        # 스택에 대기 중인 숫자들 중 현재 숫자 n보다 작은 것들은 모두 pop하며 정답 기록
        while stack and numbers[stack[-1]] < n:
            answer[stack.pop()] = n
        stack.append(idx)
        
    return answer
```

---

### 🎯 4) 그리디(Greedy) & 투 포인터(Two Pointers) 🔥 [10월 신규]

#### ① 양 끝단 투 포인터 (구명보트)
- 정렬 후 가장 무거운 사람과 가장 가벼운 사람을 짝짓는 패턴입니다.
- **우아한 설계**: 단 한 명만 남았을 때(`left == right`)를 위한 불필요한 `if` 방어문 없이, 무거운 사람(`right`)은 매 턴 무조건 배를 타고, 탈 수 있을 때만 가벼운 사람(`left`)을 전진시키면 루프 조건(`while left <= right`)에 의해 완벽하게 자동 처리됩니다.
```python
def solution_boat(people, limit):
    answer = 0
    people.sort()
    left, right = 0, len(people) - 1
    
    while left <= right:
        if people[left] + people[right] <= limit:
            left += 1   # 가벼운 사람 탑승
        right -= 1      # 무거운 사람은 무조건 탑승
        answer += 1     # 보트 출발
        
    return answer
```

#### ② 에이스 맞대결 & 포인터 지연 진행 (숫자 게임)
- A팀의 큰 카드를 B팀의 카드로 이겨야 할 때:
  1. 두 팀 모두 내림차순(`reverse=True`)으로 정렬합니다.
  2. B팀의 에이스 카드(`B[left]`)가 A를 이길 수 있다면 승점 획득 후 `left += 1`.
  3. **못 이긴다면**: `left`를 그대로 멈춰두고 A만 지나칩니다. 이는 **"B팀의 가장 약한 카드를 제물로 바쳐 A의 에이스 카드를 낭비시킨 것"**과 완벽히 동일한 효과를 냅니다!
```python
def solution_number_game(A, B):
    answer = 0
    A.sort(reverse=True)
    B.sort(reverse=True)
    
    left = 0
    for a in A:
        if B[left] > a:
            answer += 1
            left += 1
    return answer
```

#### ③ 교집합 사전 분리 (체육복)
- 여벌이 있는 학생이 도난당했을 수 있는 조건이 있다면, 복잡한 조건문 대신 사전에 집합(`set`) 차집합으로 순수 대상자만 분리하고 정렬합니다.
```python
def solution_greedy_set(n, lost, reserve):
    # 여벌이 있는데 도난당한 인원 사전 제거
    real_reserve = sorted(list(set(reserve) - set(lost)))
    real_lost = set(lost) - set(reserve)
    
    for r in real_reserve:
        if r - 1 in real_lost:
            real_lost.remove(r - 1)
        elif r + 1 in real_lost:
            real_lost.remove(r + 1)
            
    return n - len(real_lost)
```

---

### 🌲 5) 최소 신장 트리(MST) & 유니온 파인드 🔥 [10월 신규]

#### ① 유니온 파인드 (Union-Find) 정석
- 사이클 판별 및 원소 간 그룹 묶기에 사용 (경로 압축 포함).
```python
def find_parent(parent, x):
    if parent[x] != x:
        parent[x] = find_parent(parent, parent[x]) # 경로 압축
    return parent[x]

def union_parent(parent, a, b):
    root_a = find_parent(parent, a)
    root_b = find_parent(parent, b)
    if root_a < root_b:
        parent[root_b] = root_a
    else:
        parent[root_a] = root_b
```

#### ② 크루스칼 (Kruskal) 템플릿
- 간선 비용 오름차순 정렬 후, 사이클이 발생하지 않는 간선만 $N-1$개 선택.
```python
def kruskal(n, costs):
    costs.sort(key=lambda x: x[2]) # 비용 기준 정렬
    parent = [i for i in range(n)]
    answer = 0
    connects = 0
    
    for a, b, cost in costs:
        if find_parent(parent, a) != find_parent(parent, b):
            union_parent(parent, a, b)
            answer += cost
            connects += 1
            if connects == n - 1: # 조기 종료
                break
    return answer
```

#### ③ 프림 (Prim) 템플릿 (섬 연결하기)
- 시작 노드에서 출발하여 영토를 넓혀나가는 방식.
- **핵심 최적화**: 모든 섬이 연결되면(`connects < n`) 큐에 남은 데이터를 검사하지 않고 즉시 루프를 탈출합니다.
```python
import heapq

def prim(n, costs):
    answer = 0
    cost_heap = {i: [] for i in range(n)}
    for i1, i2, cost in costs:
        cost_heap[i1].append([cost, i2])
        cost_heap[i2].append([cost, i1])
        
    visited = [False] * n
    visited[0] = True
    connects = 1
    wait_heap = list(cost_heap[0])
    heapq.heapify(wait_heap)
    
    while connects < n: # 조기 종료 조건
        cost, i = heapq.heappop(wait_heap)
        if not visited[i]:
            visited[i] = True
            connects += 1
            answer += cost
            for next_cost, next_node in cost_heap[i]:
                if not visited[next_node]:
                    heapq.heappush(wait_heap, [next_cost, next_node])
                    
    return answer
```

---

### 🚀 6) 다익스트라 (Dijkstra) 최단 경로 🔥 [필수 템플릿]
- **사용처**: 간선마다 **비용(시간, 가중치)이 서로 다를 때** 한 지점에서 다른 모든 지점까지의 최단 거리. (가중치가 모두 1이면 BFS, 다르면 다익스트라)
```python
import heapq

def dijkstra(n, graph, start):
    # 최단 거리 테이블을 무한대로 초기화
    distance = [float('inf')] * (n + 1)
    distance[start] = 0
    
    pq = []
    heapq.heappush(pq, (0, start)) # (비용, 노드)
    
    while pq:
        dist, now = heapq.heappop(pq)
        
        # 이미 처리된 적 있는(더 짧은 경로가 있는) 노드라면 무시
        if distance[now] < dist:
            continue
            
        for next_node, weight in graph[now]:
            cost = dist + weight
            if cost < distance[next_node]:
                distance[next_node] = cost
                heapq.heappush(pq, (cost, next_node))
                
    return distance
```

---

### 🎯 7) 이분 탐색 (Binary Search / 매개변수 탐색) 🔥 [필수 템플릿]
- **사용처**: 탐색 범위가 **10억 단위**로 엄청나게 크거나, **"조건을 만족하는 최솟값/최댓값을 구하라"**는 문제 (입국심사, 징검다리 건너기 등).
- **접근법**: 정답을 `mid`라고 가정하고, "이 `mid` 값으로 조건이 성립하는가?(True/False)"를 판별하며 범위를 절반씩 좁힙니다.
```python
def parametric_search(start, end, target_condition):
    answer = 0
    while start <= end:
        mid = (start + end) // 2
        
        # mid 값으로 조건을 만족하는지 검사
        if check(mid):
            answer = mid       # 정답 후보 기록
            start = mid + 1    # 더 큰 값 탐색 (최댓값을 구할 때)
        else:
            end = mid - 1      # 더 작은 값 탐색
            
    return answer
```

---

### 📊 8) 누적 합 (Prefix Sum) & 구간 합 🔥 [필수 템플릿]
- **사용처**: 배열의 특정 구간 `[left, right]`의 합을 여러 번 빠르게 구해야 할 때. 매번 구하면 $O(N)$이지만, 누적 합을 미리 구해두면 $O(1)$에 계산 끝.
```python
# 원본 배열: arr = [10, 20, 30, 40, 50]
def get_prefix_sum(arr):
    prefix_sum = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        prefix_sum[i + 1] = prefix_sum[i] + arr[i]
    return prefix_sum

# 구간 [left, right] (0-indexed) 합 구하기 공식:
# sum_val = prefix_sum[right + 1] - prefix_sum[left]
```

---

### ⏱️ 9) 기타 시뮬레이션 & 기출 특수 패턴

#### ① 이중 큐 스케줄링 (디스크 컨트롤러)
- `waits` (대기 큐: 요청 시간 순 정렬)와 `prioritys` (실행 큐: 소요 시간 순 힙).
- 현재 시간(`end`) 이전에 요청된 모든 작업을 `waits`에서 꺼내 `prioritys`에 붓고, 가장 짧은 작업을 하나 처리하며 `end`를 전진시킵니다. 작업이 없으면 `end`를 다음 작업 요청 시간으로 점프시킵니다.

#### ② 격자 시뮬레이션 조건부 원상복구 (공원 산책)
- 연속으로 몇 칸 이동하다가 장애물이 있으면 이동 전체를 무효화해야 하는 경우:
```python
nx, ny = x, y
possible = True
for _ in range(dist):
    nx += dx[dir]
    ny += dy[dir]
    if not (0 <= nx < H and 0 <= ny < W) or grid[nx][ny] == 'X':
        possible = False
        break
if possible:
    x, y = nx, ny # 온전히 다 돌았을 때만 실제 좌표 갱신!
```

---

## 4. 자주 나오는 핵심 구현 모음

### 🧮 1) N진수 변환 함수
```python
def to_n_base(n, q):
    if n == 0: return '0'
    rev_base = ''
    while n > 0:
        n, mod = divmod(n, q)
        rev_base += str(mod)
    return rev_base[::-1] # 뒤집어서 반환
```

### 🛡️ 2) 소수 판별 (제곱근 탐색)
```python
import math
def is_prime(x):
    if x < 2: return False
    for i in range(2, math.isqrt(x) + 1):
        if x % i == 0: return False
    return True
```

### 🔄 3) 2차원 배열 시계 방향 90도 회전 (한 줄 꿀팁)
카카오 자물쇠와 열쇠 등 격자 회전 문제에서 반복문 없이 한 줄로 회전시키는 마법의 코드입니다.
```python
def rotate_90(matrix):
    return [list(row) for row in zip(*matrix[::-1])]
```

---

## 5. 시험 직전 시간 복잡도 판별 & 금기사항 체크리스트

| $N$의 크기 | 허용 가능한 시간 복잡도 | 추천 알고리즘 |
| :--- | :--- | :--- |
| **$N \le 10$ ~ $20$** | $O(2^N)$, $O(N!)$ | 완전 탐색, 순열/조합 (`permutations`, 백트래킹) |
| **$N \le 500$ ~ $1,000$** | $O(N^2)$, $O(N^3)$ | 플로이드-워셜, 2차원 DP, 이중 루프 시뮬레이션 |
| **$N \le 100,000$** | $O(N \log N)$ | 정렬, 우선순위 큐(`heapq`), 다익스트라, 투 포인터 |
| **$N \le 1,000,000$** | $O(N)$ | 스택/단조 스택, 큐(`deque`), 단일 루프 그리디 |
| **$N > 10,000,000$ (10억 이상)** | $O(\log N)$ | 이분 탐색(매개변수 탐색), 거듭제곱 거듭 계산 |

### ⚠️ 시간 초과를 부르는 3대 금기
1. **반복문 내부 문자열 이어붙이기 금지**: `s = s[:i] + s[i+k:]` 대신 **`stack.pop()`** 사용!
2. **리스트 앞부분 조작 금지**: `list.pop(0)`은 $O(N)$이므로 무조건 **`deque.popleft()`** 사용!
3. **리스트 내부 포함 여부 검사 금지**: `x in list`는 $O(N)$이므로 탐색 대상은 무조건 **`set` 또는 `dict`**로 변환 ($O(1)$)!
