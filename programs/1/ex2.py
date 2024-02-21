'''
Parameters:
  - n: αριθμός παραγγελιών
  - m: αριθμός διαθέσιμων φορτηγών
  - compatibility: λίστα από tuples (x,y) που υποδηλώνουν ότι
    το φορτηγό y μπορεί να παραδώσει την παραγγελία x.
    Θα ισχύει ότι 1 <= x <= n και 1 <= y <= m

Returns:
  - assignment: μια λίστα με tuples (x,y) τα οποία υποδηλώνουν ότι η παραγγελία
    x θα παραδοθεί από το φορτηγό y.

Sample input:
  n = 3
  m = 2
  compatibility = [(1,1), (2,1), (3,1), (2,2), (3,2)]

Sample output:

  [(1,1), (2,2)]

Σημείωση: υπάρχουν και άλλες λύσεις στις οποίες ταξινομούνται 2 παραγγελίες,
π.χ. [(2,1), (3,2)]. Μπορείτε να επιστρέψετε οποιαδήποτε από αυτές θέλετε.
'''

from ortools.linear_solver import pywraplp

def assign(n, m, compatibility):
    sol = pywraplp.Solver.CreateSolver('SCIP')
    track = {}
    job = {}
    A = {}
  
    for i in range(1,m+1):  #track[i]: a list of the jobs whitch the track i can transfer
        track[i] = []
  
    for i in range(1,n+1): #job[i]: a list of the tracks which can transfer the job i
        job[i] = []
  
    for (x,y) in compatibility:
        track[y].append(x)
        job[x].append(y)
  
    for tr in track:
        for jb in track[tr]:
            A[(jb, tr)] = sol.IntVar(0, 1, 'f"A[{jb}][{tr}]"')
  
    for tr in track:
        sol.Add(sol.Sum([A[(i,tr)] for i in track[tr] ]) <= 1)
  
    for jb in job:
        sol.Add(sol.Sum([A[(jb,i)] for i in job[jb] ]) <= 1) 

    sol.Maximize(sol.Sum([A[(i,j)] for (i,j) in A]))
    flag = sol.Solve()
    res = [] 

    if flag == pywraplp.Solver.OPTIMAL or flag == pywraplp.Solver.FEASIBLE:
        res = [(x,y) for (x,y) in A if A[(x,y)].solution_value() > 0]
    return res