from ortools.linear_solver import pywraplp
'''
Parameters:
  - points: a list of 2-dimensional tuples (x,y)

Returns:
  - (a,b): a tuple with the line's coefficients
'''
def fit_line(points):
    
    n = len(points)
    sol = pywraplp.Solver.CreateSolver('GLOP')
    inf = sol.infinity()
    a = sol.NumVar(-inf, inf, 'a')
    b = sol.NumVar(-inf, inf, 'b')
    h = {}
    
    for i in range(n):
        h[i] = sol.NumVar(-inf, inf, f'h_{i}')
    
    j = 0
    for (x,y) in points:
        sol.Add(-a*x - b + y <= h[j])
        sol.Add(-a*x - b + y >= -h[j])
        j += 1
    
    sol.Minimize(sol.Sum(h[i] for i in range(n)))
    flag = sol.Solve()
    
    if flag == sol.OPTIMAL or flag == sol.FEASIBLE:
        res = (a.solution_value(), b.solution_value())
    
    return res