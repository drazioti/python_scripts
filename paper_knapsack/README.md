
There are five files here :

[1] testing_Schnorr_She_method-fpylll.py (uses fpylll library)

[2] branch-and-bound(sage).py (written in sagemath ver 6.9)

[3] comparison_for_small_solutions(sage).py  (written in sagemath ver 6.9)

[4] cvp_attack_1_sage.py (written in sagemath ver 6.9)

[5] cvp_attack_2_sage.py (written in sagemath ver 6.9)

The first one contains the basic experiments of two variants of Schnorr-Shevchenko method.
The second is an heuristic algorithm using branch and bound to solve compact knapsack problem.
The third is a comparison between three algorithms in order to find small solutions of a linear equation, a1x1+...+anxn=s.
The two last files contain an attack to compact knapsack problems by reducing to a suitable cvp problem.

The code concerns the paper (https://goo.gl/o9CnHB): Improved attacks on knapsack problem with their variants and a knapsack type ID-scheme. Advances in Mathematics of Communication 2018, 12(3), Pages 429-449, American Institute of Mathematical Sciences  - Joint work with A. Papadopoulou.
