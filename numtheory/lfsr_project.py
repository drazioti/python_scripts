"""
 lfsr_project.py
 AUTHORS:
 K.Draziotis (3-3-2016): initial version
 
 Tested in python 2 and python 3.
 
 TESTS:In the example below we use the function 'lfsr' to compute the keysrteam of an lfsr given the initial seed 
 and a feedback function. It accepts a third argument which counts the number of the keystream bits. 
 Furthermore, if the fourth argument is 0 prints the interior states of the lfsr, else only the keystream is printed.
 
>lfsr([1,1,1,0],[0,0,1,1],15,0)
 	initial seed : deque([1, 1, 1, 0])
	state 1 of the lfsr : deque([1, 1, 1, 1])
	state 2 of the lfsr : deque([0, 1, 1, 1])
	state 3 of the lfsr : deque([0, 0, 1, 1])
	state 4 of the lfsr : deque([0, 0, 0, 1])
	state 5 of the lfsr : deque([1, 0, 0, 0])
	state 6 of the lfsr : deque([0, 1, 0, 0])
	state 7 of the lfsr : deque([0, 0, 1, 0])
	state 8 of the lfsr : deque([1, 0, 0, 1])
	state 9 of the lfsr : deque([1, 1, 0, 0])
	state 10 of the lfsr : deque([0, 1, 1, 0])
	state 11 of the lfsr : deque([1, 0, 1, 1])
	state 12 of the lfsr : deque([0, 1, 0, 1])
	state 13 of the lfsr : deque([1, 0, 1, 0])
	state 14 of the lfsr : deque([1, 1, 0, 1])
	state 15 of the lfsr : deque([1, 1, 1, 0])
[0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 1]

The next function : 
	text_enc(a string) 
converts the string to a binary sequence according to a five-bit dictionary defined below.
Example:
>text = 'helloandgoodbuy'
>text_enc(text)

	'001110010001011010110111000000011010001100110011100111000011000011010011000'
	
The inverse of the previous function is : 
	text_dec(a binary string)
Example:
>text_dec('0011100100010110101101110')
	'hello'
	
Also, the function string_xor( a binary string,a binary string) xor's, bit by bit, the bits from the two strings
Example:
>key='1'*25;
>string_xor(text_enc('hello'),key)

	'1100011011101001010010001'
	
Say for instance that you want to encrypt the text 'Simplecanbeharderthancomplex' with an lfsr defined by the seed
[0,0,0,0,1,0,1,0,1,1] and the feedback polynomial : x^10+x^9+x^7+x^6+1.

>text = 'Simplecanbeharderthancomplex'
>streambits = text_enc(text)
>initial_seed = [0,0,0,0,1,0,1,0,1,1]
>O = lfsr(initial_seed,[0,0,0,0,0,1,1,0,1,1],len(streambits),1)
>keystream = list_to_string(O)
>text_dec(string_xor(text_enc(text),keystream))
'iy-t)ocojaiz(lwu!egr!ghglgn)'

"""
#*****************************************************************************
#       Copyright (C) 2015 K.Draziotis <drazioti@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************



aDict = dict(zip('abcdefghijklmnopqrstuvwxyz.!?()-ABCDEFGHIJKLMNOPQRSTUVWXYZ', 
                              ['00000','00001','00010','00011','00100',
                              '00101','00110','00111','01000',
                              '01001','01010','01011','01100','01101','01110','01111',
                              '10000','10001','10010','10011',
                              '10100','10101','10110','10111',
                              '11000','11001',
                              '11010','11011','11100','11101','11110','11111',
                              '00000','00001','00010','00011','00100',
                              '00101','00110','00111','01000',
                              '01001','01010','01011','01100','01101','01110','01111',
                              '10000','10001','10010','10011',
                              '10100','10101','10110','10111',
                              '11000','11001'])) #the function from our alphabet to 5-bit binary strings
							  
def list_to_string(l):
    return ''.join(str(e) for e in l)

# btext is a binary string of the form 'something...'
# key is a binary string of the form '01010...'
# the result of the function is xoring bit-bit the btext with the key

def string_xor(btext,key): 
    cipher = []
    if len(btext)!=len(key):
        print("key and message must have the same lengths!")
        return 0
    for i in range(len(btext)):
        cipher.append(int(btext[i])^int(key[i])) #xoring bit-bit
    cipher = ''.join(str(e) for e in cipher)
    return cipher

# the function below converts a text of the form 'something' to 
# a binary string according to our 5-bit encoding


def text_enc(text):
    text = text[::-1]
    length = len(text)
    coded_text = ''
    for i in range(length):
        coded_text = aDict[text[i]]+ coded_text
    return coded_text.lower()
	
	
# The function below converts a binary string to an alphabetic text 
# according to our 5-bit encoding

def text_dec(binary_string):
    length = len(binary_string)
    inv_map = {v: k for k, v in aDict.items()}
    decoded_text = ''
    for i in range(0,length,5):
        decoded_text = inv_map[binary_string[i:i+5]] + decoded_text # + in strings is the join function.
    decoded_text = decoded_text[::-1]
    return decoded_text.lower()
	

# the function sumxor
# accepts a binary list of the form [1,0,1,...]
# and returns the xor-sum of the bits

from collections import deque
def sumxor(l):
    r = 0
    for v in l: 
        r = r^v
    return r

# the function lfsr accepts three arguments
# seed : a binary list of the form [0,1,1,1,0,1,0,1,...] which is the initial seed
# feedback : a binary list which defined by the feedback polynomail 
# for instance [0,0,1,1]-->x^4+x^3+1
# bits : is an integer, which tells the function to return bits-number of the resulting stream of the lfsr
# the function prints the internal states if flag = 0 and always returns the output

def lfsr(seed,feedback,bits, flag):
    index_of_ones = []
    feedback_new = []
    for i in range(len(feedback)):
        if 1 in feedback:
            index_of_ones.append(feedback.index(1))
            feedback[feedback.index(1)] = 0
    feedback_new = index_of_ones    #this is a list which contains the positions of 1s in feedback list
    seed = deque(seed)              # make a new deque 
    output = []
    if flag==0:
        print('initial seed :',seed)
    for i in range(bits):
        xor = sumxor([seed[j] for j in feedback_new])
        output.append(seed.pop()) #extract to output the right-most bit of current seed
        seed.appendleft(xor)      #insert from left the result of the previous xor 
        if flag==0:
            print('state', i+1, 'of the lfsr :',seed)
    return output
