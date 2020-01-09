''' 

Miller - Rabin.
Works for large numbers.
We need gmpy2 library. Tested in python 2. 

>>>miller_rabin(2**1024-1,8)
>>>'composite'

'''



def miller_rabin(n,k):
    
    import random
    import math
    import gmpy2
    from gmpy2 import mpz,mpq,mpfr,mpc

    

    def find_s_t(n):
        n = mpz(n)
        # here we have to compute the order_2 of n
        i = mpz(1)
        isint = 0
        while isint == 0:
            
            isint = gmpy2.powmod(n-1,1,2**i)
            #print isint
            #isint = gmpy2.floor( (n-1)/(2.**i)) - gmpy2.ceil( (n-1)/(2.**i))
            # sos : the variable isint does not work for large n, say 2048 bits
            # TODO :  fix it
            
            if isint == 0: # i.e. if n/2^i is integer, continue
                i = i + 1
            else:
                isint = 1
                s = i - 1
                return s,(n-1)/2**s

    i = 1
    j = 0
    s,t = find_s_t(n)
    while i<=k:
        a = random.randint(2,n-1)
        b =  gmpy2.powmod(a,t,n)
        if b == 1:
            j = j + 1
            if j == k:
                return "n is strong probable prime"
        for r in range(0,s):
            if b == (n-1):
                j = j + 1
                if j == k:
                    return "n is strong probable prime"
            b =  gmpy2.powmod(b,2,n)
        i = i + 1
    return "composite"
