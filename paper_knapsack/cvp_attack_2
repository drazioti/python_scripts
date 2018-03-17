"""
 We provide an attack to compact knapsack proble by reducing to a suitable CVP-problem.
 The solution set is of the form [a1,b1]^{n/3} x [a2,b2]^{n/3} x [a3,b3]^{n/3}  
 
 Requirements : The code is written in sagemath ver. 6.9
  
 AUTHORS: K. Draziotis : initial version
 
 EXAMPLES: 
    sage code:
    n,R,t=30,40,0
    Q=count(n,R,10,t,R,R/2,R/2, R,R,R/2) # the topology of the solution set is : R-bits x R/2 bits x R/4 bits. We run 10 instances.
    print
    print np.mean(Q),max(Q),min(Q),float(100*np.mean(Q)/n),float(100*max(Q)/n),float(100*min(Q)/n)
    
    result:
    20.0 20 20 66.6666666667 66.6666666667 66.6666666667

    We got 20 right bits of the solution
"""

#*****************************************************************************
#       Copyright (C) 2018 K.Draziotis <drazioti@gmail.com>
#                         
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************


import numpy as np

def number_of_good_entries(list,upper,lower,upper1,lower1,upper2,lower2): #the number of entries in the intrval [lower,uppper]
        C=0
        for i in range(len(list)):
            if (list[i]<=upper and list[i]>=lower) or (list[i]<=upper1 and list[i]>=lower1) or (list[i]<=upper2 and list[i]>=lower2):
                C=C+1      
        return C,len(list)-C #no. of good and bad entries  
    
    
#basis of the lattice L:sum(aixi=0)
def kernel(A):
    k=len(A)
    A=matrix(ZZ,[A])
    Q=A.smith_form()[2]
    X=matrix(ZZ,[Q.column(i) for i in range(1,k)])
    #print "A basis of the lattice is:"
    return X

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


def babai(B,v):
    Y=[]
    i=0
    j=0
    row=int(B.nrows())
    col=int(B.ncols())
    w=vector([0 for i in range(0,len(v))])
    Gram=B.gram_schmidt()[0]
    w=vector(v)
    for j in range(row):        
        i=row-j-1
        #print len(w),Gram.dimensions()
        c1=w.dot_product((Gram[i]))
        c2=Gram[i].dot_product(Gram[i])
        l=c1/c2
        e=floor(l+0.5)*(B.row(i))
        Y.append(e)
        w=w-(l-floor(l+0.5))*Gram[i]-(floor(l+0.5)*B.row(i))   
    u=sum(Y)        
    return u

def count_good(F,n,R,t,parameter1,parameter2,parameter3,parameter11,parameter22,parameter33):      
    u=2^(parameter1+t)-1   #upper bound
    l=2^(parameter1+t-1)   #lower bound
    u1=2^(parameter2+t)-1  #upper bound
    l1=2^(parameter2+t-1)  #lower bound
    u2=2^(parameter3+t)-1  #upper bound
    l2=2^(parameter3+t-1)  #lower bound
    #print "u,l,u1,l1,u2,l2:",u,l,u1,l1,u2,l2
        
    #we call a method for finding a solution to sum_i(aixi)=a0 
    N2 = 2^(R+t)
    Sec_ver = second_version(n,F[0],F[1],N2) 
    L1 = Sec_ver[2]   
    # we apply Babai to get a better initial solution i.e. with more hits in [lower,upper]
    A = kernel(F[0])
    Alll=A.LLL()
    #Alll=A.BKZ(block_size=35)
    target1 = [2^(parameter11+t-1)+2^(parameter11+t-2)]*int(n/3)
    target2 = [2^(parameter22+t-1)+2^(parameter22+t-2)]*int(n/3) 
    target3 = [2^(parameter33+t-1)+2^(parameter33+t-2)]*int(n/3)     
    target=vector(target1+target2+target3)
    #print target
    #target=vector(np.random.permutation(target))
    babai_vector = babai(Alll,target) # a closest vector to target  
    Xdn = [vector(Sec_ver[0])-i*vector(babai_vector) for i in range(220)] #the vector return by CVP method
    Xdp = [vector(Sec_ver[0])+i*vector(babai_vector) for i in range(220)] #the vector return by CVP method 
    
    xd10=Sec_ver[0]  #initial solution
    
    C1=[number_of_good_entries(list(Xdn[i]),u,l,u1,l1,u2,l2)[0] for i in range(220)] 
    C2=[number_of_good_entries(list(Xdp[i]),u,l,u1,l1,u2,l2)[0] for i in range(220)] 
    C3=max(max(C1),max(C2)) # since +v or -v are both closest we consider the better for our situtation
    L=C1+C2
    M=Xdn+Xdp
    max_index=L.index(max(L))
    xd = M[max_index]
    return C3  # we return the number of good entries using cvp 
 
def find(n,R,t,parameter1,parameter2,parameter3): #n=dimension, R=number of bits, t=parameter of solution's bits
#construct the parameters a[i] such that half of them have R-bits and the other half have R/2-bits
        import numpy as np
        a1 = vector([ZZ.random_element(2^(floor(R/8)-1),2^(floor(R/8))-1) for _ in range(n/2)])
        a2 = vector([ZZ.random_element(2^(floor(R/4)-1),2^(floor(R/4))-1) for _ in range(n/2)])
        a=list(a1)+list(a2)
        a=np.array(a)
        #a = np.random.permutation(a)
        a = vector(a)        
        solution1= vector([ZZ.random_element(2^(parameter1-1+t),2^(parameter1+t)-1) for _ in range(n/3)])
        solution2= vector([ZZ.random_element(2^(parameter2-1+t),2^(parameter2+t)-1) for _ in range(n/3)])
        solution3= vector([ZZ.random_element(2^(parameter3-1+t),2^(parameter3+t)-1) for _ in range(n/3)])
        solution=vector(list(solution1)+list(solution2)+list(solution3))
        #solution=vector(np.random.permutation(solution))
        #print "----------"
        #print "solution:"
        #print solution,"\n"
        a0 = solution.dot_product(vector(a));    
        return a,a0,solution,norm(solution).n()
        
def count(n,R,k,t,parameter1,parameter2,parameter3,parameter11,parameter22,parameter33):
    A=[]
    
    for i in range(k):
        F=find(n,R,t,parameter1,parameter2,parameter3)
        A.append(count_good(F,n,R,t,parameter1,parameter2,parameter3,parameter11,parameter22,parameter3))
    return A
