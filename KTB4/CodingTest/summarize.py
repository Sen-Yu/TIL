import os
import re

dir_path = "/Users/emet/TIL/KTB4/CodingTest"
files = [f for f in os.listdir(dir_path) if f.endswith(".md") and f != "README.md"]

algorithms = {}
libraries = {}
concepts = {}
patterns = []

for file in files:
    with open(os.path.join(dir_path, file), 'r', encoding='utf-8') as f:
        content = f.read()
        
        # Extract Libraries
        imports = re.findall(r'from\s+(\w+)\s+import\s+(\w+)|import\s+(\w+)', content)
        for imp in imports:
            lib = imp[0] or imp[2]
            func = imp[1] if imp[1] else lib
            if lib not in libraries:
                libraries[lib] = set()
            libraries[lib].add(func)
            
        # Extract keywords for algorithms
        if 'BFS' in content or 'bfs' in content:
            algorithms['BFS (Breadth-First Search)'] = algorithms.get('BFS (Breadth-First Search)', 0) + 1
        if 'DFS' in content or 'dfs' in content:
            algorithms['DFS (Depth-First Search)'] = algorithms.get('DFS (Depth-First Search)', 0) + 1
        if 'DP' in content or 'dp' in content or '동적' in content:
            algorithms['DP (Dynamic Programming)'] = algorithms.get('DP (Dynamic Programming)', 0) + 1
        if '그리디' in content or 'Greedy' in content:
            algorithms['Greedy (탐욕법)'] = algorithms.get('Greedy (탐욕법)', 0) + 1
        if '이분 탐색' in content or '이진 탐색' in content:
            algorithms['Binary Search (이분 탐색)'] = algorithms.get('Binary Search (이분 탐색)', 0) + 1
        if '백트래킹' in content or 'Backtracking' in content:
            algorithms['Backtracking (백트래킹)'] = algorithms.get('Backtracking (백트래킹)', 0) + 1
        if '힙' in content or '우선순위 큐' in content or 'heapq' in content:
            algorithms['Heap / Priority Queue'] = algorithms.get('Heap / Priority Queue', 0) + 1
        if '투 포인터' in content or '슬라이딩' in content:
            algorithms['Two Pointers / Sliding Window'] = algorithms.get('Two Pointers / Sliding Window', 0) + 1
        if '해시' in content or '딕셔너리' in content or 'Counter' in content:
            algorithms['Hash / Dictionary'] = algorithms.get('Hash / Dictionary', 0) + 1
        if '완전탐색' in content or '브루트포스' in content:
            algorithms['Brute Force (완전탐색)'] = algorithms.get('Brute Force (완전탐색)', 0) + 1
        if '진수' in content:
            concepts['N-ary conversion (N진수 변환)'] = concepts.get('N-ary conversion (N진수 변환)', 0) + 1
        if '소수' in content:
            concepts['Prime Numbers (소수 판별)'] = concepts.get('Prime Numbers (소수 판별)', 0) + 1

print("### 빈출 알고리즘 / 자료구조")
for alg, count in sorted(algorithms.items(), key=lambda x: -x[1]):
    print(f"- {alg} ({count}회 등장)")

print("\n### 빈출 개념")
for con, count in sorted(concepts.items(), key=lambda x: -x[1]):
    print(f"- {con} ({count}회 등장)")
    
print("\n### 자주 사용된 라이브러리 및 함수")
for lib, funcs in libraries.items():
    if lib in ['collections', 'heapq', 'math', 'itertools', 'sys']:
        print(f"- **{lib}**: {', '.join(funcs)}")
        
