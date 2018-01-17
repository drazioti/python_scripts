"""
 We provide a class for Naccache-Stern Knapsack cryptosystem.
 It contains the method attack, which, given a cryptographic message c, tries to find
 the original message. If the hamming weight is small (or large) enough, the attack will succeed.
 
 Please, feel free to report bugs.

References : D. Naccache and J. Stern, A new public key cryptosystem, Proceedings of Eurocrypt 97, LNCS 1233,(1997), Springer-Verlag, p.27--36.
 
 AUTHOR(S):  K. Draziotis (drazioti@gmail.com), initial version : 2017
 credits  :  N.Chatzis, M.Anastasiadis 
	
	EXAMPLES: 
	===========
sage:X = ns()  					# Create an instance of the class ns() 
sage:p,q,n,u,s = X.choose_pk_sk(600) 		# we choose the public and secret key with prime p 600 bits (p is a safe prime)
						# Other choices are 1024,2048 bits

sage:m = 2^(n)+2^(n-1)+2^(n-20)+2^(23)+2^(8)+2^7+2^5+2^4+2 	# The message
sage:c = X.encrypt(m,p,u)
sage:X.decrypt(c,n,p,s)==m # check that the decryption is correct
True

sage:hamming  = X.popcount_py(bin(m))   # the hamming weight of the message m
sage:bound = 42                         # the auxiliary variable bound. Here we choose bound = n/2
sage:print "hamming,n,bound:",hamming,n,bound
hamming,n,bound: 9 84 42

sage:flag = 0 # when you choose bound = n/2 = 42, you have to set flag = 0

# Here we provide an example sage-code for attacking the system

import time

I1=[];I2=[];U1=[];U2=[]
reset('U1','U2')
start = time.time()

R = []
L = []
r = 1
msg = None
while msg==None:
    print "round:",r
    R.append(r)
    I1,I2,U1,U2 = X.gen(n,bound,flag)
    msg = X.attack(n,bound,p,c,hamming,s,flag,I1,I2,U1,U2) 
    # we called the method attack()
    
    if msg!=None: 
        print msg==m    
        A = time.time()-start
        L.append(A)  
    r = r + 1
print "time on average:",mean(L)   
print "rounds on average:",mean(R).n()

===Results===
round: 1
round: 2
round: 3
round: 4
round: 5
We found the message!
True
time on average: 301.890817881
rounds on average: 3.00000000000000

In the case :
    
sage:bound = 38
sage:flag = 2 # If bound < n/2 we set flag=2

===Results===
round: 1
round: 2
round: 3
round: 4
round: 5
round: 6
round: 7
round: 8
round: 9
round: 10
round: 11
round: 12
We found the message!
True
time on average: 407.758924007
rounds on average: 6.50000000000000

"""

#*****************************************************************************
#       Copyright (C) 2017 K.Draziotis <drazioti@gmail.com>
#               
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

