'''
 Requirements : The code is written in Sagemath ver. 8.1
  
 AUTHORS: K. Draziotis (drazioti@gmail.com) 2018: initial version 

 REFERENCES:  http://www.sagemath.org/

 * Please report bugs *

The following code generates a random DSA-system with secret key
159-bits and derivative ephemeral keys 157-bits. q is fixed to a specific prime of 160-bits.
We used the function ZZ.random_element(bound) of sagemath to generate random integers <= bound.

For instance the following code generates a DSA-system (line 2), build the DSA matrix (line 3),
execute BKZ with blocksize 70 as preprocessing for Babai (line 5), and in line 8 we execute Babai algorithm for 
the lattice generated by the rows of matrix M and target vector t :

1:    n = 200;
2:    q,A,target,sol,nr,M_n= equivalences_dsa(n,159,157,'',3) # an instance of a DSA-system
3:    M = matrix_dsa(A,q,n)       # we generate the DSA-matrix
4:    print "n=",n
5:    M = M.BKZ(block_size=70)    # preprocessing wth BKZ (block_size=70)
6:    M_GS = M.gram_schmidt()[0]  # The Gram-Schimdt basis of the matrix M
7:    t=target                    # our target vector
8:    bab = babai(M,M_GS,t)       # we execute Babai with input the DSA matrix M, its GSO, and the target vector
9:    print bab[0]==sol[0]        # returns true if Babai found the secret key, else false


We provide the code we used to generate table 1 :


    Experiment - 2 : Table 1
    # case  f = (ln(c*(n+1))).n()/(b*n^d*ln(q)).n()
    # the constants c,b and d are defined in the code

    count = 100 # number of instances
    j = 0       # counts the successes
    n = 206     # this is the maximum suitable n for the specific sequence f_q(n)

    for i in range(count):
        q,A,target,sol,nr,M_n= equivalences_dsa(n,159,157,'',2) # an instance of DSA system (q is fixed) 
        M = matrix_dsa(A,q,n)
        M = M.BKZ(block_size=70)
        M_GS = M.gram_schmidt()[0]
        t=target
        bab = babai(M,M_GS,t)
        print "i=",i+1
        if bab[0]==sol[0]: # in a real situtation you check g^(bab[0]) == public key 
            j = j + 1
        print "j=",j
        print "----"
    print j/count*100.
           
The improved heuristic attack :
    
    # improved heuristic Babai attack for large keys
    # q is the same in all examples
    # q = 1097479964745794789728520663375990048516704632017L

    j = 0
    count = 100
    alpha = 160   # bits of the secret key
    beta  = 159   # bits of the derivative ephemeral keys (multiples of the ephemeral keys)
    epsilon  = 2**(beta) - 2**(beta-2)
    n = 206  # this is the maximum suitable n. n is the number of signed messages.
    k = 0

    for i in range(count):    
        q,A,target,sol,nr,M_n= equivalences_dsa(n,alpha,beta,'',2) # instances of dsa
        M = matrix_dsa(A,q,n)
        M = M.BKZ(block_size=70)
        M_GS = M.gram_schmidt()[0]
        t = vector(target) + vector((n+1)*[epsilon])
        bab = babai(M,M_GS,t)
        print "i=",i+1
        if bab[0] == sol[0]:
            j = j + 1
        print "current success rate:",j/(i+1)*100.
    print "success rate:",j/count*100.

#*****************************************************************************
#       Copyright (C) 2018-2019 K.Draziotis <drazioti@gmail.com>
#                         
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************
'''

from fpylll import *     # we use fpylll library for computing GSO
from copy import copy
import numpy as np
from numpy import linalg as LA

### auxiliary functions

def bits(x):
    ''' returns the number of bits of the positive integer x'''
    
    if x>0:
        return floor(log(x,2))+1;
    else:
        return 0
 
def constant_of_the_attack(n,q,f):
    M_n = 1/4 * q^(f + n/(n+1))
    return M_n.n()
    
def matrix_dsa(B,q,n):
    '''Input  :  B is a list, the first row of the DSA matrix
       Output :  A DSA-like matrix with first row the entries of B
    '''
    if len(B)!=n:
        return false
    A = matrix([B])
    M = identity_matrix(ZZ, n);
    M=q*M;
    zero_matrix=matrix(1,n,[0 for i in range(0, n)]).transpose();
    M1=block_matrix([[zero_matrix,M]]);
    M2=block_matrix([[-1,A]]);
    M3=block_matrix([ [M2],[M1] ]);
    return M3 

### Babai's Nearest Plane Algorithm
### * Input : a basis of a lattice, given as a matrix M (the rows generates the lattice), 
### the associated Gram-Schmidt basis matrix M_GS and a target vector t. 
### * Output :  an approximate closest vector to t
### The pseudocode can be found in the paper
    
def babai(M,M_GS,t):
    w=vector(t)
    t=vector(t)
    for i in range(rank(M)-1,-1,-1):
        w = w - round((w.dot_product(M_GS[i]))/(M_GS[i].norm())^2)*M[i]
    return t - w

