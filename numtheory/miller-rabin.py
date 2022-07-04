''' 

Miller - Rabin.
Works for large numbers.
We need gmpy2 library. Tested in python 2. 

>>>miller_rabin(2**1024-1,8)
>>>'composite'
>>>miller_rabin(2**2048+981,3)
>>>'n is strong probable prime'

#*****************************************************************************
#       Copyright (C) K.Draziotis <drazioti@gmail.com>,
#                         
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************
'''
def miller_rabin(n,k):
    
    import random
    import math
    import gmpy2
    from gmpy2 import mpz,mpq,mpfr,mpc

    

    def find_s_t(n):
        # here we have to compute the order_2 of n-1. That is an integer s : n-1=2^s * k, for some k odd 
        n = mpz(n)
        i = mpz(1)
        isint = 0
        while isint == 0:
            
            isint = gmpy2.powmod(n-1,1,2**i)            
            if isint == 0: # i.e. if n/2^i is integer, continue
                i = i + 1
            else:
                isint = 1
                s = i - 1
                return s,(n-1)//2**s

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
