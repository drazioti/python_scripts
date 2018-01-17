"""
Univariate Coppersmith method for the computer algebra system Sagemath
 AUTHORS: K.A.Draziotis
 
     Copyright (C) 2015   K.A.Draziotis

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
 
     TESTS: 
     
    sage:version(); 
         	
         'Sage Version 6.5, Release Date: 2015-02-17'

    sage:R.<x> = QQ[]
    sage:p = 2^30 + 3
    sage:q = 2^32 + 15
    sage:N=p*q
    sage:f=1942528644709637042+ 1234567890123456789*x+ 987654321987654321*x^2 + x^3
    sage:univ_cop(f,N,0.09)
      
         h= 4
         X= 17399
         rank of lattice, n= 12
         [16384]   



"""

def univ_cop(f,N,epsilon):
    
#### define your polynomial not a symnbolic expression
    R.<x> = QQ[]
    d=f.degree()
    #print "degree of the polynomial, d=",d
    h=ceil(1/(d*epsilon)) # this is relation (21.3) of Galbraith's book
    print('h='),h
    if h.is_one():
        print "choose a new value for epsilon"

################### computation of the bound X which laso depends on epsilon #################
    X=ceil(0.5*N^(1/d-epsilon))
# Coppersmith's theorem provide us with X<=1/2*N^{1/d-epsilon}
###################

###################
    print 'X=',X
### n=rank of the lattice
    n=d*h
    print "rank of lattice, n=",n


################### construction of the lattice ##############

    L1=[N^(h-1-j)*(X*x)^i*f(x*X)^j for j in range(0,h) for i in range(0,d)]; # every element corresponds to a row of our lattice

### So now we need a map from polynomials to vectors f-->b_{f}
### Also, we shall need the inverse map. That is
### when we compute LLL basis, we shall need the correspoding polynomial of the rows
################### the map ###########################
    def map_g(f,n):
        j=0
        M=vector(ZZ,n)
        if f.degree()>=n:
            return "the degree of f must be smaller"
        for i in f.exponents():
            M[i]=f.coefficients()[j]
            j=j+1
        return M 
#########################################################
    M=matrix(n,n,[(map_g(L1[i],n)) for i in range(n)])
    ML=M.LLL()

    g=sum(ML[0][i]*x^i/X^i for i in range(n))    
    return g.roots(multiplicities=False)  
