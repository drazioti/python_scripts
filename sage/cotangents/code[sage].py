"""
We provide a simple sagemath script to compute cotangents sums and generate images.

For instance the following code uses k = 601  (prime)and generates points (h/600,f(h/600))
where f (h/k) = - sum ( i/k * cot(pi*i*h/k) , m =1...k-1)

sage:M=[];L=[]
sage:import time
sage:k = 601
sage:A = time.time()
...  L = [[h/k,cotangent(h,k).n()] for h in range(1,k) if cotangent(h,k)<>0 ]
...  B = time.time()-A
...  print "time passed:",B

To save the file to a text file.

with open('601.txt', 'w') as f:
    for item in L:
        f.write("%s\n" % item)

To generate the image,

sage:list_plot(L)

"""

def cotangent(h,k):
    var('m')
    if gcd(h,k)==1:
        S = - sum(m/k * cot(pi*m*h/k),m,1,k-1)
        return S
    else:
        return 0
