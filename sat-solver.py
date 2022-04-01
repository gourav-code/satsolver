#!/usr/bin/python3
import random
import sys
import csv
import numpy.random as npr


def propagate_units(F):
	for temp in F:
		if 0 in temp:
			continue
		if len(temp) == 1:
			for i,temp1 in enumerate(F):
				if 0 in temp1:
					continue
				if temp[0] in temp1 and len(temp1) > 1:
					# print(f'F[i] : {F[i]}')
					F[i].append(0)
					# print(f'F[i] : {F[i]}')
				elif (-1*temp[0]) in temp1:
					if len(temp1) > 1:
						temp1.remove((-1*temp[0]))
					else:
						F[i].append(0)

	
def pure(F,x):
	for temp in F:
		if 0 in temp:
			continue
		if (-1*x) in temp:
			return False

	return True 

def pure_elim(var,F):
	for temp in range(1, var+1):
		if pure(F,temp):
			for i,temp1 in enumerate(F):
				if 0 in temp1:
					continue
				if temp in temp1:
					F[i].append(0)
			F.append([temp])
		elif pure(F,-1*temp):
			for i,temp1 in enumerate(F):
				if 0 in temp1:
					continue
				if -1*temp in temp1:
					F[i].append(0)
			F.append([-1*temp])

	

def check(var, F):
	for temp in F:
		if 0 in temp:
			continue
		if len(temp) != 1:
			return False

	local_list = []
	for temp in range(1,var+1):
		local_list.append(0)

	for temp in F:
		if 0 in temp:
			continue
		local_list[abs(temp[0])-1] = 1

	for temp in local_list:
		if temp == 0:
			return False

	return True


def solve(VARS, F):
	
	propagate_units(F)
	pure_elim(VARS, F)

	#checking for empty clause
	for temp in F:
		if 0 in temp:
			continue
		if len(temp) < 1:
			return 0

	#checking if F contains all unit clauses 
	if check(VARS, F):
		return F
	
	var_list = []
	for temp in range(1,VARS+1):
		var_list.append(temp)

	i = npr.choice(var_list)
	# print(f'F[i] 96 : {F[-1]}')
	F.append([i])
	# print(f'F[i] 98 : {F[-1]}   i : {i}')
	ans = solve(VARS, F)
	if ans == 0:
		# print(f'F[i] 101 : {F[-1]}')
		F[-1].append(0)
		# print(f'F[i] 103 : {F[-1]}')
	else:
		return F
	# print(f'F[i] 106 : {F[-1]}')
	F.append([-1*i])
	# print(f'F[i] 108 : {F[-1]}')
	
	return solve(VARS,F)

	

def main():
	file_name = sys.argv
	if len(file_name) <= 1:
		print('!ERROR Give file name')
		exit()
	

	VAR = 0
	CLAUSE = []
	with open(file_name[1],'r',encoding='utf-8') as inFile:
		reader = csv.reader(inFile)
		for row in reader:
			row = row[0].split()
			if row[0] == 'p':
				VAR = int(row[2])
				continue
			elif row[0] != 'p' and row[0] != 'c':
				row.pop(-1)
				for i in range(len(row)):
					row[i] = int(row[i])
				CLAUSE.append(row)

	# print(f'clause : {CLAUSE}')		
	result = solve(VAR, CLAUSE)

	if result == 0:
		print("unsatisfiable")

	else:
		for temp in result:
			if 0 in temp:
				continue
			print(temp[0])



if __name__ == '__main__':
    main()