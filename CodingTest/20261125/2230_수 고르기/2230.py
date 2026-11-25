import  sys

def main():
    input = sys.stdin.readline
    
    N, M = map(int, input().split())
    A = [int(input().strip()) for i in range(N)]
    A.sort()
    
    left = 0
    answer = A[-1]-A[0]
    for right in range(1,N):
        now = A[right]-A[left]
        
        while now >= M and left < right:
            answer = min(now, answer)
            if answer == M:
                break
            left+=1
            now = A[right]-A[left]

        
    print(answer)
        

main()
