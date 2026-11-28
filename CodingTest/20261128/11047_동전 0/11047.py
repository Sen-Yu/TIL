import sys
def main():
    
    input = sys.stdin.readline
    N, K = map(int, input().split())
    A = [ int(input().strip()) for idx in range(N) ]

    now = N-1
    answer = 0
    
    while now >= 0:
        
        coin = A[now]
        if K // coin > 0:
            answer += K // coin
            K %= coin

        now-=1
    
    print(f"{answer}")
    
main()
