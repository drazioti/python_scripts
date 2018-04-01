"""
 Continued fractions

 AUTHORS:

 K. Draziotis (26-5-2015): initial version
 Stavros Mekesis (16-4-2016): refactoring and performance improvement


 EXAMPLES: continued_fraction(821112,28062010)
           [0, 34, 5, 1, 2, 3, 1, 2, 2, 1, 1, 4, 1, 30, 2]

           convergents(continued_fraction(821112,28062010))
           [Fraction(0, 1),
            Fraction(1, 34),
            Fraction(5, 171),
            Fraction(6, 205),
            Fraction(17, 581),
            Fraction(57, 1948),
            Fraction(74, 2529),
            Fraction(205, 7006),
            Fraction(484, 16541),
            Fraction(689, 23547),
            Fraction(1173, 40088),
            Fraction(5381, 183899),
            Fraction(6554, 223987),
            Fraction(202001, 6903509),
            Fraction(410556, 14031005)]

 REFERENCES: The joy of factoring, S.S.Wagstaff, Jr. AMS

"""


#*****************************************************************************
#       Copyright (C) 2015 K.Draziotis <drazioti@gmail.com>,
#                          Stavros Mekesis <mekstav@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************


from fractions import Fraction
from functools import reduce


def continued_fraction(p, q):
    """Returns the finite continued fraction of p/q as a list."""
    cf = []
    while q:
        cf.append(p // q)
        p, q = q, p % q
    return cf


def convergents(cf):
    """Returns the list of convergents of the finite continued fraction cf."""
    return [_convergent(partial) for partial in _inits(cf)]


def _convergent(cf):
    """Returns the last convergent to the finite continued fraction cf."""
    cf.reverse()
    cf[0] = Fraction(cf[0])
    return reduce(lambda a, b: b + 1 / a, cf)


def _inits(L):
    """Returns a generator of initial segments of L, shortest first."""
    return (L[:i] for i in range(1, len(L) + 1))
