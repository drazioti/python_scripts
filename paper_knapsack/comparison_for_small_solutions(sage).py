"""
 We implemented the three following methods to find small solutions
 of a linear equation :
 
 1.  K. Aardal, C. Hurkens, A. Lenstra, Solving a linear Diophantine equation 
 with lower and upper bounds on the variables. Integer programming and 
 combinatorial optimization LNCS 1412, p.229--242, 1998.
 2.   K. A. Draziotis, Balanced Integer solutions of linear equations, AMIMS 2013(Greece), 
 Optimization and its Applications (SOIA), vol. 91, p. 173--188, Springer 2014.
 in order to compute small integer solutions of a linear equation.
 3. A variant of Solving Subset Sum Problems of Density close to 1 by "randomized" BKZ-reduction
 by Claus P. Schnorr and Taras Shevchenko [https://eprint.iacr.org/2012/620]

 Then, we compared them.
 
 Requirements : The code is written in sagemath ver. 6.9
  
 AUTHORS: K. Draziotis (2016): initial version
 
 EXAMPLES:
 
 
 REFERENCES:  [1] Solving Subset Sum Problems of Density close to 1 by "randomized" BKZ-reduction
 by Claus P. Schnorr and Taras Shevchenko [https://eprint.iacr.org/2012/620]
              [2] sagemath          
              [3] numpy
"""

#*****************************************************************************
#       Copyright (C) 2016 K.Draziotis <drazioti@gmail.com>
#                         
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************



def find(n):
        a = vector([ZZ.random_element(2^n,2^(n+1)) for _ in range(n)])
        solution = vector([ZZ.random_element(-n,n) for _ in range(n)])
        a0 = solution.dot_product(vector(a));      
        aold = a;
        a0old = a0;
        return a,a0,solution,norm(solution).n()

#### 1st algorithm : Lenstra's et al algorithm 
##############################################

def Lenstra(n,a,a0,N1,N2):
    zerom=matrix(1,n,0);
    X=[1 for i in range(0, n)];
    L3 = [];L1 = [];L2 = [];
    L3=matrix(ZZ,2,[[0 for i in range(0, n)],[N2*a[i] for i in range(0, n)]]);
    L=L3.transpose();
    M = identity_matrix(ZZ, n);
    Mb=block_matrix([[M,L]]);Mb;Mb.dimensions();
    zerom=block_matrix([[zerom,N1,-N2*a0]]);
    Mb1=Mb.stack(zerom)
    Mb1.dimensions()
    L=Mb1.LLL()    
    # here we compute all the inner product, and if someone is zero I retrieve the solution
    L1=[[L[j][i] for i in range(0,n)] for j in range(0,n)];
    L2=[vector(L1[i]).dot_product(vector(a))-a0 for i in range(0,n)]; 
    if L2.count(0)>0:
        return L1[L2.index(0)], float(vector(L1[L2.index(0)]).norm())
    else:
        return "NULL"

# second algorithm

def draz(n,a,a0,par):
    r=0;
    zerom=matrix(QQ,1,[r for i in range(0, n)]); # part of the last row
    X=[par for i in range(0, n)];
    L=matrix(QQ,2,[[0 for i in range(0, n)],[a[i] for i in range(0, n)]]);
    L=L.transpose();
    M = identity_matrix(ZZ, n);
    M=matrix(QQ,n,[1/X[i]*M.row(i) for i in range(0,n)]);
    Mb=block_matrix([[M,L]]);
    zerom1=block_matrix([[zerom,1,-a0]]);  # this is the last row
    Mb1=Mb.stack(zerom1);#show(Mb1);
    L=Mb1.LLL();
    L1=[[(L[j][i]-r)*X[i] for i in range(0,n)] for j in range(0,n+1)];#if the last row has 1/2 instead of 0
    L2=[vector(L1[i]).dot_product(vector(a))-a0 for i in range(0,n+1)];
    if L2.count(0)>0:
        sol = L1[L2.index(0)]
        return sol,vector(sol).norm().n()
    else:
        return "NULL"               

### algorithm of schnorr-shevchenko (suitable variant)

import numpy
from time import time

def checking(b,n):
    x=vector([0 for _ in range(n)])   
    if  (b[n]==0) & (abs(b[n+1])==1):       
        for i in range(n):
            if b[n+1]==-1:
                x[i]=(b[i]-b[n+1])/2
            if b[n+1]==1:
                x[i]=(-b[i]+b[n+1])/2                
        return 'Solution found!',x
    else:
        return "NULL"


            
def schnorr(n,a,a0):

    if n<10:
        N=4;
    elif n<30:
        N=8
    elif n<60:
        N=12
    else:
        N=16
    
    L=matrix(ZZ,2,[[N*a[i] for i in range(0, n)],[0 for i in range(0, n)]]);
    L=L.transpose(); 
    M1 = identity_matrix(ZZ, n);
    M1=matrix(ZZ,n,[2*M1.row(i) for i in range(0,n)]); 
    Mb=block_matrix([[M1,L]]);
    Mb.dimensions();
    zerom=matrix(ZZ,1,[1 for i in range(0, n)]);
    zerom1=block_matrix([[zerom,N*a0,1]]);
    B = Mb.stack(zerom1);
    
    ### main algorithm (round: 1-5)
    best_so_far = 10^n # some very large number I take for the first comparison with the length of the first solution
    best_so_far_vector = []
    k=0
    t1=time()
         
    for j in [0..20]:
        z=(30 + j)%3 
        if floor(n/3) + j<n: #in order to make sense to consider blocksize=30+j
            B=B.BKZ(block_size=floor(n/3)+j, prune=5+z)
            for i in range (n+1):
                if B[i][n+1]!=0:
                    k=i;
                    break;
            b=B.row(k)
            ch=checking(b,n)
            if ch[0]=='Solution found!':
                if best_so_far>float(ch[1].norm().n()):
                    best_so_far = float(ch[1].norm().n())
                    best_so_far_vector = ch[1]
    
    return best_so_far_vector,best_so_far
  ### we execute the following experiments
from time import time
# we define a problem of dimension 20
n = 25 # the dimension of the compact knapsack, (we set our algorithm to work for n>=22)
F = find(n)

# we measure the norm of the solution and the cpu time for each one method
T = time()
first = Lenstra(n,F[0],F[1],300,500)
print "first:",first[1]
print time()-T
print "-----"
T = time()
Second = draz(n,F[0],F[1],n);
print "second",Second[1]
print time()-T
print "----"
T = time()
third = schnorr(n,F[0],F[1])
print "the SS variant:",third[1]
print third[1]
print time()-T
print vector(first[0]).dot_product(F[0])==F[1]
print vector(Second[0]).dot_product(F[0])==F[1]
vector(third[0]).dot_product(F[0])==F[1]
