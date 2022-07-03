'''
sumOfDiv(10**15)
499961853010960

'''

def find_s_t(n):
    '''
    we compute the order_2 of n i.e. we compute s such that n = 2**s * m, for some odd m.
    '''
    i = 1
    isint = 0
    while isint == 0:
        isint = pow(n,1,2**i)
        if isint == 0: # i.e. if n/2^i is integer, continue
            i = i + 1
        else:
            isint = 1
            s = i - 1
            return s,n//2**s

def sumOfDiv(a):
    ''' we search for divisors up to square root of a
    Say k a divisor of a which is < sqrt(a). Then we add k and a/k to a list.
    Finaly we return the previous list.'''
    import math
    import numpy as np
    divs = []
    s,a=find_s_t(a)
    M = math.ceil(a ** 0.5)
    if M == (a ** 0.5):
        divs.extend([M])
    for i in range(1,M,2):
        if a % i == 0:
            divs.extend([i, a // i])            
    return np.sum(divs) * (2**(s+1)-1)
