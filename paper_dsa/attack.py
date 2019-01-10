'''
 Requirements : The code is written in sagemath ver. 8.1
  
 AUTHORS: K. Draziotis (2018): initial version
 
 REFERENCES:  

For instance the following code generates a random DSA-system with secret key
159-bits and derivative ephemeral keys 157-bits. q is fixed to a specific prime of 160-bits.


n = 200;
q,A,target,sol,nr,M_n= equivalences_dsa(n,159,157,'',3) # an of DSA-system
M = matrix_dsa(A,q,n) # we generate the DSA-matrix
print "n=",n
M = M.BKZ(block_size=70)    # preprocessing wth BKZ (block_size=70)
M_GS = M.gram_schmidt()[0]  # The Gram-Schimdt basis of the matrix M
t=target #our target vector
bab = babai(M,M_GS,t)       # we execute babai with input the DSA matrix M, its GSO, and the target vector
print bab[0]==sol[0]        # returns true if babai found the secret key, else false

The exact experiment we execute in the paper are the follwing

Experiment - 1
# case f = 0
count = 100 # number of instances
j = 0
n = 200 # this is the maximum suitable n for the f_q we chose
for i in range(count):    
    q,A,target,sol,nr,M_n= equivalences_dsa(n,159,157,'',3) # instances of dsa
    M = matrix_dsa(A,q,n)
    M = M.BKZ(block_size=70)
    M_GS = M.gram_schmidt()[0]
    t=target
    bab = babai(M,M_GS,t)
    if bab[0]==sol[0]:
        j = j + 1
print j/count*100.

Experiment - 2
#case  f = (ln(c*(n+1))).n()/(b*n^d*ln(q)).n()
count = 100
j = 0
n = 206 # this is the maximum suitable n fir the specific f_q
for i in range(count):
    q,A,target,sol,nr,M_n= equivalences_dsa(n,159,157,'',2) # instances of dsa (q is fixed) 
    M = matrix_dsa(A,q,n)
    M = M.BKZ(block_size=70)
    M_GS = M.gram_schmidt()[0]
    t=target
    bab = babai(M,M_GS,t)
    print "i=",i+1
    if bab[0]==sol[0]:
        j = j + 1
    print "j=",j
    print "----"
print j/count*100.
           

#*****************************************************************************
#       Copyright (C) 2018-2019 K.Draziotis <drazioti@gmail.com>
#                         
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

'''

from fpylll import *
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
    '''B is a list'''
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
### Input : a basis matrix M of lattice, 
### the associated Gram-Schmidt basis matrix M_GS and a target vector t and returns the result of Babai's algorithm.
### Output :  an approximate closest vector to t

def babai(M,M_GS,t):
    v = vector([0 for i in range(len(t))])
    t=vector(t)
    for i in range(len(t)-1,-1,-1):
        v = v + round(((t-v).dot_product(M_GS[i]))/(M_GS[i].norm())^2)*M[i]
    return v+t

def equivalences_dsa(n,BITS,BITS_e,flag,flag_2): 
    '''
     We generate DSA parameters. In fact we generate a vector (x,y_1,...,y_n)
     which is a solution of a system y_i + A_ix_i + B_i = 0 mod q
     where A_i are chosen as in Proposition 
     input
        -----
        > n      : number of messages to be signed
        > BITS   : number of bits of the secret key
        > BITS_e : number of bits of the (derivative) ephemeral keys (yi=AiCi^{-1}ki mod q
        > flag = 'print' or ''
        > flag_2 = 1 or 2 or 3
        > if flag_2=1 then f=0
        > if flag_2=2 then  f = (ln(c*(n+1)))/(b*n^d*ln(q))
        > if flag_2=3 then  f = (ln2+ln((n+1)))/(n*ln(q)).
        
        output
        ------
        > a vector B = (0,b1,...,bn) : the target vector
        > a vector A = (A1,A2,...,An), with Ai in suitable intervals
        > the solution vector (a,y1,y2,...,yn) for the n equivalences : yi + Ai*x + bi =0 mod q.
        > the norm of the solution vector
     
       
    '''
    import numpy as np
    from numpy import linalg as LA
    from Crypto.Util.number import bytes_to_long, long_to_bytes   
    import random
            
    q = 1097479964745794789728520663375990048516704632017L # a prime 160 bits
    a = int(ZZ.random_element(2^BITS)); # the secret key
    while a>q:
         a = int(ZZ.random_element(2^BITS));
       
    # generation of the derivative ephemeral keys
    y = []
    if BITS==160:
        for i in range(0,n):
            y.append(int(ZZ.random_element(q))); # the derivative of the ephemeral keys
    else:
        for i in range(0,n):
            y.append(int(ZZ.random_element(2^BITS_e))); # the derivative of the ephemeral keys
    A = []
    yi = []
    B = []
    sol = []
    
    if flag_2 ==1:
        f = (ln(2)+ln(n+1))/(2*n*ln(q)).n()

    # here we have to choose b,c,d    
    if flag_2 ==  2: 
        b = 1      # b<=2
        c = 170    # c>=1
        d = 0.99   # d<=1
        
        f = (ln(c*(n+1))).n()/(b*n^d*ln(q)).n()
    if flag_2 == 3:
        f= 0
    
    # we shall randomly pich integers A_i in specific intervals
    for i in range(0,n):  
        left  = ceil( q^( f + (i+1) / (n+1) )/2 )
        right = floor( q^( f + (i+1)/(n+1) )/1.5 )
        
        if left==right:
            A.append(int(left))
        else:
            A.append( int(ZZ.random_element(left,right))); # the vector A
            
    # we generate the constant terms of the system        
    for i in range(n):
            B.append(int(mod(-y[i]-A[i]*a, q)) ) # the vector of constants B

    sol = [a] + y
    target = [0]+B
    if flag == 'print':
        for i in range(n):
            print "verifying...",mod(A[i]*a + y[i] + B[i],q)==0
        print "sol=",sol
        print "q=",q
        print "a=",a
        print "ephemeral keys=",y
        print "\n"
        print "A=",A
        print
    #print "norm=",norm(vector(sol)).n()
    M_n = constant_of_the_attack(n,q,f)
    #print "M_n=",M_n
    return q,A,target,sol,norm(vector(sol)).n(),M_n
    
def guess_suitable_n(n,flag_2):
    ''' this algorithm first generates a random DSA-system and then 
    finds all the positive integers m < n
    such that the interval I_j(m) contain at least one integer.
    Our goal is to find the maximum such m < n
    '''
    
    from Crypto.Util.number import bytes_to_long, long_to_bytes   
    from Crypto.PublicKey import DSA
    import random
    
    def randfunc(n):
        return ''.join(str(random.random())[4] for _ in xrange(n));
          
    DSAkey=DSA.generate(int(1024),randfunc);
    q=DSAkey.q  # we generate a prime q 160 bits 
    A = []
    
    if flag_2 ==1:
        f = (ln(2)+ln(n+1))/(2*n*ln(q)).n()
    if flag_2 ==  2: 
        ### here b,c, and d must agree with b,c, and of function
        b = 1 #b<=2
        c = 170 #c>=1
        d = 1 #d<=1
        f = (ln(c*(n+1))).n()/(b*n^d*ln(q)).n()
    if flag_2 == 3:
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
   
   