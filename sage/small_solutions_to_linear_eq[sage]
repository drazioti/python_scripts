"""
We provide two algorithms for finding small solutions to linear equations using LLL reduction algorithm\
Tested in Sagemath
 AUTHORS:
 K. Draziotis (26-5-2015): initial version

 EXAMPLES: 
        sage:version()
        'SageMath Version 6.9, Release Date: 2015-10-10'
        sage:n=20;
        sage:  a=[872934623064, 362643350651979, 231593889792433, 1084529488472651, 152647947850799, 
          739407904067188, 1078361055147110, 522287723336618, 1048278073142822, 71464720981315, 
          1026144865912, 401128969656441, 1104125375426692, 223040948030783, 259134135114376, 
          477165086702863, 693696459173357, 956101007737750, 1076391779531258, 887808907972169]
        sage:  a0=2*a[1]+3*a[4]+a[5]+5*a[7]+6*a[9]+7*a[11]+8*a[17]+9*a[19]
        sage: draz(n,a,a0)
        ([-1, 2, 2, 3, -2, 2, 0, 3, 2, -2, -1, 4, 1, 0, 0, -1, 2, 2, 4, 5],
          10.5356537528527)
        sage:lenstra(n,a,a0)
        ([-1, 2, 2, 3, -2, 2, 0, 3, 2, -2, -1, 4, 1, 0, 0, -1, 2, 2, 4, 5],
        10.5356537528527)
          

 REFERENCES: [1] K. Aardal, Cor. A.J. Hurkens, A.K. 
              Lenstra Solving a system of linear diophantine equation with lower and upper bounds on the variables.
               Math. Oper. Res. 25 (2000), no. 3
             [2] K.A.Draziotis, Balanced Integer solutions of linear equations,
              Springer Optim. Appl., 91, Springer, Cham, 2014.
"""

#*****************************************************************************
#       Copyright (C) 2015 K.Draziotis <drazioti@gmail.com>
#               
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

#############################
##### 1st algorithm  ########
#############################
def draz(n,a,a0):
    print(n);
    r=0;
    zerom=matrix(QQ,1,[r for i in range(0, n)]); # part of the last row
    X=[5 for i in range(0, n)];
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
        return L1[L2.index(0)]

##############################################
#### 2nd algorithm : Lenstra's et al algorithm 
##############################################

def lenstra(n,a,a0):
    
# N1,N2 are the parameters of the lattice
    N1=4200;
    N2=12500;
    zerom=matrix(1,n,0);
    X=[1 for i in range(0, n)];    
    L3 = [];L1 = [];L2 = [];

    L3=matrix(ZZ,2,[[0 for i in range(0, n)],[N2*a[i] for i in range(0, n)]]);
    L=L3.transpose();
    M = identity_matrix(ZZ, n);
    Mb=block_matrix([[M,L]]);Mb;Mb.dimensions();
    zerom=block_matrix([[zerom,N1,-N2*a0]]);
    Mb1=Mb.stack(zerom);
    Mb1;
    Mb1.dimensions();
    L=Mb1.LLL();
    # here we compute all the inner product, and if someone is zero I retrieve the solution
    L1=[[L[j][i] for i in range(0,n)] for j in range(0,n)];
    L2=[vector(L1[i]).dot_product(vector(a))-a0 for i in range(0,n)];

    if L2.count(0)>0:
        return L1[L2.index(0)],vector(L1[L2.index(0)]).norm().n()
    
