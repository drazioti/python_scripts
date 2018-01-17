"""
We provide the sage-code for the construction of table 1
check : http://goo.gl/s4yAaS

- sage code -
n=232
b = n/2
for H in range(7,12):
    print "hamming weight:",H
    L,L1,L2 = generateJ2(H)
    print bits2Gbytes(cmem(b,H,2048,L1,L2)).n(),H,":J"
    L,L1,L2 = generateJ1(H)
    print bits2Gbytes(cmem(b,H,2048,L1,L2)).n(),H,":W"

hamming weight: 7
1.76756501197815 7 :J
11116.8659784794 7 :W
hamming weight: 8
3.41427087783813 8 :J
151467.298953772 8 :W
hamming weight: 9
39.9469692707062 9 :J
1.81760758744264e6 9 :W
hamming weight: 10
76.4796676635742 10 :J
1.94484011856339e7 10 :W
hamming weight: 11
745.676759719849 11 :J
1.87411865970652e8 11 :W
"""
def generateJ1(H): # the set W of the paper   
    L=[]
    for h1 in range(0,H+1):
        for h2 in range(0,H+1):
            if h1+h2<=H and h1+h2>0:
                L.append([h1,h2])
    L1 = [item[0] for item in L]
    L2 = [item[1] for item in L]
    L3 = [L1[i]+L2[i] for i in range(len(L1))]
    return L,L1,L2

def generateJ2(H):#the set J of the paper
    L=[]
    for h1 in range(1,ceil(H/2)+1):
        for h2 in range(h1-1,h1+1):
            if h1+h2<=H and h1+h2>0:
                L.append([h1,h2])
    L1 = [item[0] for item in L]
    L2 = [item[1] for item in L]
    L3 = [L1[i]+L2[i] for i in range(len(L1))]
    #print L
    return L,L1,L2

def cmem(b,H,coef,L1,L2): 
    A=[]
    for i,j in zip(L1,L2):   
        A.append(coef*(binomial(b,i)+binomial(b,j)) )
    return max(A)

def bits2Gbytes(n):
    return n/(2^33)