class ns(object):
        
    global init,int2bin,int2bin_,bin2int,func1,func2,perms_out,perms,rounds
       
    def int2bin_(m,b):
        """ This function converts an integer to a binary list."""
        def int2bin1(m):
            L = []
            L.append(str(bin(m))[2:])
            return L[0]
        M = int2bin1(m)
        M1 = [int(M[i]) for i in range(len(M))]
        zeros = [0,0]
        if len(M1)<b:
            M1 = [0]*(b-len(M1)) + M1 
        return M1
    
    def int2bin(m):
        """ this function converts an integer to a binary list   """ 
        def int2bin1(m):
            L = []
            L.append(str(bin(m))[2:])
            return L[0]
        M = int2bin1(m)
        M1 = [int(M[i]) for i in range(len(M))]
        return M1
    
    def bin2int(a):
        return int("".join(str(x) for x in a),2)
    
    def bits(n):
        return floor(log(n,2))+1
                        
    def perms(n,hamming,flag): 
    # returns all the permutaions of n-bit words with specific hamming weight. 
    # if flag!=0 then returns all the n-bit words (the algorithm ignores the variable hamming).
    # Finally, it returns a set of strings not lists.
        import itertools
        if not n:
            return
        if flag == 0:
            result = []
            for bits in itertools.combinations(range(n), hamming):
                s = ['0'] * n
                for bit in bits:
                    s[bit] = '1'
                result.append(''.join(s))
            yield result
            
        if flag!=0:
            for i in xrange(2**n):
                s = bin(i)[2:]
                s = "0" * (n-len(s)) + s
                yield s
                
    def perms_out(n,hamming,flag):
        # the same as the previous fuinction, but returns the elements as lists (not strings)
        s = list(perms(n,hamming,flag))
        if flag!=0:
            return [[int(s[j][i]) for i in range(n)] for j in range(len(s))]
        if flag==0:
            s = s[0]
            return [[int(s[j][i]) for i in range(n)] for j in range(len(s))]
        
    def popcount_py(self,x):
        # the hamming weight of a binary string x
        return x.count("1")
        
    def func1(L, M, p, c):
        import hashlib
        if len(L)!=len(M):
            return "func1 : lists L,M must have the same length"
        if c>1:
            A = str( int( mod(c*prod(L[i]^(-M[i]) for i in range(len(L))),p) ) )
            B = hashlib.md5(A).hexdigest()[0:12]
        else:
            A = str( int( mod(c*prod(L[i]^(M[i]) for i in range(len(L))),p) ) )
            B = hashlib.md5(A).hexdigest()[0:12]        
        del A
        return B
    
    # Note that func2() returns two lists [A,B], the list A contains the products prod(u_i) and the second 
    # is needed, when we reconstruct the message m.    
    
    def func2(L,M,p,c): #M is a list of lists 
        return [ [func1(L,M[i],p,c),bin2int(M[i]) ] for i in range(len(M))]
            
    def find_n(p):
        # in the NS-system, n is defined from the prime p.
        n=5 
        P = [Primes().unrank(i) for i in range(n)]
        product_ = prod(P)
        while(p>product_):
            P = [nth_prime(n+1)]+P
            product_ = prod(P)
            n = n + 1
        return n - 2
  
    def init(n,p,s):
        # this function constructs the public key  : (u[i]:i=0,1,2,...,n , a list with n+1 integers)
        if is_prime(p):
            P = [Primes().unrank(i) for i in range(n+1)]
            u = []            
            u.append([int ( power_mod(P[i],int(mod(s^(-1),p-1) ),p)  ) for i in range(n+1)])   
        return u[0]

        
    def encrypt(self,m,p,u):
        L =int2bin(m)
        return [prod(u[::-1][i]^L[i] for i in range(len(L)) )%p][0]
      
    def decrypt(self,c,n,p,s):
        cs = int(power_mod(c,s,p))
        P = [Primes().unrank(i) for i in range(n+1)]
        return sum( (gcd(cs,P[i])-1)*2^i/(P[i]-1) for i in range(n+1) )
          
        
    ### choosing the lists randomly (balanced lists)
    # take uniformly n/2-elements from the set I_n = {0,1,...,n}
    # flag = 0 the usual attack
    # flag = 2 we choose the sets I_1, I_2 to have << n/2 elements 
    
    
    # The following function returns two sets I1,I2 with almost the same length.
    # I_1,I_2 are subsets of {a1,...,b1}
    # Usually a1=0,b2=n and bound1 = n/2. So in this case we get a disjoint union of the set {a1,a1+1,...,b1}       
    # bound is the length of the first set I1.
        
    def gen(self,n,bound1,flag):
        import hashlib,random
        
        a1 = 0
        b1 = n
        L = []
        I2 = []
        I1 = []
        U1 = []
        U2 = []
        bound = floor(bound1)
        if bound1>=b1 - a1:
            print "bound must be smaller than ",b1-a1
            return
        if flag not in [0,2]:
            print "flag is either 0 or 2"
            return         
        if flag==0: # when you choose flag=0 then bound = n/2. The function ignores the bound1.
            hash = hashlib.md5(os.urandom(2*n)).digest()
            random.seed(hash)
            L = random.sample(range(a1,b1+1), n+1)
            I1 = L[0:bound]
            I2 = L[bound:len(L)]        
        if flag==2:
            hash = hashlib.md5(os.urandom(2*n)).digest()
            random.seed(hash)
            L = random.sample(range(a1,b1+1), 2*bound)
            I1 = L[0:bound]
            I2 = L[bound:2*bound]
            if n not in list(set.union(set(I1),set(I2))):
                I1 = I1 + [n]
        U1 = [u[i]%p for i in I1]
        U2 = [u[i]%p for i in I2]
        return I1,I2,U1,U2
        
    #attack : Is the modified birthday attack to Naccache-Stern Knapsack cryptosystem
      
    def attack(self,n,bound1,p,c,hamming,s,flag,I1,I2,U1,U2):   
        import itertools
        
        def decrypt(c,n,p,s):
            cs = int(power_mod(c,s,p))
            P = [Primes().unrank(i) for i in range(n+1)]
            return sum( (gcd(cs,P[i])-1)*2^i/(P[i]-1) for i in range(n+1) )
                    
        a1 = 0
        b1 = n
        bound = floor(bound1)
        if bound>=b1-a1:
            print "bound must be < b1-a1"
            return 0
        if flag in [0,2]:       
            h1 = 0 # the initial hamming weight for the first set
            h2 = 0 # the initial hamming weight for the second set
            lim = hamming  
            M3 = []
            M1 = []
            M2 = []
            if lim%2==0:
                lim1 = lim/2           
            else:
                lim1 = (lim+1)/2 
                    
            for h1 in range(1,lim1+1):
                del M1
                M1 = func2(U1,perms_out(len(U1),h1,0),p,1) # construction of the first set {prod(ui^ei)}
                for h2 in range(h1-1,h1+1):
                    if h1+h2<=hamming:
                        if h1==1: 
                            M3=[];M2=[]
                            M2 = func2(U2,perms_out(len(U2),h2,0),p,c) # construction of the second set {c*prod(uj^(-ej))}
                            M3.append(M2)
                            
                        if h1>1 and h2==h1-1:
                            M2 = M3[0]
                            
                        if h1>1 and h2==h1:
                            M2 = [] 
                            M3 = []
                            M2 = func2(U2,perms_out(len(U2),h2,0),p,c) # construction of the second set {c*prod(uj^(-ej))}
                            M3.append(M2)
                            
                        
                    # We check if the intersection of the sets M1 and M2 is non  null. If it is non null
                    # we compute the common elements and the algorithm will terminate. Else, we take the next values for h1,h2.
                        intersection = list(Set(zip(*M1)[0]).intersection(Set(zip(*M2)[0])))
                        leninter = len(intersection)
                        if intersection!=[]: 
                            if leninter==1:
                                R1=[];R2=[];R3=[];R4=[]                          
                                sol =  intersection[0]                            
                                R1 = int2bin_(M1[zip(*M1)[0].index(sol)][1],len(I1) )
                                R2 = int2bin_(M2[zip(*M2)[0].index(sol)][1],len(I2) )                    
                                # We reconstruct the initial message                        
                                msg = vector([2^j for j in I1]).dot_product(vector(R1))+vector([2^j for j in I2]).dot_product(vector(R2))
                                if decrypt(c,n,p,s)==msg:
                                    print "We found the message!"
                                    return msg
                                    break
                            else:
                              print "length of the intersection,h1,h2:",leninter,h1,h2
                              for i in range(leninter):
                                    R1=[]
                                    R2=[]
                                    R3=[]
                                    R4=[]
                                    sol = intersection[i]
                                    R1 = int2bin_(M1[zip(*M1)[0].index(sol)][1],len(I1) )
                                    R2 = int2bin_(M2[zip(*M2)[0].index(sol)][1],len(I2) )
                                    # We reconstruct the initial message                        
                                    msg = vector([2^j for j in I1]).dot_product(vector(R1))+vector([2^j for j in I2]).dot_product(vector(R2))
                                    if decrypt(c,n,p,s)==msg:                                        
                                        del R1
                                        del R2
                                        del R3
                                        del R4
                                        print "We found the message!"
                                        return msg
                                        break
                        
    def rounds(n,b,h):
        ind=min(n-2*b,h)   
        if 2*b < h:
            return "NONE"
        if ind>0:            
            var('k')
            if n<2*b:
                return error
            prob_suc = (sum( (-1)^k*binomial(n-k,2*b)*binomial(h,k),k,0,ind))/binomial(n,2*b)
            r = ceil(1/(prob_suc))
            return r
        else:
            return "NONE"
            
    def find_b(self,n,h,R):
        """ Returns the possible values for the bound b, such that on average, R rounds are needed for success. 
        e.g. sage:X = ns()
             sage:X.find_b(84,10,10)
             [[34, 10], [35, 7], [36, 6], [37, 4], [38, 3], [39, 3], [40, 2]]"""
        B = []
        for b in range(2,ceil(n/2)-1):
            if (rounds(n,b,h)) <=R:
                B.append([b,rounds(n,b,h)])
        return B
    

    def choose_pk_sk(self,lenp):
        """here we have a safe prime p with 600 bits. p=2q+1"""
        if lenp == 600:
            n = 84
            p,q =2074757784440496479256203931845580575506223116121218449997828664845326405706454073199853524473551897144098943305650394591197575537705887653943437417056981843530590901700771609797439,1037378892220248239628101965922790287753111558060609224998914332422663202853227036599926762236775948572049471652825197295598787768852943826971718708528490921765295450850385804898719
        
   
    #################
    # here we have a safe prime p with 2048 bits. p=2q+1
    #################
    
        if lenp==2048:
            n = 232


            p,q =49602036983371092259147540363584647204071653867172430513214426393945899721358727738639843690176877714453506962352346127699675984824298521566661548583161306302109776282592070527665917209557680638514225792771513660101454532957236581944526547561559549110008028374143260964378198717998418190150986828475191457976974248469899690659796179217094422955203899925977675132323008288807247334985222480184208553922524595153266221641790574520331591186042123578501071416938635911581975938357315995683256002600487269950091337172447883358779407250169914463238033964605233448547936216145839488555331364566643703592667232766768858537619,24801018491685546129573770181792323602035826933586215256607213196972949860679363869319921845088438857226753481176173063849837992412149260783330774291580653151054888141296035263832958604778840319257112896385756830050727266478618290972263273780779774555004014187071630482189099358999209095075493414237595728988487124234949845329898089608547211477601949962988837566161504144403623667492611240092104276961262297576633110820895287260165795593021061789250535708469317955790987969178657997841628001300243634975045668586223941679389703625084957231619016982302616724273968108072919744277665682283321851796333616383384429268809
   
    #################
    # here we have a safe prime p with 1024 bits i.e. p=2q+1 for q prime
    #################
        if lenp==1024:
            n = 130
         
            p,q =356016873783498533947581036092641272306360368050925808571238846207127055154301347886337239040241779594156481218243271432984000696808011616039210639390840176709567072017753811949256718002480410000475130359737947125690893606890239817035840801874264111611236566297668497801840516568157731657056332626732525479259,178008436891749266973790518046320636153180184025462904285619423103563527577150673943168619520120889797078240609121635716492000348404005808019605319695420088354783536008876905974628359001240205000237565179868973562845446803445119908517920400937132055805618283148834248900920258284078865828528166313366262739629
            
        s = 5649012341 # the secret key
        print gcd(p-1,s) == 1
        u = init(n,p,s) # we generate the public key i.e. the u_i's
        return p,q,n,u,s # we return the primes (p,q) with p=2q+1, the parameter n of the system,the sets u and the secret key s

