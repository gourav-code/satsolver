import sys
import csv
 
#  this is the implementation of recursive dpll algorithm which takes in arguements as cut down cnf at that level and assumptions if for backtracking call 
def dpll(cnf, assumption={}):
    # print(assumption)
    if len(cnf) == 0:
        return True, assumption
 
    if any([len(c)==0 for c in cnf]):
        return False, None
 
    l = iterate_over_literal(cnf)
 
    chnged_cnf = [c for c in cnf if (l, True) not in c]
    chnged_cnf = [c.difference({(l, False)}) for c in chnged_cnf]
    sat, vals = dpll(chnged_cnf, {**assumption, **{l: True}}) # for less space and doesnot have to think for removal of l==true
    if sat:
        return sat, vals
 

    chnged_cnf = [c for c in cnf if (l, False) not in c]
    chnged_cnf = [c.difference({(l, True)}) for c in chnged_cnf]
    sat, vals = dpll(chnged_cnf, {**assumption, **{l: False}}) # for less space and doesnot have to think for removal of l==false
    if sat:
        return sat, vals
 
    return False, None

def iterate_over_literal(cnf):
    for c in cnf:
        for literal in c:
            return literal[0]

def main():
    file_name = sys.argv
    if len(file_name) <= 1:
        print('!ERROR Give file name')
        exit()
    CLAUSE = []
    with open(file_name[1],'r',encoding='utf-8') as inFile:
        reader = csv.reader(inFile)
        for row in reader:
            row = row[0].split()
            if row[0] == 'p':
                continue
            elif row[0] != 'p' and row[0] != 'c':
                row.pop(-1)
                l = set()
                for temp in row:
                    value = True
                    if '-' in temp:
                        value = False
                        temp = temp.replace('-','')
                    # print(type(temp))
                    l.add((temp,value))
                # print(l)
                CLAUSE.append(l)
    # print(f'clause : {CLAUSE}')	
    result,formula = dpll(CLAUSE)
    if result:
        print('sat')
        print(formula)
    else:
        print('unsat')


if __name__ == '__main__':
    main()