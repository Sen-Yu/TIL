import sys

def main():
    
    input = sys.stdin.readline
    S, K = map(int, input().split())
    arr = list(map(int, input().split()))
    
    answer = 0
    left = 0
    count = 0

    for right in range(S):
        if arr[right] % 2 == 1:
            count+=1
            
        while count > K :
            if arr[left] % 2 == 1:
                count -= 1
            left += 1
        answer = max(answer, right-left+1-count)
    
    print(answer)
    
main()
