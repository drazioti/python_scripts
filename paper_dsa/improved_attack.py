''' 
Requirements : The code is written in Sagemath ver. 8.1
  
 AUTHORS: K. Draziotis (drazioti@gmail.com) 2018: initial version 
 REFERENCES:  http://www.sagemath.org/
 * Please report bugs *

The following code implements the attack : "Conditional Babai attack".

# Conditional Babai Attack.
# We use the two oracles, length oracle A and binary lenght oracle B.
# Prime q changes for every instance.
import time

j = 0             # counts the successes of the attack
count = 100       # number of instances
b = 160           # Here we choose the parameter. b = 160 or 224 or 256

if b == 160:
    n = 204       # this is the maximum suitable n. n is the number of signed messages.
if b == 256:
    n = 300
if b == 225:
    n = 260
    
flag = '' 

for i in range(count):
    T1 = time.time()
    q  = gen_q(b)            # generate a random prime number with b bits
    print "i=",i+1 
    A, minus_target, minus_sol, minus_nr, nr, M_n, epsilon = equivalences_dsa_new_3(n,q,flag,b) # the minus_DSA system
    print "n+1=",n+1
    M = matrix_dsa(A,q,n)
    M = M.BKZ(block_size=70) # preprocessing
    M_GS = M.gram_schmidt()[0]
    t = vector(minus_target) + vector(ZZ,epsilon)
    bab = babai(M,M_GS,t)
    if bab[0] == minus_sol[0]:
        j = j + 1
    print "current success rate:",j/(i+1)*100.
    T2 = time.time() - T1
    print "time :",T2
    print "Is norm of (babai - target)  < M_n?" , norm(vector(bab)-vector(t)).n() < M_n
    print
    print "norm of (babai - target), M_n, 4*M_n : \n" ,norm(vector(bab)-vector(t)).n(),M_n,4*M_n
print "success rate:",j/count*100.
'''


reset()

def bits(x):
    ''' returns the number of bits of the positive integer x'''
    
    if x>0:
        return floor(log(x,2))+1;
    else:
        return 0
 
def constant_of_the_attack(n,q,f):
    M_n = 1/4 * q^(f + n/(n+1))
    return M_n.n()
    
def gen_q(b):
    q = random_prime(2^b)
    while bits(q)!=b:
        q = random_prime(2^b)
    return q
    
    
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

    
def babai(M,M_GS,t):
    '''
    Babai's Nearest Plane Algorithm
    *Input : a basis of a lattice, given as a matrix M (the rows generates the lattice),                          
    the associated Gram-Schmidt basis matrix M_GS and a target vector t. 
    *Output :  an approximate closest vector to t
    '''
    
    w=vector(t)
    t=vector(t)
    for i in range(rank(M)-1,-1,-1):
        w = w - round((w.dot_product(M_GS[i]))/(M_GS[i].norm())^2)*M[i]
    return t - w

def length_oracle(M,q,parameter): # here parameter is the number of bits of q
    if parameter>bits(q):
        return "oracle failed"
    if M>q:
        return "oracle failed"
    if bits(M)==parameter:
        return 0
    if bits(M)==parameter - 1:
        return 1
    if bits(M) < parameter - 1:
        return 2

def binary_oracle(M,q,parameter):
    if parameter>bits(q):
        return "binary oracle failed"
    if M<q:
        if bits(q-M)==parameter-1:
            return 'true'
        else:
            return 'false'
    if M>q:
        return "binary oracle failed"
        