def equivalences_dsa(n,BITS,BITS_e,flag,flag_2): 
    '''
     We generate DSA parameters. In fact we generate a vector (x,y_1,...,y_n)
     which is a solution of a system y_i + A_ix_i + B_i = 0 mod q
     where A_i are chosen as in Proposition 
        Input
        -----
        - n      : number of messages to be signed
        - BITS   : number of bits of the secret key
        - BITS_e : number of bits of the (derivative) ephemeral keys (yi=AiCi^{-1}ki mod q
        - flag = 'print' or ''
        - flag_2 = 1 or 2 or 3
        - if flag_2=1 then f=0
        - if flag_2=2 then  f = (ln(c*(n+1)))/(b*n^d*ln(q))
        
        Output
        ------
        - a vector B = (0,b1,...,bn) : the target vector
        - a vector A = (A1,A2,...,An), with Ai in suitable intervals
        - the solution vector (a,y1,y2,...,yn) for the n equivalences : yi + Ai*x + bi =0 mod q.
        - the norm of the solution vector
        - the Gaussian Heuristic
       
    '''

    import numpy as np
    from numpy import linalg as LA
    from Crypto.Util.number import bytes_to_long, long_to_bytes   
    import random
            
    q = 1097479964745794789728520663375990048516704632017L # a prime 160 bits
    a = int(ZZ.random_element( 2^(BITS-1) , 2^BITS - 1 ))  # when the number of bits is exactly = BITS
    while a>q:
         a = int(ZZ.random_element( 2^(159), q));          # we use the PRG of Sagemath : ZZ.random_element
       
    # generation of the derivative ephemeral keys
    y = []

    if BITS_e == 160:
        for i in range(0,n):
            y.append(int(ZZ.random_element( 2^(159), q)));              # the derivative ephemeral keys are <= q
    else:
        for i in range(0,n):
            y.append(int(ZZ.random_element(2^(BITS_e-1) ,2^BITS_e-1))); # the derivative of the ephemeral keys, have BITS_e bits
    A = []
    yi = []
    B = []
    sol = []
    
    if flag_2 ==1:
        f = (ln(2)+ln(n+1))/(2*n*ln(q)).n()

    # here we choose b,c,d    
    if flag_2 ==  2: 
        b = 1      
        c = 170    
        d = 0.99   
        
        f = (ln(c*(n+1))).n()/(b*n^d*ln(q)).n()

    
    # we randomly pick integers A_i in the specific intervals [left,right]
    for i in range(0,n):  
        left  = ceil( q^( f + (i+1) / (n+1) )/2 )
        right = floor( q^( f + (i+1)/(n+1) )/1.5 )
        
        if left==right:
            A.append(int(left))
        else:
            A.append( int(ZZ.random_element(left,right))); # the vector A, chose randomly from the interval (left,right)
            
    # we generate the constant terms of the DSA system : From these we build the target vector        
    for i in range(n):
            B.append(int(mod(-y[i]-A[i]*a, q)) ) # the vector of constants B
    sol = [a] + y       # A solution of the system
    target = [0]+B      # the target vector
    if flag == 'print': # these are printed only when we choose flag = 'print'
        for i in range(n):
            print "verifying...",mod(A[i]*a + y[i] + B[i],q)==0
        print "sol=",sol
        print "q=",q
        print "a=",a
        print "ephemeral keys=",y
        print "\n"
        print "A=",A
        print
    M_n = constant_of_the_attack(n,q,f)
    return q,A,target,sol,norm(vector(sol)).n(),M_n
    

def guess_suitable_n(q,n,flag_2):
    ''' this algorithm first generates a random DSA-system and then 
    finds all the positive integers m <= n
    such that the interval I_j(m) contains at least one integer.
    Our goal is to find the maximum such m <= n
    '''
    
    from Crypto.Util.number import bytes_to_long, long_to_bytes   
    from Crypto.PublicKey import DSA
    import random
    
    def randfunc(n):
        return ''.join(str(random.random())[4] for _ in xrange(n));
          
    #DSAkey = DSA.generate(int(1024),randfunc);
    #q = DSAkey.q  # we generate a prime q 160 bits 
    
    A = []
    
    # Every value of flag_2 = 1 or 2 or 3, corresponds to a specific form of the sequence f_q(n)

    if flag_2 == 1:
        f = (ln(2)+ln(n+1))/(2*n*ln(q)).n()

    if flag_2 ==  2: 
    
        ### here (b,c,d) agrees with (b,c,d) of function        
        b = 1 
        c = 170
        d = 1 
        f = (ln(c*(n+1))).n()/(b*n^d*ln(q)).n()
    
    if flag_2 == 3: #
        f= 0
        
    print "f=",f
    N = []
    for n_ in range(n):
        leftright= []
        for i in range(0,n_):  
            left  = ceil( q^( f + (i+1) / (n_+1) )/2 )
            right = floor( q^( f + (i+1)/(n_+1) )/1.5 )    
            leftright.append(right-left)
        if np.all(np.array(leftright) >= 0):
            N.append(n_)
    return max(N)
