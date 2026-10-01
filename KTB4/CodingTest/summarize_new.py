import os
import re

dir_path = "/Users/emet/TIL/KTB4/CodingTest"
files = [
    "20260913_프로그래머스 - 공원 산책 (172928).md",
    "20260913_프로그래머스 - 게임 맵 최단거리 (1844) 재풀이 비교.md",
    "20260914_프로그래머스 - 여행경로 (43164) 재풀이 비교.md",
    "20260915_프로그래머스 - 도둑질 (42897).md",
    "20260915_프로그래머스 - 호텔 방 배정 (64063).md",
    "20260919_프로그래머스 - 명예의 전당 1 (138477).md",
    "20260920_프로그래머스 - 더 맵게 (42626) 재풀이 비교.md",
    "20260925_프로그래머스 - 디스크 컨트롤러 (42627).md"
]

for file in files:
    filepath = os.path.join(dir_path, file)
    if os.path.exists(filepath):
        print(f"=== {file} ===")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Try to print '아이디어' or '배운 점' or '해결 방법' or '핵심'
            match = re.search(r'(## 아이디어|## 배운 점|## 해결 방법|## 핵심).*?(?=## |\Z)', content, re.DOTALL)
            if match:
                print(match.group(0)[:500].strip())
                print("...")
            else:
                print("No clear summary block found.")
        print("\n")
