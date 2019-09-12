''' 
Requirements : The code is written in Sagemath ver. 8.1
  
 AUTHORS: Marios Adamoudis 
          2019: initial version 
 REFERENCES:  http://www.sagemath.org/
 * Please report bugs *
The following code implements the attack : "Babai attack". === Table 1 ===
 

# FOR INSTANCE : Experiment for n=206, a=158 bits, all derivative ephemeral=157 bits and 
# f = (ln(c*(n+1))).n()/(b*n^d*ln(q)).n() with b=2 c=d=1  and LLL preprocessing

k=157
a=158
n=206
sum=0
for i in range(100): # 100 instances
    q,A,target1,target2,sol,nr,M_n = equivalences_dsa(n,a,k,55/100)   
    M = matrix_dsa(A,q,n)
    M = M.LLL()
    M_GS = M.gram_schmidt()[0]
    bold = vector(target1)
    babold = babai(M,M_GS,bold)
    if ( (babold[0]== sol[0]) or (babold[0]== sol[0]+1) or (babold[0]== sol[0]-1) ):
         print("True")
         sum=sum+1
         print("babold[0]- sol[0]="),babold[0]- sol[0]
         print("----------------------------------")
    else:
        print("False")
        print("babold[0]- sol[0]="),babold[0]- sol[0]
        print("----------------------------------")     
print (sum/100*100).n()

'''

def constant_of_the_attack(n,q,f,C):
    M_n = C * q^(f+n/(n+1))
    return M_n.n()
    
def matrix_dsa(B,q,n):
    '''B is a list : the first row of the DSA matrix'''
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
    w=vector(t)
    t=vector(t)
    for i in range(rank(M)-1,-1,-1):
        w = w - round((w.dot_product(M_GS[i]))/(M_GS[i].norm())^2)*M[i]
    return t - w
    

def equivalences_dsa(n,BITS,BITS_e,C): 
    '''
     We generate DSA parameters. In fact we generate a vector (x,y_1,...,y_n)
     which is a solution of a system y_i + A_ix_i + B_i = 0 mod q
     where A_i are chosen as in Proposition 
        input
        -----
        > n      : number of messages to be signed
        > BITS   : number of bits of the secret key
        > BITS_e : number of bits of the (derivative) ephemeral keys (yi=AiCi^{-1}ki mod q
        f = (ln(c*(n+1)))/(b*n^d*ln(q))
        
        
        output
        ------
        > a vector B = (0,b1,...,bn) : the target vector
        > a vector A = (A1,A2,...,An), with Ai in suitable intervals
        > the solution vector (a,y1,y2,...,yn) for the n equivalences : yi + Ai*x + bi =0 mod q.
        > the norm of the solution vector
        > the Gaussian Heuristic
       
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
            y.append(int(ZZ.random_element( 2^(159), q))); # the derivative of the ephemeral keys are at most q-bits
    else:
        for i in range(0,n):
            y.append(int(ZZ.random_element(2^(BITS_e-1) ,2^BITS_e-1))); # the derivative of the ephemeral keys, have BITS_e bits
    A = []
    yi = []
    B = []
    sol = []
    F = []
 
    # here we choose b,c,d    
    
    b = 2      
    b = 1 
    c = 1   
    d = 1      
    f = (ln(c*(n+1))).n()/(b*n^d*ln(q)).n()

   
    for i in range(1,n+1):
        temp=floor( C*q^( i/(n+1)+f )   )+1
        A.append(int(temp))  
        
            
    # we generate the constant terms of the system        
    for i in range(n):
        B.append(int(mod(-y[i]-A[i]*a, q)) ) # the vector of constants B
        F.append(int(mod(y[i]+A[i]*a, q)) )
        
            
    sol = [a] + y
    target1 = [0]+B
    target2 = [0]+F
    M_n = constant_of_the_attack(n,q,f,C)
    return q,A,target1,target2,sol,norm(vector(sol)).n(),M_n