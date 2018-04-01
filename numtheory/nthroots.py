"""
 "nth roots of large integers"

 We use gmpy2 library to compute the real nth root of a large integer, and we check
 if is integer. In this case we return the nth root

 AUTHOR:
 K. Draziotis (26-3-2018): initial version

 EXAMPLES: 
 >>>m = 931842348902840923840928092349098450983904582390803450738
 >>>c  = m**7
 >>>inv_root(c,7)
    931842348902840923840928092349098450983904582390803450738


"""


#*****************************************************************************
#       Copyright (C) 2018 K.Draziotis <drazioti@gmail.com>,
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

import gmpy2
from gmpy2 import mpz,iroot
def inv_root(x,n):
    x=mpz(x)
    nthroot,boolean=iroot(x,n)
    if boolean:
        print nthroot
        return 
    else:
        print "the",n,"th root is not an integer"
        return
