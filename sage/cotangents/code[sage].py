"""
We provide a simple sagemath script to compute cotangents sums and generate images.

For instance the following code uses k = 601  (prime)and generates points (h/600,f(h/600))
where f (h/k) = sum ( i/k * cot(pi*i*h/600) , m =1...k-1)

M=[];L=[]
import time
k = 601
A = time.time()
L = [[h/k,cotangent(h,k).n()] for h in range(1,k) if cotangent(h,k)<>0 ]
B = time.time()-A
print "time passed:",B

"""

def cotangent(h,k):
    var('m')
    if gcd(h,k)==1:
        S = - np.sum(m/k * cot(pi*m*h/k),m,1,k-1)
        return S
    else:
        return 0