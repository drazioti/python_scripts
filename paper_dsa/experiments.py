'''
This experiment studies how many digital signatures we need to collect
in order to take derivative ephemeral keys with prescribed number of bits.
In our case the prime q has 160 bits and we need 206 signatures such that their
ephemeral keys have 160-bits. We see that on average we need about 1500 signatures
to collect.

sage:ell = 160
sage:number_of_desired_signatures = 204
sage:number_of_instances = 100
sage:mean([samples(ell,number_of_desired_signatures) for i in range(number_of_instances)])
1406
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
    q = genq(ell) # generate a prime having ell b its
    c = 0
    R = 0
    while c<number_of_signatures:
        R = R + 1 # counts the number of signatures
        multiplayer = int(ZZ.random_element(q));
        ephemeral_key = r(q,ell)
        mult = int(mod(ephemeral_key * multiplayer,q))
        if bits(mult) == ell:
            c = c + 1 # c: counts the number of desired signatures
    #print R,c
    return R.n()

