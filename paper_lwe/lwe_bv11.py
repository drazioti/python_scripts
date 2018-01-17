"""
 We provide a class for BV11 cryptosystem based on LWE. The code contains enough comments.
 Please, feel free to report bugs.
 
 AUTHORS:  K. Draziotis (drazioti@gmail.com), initial version : 20-5-2017

EXAMPLES: 
===========
#LWE and BV11 parameters 
import time
n=23;ell = 20;rho=4;ell1 =  floor(2*ell+4*log(rho));t=2^ell1                
q=next_prime(t * (2^(16.5*rho+5.4)*8^(2*rho-3)*n^rho) )
alpha1 = 3.2*sqrt(2*pi);
sigma = (alpha1/sqrt(2*pi)).n()

X = lwe_operation()    # Create an instance of the class lwe_operation
lwe, secret_key = X.initialize_lwe(n,q,sigma)

#two auxiliary funtions:
#the first one generates some points in ZZ^d having entries in the interval  (1, (t^.5)/(d*N) )
#the second extends the classical lwe_encrypt for points.

def Gen(d,N,t):
    P = []
    def random_between(j,k):
        a = int(random()*(k-j+1))+j
        return a
    for i in range(N):
        Q = [random_between(1,floor( (t^.5)/(d*N) )  ) for i in [0..d-1]] # random integer points with at most ell-bits
        P.append(Q)
    return P
 
def client_encrypt_points(N,P,t,n,q,secret_key):
    c = []
    d = len(P[0])
    for j in range(N):
        c.append([X.encrypt_lwe(P[j][i],t,n,q,secret_key) for i in range(dim)])
    return c
 

dim =  12 # the dimension of the space
N   =  1  
print "dim",dim

P = Gen(dim,N,t)
Q = Gen(dim,N,t)
print "The points:"
print P
print Q
c = client_encrypt_points(N,P,t,n,q,secret_key) # c returns a list of encypted points
d = client_encrypt_points(N,Q,t,n,q,secret_key) # c returns a list of encypted points
c0 = [c[0][i] for i in range(dim)]
d0 = [d[0][i] for i in range(dim)]
A=time.time()
I = X.inner_product( c0, d0,n,q)[0][0] # c1*c2
B=time.time()
print "Decrypt, after the computation of the homomorphic inner product :",X.decrypt_lwe_mult(I,n,secret_key,t,q)
print "The inner product :",vector(P[0]).dot_product(vector(Q[0]))
C=time.time()
print "========="
print "homomorphic (cpu-time):",B-A
print "non-homomorpic (cpu time):",C-B

RESULTS :
=========
dim 12
The points:
[[310069, 323501, 225223, 68327, 246093, 39058, 135837, 317702, 483650, 351473, 482597, 14913]]
[[175956, 39624, 251214, 103001, 418586, 1375, 409014, 201158, 86005, 488524, 358186, 104257]]
Decrypt, after the computation of the homomorphic inner product : 741239735304
The inner product : 741239735304
=========
homomorphic (cpu-time): 1.60890603065
non-homomorpic (cpu time): 0.0596539974213

          
             
"""

#*****************************************************************************
#       Copyright (C) 2017 K.Draziotis <drazioti@gmail.com>
#               
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

##### We need to choose our keys such that the resulting system be secure #####
# Say we have the security parameter of LWE, lambda. Usually lambda=80 
# So for a given security parameter *lambda* and given *n* we must choose
# https://eprint.iacr.org/2015/046.pdf
# 1.the width and sigma of the Gaussian distribution                 
# 2. the prime q

# The disrtibution we use is the discrete gaussian overn Z^n with     
# width paramter alpha*q. First do not choose alpha*q<\sqrt{n}, since
# then there is a subexponential attack.
# So always choose alpha*q>=\sqrt{n}.

# We define four operations :
# Addition, Multiplication, Scalar Multiplication, Inner Product
# Remark that Addition also works for negative integers. The same for multiplication.
# We define the class : lwe_operation()
# and four methods : add, mult, scalar, inner


reset()        # restart sage
      