def equivalences_dsa_new_3(n,q,flag,parameter): 
    '''
     We generate DSA parameters. In fact we generate a vector (x,y_1,...,y_n)
     which is a solution of a system y_i + A_ix_i + B_i = 0 mod q
     where A_i are chosen as in Proposition.
     We modify the original DSA system to exploit the fact that q-yi and q-a
     have at most 159 bits. Our assumption is that we have a binary length oracle which
     decides in polynomial time if q-yi or q-a has 159 bits or not and a length oracle. According to the output
     of the oracle we modify the system. If q-yi has <159 bits the we add and subtruct 2^(158).
     So the final DSA system has always a solution with all the entries 159-bits (except maybe the first entry),
     and our attack is feasible with a large probability (approx. 93%) having 204 signatures. 
        
        Input
        -----
        - q         : a prime number
        - n         : number of signed messages
        - flag      : 'print' or ''
        - parameter : is the binary length of q, usually parameter = 160
        
        Output
        ------
        - a vector A = (p_1A1,p_2A2,...,p_nAn), with Ai in the suitable intervals and p_i = 1 or -1
        - a vector B = (0,b1,...,bn) 
        - a vector e   s.t. B+e is the target vector
        - the solution vector (a,z1,p_2z2,...,zn) for the n equivalences 
          where, zi = epsilon_i 2^(parameter-2) + delta_i yi
          with (a,y1,...,yn) a solution of the unmodified system                                                   
        - the norm of the solution vector
        - the Gaussian Heuristic  M_n
    '''

    import numpy as np
    from numpy import linalg as LA 
    import random

    a = int(ZZ.random_element( 2^(parameter-1), q));  # we generate randomly the secret key having parameter bits       
    
    y   = []
    A   = [] 
    B   = [] # this will be the target vector
    sol = [] # the solution of the unmodified system
    
    # we choose f_q(n)
    
    b = 1/(n+1)
    c = ( ln( -3*q^(-b) + sqrt( 96 + 9*q^(-2*b) ) ) - ln(8) )/ln(q)  - 10e-10       
    f = min(b.n(),c.n())

    # We randomly pick integers A_i in the specific intervals [left,right]
    # the vector A is chosen randomly from the interval (left,right)
    
    for i in range(0,n):
        left  = ceil(  q^( f + (i+1) / (n+1) )/2 )
        right = floor( q^( f + (i+1)/(n+1) )/1.5 )
        if left == right:
            A.append(int(left))
        else:
            A.append( int(ZZ.random_element(left,right))); 
            
    #############################################################################################        
    # We generate the constant terms of the DSA system : From these we build the target vector. # 
    # Here we use two oracles. The length oracle and                                            #
    # the binary length oracle which decides in probabilistic polynomial time,                  #
    # if the length of a derivative_key is 159 bits or not.                                     #
    #############################################################################################        
    
    minus_A = []
    minus_y = []
    B       = []   # the list of constant terms
    minus_B = []
    tr      = 0    # oracle B outputs True
    fal     = 0    # oracle B outputs False
    zero    = 0    # oracle A outputs 0
    one     = 0    # oracle A outputs 1
    two     = 0    # oracle A outputs 2        

    
    # We choose the derivative ephemeral keys randomly from Z_q
    
    for i in range(0,n):
        y.append(int(ZZ.random_element(q) ) );
                   
    if flag=='' or flag=='print':                 
        for i in range(n):
            minus_Ai = int(mod(-A[i],q))
            M    = int(mod(-y[i],q))
            Cons = int(mod(-y[i]-A[i]*a, q))
            minus_Cons = int(mod(-Cons ,q))    # the constants of the modified system, using the two orcles.
                        
            if length_oracle(y[i],q,parameter) == 0:
                zero = zero + 1
                minus_A.append(minus_Ai)
                if binary_oracle(y[i],q,parameter)=='false':
                    fal = fal + 1
                    minus_y.append(2^(parameter-2) + M)     
                    minus_B.append(-2^(parameter-2) + minus_Cons) # constant terms
                else:
                    tr = tr + 1            
                    minus_y.append(M)
                    minus_B.append(minus_Cons)  # constant terms

            if length_oracle(y[i],q,parameter) == 1:
                one = one + 1
                minus_A.append(A[i])
                minus_y.append(int(mod(y[i],q)))     
                minus_B.append(Cons) # constant terms

            if length_oracle(y[i],q,parameter) == 2:
                two = two + 1
                minus_A.append(A[i])
                minus_y.append(2^(parameter-2) + y[i])     
                minus_B.append(-2^(parameter-2) + Cons) # constant terms

    minus_sol    = [a] + minus_y     # a solution of the minus DSA system    
    minus_target = [0] + minus_B
    e     = []
    e.append( [ 2^(parameter-1) - 2^(parameter-3) for i in range(0,n)]) # all entries are the same
    e  = flatten([2^(parameter)  - 2^(parameter-2)] + e)
    
    if flag == 'print': # the following are printed only when we choose flag = 'print'
        for i in range(n):
            print "verifying the minus signing equation...",mod(minus_A[i]*a + minus_y[i] + minus_B[i],q)==0
    print "Result of the length oracle-binary length oracle"
    print "0:",zero,"true:",tr,"false:",fal
    print "1:",one
    print "2:",two
    print "bits of a : ",bits(a)
    print "max bits for derivative keys :", max([bits(x) for x in minus_y])
    print "min bits for derivative keys :", min([bits(x) for x in minus_y])
    M_n = constant_of_the_attack(n,q,f)
    return minus_A,minus_target, minus_sol, norm(vector(minus_sol)).n(), norm(vector(sol)).n(), M_n, e
