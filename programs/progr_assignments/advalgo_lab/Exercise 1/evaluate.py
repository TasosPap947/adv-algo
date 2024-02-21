import argparse
import pickle

parser = argparse.ArgumentParser()

parser.add_argument("--ex1", action="store_true")
parser.add_argument("--ex2", action="store_true")
parser.add_argument("--both", action="store_true")
args = parser.parse_args()


if args.ex1 or args.both:
    from ex1 import fit_line
if args.ex2 or args.both:
    from ex2 import assign

def evaluate_ex1():
    file = 'ex1_public.pickle'
    epsilon = 1e-9
    testcases = []

    with open(file,'rb') as f:
        testcases = pickle.load(f)


    print('\n==============================\n')
    print('Testing solver for problem 1\n')

    for i, t in enumerate(testcases):
        points, opt_error = t
        a, b = fit_line(points)

        error_incurred = sum([abs(a * x + b - y) for x,y in points])

        if opt_error + epsilon >= error_incurred:
            print(f'+++ Testcase {i} OK.')
        else:
            print(f'--- Testcase {i} failed.')

    print('\n==============================\n')

def evaluate_ex2():
    file = 'ex2_private.pickle'

    testcases = []

    with open(file,'rb') as f:
        testcases = pickle.load(f)

    print('\n==============================\n')
    print('Testing solver for problem 2\n')
    for j, t in enumerate(testcases):
        testcase, opt = t
        n, m, compatibility = testcase

        solution = assign(n, m, compatibility)

        suboptimal = len(solution) < opt

        if suboptimal:
            print(f'--- Testcase {j} failed.\n The solver returned a suboptimal matching.\n')
            continue

        adj_orders = {}
        order_used = {}
        for i in range(1,n+1):
          adj_orders[i] = []
          order_used[i] = False

        adj_trucks = {}
        truck_used = {}
        for i in range(1,m+1):
          adj_trucks[i] = []
          truck_used[i] = False

        for u,v in compatibility:
            adj_orders[u].append(v)
            adj_trucks[v].append(u)

        for u,v in solution:
            wrong = u > n or v > m or order_used[u]\
                    or truck_used[v] or (not u in adj_trucks[v])\
                    or (not v in adj_orders[u])
            if wrong:
                print(f'--- Testcase {j} failed.\n The solver returned an infeasible matching.\n')
                continue

        print(f'+++ Testcase {j} OK.')


    print('\n==============================\n')


if args.ex1 or args.both:
    evaluate_ex1()
if args.ex2 or args.both:
    evaluate_ex2()
