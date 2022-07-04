%%cython

'''
sumOfDiv(10**15)
499961853010960

'''

def trial_division(n):
    multiplicity   = 0
    a = []    
    # now we find the multiplicity of divisor 2    
    while n % 2 == 0:
        n /= 2 # set as n the integer n/2
        a.append(2)  
    f = 3 # f is a possible prime divisor. We shall search up to sqrt(n).
    multiplicity = 0
    while f**2<= n:
        if n % f == 0: # similar as previous. We check if f divides n.
            n /= f    # we update n with n/f
            multiplicity  +=1 
            a.append(f)
        else:
            f += 2   # we increase the possible divisor f by 2. So f = 3,5,7,9,11....
            #multiplicity = 0
    if n != 1: a.append(int(n))
    L = a
    L_set = list(set(L))
    M = []
    for i in L_set:
        M.append([i,L.count(i)])    
    return M

def my_sigma(n):
    import math
    L = trial_division(n)
    A = math.prod([ ( L[i][0]**(L[i][1]+1) - 1)//(L[i][0] - 1) for i in range(len(L))] )
    return int(A)


def find_s_t(int n):
    '''
    we compute the order_2 of n i.e. we compute s such that n = 2**s * m, for some odd m.
    '''
    cdef:
        int i = 1
        int isint = 0
        int s
    while isint == 0:
        isint = pow(n,1,2**i)
        if isint == 0: # i.e. if n/2^i is integer, continue
            i = i + 1
        else:
            isint = 1
            s = i - 1
            return s,n//2**s

def sumOfDiv(int a):
    ''' we search for divisors up to square root of a.
    Say k a divisor of a which is < sqrt(a). Then we add k and a/k to a list.
    Finaly we return the previous list.'''
    import math
    import numpy as np
    cdef:
        int SUM = 0
        int M = 0
        int s
    if a<=0:
        return "error. Provide a positive integer"
    if a>10**10:
        return my_sigma(a)
    s,a=find_s_t(a)
    M = math.ceil(a ** 0.5)
    if M == (a ** 0.5):
        SUM = M
    for i in range(1,M,2):
        if a % i == 0:      
            SUM+=i + a//i
    return SUM*(2**(s+1)-1)
