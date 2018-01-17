"""
 We implemented the method provided in the paper :
 Solving Subset Sum Problems of Density close to 1 by "randomized" BKZ-reduction
 by Claus P. Schnorr and Taras Shevchenko 
 We compare the previous method with two variants.
 
 Requirements : The code uses the library fpyLLL and is written in python2.
  
 AUTHORS: K. Draziotis (2016): initial version
 
 EXAMPLES:
 
 We need to execute the following code:
 >> import sys
    f = open('foo.txt', 'w') # the name of the file where the outputs will be written
    orig_stdout = sys.stdout    
    sys.stdout = f
    for i in range(20): # The number of instances
      print ('------------------',i+1,'-----------------')
      F = find_random(80,1,40)    
      G1 = schnorr2(F[0],F[1],F[3],30) # the original method
      print G1
      G2 = schnorr_variant_with_initial_bits(F) # the variant
      print G2
    sys.stdout = orig_stdout
    f.close()
 
 
 The output (for the first variant) will be a text file containing data of the following form :
 
 ('------------------', 1, '-----------------')
('Solution found!', array([0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0,
       1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0,
       1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0,
       1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0]))
Overall time/round :  758.919426
Round: 14
Density : 1.00009284585
1
Now we measure the time using the Schnorr variant...
new density: 0.950088203555
new dimension: 76
('Solution found!', array([1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1,
       0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0,
       1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0,
       1, 0, 1, 0, 0, 1, 0]))
Overall time : 39.897118
Round: 5
Density : 0.950088203555
Overall time (for all the rounds):  225.944332

In this example the original method took 758s and the variant 225s

To execute the second variant, we executed the following code :
>>  import sys
    orig_stdout = sys.stdout
    f = open('foo.txt', 'w') # the name of the file where the output will be written
    sys.stdout = f
    for i in range(10):
      F = find_random(80,1,40)  # we generate a random hard knapsack instance of dimension  80
      if F[5][0] == 1:          # this is probabilistic method. So it will work only if we know the first bit.
        print "===============",i+1,"===================="
        G1 = schnorr2(F[0],F[1],F[3],30)  # we execute the original method
        # we execute our variant :
        G = update(F)                   
        print G[2]
        G2 = schnorr2(G[0],G[1],G[3],30)
        print G1
        print('****************************************')
        print G2
    sys.stdout = orig_stdout
    f.close()
    
The output (for the second variant) will be a text file containing data of the following form :



 
 REFERENCES:  [1] Solving Subset Sum Problems of Density close to 1 by "randomized" BKZ-reduction
 by Claus P. Schnorr and Taras Shevchenko [https://eprint.iacr.org/2012/620]
              [2] python 2
              [3] fpyLLL (based on fpLLL version 4.2)
              [4] numpy
"""

#*****************************************************************************
#       Copyright (C) 2016 K.Draziotis <drazioti@gmail.com>
#                         
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************


# The basic libraries we used

from fpylll import *
import random,math,operator,time
from operator import itemgetter
import numpy as np
from __future__ import division
from numpy import matrix
from numpy import linalg as LA
from numpy import matlib

# Some auxiliary functions

## The dot product of two vectors
def dot_product(a,b):
    return sum(map( operator.mul, a, b))

## Generation of a random vector of dimension N with K zeros 
def rand_bin_array(K, N): # K zeros, N-K ones
    arr = np.array([0] * K + [1] * (N-K))
    np.random.shuffle(arr)
    return  arr

## Generation of a random knapsack instance of density closed to 1 (i.e. a hard one)
def find_random(n,d,hamming): # n: dimension, d: density, hamming: the Hamming weight of the solution
    a =  [random.randint(1,2**((2-d)*n)) for _ in xrange(n)]     
    density=float(len(a)/math.log(max(a),2));
    solution = rand_bin_array(n-hamming,n)
    a0 = dot_product(solution,a);      
    aold=a;
    a0old=a0;
    return a,a0,density,sum(solution),len(solution),solution
    
## Soring of the rows of a matrix with respect their Euclidean norm
def permutation(B,n):
    k=0;
    for i in range(n+1):
        if B[i-k,n+1]==0:
            temp=B[i-k];
            B = np.delete(B,i-k,0); # delete row i-k
            B = np.vstack([B,temp]);
            k=k+1;
    if k!=0:
        l=[]
        
        for i in range(n+1-k,n+1):
            l = l + [LA.norm(B[i])]
        list=B[n+1-k:n+1,:]
        L=sorted(zip(l,list),key = itemgetter(0))
        sorted_B=[list for (l,list) in L] 
        m = matrix([sorted_B[i].tolist()[0] for i in range(len(sorted_B))])        
        B = np.vstack([matrix(B[0:n+1-k,:]),m])
    return B
    
## *This is a techinicality* We convert a fpyLLL type matrix to a matrix than numpy can understand (and vice verca)   
def fp2mat(A):    
    L = np.zeros(shape=(A.nrows,A.ncols))
    for i in range(A.nrows):
        for j in range(A.ncols):
            L[i,j] = A[i,j]
            L = matrix(L)
    return L

def mat2fp(A):
    L = IntegerMatrix(A.shape[0],A.shape[1])
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            L[i,j] = int(A[i,j])
    return L
   
