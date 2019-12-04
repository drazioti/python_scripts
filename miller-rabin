def miller_rabin(n,k):
    
    import random
    import math

    def find_s_t(n):
        i = 1
        isint = 0
        while isint == 0:
            isint = math.floor( (n-1)/(2.**i)) - math.ceil( (n-1)/(2.**i))
            if isint == 0: # i.e. if n/2^i is integer, continue
                1==1
                i = i + 1
            else:
                isint = 1
                s = i - 1
                return s,(n-1)/2**s

    i = 1
    j = 0
    s,t = find_s_t(n)
    while i<=k:
        a = random.randint(2,n-1)
        b = a**t % n
        if b == 1:
            j = j + 1
            if j == k:
                return "n is strong probable prime"
        for r in range(0,s):
            if b == (n-1):
                j = j + 1
                if j == k:
                    return "n is strong probable prime"
            b = (b ** 2) % n
        i = i + 1
    return "composite"
