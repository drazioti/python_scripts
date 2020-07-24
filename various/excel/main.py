# wriiten in python3
# author : K.A.Draziotis
# Licence : GPL
# dependencies : 
# pip3 install xlrd

import pandas as pd
import xlsxwriter
from pandas_ods_reader import read_ods

counter = 0 # counts the number of grades successfully passed to the second excel
input_path  = 'A.xlsx'
output_path = 'B.xls'

A = []
B = []

SKIPROWS = 1    # depends on the format of the file A.xlsx : input path (the header does not count)
NROWS    = 394  # TODO : equals to : [number of grades] - [SKIPROWS+1]
first  = pd.read_excel(input_path,skiprows=SKIPROWS,nrows=NROWS,usecols='A:B',index_col=None)
second = pd.read_excel(output_path,index_col=None)

#1. take from 'first' the pair first [AEM,Σύνολο]

for i in range(0,NROWS):
	A.append(list(first.xs(i)))
print(A)


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

print("the number of grades are:",len(A))
print("successes:",counter)
print("fails:",len(A)-counter)
print(B)

#3. convert 'second' to xlsx.

second.to_excel(output_path,index=False) # make the header bold.

