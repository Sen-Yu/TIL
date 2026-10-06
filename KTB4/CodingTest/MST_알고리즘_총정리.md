# 🌲 최소 신장 트리(MST)와 프림, 크루스칼, 유니온 파인드 총정리

그래프 탐색에서 다익스트라(최단 경로)만큼이나 코딩테스트에 자주 나오는 **최소 신장 트리(MST)**와 이를 구현하는 두 가지 방법, 그리고 필수 개념인 유니온 파인드까지 하나로 연결해 정리한 문서입니다.

---

## 1. 최소 신장 트리 (MST, Minimum Spanning Tree)란?
- **신장 트리(Spanning Tree):** 그래프 내의 **모든 노드(정점)를 포함하면서 사이클이 없는** 연결된 트리를 말합니다. (노드가 N개일 때 간선은 무조건 N-1개입니다.)
- **최소 신장 트리(MST):** 여러 신장 트리 중에서 **간선들의 가중치(비용) 합이 가장 작은 트리**입니다.
- **주요 출제 유형:** "모든 도시를 가장 적은 비용으로 연결하라", "모든 섬을 통행 가능하게 만들되 다리 건설 비용을 최소화하라" (예: 프로그래머스 - 섬 연결하기)

이 MST를 구하는 두 가지 대표적인 알고리즘이 바로 **프림(Prim)**과 **크루스칼(Kruskal)**입니다.

---

## 2. 크루스칼(Kruskal) 알고리즘 & 유니온 파인드(Union-Find)

크루스칼 알고리즘은 **"가장 비용이 싼 간선부터 무작정 연결하자!"**라는 완벽한 그리디 방식입니다. 
하지만 무작정 연결하다 보면 **사이클(순환)**이 생길 위험이 있습니다. 사이클이 생기는지 안 생기는지 판별하기 위해 반드시 **유니온 파인드(Union-Find)** 자료구조를 함께 써야 합니다.

### 🔗 유니온 파인드 (Disjoint Set) 템플릿
노드들이 같은 집합(그래프)에 속해있는지 확인(`Find`)하고, 다른 집합이라면 하나로 합치는(`Union`) 알고리즘입니다.

```python
# 1. 부모 노드를 찾는 함수 (경로 압축 최적화 포함)
def find_parent(parent, x):
    if parent[x] != x:
        # 루트 노드를 찾을 때까지 재귀 호출하며 부모를 루트로 바로 갱신(경로 압축)
        parent[x] = find_parent(parent, parent[x])
    return parent[x]

# 2. 두 노드가 속한 집합을 합치는 함수
def union_parent(parent, a, b):
    root_a = find_parent(parent, a)
    root_b = find_parent(parent, b)
    
    # 더 작은 번호의 노드가 부모가 되도록 합침 (규칙은 자유)
    if root_a < root_b:
        parent[root_b] = root_a
    else:
        parent[root_a] = root_b
```

### 🌉 크루스칼 알고리즘 템플릿
```python
def kruskal(n, costs):
    answer = 0
    # 모든 간선을 비용(cost) 기준으로 오름차순 정렬
    costs.sort(key=lambda x: x[2])
    
    # 부모 테이블 초기화 (처음엔 자기 자신을 부모로 가짐)
    parent = [i for i in range(n + 1)]
    
    connects = 0 # 연결된 간선의 수
    
    for a, b, cost in costs:
        # 두 노드의 최상위 부모가 다르다면 (사이클이 발생하지 않는다면)
        if find_parent(parent, a) != find_parent(parent, b):
            union_parent(parent, a, b) # 두 노드를 연결
            answer += cost             # 비용 추가
            connects += 1
            
            # 간선이 N-1개 연결되면 완성된 것이므로 조기 종료
            if connects == n - 1:
                break
                
    return answer
```

---

## 3. 프림(Prim) 알고리즘

크루스칼이 '간선' 중심이었다면, 프림은 **'노드(영토)' 중심**입니다.
시작 노드 하나를 정해두고, **내 영토와 인접한 간선들 중 가장 싼 간선을 골라 영토를 계속 확장**해 나가는 방식입니다. "가장 싼 간선"을 빠르게 찾기 위해 **우선순위 큐(최소 힙)**를 사용합니다. (다익스트라와 구조가 매우 비슷합니다.)

### 🏝️ 프림 알고리즘 템플릿
```python
import heapq

def prim(n, costs, start_node=0):
    answer = 0
    # 1. 인접 리스트 딕셔너리로 그래프 구성
    graph = {i: [] for i in range(n)}
    for a, b, cost in costs:
        graph[a].append([cost, b])
        graph[b].append([cost, a])
        
    visited = [False] * n
    visited[start_node] = True
    connects = 1
    
    # 2. 시작 노드와 연결된 모든 간선을 우선순위 큐에 넣음
    # (비용이 첫 번째 원소이므로 비용순으로 자동 정렬됨)
    wait_heap = list(graph[start_node])
    heapq.heapify(wait_heap) 
    
    # 3. 모든 노드가 연결될 때까지 반복
    while connects < n:
        cost, node = heapq.heappop(wait_heap)
        
        # 이미 방문(내 영토에 포함)한 노드라면 무시
        if not visited[node]:
            visited[node] = True
            answer += cost
            connects += 1
            
            # 방금 편입된 노드와 연결된 간선들을 큐에 추가
            for next_cost, next_node in graph[node]:
                if not visited[next_node]:
                    heapq.heappush(wait_heap, [next_cost, next_node])
                    
    return answer
```

---

## 🆚 크루스칼 vs 프림, 언제 무엇을 쓸까?

두 알고리즘 모두 완벽하게 최소 신장 트리를 구해주지만, **그래프의 형태(간선의 개수)**에 따라 성능 차이가 발생합니다.

| 구분 | 크루스칼 (Kruskal) | 프림 (Prim) |
| :--- | :--- | :--- |
| **핵심 아이디어** | 가장 싼 간선부터 무작정 고르기 | 시작점에서 출발해 싼 간선으로 영토 넓히기 |
| **필수 자료구조** | 유니온 파인드 (Union-Find) | 우선순위 큐 (Heapq) |
| **유리한 경우** | 간선(Edge)의 수가 적은 **희소 그래프** | 간선(Edge)의 수가 엄청 많은 **밀집 그래프** |
| **시간 복잡도** | $O(E \log E)$ (간선 정렬에 지배됨) | $O(E \log V)$ (우선순위 큐 연산에 지배됨) |

**💡 실전 팁:** 
프로그래머스나 백준의 대부분의 일반적인 코딩테스트 문제는 둘 중 본인 손에 더 잘 익고 자신 있는 코드로 풀어도 모두 통과하도록 설계되어 있습니다. (유니온 파인드를 확실히 외웠다면 크루스칼을, 우선순위 큐와 다익스트라 폼이 익숙하다면 프림을 주력으로 쓰시면 좋습니다.)
