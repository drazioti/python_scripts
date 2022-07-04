# written in python3
# author : K.A.Draziotis
# Licence : GPL
# dependencies : 
# pip3 install numpy
# pip3 install pandas
# pip3 install xlrd
# pip3 install xlsxwriter
# pip3 install pandas-ods-reader
# pip3 install openpyxl

'''
Example

You have to hardcode the paths of the xlsx files. Here we denote them as A.xlsx and B.xls

$python3 main.py

In practice: 
1. Download the grade file from the old sis, say B.xlsx
2. sort with respect to aem and save it.
3. Save with the name B_.xlsx
4. set input the file from *elearning*
This file must have two columns, where in the first row we have 'AEM' and the first row,second column 'Βαθμός'
5. set output the file     *B_.xlsx*
6. run python3 main.py
7. get the column 'βαθμός' from B_.xlsx
8. paste it to the column 'βαθμός' of B.xlsx
9. end
'''

import pandas as pd
import xlsxwriter
import numpy as np
from pandas_ods_reader import read_ods

def checkIfDuplicates(listOfElems):
    ''' Check if given list contains any duplicates '''
    if len(listOfElems) == len(set(listOfElems)):
    	print("there are no duplicates")
    else:
    	print("[+]there ARE duplicates")



counter = 0    # counts the number of grades successfully passed to the second excel
input_path  = 'grades_ma_2.xlsx'
output_path = '2021-2022_ΙΟΥΝΙΟΣ_NCO-02-01_ΜΑΘΗΜΑΤΙΚΗ ΑΝΑΛΥΣΗ ΙΙ_.xlsx'

A1 = []
A = []
B = []

# the follow two lines must be hardcoded

SKIPROWS = 0    # depends on the format of the file A.xlsx : input path (the header does not count)
NROWS1   = 1000 # a large number

first  = pd.read_excel(input_path, skiprows=SKIPROWS, nrows=NROWS1, usecols='A:B', index_col=None, sheet_name='0')
second = pd.read_excel(output_path, index_col=None)

NROWS = first.count(axis=0)[1] # counts without the headers
print("Rows:",NROWS) # please check with the real number

#1. take from 'first' the pair first [AEM,Σύνολο]

for i in range(0,NROWS):
	A1.append(list(first.xs(i)))

# since the first coordinate is float i.e. AEM is considered here float, convert it to integer
for x in A1:
    A.append([int(x[0]),x[1]])
print(A)
		
#2. find 'ΑΕΜ' in second and add Σύνολο to Βαθμός
#   if there is not such aem print that this aem does not exist.

print("\n")
for i in range(len(A)):	
	test_value = int(A[i][0])
	grade      = A[i][1]
	
	output     = second.loc[second['ΑΕΜ'] == test_value] 
	if len(output) == 0:
		print("the student with AEM:",test_value,"does not exist")
		B.append([test_value,grade])
	else:
		# bug: δεν ελεγχει διπλοεγγραφές
		counter = counter + 1
		found_the_row = output.index[0]
		#print("line:",found_the_row)
		second.at[found_the_row,' Βαθμός ']=grade
		#print(second.iloc[found_the_row])
		#print(second.at[found_the_row,'ΑΕΜ']) # for the new sis


c = 0
C = []
tens  = 0
nines = 0
for i in range(len(A)):
	if int(A[i][1])>=5:
		c+=1
		C.append(A[i][1])
	if int(A[i][1])==10:
		tens+=1
	if int(A[i][1])>=9 and int(A[i][1])<10:
		nines+=1

S = np.sum([C[i] for i in range(len(C)) ])


check_list = []
check_list = [z[0] for z in A] # take a list with AEM only
checkIfDuplicates(check_list)

print("the number of grades are:",len(A))
print("successes:",counter)
print("fails:",len(A)-counter)
print(B)
print("\n",">=5 :",c)
print(" <5  :",counter-c)
print(" mean:",S/c)
print(" success rate:",100*c/counter)
print(" tens:",tens)
print(" >=9 and <10:",nines)

#3. convert 'second' to xlsx.

second.to_excel(output_path,index=False) # for some reason it makes the header bold.
