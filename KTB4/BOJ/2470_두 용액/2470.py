import sys
def main():
    input = sys.stdin.readline   
    n = int(input())
    arr = list(map(int, input().split()))     
    arr.sort()
    
    answer = [arr[0] , arr[-1]]

    left = 0
    right = n - 1
    while left < right:                     # 같은 용액을 두 번 고르지 않도록
        now = arr[left] + arr[right]

        if abs(now) < abs(answer[0] + answer[1]):
            answer = [ arr[left], arr[right]]

        if now < 0:
            left+=1          # 합이 음수 → 더 큰 수가 필요
        else:
            right-=1          # 합이 양수 → 더 작은 수가 필요

    return answer

answer = main()
print(*answer)
