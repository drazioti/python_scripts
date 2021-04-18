'''
This experiment studies how many digital signatures we need to collect
in order to take derivative ephemeral keys with prescribed number of bits.
In our case the prime q has 160 bits and we need 204 signatures such that their
ephemeral keys have 160-bits. We see that on average we need to collect about 1500 signatures.
Now providing special type of primes q, for instance having more MSB, we see that, we need (on average)
<< 1500 signatures.
You can use sagemathcell to test the code.

sage:ell = 160
sage:number_of_desired_signatures = 204
sage:number_of_instances = 2000
sage:mean([samples(ell,number_of_desired_signatures) for i in range(number_of_instances)])
1791.20300000000 # this is the average

The followinf experiment shows that, for denser primes q, i.e. having more significant bits, we more often have derive ephemeral keys with 160-bits

sage:ell = 160
sage:V = 30000 # number of instances
sage:C = []
sage:for i in [1,2,3,4,5,6,7,8,9,10,11,12]:
...     q = prime_of_specific_form(ell,i)
...     L = distribution(ell,V,q)
...     C.append(count_all(L)/V)
sage:print C

[0.196166666666667,
 0.376366666666667,
 0.428333333333333,
 0.475933333333333,
 0.486200000000000,
 0.491833333333333,
 0.496866666666667,
 0.497133333333333,
 0.499633333333333,
 0.498266666666667,
 0.498266666666667,
 0.500633333333333]


'''


def bits(x):
    ''' returns the number of bits of the positive integer x'''
    if x>0:
        return floor(log(x,2))+1;
    else:
        return 0

# choose ell and generate a prime with ell bits


import random 
def genq(ell):
    while 1==1:
        q = int(ZZ.random_element( 2^(ell-1), 2^(ell) - 1));
        if is_prime(q):
            return q

def r(q,k):
    return int(ZZ.random_element( 2^(k-1), q));

def samples(ell,number_of_signatures):
    q = genq(ell) # generate a prime having ell bits
    c = 0
    R = 0
    while c<number_of_signatures:
        R = R + 1 # counts the number of signatures
        multiplier = int(ZZ.random_element(q));
        ephemeral_key = r(q,ell)
        mult = int(mod(ephemeral_key * multiplier,q))
        if bits(mult) == ell:
            c = c + 1 # c: counts the number of desired signatures
    #print R,c
    return R.n()

def prime_of_specific_form(ell,m):
    ''' Output a prime of the form q = 2^{ell-1}+2^{ell-2}+...+2^{ell-k}+ a random positive integer less than 2^{ell - k-2} '''
    g = 1
    var('k')
    while is_prime(g)==False:
        g = sum(2^k,k,ell-m,ell-1) + int(ZZ.random_element(2^(ell-m-2)))
    #print g
    return g
     
def countX(lst, x): 
    count = 0
    for ele in lst: 
        if (ele == [x]): 
            count = count + 1
    return count 
    
def count_all(lst):
    minimum = min(lst)
    maximum = max(lst)
    minimum,maximum = minimum[0],maximum[0]
    M = range(minimum,maximum+1)
    B = []
    for i in M:
        A = countX(lst,i)
        #print i,A
        B.append([i,A])
    C = []
    for i in B:
        C.append(i[1])
    return C[len(C)-1]
    
def distribution(ell,count,q):
    B = []
    for i in range(count): # count is th number of instances
        multiplier = int(ZZ.random_element(q));
        ephemeral_key = r(q,ell)
        mult = int(mod(ephemeral_key * multiplier,q))
        B.append([bits(mult)])
    return B
