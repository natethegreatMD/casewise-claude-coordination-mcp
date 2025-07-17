#!/usr/bin/env python3
"""Demo script created by CCC-controlled autonomous Claude session"""

def get_first_n_primes(n):
    """Generate the first n prime numbers"""
    primes = []
    num = 2
    
    while len(primes) < n:
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        
        if is_prime:
            primes.append(num)
        
        num += 1
    
    return primes

def main():
    print("Hello from CCC-controlled Claude!")
    print("\nThe first 10 prime numbers are:")
    
    primes = get_first_n_primes(10)
    for i, prime in enumerate(primes, 1):
        print(f"{i}. {prime}")

if __name__ == "__main__":
    main()