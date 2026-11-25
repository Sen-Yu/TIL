import  sys

def main():
    input = sys.stdin.readline
    N, S = map(int, input().split())
    arr = list(map(int, input().split()))
    
    left = 0
    sum=0
    answer = N+1

    for right in range(N):    
        sum+=arr[right]
        
        while sum >= S :
            answer = min(answer, right-left+1)
            sum-=arr[left]
            left+=1

    if answer == N+1:
        answer = 0
    
    print(answer)

main()
