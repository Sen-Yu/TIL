"""
백준 <번호> - <제목>
https://www.acmicpc.net/problem/<번호>

아이디어 메모:

"""
import sys
import os

# 로컬에서만 input.txt를 입력으로 사용 (백준에는 이 파일이 없어서 그냥 넘어감)
# run_cases.py로 돌릴 때(RUN_CASES=1)는 케이스 입력을 써야 하므로 건너뜀
_local_input = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
if os.path.exists(_local_input) and not os.environ.get("RUN_CASES"):
    sys.stdin = open(_local_input, encoding="utf-8")

input = sys.stdin.readline


def main():
    n = int(input())
    arr = list(map(int, input().split()))

    answer = 0
    # TODO: 여기서 풀이

    print(answer)


main()
