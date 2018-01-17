"""
 LLL algorithm over Q
 AUTHORS: K. Draziotis (2016): initial version

 EXAMPLES:
 We define a funnction LLL(L,delta), where L is a list of lists, where rational numbers are allowed.
delta is the parameter of LLL, usually delta = 3/4.
 Rational numbers are expressed as F(a,b)==a/b
 There is one more parameter which is a string.
 If you set it 'true', then the function will print the intermediate steps of LLL.
 
 
 >>LLL( [  [2,F(3,2),4,F(-5,3)],[1,-3,2,1], [4,2,16,1], [0,0,3,1] ],F(3/4),'false')
           
 [array([Fraction(0, 1), Fraction(-1, 1), Fraction(-1, 1), Fraction(4, 3)], dtype=object),
 array([Fraction(2, 1), Fraction(-1, 2), Fraction(-1, 1), Fraction(0, 1)], dtype=object),
 array([Fraction(-1, 1), Fraction(-3, 2), Fraction(1, 1), Fraction(-4, 3)], dtype=object),
 array([Fraction(2, 1), Fraction(-1, 2), Fraction(2, 1), Fraction(1, 1)], dtype=object)]
 
 Finally, a function GSO was defined, which returns a set of vectors (orthogonal to the initial basis)
 and the matrix mu of the coefficients.
 
 >>gso = GSO([  [2,F(3,2),4,F(-5,3)],[1,-3,2,1], [4,2,16,1], [0,0,3,1]  ]);gso
 
 ([array([2, Fraction(3, 2), 4, Fraction(-5, 3)], dtype=object),
  array([Fraction(625, 901), Fraction(-2910, 901), Fraction(1250, 901),
         Fraction(1131, 901)], dtype=object),
  array([Fraction(-36511, 12986), Fraction(13211, 6493),
         Fraction(15433, 6493), Fraction(54045, 12986)], dtype=object),
  array([Fraction(-27242, 151567), Fraction(-9328, 151567),
         Fraction(9169, 151567), Fraction(-19080, 151567)], dtype=object)],
 matrix([[1, 0, 0, 0],
         [Fraction(138, 901), 1, 0, 0],
         [Fraction(2640, 901), Fraction(17811, 12986), 1, 0],
         [Fraction(372, 901), Fraction(4881, 12986), Fraction(48881, 151567),
          1]], dtype=object))
 
 REFERENCES: S.Galbraith
"""


#*****************************************************************************
#       Copyright (C) 2016 K.Draziotis <drazioti@gmail.com>,
#                         
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

import numpy as np
from fractions import Fraction as F
import fractions
from __future__ import division
    

def mu(u,v):          # Gram-Schimdt coefficient of the projection of u over v : proj_{v}(u)
    return  F(np.dot(np.array(u),np.array(v)),np.dot(np.array(v),np.array(v)))


def size_reduction(u,v,m):
    
    u = F(1,1)*np.array(u)    # we multiplied with F(1,1) in order to change the base from integers to rationals
    v = F(1,1)*np.array(v)    
    np.put(u,range(0,len(u)),u-int(round(m))*v)    
    return u

def lovasz(u,v,delta,m): # u,v are two vectors, m is the gram-schmidt coefficient
                         # of u,v where u,v are consecutive vectors
                         # of a basis {v1,v2,...,vi=u,v_{i+1}=v,...,vn}    
    u = np.array(u)
    v = np.array(v)    
    #print u,v
    if np.dot(u,u) >= (delta - m**2)*np.dot(v,v):  
        return True
    return False

# L is a list of the form [[a1,...,an],[b1,..,bn],...,[d1,...,dn]]
# This functions returns two lists. The first is the GM basis.
# The second is the GM coefficient mu[i,j], where
# in the form [ mu[2,1],mu[3,2],mu[3,1],mu[4,3],mu[4,2],...,mu[n,n-1],mu[n,n-2],...,mu[n,1] ]

def GSO(L):            
    V = []
    M = []
    V.append(np.array(L[0]))
    for i in range(1,len(L)):
        t1 = np.array(L[i])
        t3 = t1
        for j in range(i-1,-1,-1):
            m = mu( t1,list(V[j]))   
            t2 = t3 - proj(t1,list(V[j]))
            t3 = t2 
            M.append(m)
        V.append(t3)  
    # reshape and print M as a lower triangular gram-schimdt coefficient matrix
    import numpy.matlib
    M1 = np.matlib.identity(4,dtype = fractions.Fraction);
    k=0
    for i in range(1,len(L)):
        for j in range(0,i)[::-1]:
            M1[i,j] = M[k]
            k=k+1 
    return V,M1

def proj(u,v):
    return mu(u,v)*np.array(v)

def LLL(L,delta,verbose):
   
    r=0
    V = []    
    gso = GSO(L)
    m = gso[1]
    gm = gso[0]
    i=1   
    while(i<len(L)):      
        for j in  range(0,i)[::-1]: # for j = i-1, ..., 0 (j<i)           
            # Size reduction            
          
            c = ( size_reduction( L[i], L[j], m[i,j] ) )
            L[i]= np.array(c)                     # we update the initial list
            if verbose=='true':
                r=r+1
                print "size reduction step",r,"\n update basis",L
            gso = GSO(L)                         # we update the Gram-Schimdt basis
            m = gso[1]
            gm = gso[0]
            # SWAP step
            
        lov = lovasz(gm[i],gm[i-1],delta,m[i,i-1]) 
        
        if lov == True:
            i = i + 1
            if verbose=='true':
                print "Lovasz condition is true \n"
                       
        else:
            L[i-1], L[i] = L[i], L[i-1]
           
            gso = GSO(L)
            gm = gso[0]
            m=gso[1]
            i = max(1,i-1)      
            if verbose=='true':
                print "Lovasz condition is false \n"             
    return L
