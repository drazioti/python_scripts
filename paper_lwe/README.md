# Brakerski-Vaikuntanathan cryptosystem (BV11)
https://eprint.iacr.org/2011/344.pdf

There is one file written in sagemath (http://www.sagemath.org/) that provides
a class lwe_operation().
It contains the following methods :

1. initialize_lwe(self,n,q,sigma)
2. encrypt_lwe(self,m,t,n,q,s)
3. decrypt(self,c,t,n,q,s)
4. decrypt_lwe_mult(self,C,n,s,t,q)
5. decrypt_points(self,C, t, n, q, s)
6. add(self,c1,c2,q)
7. sub(self,c1,c2,q)
8. add_vectors(self,C,n,q)
9. mult(self,c1,c2,n,q)
10. madd(self,C,n,q) 
11. scalar(self,N,c,n,q)
12. inner_product(self,C1,C2,n,q)
13. hom_distance(self,C1,C2,n,q) 

The previous class was used in the paper http://ieeexplore.ieee.org/document/8024510/
