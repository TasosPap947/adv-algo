from ortools.linear_solver import pywraplp

def load(order, truck):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    assignment = [[0 for i in range(len(truck))] for j in range(len(order))]
    x = {}
    q = {}
    l = solver.IntVar(0, 1, 'f"l"')
    for i in range(len(order)):
        for j in range(len(truck)):
            x[(i, j)] = solver.IntVar(0, order[i], 'f"x[{i}][{j}]"')
            q[(i, j)] = solver.IntVar(0, 1, 'f"q[{i}][{j}]"')
  
  #1st and 2nd constraint
    for j in range(len(truck)):
        solver.Add(solver.Sum(x[i,j] for i in range(len(order))) <= truck[j])
        solver.Add(solver.Sum(q[i,j] for i in range(len(order))) <= 1)

  #max compartment and 3rd,4th,6th constraint
    maxim = max(truck)
    idx = truck.index(maxim)
    solver.Add(solver.Sum(x[i,idx] for i in range(len(order))) >= 0.8*maxim*l)
    solver.Add(solver.Sum(x[i,idx] for i in range(len(order))) <= 0.2*maxim + 0.8*maxim*l)
 
  #5th constraint
    solver.Add(solver.Sum(x[i,0] for i in range(len(order))) >= 0.9*truck[0]) 

  #7th constraint
    for i in range(len(order)):
        for j in range(len(truck)):
            solver.Add(x[i,j] <= q[i,j]*order[i])

  #8th constraint
    for i in range(len(order)):
        solver.Add(solver.Sum(x[i,j] for j in range(len(truck))) == order[i])
  
  
  
  #solution
    solver.Maximize(7)   #c=7
    status = solver.Solve() 
  
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        for i in range(len(order)):
            for j in range(len(truck)):
                if x[(i,j)].solution_value() > 0:
                    assignment[i][j] = x[(i,j)].solution_value()
    else:
        assignment = []
    return assignment




def assign(orders,trucks):
    solver = pywraplp.Solver.CreateSolver('SCIP')
    assignments = []
    d = {} #d_ij
    
    for i in range(len(orders)):
        for j in range(len(trucks)):
            d[(i, j)] = solver.IntVar(0, 1, 'f"d[{i}][{j}]"')
            t = load(orders[i],trucks[j])
            if(not t):
                solver.Add(d[(i,j)] == 0)
                
   #1st constraint
    for j in range(len(trucks)):
        solver.Add(solver.Sum(d[i,j] for i in range(len(orders))) <= 1)
   #2nd constraint 
    for i in range(len(orders)):
        solver.Add(solver.Sum(d[i,j] for j in range(len(trucks))) <= 1)
                
    solver.Maximize(solver.Sum(y for y in d.values()))
    status = solver.Solve() 
  
    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        for i in range(len(orders)):
            for j in range(len(trucks)):
                 if d[(i,j)].solution_value() > 0:
                    assignments.append((i,j, load(orders[i],trucks[j]))) 

    return assignments