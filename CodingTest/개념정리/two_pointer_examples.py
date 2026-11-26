"""
투포인터 기본 틀 예제 (투포인터.md 와 함께 보기)
VS Code에서 F5로 실행하면 각 틀이 한 단계씩 어떻게 움직이는지 출력된다.
"""


# ① 같은 방향 - 가장 짧은 구간: 합이 S 이상인 가장 짧은 구간의 길이 (백준 1806)
#    좋은 구간인 "동안" 줄이고, while "안"에서 갱신
def shortest(arr, S, trace=False):
    n = len(arr)
    left = 0
    total = 0                  # 정의: total = arr[left] ~ arr[right] 합 (양 끝 포함)
    answer = n + 1             # 나올 수 없는 값 = "아직 못 찾음"

    for right in range(n):
        total += arr[right]                        # 1) 오른쪽을 넣고

        while total >= S:                          # 2) 좋은 구간인 동안
            answer = min(answer, right - left + 1)  #    줄이기 전에 갱신
            if trace:
                print(f"  [{left}, {right}] {arr[left:right + 1]} 합 {total} -> 길이 {right - left + 1} 기록")
            total -= arr[left]                     #    왼쪽을 빼서 더 짧게
            left += 1

    return answer if answer <= n else 0


# ② 같은 방향 - 가장 긴 구간: 합이 S 이하인 가장 긴 구간의 길이
#    나쁜 구간인 "동안" 줄이고, while "뒤"에서 갱신 (백준 22862와 같은 틀)
def longest(arr, S, trace=False):
    left = 0
    total = 0
    answer = 0

    for right in range(len(arr)):
        total += arr[right]                        # 1) 오른쪽을 넣고

        while total > S:                           # 2) 나쁜 구간인 동안
            total -= arr[left]                     #    왼쪽을 빼서 다시 좋게
            left += 1

        answer = max(answer, right - left + 1)     # 3) 다시 좋아진 뒤 갱신
        if trace:
            print(f"  [{left}, {right}] {arr[left:right + 1]} 합 {total} -> 길이 {right - left + 1}")

    return answer


# ③ 양 끝에서 안쪽으로: 합이 0에 가장 가까운 두 수 (백준 2470)
#    정렬 후, 합의 부호로 한쪽만 움직임
def closest_pair(arr, trace=False):
    arr = sorted(arr)
    left, right = 0, len(arr) - 1
    answer = (arr[left], arr[right])

    while left < right:                            # 같은 원소를 두 번 고르지 않게
        now = arr[left] + arr[right]
        if abs(now) < abs(answer[0] + answer[1]):
            answer = (arr[left], arr[right])
        if trace:
            print(f"  {arr[left]} + {arr[right]} = {now}")
        if now < 0:
            left += 1                              # 더 큰 수가 필요
        else:
            right -= 1                             # 더 작은 수가 필요

    return answer


if __name__ == "__main__":
    arr = [2, 1, 3, 2, 4, 1]

    print(f"① 가장 짧은 구간: {arr}, 합 >= 6")
    print("  답:", shortest(arr, 6, trace=True))

    print(f"\n② 가장 긴 구간: {arr}, 합 <= 6")
    print("  답:", longest(arr, 6, trace=True))

    pair = [-2, 4, -99, -1, 98]
    print(f"\n③ 0에 가장 가까운 두 수: {pair}")
    print("  답:", closest_pair(pair, trace=True))
