import pickle
import argparse
import numpy as np

parser = argparse.ArgumentParser()

parser.add_argument("--ex1", action="store_true")
parser.add_argument("--ex2", action="store_true")
args = parser.parse_args()


if args.ex1:
    from solution import load
if args.ex2:
    from solution import assign

def check_assignment(order, truck, assignment):
    n = len(order)
    m = len(truck)

    assignment = np.array(assignment)

    for i in range(n):
        if sum(assignment[i]) != order[i]:
            return False

    for j in range(m):
        if sum(assignment[:,j]) > truck[j]:
            return False

    if sum(assignment[:,0]) < 0.9*truck[0]:
        return False

    max_ = truck.index(max(truck))
    fuel_in_max = sum(assignment[:,max_])

    if  fuel_in_max < 0.8*truck[max_] and fuel_in_max > 0.2*truck[max_]:
        return False

    for j in range(m):
        orders_in_compartment = len([x for x in assignment[:,j] if x > 0])
        if orders_in_compartment > 1:
            return False

    return True

def evaluate_ex1():
    testcases = []

    with open('ex1_public.pickle','rb') as f:
        testcases = pickle.load(f)

    i = 0
    for o,t,a in testcases:
        assignment = load(o,t)
        wrong = False

        if a == 0 and assignment != [] and not check_assignment(o,t,assignment):
            wrong = True

        if a == 1 and (assignment == [] or not check_assignment(o,t,assignment)):
            wrong = True

        if wrong:
            print(f'--- Testcase {i} failed!')
        else:
            print(f'+++ Testcase {i} OK!')
        i += 1

def evaluate_ex2():
    testcases = []

    with open('ex2_public.pickle','rb') as f:
        testcases = pickle.load(f)

    i = 0
    for o,t,m in testcases:
        assignments = assign(o,t)
        if len(assignments) < len(m):
            print(f'--- Testcase {i} failed!')

        wrong = False
        trucks_used = set()
        orders_used = set()

        for x,y,z in m:
            if x in orders_used:
                wrong = True
                break
            orders_used.add(x)

            if y in trucks_used:
                wrong = True
                break
            trucks_used.add(y)

            if not check_assignment(o[x],t[y],z):
                wrong = True
                break

        if not wrong:
            print(f'+++ Testcase {i} OK!')
        else:
            print(f'--- Testcase {i} failed.')

        i += 1



if __name__ == '__main__':
    if args.ex1:
        evaluate_ex1()
    if args.ex2:
        evaluate_ex2()