class lwe_operation(object):
    global DiscreteGaussianDistributionIntegerSampler,LWE, samples     
    from sage.crypto.lwe import balance_sample,Regev
    from sage.crypto.lwe import samples,LWE          # we import the basic modules samples and LWE
    from sage.stats.distributions.discrete_gaussian_integer import DiscreteGaussianDistributionIntegerSampler
        
    def initialize_lwe(self,n,q,sigma):
        D = DiscreteGaussianDistributionIntegerSampler(sigma)
        lwe= LWE(n,q, D=D)
        secret_key = lwe._LWE__s
        return lwe,secret_key           # exports the object lwe and the corresponding secret key
    
    # assume t is even
    global representation_modulo_t
    def representation_modulo_t(a,t): #returns a in {-t/2,...,t/2}
        if t%2!=0:return "t must be even"
        rem = int(mod(a,t))
        if a>0:
            if rem ==t/2:return rem
            if rem>t/2:
                return rem-t
            else:
                return rem
        else:
            rem1 = rem - t
            if rem ==t/2:return rem1
            if rem>-t/2:
                return rem
            else:
                return t-rem
                
    def encrypt_lwe(self,m,t,n,q,s): # m : message, t: The parameter of BV11
        if t>q:
            print "t must be smaller than the modulus q.\n Please choose a new t"
            return 0
        if t<=m:
            print "*the first argument m* must be larger than (the second argument) t "
            return 0
    
    # Every time that we call the function encrypt_lwe, a new "a" and "e" is generated. 
    # So, for the same message we have a different ciphertext. 
    # That is, the encryption is probabilistic (and not determenistic)
    
        S = samples(1,n,lwe)                #  this is a function implemented in sagemath which returns a vector \bf{a} for lwe
    
        a = vector(ZZ,S[0][0])              # the vector a, we transform it to a vector over Z
    
    
        D = DiscreteGaussianDistributionIntegerSampler(sigma=sigma)
        e = int(D())
    ### TODO : YOU must allow e to take negative values
    ### Q : It is the same if we consider emod q instead of e<0 ?
    
        if e<0:
            e=q-e
    # e maybe positve or zero or negative
        dot = int(a.dot_product(s) %q ) #dot is integer, this will be the *aux* polynomial in decrypt()
    
    
        dot_q = int((dot+t*e+m)%q); # this is the encryption of m, where m\in (-t/2,t/2), m!=-t/2,t/2
                                    # dot_q always is in {0,1,...,q-1}
   
   # if representation_modulo_t(dot_q - dot,t) == representation_modulo_t(t*e + m,t):
   #     print "ok"
        c = [a,dot_q]
        return c,a  #,e  # note that e does not send to Bob, onle c is sent to Bob
        
    def decrypt(self,c,t,n,q,s): # this function just decrpyts a ciphertext without previous applied add or mult
        A1 = [(', '.join('x%i'%i for i in [0.. n-1]))];
        V  = var(A1[0])
        P1 = PolynomialRing(GF(q),A1[0])  
    ### construct the decryption polynomial
        auxf = P1(vector(c[0][0]).dot_product(vector(V)))
        aux  = int(auxf(list(s)))%q     # aux in in Z_q and not Z
    
    # the problem here is that aux is not always = dot_q (dot_q=c[0][1])
    
        if c[0][1]-aux<0:             #It seems that in this case e<0. c[0][1] is the dot_q in encrypt()        
            return -representation_modulo_t(aux-c[0][1],t)
        else:
            return representation_modulo_t(c[0][1]-aux,t)
            
    global decrypt_
    def decrypt_(self,c,t,n,q,s): # this function just decrpyts a ciphertext without previous applied add or mult
        A1 = [(', '.join('x%i'%i for i in [0.. n-1]))];
        V  = var(A1[0])
        P1 = PolynomialRing(GF(q),A1[0])  
    ### construct the decryption polynomial
        auxf = P1(vector(c[0][0]).dot_product(vector(V)))
        aux  = int(auxf(list(s)))%q     # aux in in Z_q and not Z
    
    # the problem here is that aux is not always = dot_q (dot_q=c[0][1])
    
        if c[0][1]-aux<0:             #It seems that in this case e<0. c[0][1] is the dot_q in encrypt()        
            return -representation_modulo_t(aux-c[0][1],t)
        else:
            return representation_modulo_t(c[0][1]-aux,t)
     
    def add(self,c1,c2,q):
        if c1[0][1]+c2[0][1]>q:    
            return flatten((c1[0][0] + c2[0][0],c1[0][1]+c2[0][1]-q)),c1[0][0] + c2[0][0] #,c1[2] + c2[2]  
        return flatten((c1[0][0] + c2[0][0],c1[0][1] + c2[0][1])),c1[0][0] + c2[0][0] #,c1[2] + c2[2]   
    
    global add_
    
    def add_(c1,c2,q):
        if c1[0][1]+c2[0][1]>q:    
            return flatten((c1[0][0] + c2[0][0],c1[0][1]+c2[0][1]-q)),c1[0][0] + c2[0][0] #,c1[2] + c2[2]  
        return flatten((c1[0][0] + c2[0][0],c1[0][1] + c2[0][1])),c1[0][0] + c2[0][0] #,c1[2] + c2[2]   
 
    def mult(self,c1,c2,n,q): 
        A1 = [(', '.join('x%i'%i for i in [0.. n-1]))]; 
        V = var(A1[0]) # we define a finite field GF(q) 
        P1 = PolynomialRing(GF(q),A1[0]) 
    # To perform multiplication if you have the ciphertexts c1 = (a1,b1) and c2 = (a2,b2) 
    # we first must compute the polynomials f_c1, f_c2 and then compute the product 
    # Here we do not use Relin.
        f1 = c1[0][1] - c1[0][0].dot_product(vector(V)) 
        f2 = c2[0][1] - c2[0][0].dot_product(vector(V)) 
        f1 = P1(f1) 
        f2 = P1(f2) 
        product = expand(f1*f2) 
        g = P1(product) 
        F2 = Sequence([g]) 
        A,v = F2.coefficient_matrix(); 
        return A,v.transpose()
        
    global mult_
    def mult_(c1,c2,n,q): 
        A1 = [(', '.join('x%i'%i for i in [0.. n-1]))]; 
        V = var(A1[0]) # we define a finite field GF(q) 
        P1 = PolynomialRing(GF(q),A1[0]) 
    # To perform multiplication if you have the ciphertexts c1 = (a1,b1) and c2 = (a2,b2) 
    # we first must compute the polynomials f_c1, f_c2 and then compute the product 
    # Here we do not use Relin.
        f1 = c1[0][1] - c1[0][0].dot_product(vector(V)) 
        f2 = c2[0][1] - c2[0][0].dot_product(vector(V)) 
        f1 = P1(f1) 
        f2 = P1(f2) 
        product = expand(f1*f2) 
        g = P1(product) 
        F2 = Sequence([g]) 
        A,v = F2.coefficient_matrix(); 
        return A,v.transpose()
    
    
    def madd(self,C,n,q): # addition of dim encrypted texts
             
        m = add_(C[0],C[1],q)
        dim = len(C)
        if dim>=3:
            for i in range(2,dim):
                m = add_(C[i],m,q)
        return m

    global madd_
    
    def madd_(self,C,n,q): # addition of dim encrypted texts
        if len(C)==1:
            return flatten((C[0][0],C[0][1])),C[0][0] + C[0][0]
        m = add_(C[0],C[1],q)
        dim = len(C)
        if dim>=3:
            for i in range(2,dim):
                m = add_(C[i],m,q)
        return m
        
       
    
        
    def scalar(self,N,c,n,q): # N is a positive integer, c is the ciphertext, (n,q):LWE parameters
        if N<=1:
            return "N must be >1"
        m = add_(c,c,q)
        for i in range(N-2):
            m = add_(c,m,q)
        return m  
    
    
    def decrypt_lwe_mult(self,C,n,s,t,q): 
    # v<--C[1]
    # c<--C[0]
    # c   : is the ciphertext that Alice took from Bob( :cloud ).
    # Since we did not use Relin, c is a vector of Z_q^{(n+1)^2} 
    # v   : is an order over GF[x1,...,xn], works for one message and also if Bob performed addition of two messages
    # e   : is known to Alice, also the secret key s is known. 
    # n,t : are parameters of LWE, known to Bob and Alice.
        c = C[0];v = C[1];
    ### construct a suitable multivariate ring
        A1 = [(', '.join('x%i'%i for i in [0.. n-1]))];
        V = var(A1[0])
        P1 = PolynomialRing(GF(q),A1[0])  
    
    ### construct the decryption polynomial
     
        auxf = P1(vector(c.list()).dot_product(vector(v.list())))
        aux = auxf(list(s)) 
        max1 = max(c.list())

        if max1<int(aux):
            return -representation_modulo_t(q-aux,t)  #,aux1,c[0][1]
        else:
            return  representation_modulo_t(aux%q,t)
            
    def inner_product(self,C1,C2,n,q): # C1,C2 are lists of some ciphertexts. (n,q):LWE parameters     
        dim = len(C1)
       
        def add_m(c1,c2):
            A=vector(c1[0].list()) + vector(c2[0].list())
            return matrix(A),c1[1]   
        order = []               
        m1 = [] 
        m  = []
        s =  []
        m1 = mult_(C1[0],C2[0],n,q)
        m2 = mult_(C1[1],C2[1],n,q)
        m = add_m(m1,m2)
        order.append(m[1])
  
    
        if dim>=3:
           for i in range(1,dim-1):
       #print mult(c1[i],c2[i],n,q) 
               m1 = mult_(C1[i],C2[i],n,q)
               m2 = mult_(C1[i+1],C2[i+1],n,q)            
               m = add_m(m,m2)          
        out = []
    
        out.append([m,order])
        return out
        
        
    def sub(self,c1,c2,q):
        if c1[0][1] - c2[0][1]>0:          
            return flatten(( (c1[0][0] - c2[0][0])%q ,(c1[0][1] - c2[0][1])%q )),(c1[0][0] - c2[0][0])%q  
        return flatten(( -(c2[0][0] - c1[0][0])%q ,-(c2[0][1] - c1[0][1])%q  )), -(c2[0][0] - c1[0][0])%q    
    
    def add_vectors(self,C,n,q):    # C is a list of lists
        dim = len(C[0])             # the dimension space of our points
        
        column = [ [] for i in range(dim) ]
        for i in range(dim):
            column[i].append([item[i] for item in C])

        ## add the vectors
        vec = [ [] for i in range(dim) ]
        for i in range(dim):
            vec[i].append([madd_(self,column[i][0],n,q)][0][0])
        return vec
        
    def decrypt_points(self,C, t, n, q, s):
        return [decrypt_(self,C[i],t,n,q,s) for i in range(len(C)) ]
    
    def hom_distance(self,C1,C2,n,q): # C1,C2 are lists of some ciphertexts. (n,q):LWE parameters     
        
        dim = len(C1) # the dimension of C1
        
        def add_m(c1,c2):
            A = vector(c1[0].list()) + vector(c2[0].list())
            return matrix(A),c1[1] 
                     
        def sub_(self,c1,c2,q):
            if c1[0][1] - c2[0][1]>0:          
                return flatten(( (c1[0][0] - c2[0][0])%q ,(c1[0][1] - c2[0][1])%q )),(c1[0][0] - c2[0][0])%q #,c1[2] + c2[2]  
            return flatten(( -(c2[0][0] - c1[0][0])%q ,-(c2[0][1] - c1[0][1])%q  )), -(c2[0][0] - c1[0][0])%q #,c1[2] + c2[2]   
                       
        order = []               
        m1 = [] 
        m  = []
        s =  []
        sub = [ X.sub(C1[i],C2[i] , q) for i in range(dim) ]
        m1 = mult_(sub[0],sub[0],n,q)
        m2 = mult_(sub[1],sub[1],n,q)
        m = add_m(m1,m2)
        order.append(m[1])
        
        if dim>=3:
           for i in range(1,dim-1):
       #print mult(c1[i],c2[i],n,q) 
               m1 = mult_(sub[i],sub[i],n,q)
               m2 = mult_(sub[i+1],sub[i+1],n,q)            
               m = add_m(m,m2)          
        out = []
    
        out.append([m,order])
        return out
     
