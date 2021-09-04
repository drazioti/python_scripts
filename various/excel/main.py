# written in python3
# author : K.A.Draziotis
# Licence : GPL
# dependencies : 
# numpy,pandas,xlrd
# pip3 install xlrd

'''
Example

You have to hardcode the paths of the excel files. Here we denote them as A.xlsx and B.xls
Also you have to hardcode NROWS.

$python3 main.py
In practice: 
1. Download the grade file from the old sis, say B.xlsx
2. sort with respect to aem and save it (for easy crosscheck).
3. Save it with the name B_.xlsx
4. [hardcode in the code] Set as 'input' the file from elearning
5. set as 'output' the file B_.xlsx
6. run python3 main.py
7. copy the column 'βαθμός' from B_.xlsx
8. paste it to the column 'βαθμός' of B.xlsx and save it.
9. end
'''

import pandas as pd
import xlsxwriter
from pandas_ods_reader import read_ods
import numpy as np

counter = 0    # counts the number of grades successfully passed, to the second excel
input_path  = 'grades2.xlsx'
output_path = 'courseExam_NCO-02-01_2020-2021_06_ΙΟΥΝΙΟΣ_600235013_.xls'

A = []
B = []

# the follow two lines must be hardcoded

SKIPROWS = 0    # depends on the format of the file A.xlsx : input path (the header does not count)
#NROWS   = 296  # TODO : equals to : [number of non null rows] - [SKIPROWS+1]
NROWS1   = 1000 # a large number

#first  = pd.read_excel(input_path,skiprows=SKIPROWS,nrows=NROWS1,usecols='A:B',index_col=None,sheet_name='Sheet2') # if you use many sheets
first  = pd.read_excel(input_path,skiprows=SKIPROWS,nrows=NROWS1,usecols='A:B',index_col=None)
second = pd.read_excel(output_path,index_col=None)

NROWS = first.count(axis=0)[1] # counts without the headers
print(NROWS) # please check with the real number
#print(q)

#1. take from 'first' the pair first [AEM,Σύνολο]

for i in range(0,NROWS):
	A.append(list(first.xs(i)))
print(A)
S = np.sum([int(A[i][1]) for i in range(len(A)) ])
		
#2. find 'ΑΕΜ' in second and add Σύνολο to Βαθμός
#   if there is not such aem print that this aem does not exist.

print("\n")
for i in range(len(A)):	
	test_value = A[i][0]
	grade      = A[i][1]
	output     = second.loc[second[' ΑΕΜ '] == test_value] # for the old sis
	
	#output     = second.loc[second['ΑΕΜ'] == test_value] # for the new sis
	if len(output) == 0:
		print("the student with AEM:",test_value,"does not exist")
		B.append([test_value,grade])
	else:
		counter = counter + 1
		found_the_row = output.index[0]
		#print("line:",found_the_row)
		#print("βαθμός:",A[i][1]) # for old sis
		second.at[found_the_row,' Βαθμός ']=grade
		#print(second.iloc[found_the_row])
		#print(second.at[found_the_row,' ΑΕΜ ']) # for the old sis
		#print(second.at[found_the_row,'ΑΕΜ']) # for the new sis


C = [] # C contains the valid grades >=5
B1 = [x[0] for x in B]
for i in range(len(A)):
	if A[i][0] not in  B1:
		if int(A[i][1])>=5:
			C.append(A[i][1])

print("the number of grades are:",len(A))
print("the number of valid grades are:",len(A)-len(B))
print("successes:",counter)
print("fails:",len(A)-counter)
print(B)
S1 = np.sum([int(B[i][1]) for i in range(len(B)) ])
print("\n",">=5 :",len(C))
print(" <5  :",len(A)-len(B)-len(C))
print(" mean (of the valid AEMs):",(S-S1)/counter)
print(" success rate:",len(C)/counter*100,"%")

#3. convert 'second' to xlsx.

second.to_excel(output_path,index=False) # for some reason it makes the header bold.