## The following function checks if a specific binary vector b of dimension n, is a solution of a knapasack problem
## The binary vector b will be an -intermediate- output of Schnorr-Shevchenko algorithm 
## The function will check if b satisfies specific properties according to the paper
    
def checking(b,n):
    i=0
    x=np.array([0 for _ in range(n)])
    
    check=(int(abs(b[n+1]))==1)
    
    while (check==True)&(i<n):
        check=(int(abs(b[i]))==1)
        i=i+1
    
    if (i==n) & (check==True) & (b[n]==0) & (b[n+2]==0):
        
        for j in range(n):
            x[j]=abs(b[j]-b[n+1])/2
        return 'Solution found!',x
    else:
        return "There's no solution"
    
## This is the implementation of SS method :

def schnorr2(a,a0,hamming,j1): # j1 is the number of rounds for the second stage of the algorithm
    density=float(len(a)/math.log(max(a),2));
    n = len(a)
    if n==80:
        N = 16    # N must be >\sqrt{n} according to the paper
        ### We consider many cases instead the usual one n = 80
        
    if n<=60 and n>=50:
        N = 12
    if n<80 and n>60:
        N = 16
    if n>80 and n<90:
        N = 18
    if n>90 and n<=100:
        N = 20
    L=matrix([[N*int(a[i]) for i in range(0, n)],[0 for i in range(0, n)],[N for i in range(0, n)]]);
    L=L.T; # the transpose
    M1 = np.matlib.identity(n) #identiny nxn numpy matrix
    M1 = 2*M1;
    
    Mb = np.bmat([M1,L])
    zerom = matrix([1 for i in range(0, n)]);
    zerom1 = np.bmat([zerom,matrix(N*int(a0)),matrix(1),matrix(int(hamming*N))]) #side by side
    B = np.vstack([Mb,zerom1]); #Mb above zerom1
    B_old = B
    
         ### main algorithm (round: 1-5)

    overall = 0
    flag = 0
    t1=time.clock()   
    for j in range(1,6):
          
        B = permutation(B,n) 
        B=mat2fp(B)
        par = BKZ.Param(block_size=2**j, pruning = 0)
        BKZ.reduction(B, par)
        B=fp2mat(B) # trasform fpylll.matrix to numpy.matrix        
        b = B[0]
        b = np.array(b).flatten()       
        
        if checking(b,n)[0]=='Solution found!':
           
            print checking(b,n)
            print "\x1b[31mOverall time : \x1b[0m",  time.clock() - t1
            print "Round:", j
            print "Density :", density
            flag = 1
            return 1
            break
        else:
            #print "Round: ", j
            continue
    while(flag == 0): #I use the variable flag to exit from the nested loop in case we found a solution
        
        flag = 1    
             
        for j in range(j1): #number of rounds
            
            ## In case we do not find any solution, since this method is heuristic, we add the following two lines of code.
            ## (Although we did not get any example that the method failed)
            
            if j == j1 - 1:
                flag = 1           
            
            B = B_old;
            B = permutation(B,n)
            z = (30+j)%3
            
            B=mat2fp(B)
            
            if n<60 and n>=50:
                par = BKZ.Param(block_size=20+j, pruning = 0)
            if n<70 and n>=60:
                par = BKZ.Param(block_size=30+j, pruning = 8+z)
            if n<=80 and n>=70:
                par = BKZ.Param(block_size=30+j, pruning = 10+z)
            if n>80 and n<=90:
                par = BKZ.Param(block_size=30+j, pruning = 11+z)
            if n>90 and n<=100:
                par = BKZ.Param(block_size=30+j, pruning = 12+z)
            
            BKZ.reduction(B, par)
            B=fp2mat(B) # trasform fpylll.matrix to numpy.matrix        
            b = B[0]
            b = np.array(b).flatten()
           
            if checking(b,n)[0]=='Solution found!': 
                print checking(b,n)
                print "Overall time : ", time.clock() - t1
                print "Round:", 6+j
                print "Density :", density
                flag = 1
                return 1
                break                           
            else:
                #print "Round: ", 6+j
                continue

## This is the first variant :

def schnorr_variant_with_initial_bits(F):
    T = time.clock()
    R1 = []
    k =  4
    max_round = 6 #i.e. overall rounds 5+6=11
    l1 = list(itertools.product([0, 1], repeat=k))
    R1 = list(F[0])
    del R1[0:k]
    new_dimension = len(R1)
    new_density =float(len(R1)/math.log(max(R1),2));
    print "Now we measure the time using the 1st variant..."
    print "new density:", new_density
    print "new dimension:", new_dimension
    i = 1
    for l in l1:
        a0 = sum(l[j]*F[0][j] for j in range(len(l)))
        R1 = list(F[0])
        del R1[0:len(l)]
        new_hamming = sum(F[5])-sum(l)    
        S = schnorr2(R1,F[1]-a0,new_hamming,max_round)
        if S==1:
            S
            break
        i = i+1
    print 'Overall time : ', time.clock()-T  
 
## this is the second variant :

def update(F):
    n = F[4]
    a = random.randint(1,2**(n+6))
    F[0][0] = int(F[0][0] + 2**(n+6))
    F = list(F)
    FF = F[1] 
    F.pop(1)
    F.insert(1,int(FF+2**(n+6)))
    density=float(len(F[0])/math.log(max(F[0]),2))
    F.pop(2)
    F.insert(2,density)
    F = tuple(F)
    return F
  
