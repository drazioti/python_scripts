"""
 We implemented a branch and bound method to compute positive integer solutions
 of a linear diophantine equation a1x1+...+anxn=c, where 0<a_j<x_j<b-j :
  
 Requirements : The code is writen in Sagemath  ver. 6.9
 AUTHORS: A. Papadopoulou (2016): initial version
 
 EXAMPLES:
 
 Executing the code 
 
n=20  #dimension
R=10  #solution's bits
t=0
k=1  #number of experiments
Y = 2^(R+t)-1
sum=0
for i in range(k):
    F=find(n,R,t) #construct the compact knapsack
    p=alg2(F,n,R+t) #search for a bounded solution
    sum=sum+p[0] 
print "Successes:",sum #total successes
 
we get an output of the form:

Initial solution:  [216, 117, 638, 856, 1044, 5, 925, 328, 783, 3, 29,
25, 27, 1086, 26, 10, 142, 16, 18, 24]
iterations: 30649
 
xd=  [516, 131, 981, 575, 690, 130, 981, 888, 981, 788, 134, 528, 133,
980, 131, 676, 130, 131, 974, 131]
 
First v= 14 Last v= 8
First z= 2 Last z= 0
 
Successes: 0
 
 
 REFERENCES:  [1] Solving Subset Sum Problems of Density close to 1 by "randomized" BKZ-reduction
 by Claus P. Schnorr and Taras Shevchenko [https://eprint.iacr.org/2012/620]
              [2] python 2
 
"""

#*****************************************************************************
#       Copyright (C) 2016 A. Papadopoulou <anastasia3g@hotmail.com>
#                         
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************





import numpy as np

# construct the compact knapsack

def find(n,R,t): #n=dimension, R=number of bits, t=parameter of solution's bits
#construct the parameters a[i] such that half of them have R-bits and the other half have R/2-bits
        a1 = vector([ZZ.random_element(0,2^(floor(R/2))-1) for _ in range(n/2)])
        a2 = vector([ZZ.random_element(2^(floor(R/2))-1,2^(R)-1) for _ in range(n/2)])
        a=list(a1)+list(a2)
        a=np.array(a)
        a = np.random.permutation(a)
        a = vector(a)
        solution = vector([ZZ.random_element(2^(R-1+t),2^(R+t)-1) for _ in range(n)])
        a0 = solution.dot_product(vector(a));     
        return a,a0,solution,norm(solution).n()
        
# use a variant of lenstra for the computation of the initial solution

def second_version(n,a,a0,Y):
    r=0;
    
    #construction of the basis
    zerom=matrix(QQ,1,[r for i in range(0, n)]); # part of the last row
    X=[Y for i in range(0, n)];
    L=matrix(QQ,2,[[0 for i in range(0, n)],[a[i] for i in range(0, n)]]);
    L=L.transpose();
    M = identity_matrix(ZZ, n);
    M=matrix(QQ,n,[1/X[i]*M.row(i) for i in range(0,n)]);
    Mb=block_matrix([[M,L]]);
    zerom1=block_matrix([[zerom,1,-a0]]);  # this is the last row
    Mb1=Mb.stack(zerom1);
    
    L=Mb1.LLL();   #use LLL algorithm for basis reduction
    L1=[[(L[j][i]-r)*X[i] for i in range(0,n)] for j in range(0,n+1)];#if the last row has 1/2 instead of 0
    L2=[vector(L1[i]).dot_product(vector(a))-a0 for i in range(0,n+1)];
    if L2.count(0)>0:
        return L1[L2.index(0)],float(vector(L1[L2.index(0)]).norm()),L1
    else:
        return "NULL"
        
def alg2(F,n,R): 
 
    u=2^(R)-1  #upper bound
    l=2^(R-1)  #lower bound

    #call a method for finding a solution 
    N2 = 2^(R+t)
    Sec_ver = second_version(n,F[0],F[1],N2)
    L1 = Sec_ver[2]
    
    xd=Sec_ver[0]  #initial solution
    print "Intial solution: ", xd

    def vbound(xd,n):  #count the lower violated bounds
        num=0
        for j in range (n):
            if xd[j]<l : 
                num=num+1 
        return num
    
    def zbound(xd,n): #count the upper violated bounds
        num=0
        for j in range (n):
            if xd[j]>u : 
                num=num+1 
        return num
    
   
    def rng(xd):    #compute the range of solution's coordinates
        mx=max(xd)
        mn=min(xd)
        e=mx-mn
        return e
        
    def try_positive(xd,v,z,n,L1):  #search for a solution with less violated bounds(1) 
        r=0      
        e=rng(xd)
        i=0
        k=1  #positive linear combinations of the basis vectors
        while((v>0)|(z>0))&(i<n-1) :
            r=r+1
            xd2=xd
            xd=[xd[j]+k*L1[i][j] for j in range(n)]
            e2=rng(xd)
            v2=vbound(xd,n)
            z2=zbound(xd,n)
            if (e2<=e)&(v2<=v)&(z2<=z): #the condition in order to keep the new solution
                e=e2
                v=v2
                z=z2
                k=k+1
            else:
                xd=xd2
                i=i+1
                k=1
                v=vbound(xd,n)
                z=zbound(xd,n)
                e=rng(xd)
        return xd,v,z,r       
                

    def try_negative(xd,v,z,n,L1): #search for a solution with less violated bounds(2)
        r=0         
        e=rng(xd)
        i=0
        k=-1  #negative linear combinations of the basis vectors
        while((v>0)|(z>0))& (i<n-1) :
            r=r+1
            xd2=xd
            xd=[xd[j]+k*L1[i][j] for j in range(n)]
            e2=rng(xd)
            v2=vbound(xd,n)
            z2=zbound(xd,n)
            if (e2<=e)&(v2<=v)&(z2<=z):
                e=e2
                v=v2
                z=z2
                k=k-1
            else:
                xd=xd2
                i=i+1
                k=-1
                v=vbound(xd,n)
                z=zbound(xd,n)
                e=rng(xd)
        return xd,v,z,r                    
   
   
    v=vbound(xd,n)
    z=zbound(xd,n)
    initial_v=v
    initial_z=z
    
    i=0   
    r2=0
    s1=0
    s2=0
    K = 250  #experimental number of tries = 150
    while ((v>0)|(z>0))&(i<K):  
        i=i+1
        F=try_positive(xd,v,z,n,L1) #first try
        xd=F[0]
        if (xd==s1)&(xd==s2): #if the algortihm find the same solutions then stops
            print"CYCLE!"
            break
        v=F[1]
        z=F[2]
        r2=r2+F[3]
        s1=xd
        if (v>0)|(z>0):
            F=try_negative(xd,v,z,n,L1) #second try
            xd=F[0]
            v=F[1]
            z=F[2]
            r2=r2+F[3]
            s2=xd
        
    print "iterations:",r2   #number of total iterations
    print " "
    print"xd= ",xd     #the final solution
    print" "
    print"First v=",initial_v,"Last v=",v
    print"First z=",initial_z,"Last z=",z
    print " "
    p=0
    if (v==0)&(z==0):  #if all the violated bounds are 0 then we have a success
        p=1
        print"--------"
        print"SUCCESS"
        print"--------"
    return p,r2,i
