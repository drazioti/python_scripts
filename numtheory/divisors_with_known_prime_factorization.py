def find_divisors_from_primes(r,H):
    '''  
    Author : K.Draziotis
    Licence : GPL v2  
    Credits : we mimic the function divisors(n) of Sagemath.
    
    Say you have a natural number N = p1^e1 * p2^e2 *...*pn^en
    and that yu know the factorization of N.
    Then this function will return all the positive divisors of
    N, exploiting that we know all the primes dividing N. 
    e.g.
    r = [2,3,5,7]
    H = [2,1,1,1]
    C=find_divisors_from_primes(r,H)
    print C

    [1, 2, 3, 4, 5, 6, 7, 10, 12, 14, 15, 20, 21, 28, 30, 35, 42, 60, 70, 84, 105, 140, 210, 420]

    '''
    from itertools import izip
    L = list(izip(r,H))
    #print L
    pn = 1
    output = [1]
    for p,e in L:
        prev = output[:]
        pn = 1
        for i in range(e):
            pn = p * pn  
            output.extend(b * pn for b in prev)  # update output

    output.sort()
    return output
