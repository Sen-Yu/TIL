import sys

def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False

    return [i for i in range(2, n + 1) if is_prime[i]]

def main():

    input = sys.stdin.readline
    N = int(input().strip())
    answer = 0

    primes = sieve(N)
    p = len(primes)

    sums = 0
    left =0

    for right in range(p):
        sums += primes[right]

        while sums > N :
            sums -= primes[left]
            left += 1
        if sums == N:
            answer += 1
    print(answer)

main()
