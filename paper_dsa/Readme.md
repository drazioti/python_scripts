In the file attack.py, we provide the code for an attack to (EC)DSA system.
The attack is based on lattices, in fact to BDD.
The code is written in sagemath ver. 8.1 (and can be easily transfered to fpylll).

Using this code, we executed the experiments provided in the paper :
M. Adamoudis, K.A. Draziotis, D. Poulakis, Enhancing an attack to DSA schemes.
CAI 2019, p. 13-25. LNCS 11545, Springer, 2019

[https://link.springer.com/chapter/10.1007/978-3-030-21363-3_2]

[https://github.com/drazioti/Papers/blob/master/paper/C6_cai2019.pdf]

The paper improves the results of paper [1].

As far as the paper [2], the authors provide an attack using only 100 signatures and 2-MSB for (all) the corresponding
ephemeral keys. Using a BDD-enumeration with pruning method, they managed to have a success rate 23%. i.e. they found 
the secret keys for 23% of their instances. 

We provide an attack that finds the secret key of DSA systems, 
knowing 1-bit of (specific multiples) of the ephemeral keys of 206 signatures, with success rate 62%.

References
----------
[1] D. Poulakis, New lattice attacks on DSA schemes, J. Math. Cryptol., 10 (2) (2016), 135–144.

[2] M. Liu, P. Q. Nguyen, Solving BDD by Enumeration: An Update, CT-RSA 2013, LNCS, volume 7779.
