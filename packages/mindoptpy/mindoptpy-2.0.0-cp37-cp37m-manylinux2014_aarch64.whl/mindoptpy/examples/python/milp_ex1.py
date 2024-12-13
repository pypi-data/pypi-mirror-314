"""
/**
 *  Description
 *  -----------
 *
 *  Mixed Integer Linear optimization (row-wise input).
 *
 *  Formulation
 *  -----------
 *
 *  Minimize
 *    obj: 1 x0 + 2 x1 + 1 x2 + 1 x3
 *  Subject To
 *   c1 : 1 x0 + 1 x1 + 2 x2 + 3 x3 >= 1
 *   c2 : 1 x0 - 1 x2 + 6 x3 = 1
 *  Bounds
 *    0 <= x0 <= 10
 *    0 <= x1
 *    0 <= x2
 *    0 <= x3
 *  Integers
 *    x0 x1 x2
 *  End
 */
"""
from mindoptpy import *


# Step 1. Create a model and change the parameters.
model = Model("MILP_01")

# Step 2. Input model.xs
# Change to minimization problem.
model.modelsense = MDO.MINIMIZE

# Add variables.
x = []
x.append(model.addVar(0.0,         10.0, 1.0, 'I', "x0"))
x.append(model.addVar(0.0, float('inf'), 2.0, 'I', "x1"))
x.append(model.addVar(0.0, float('inf'), 1.0, 'I', "x2"))
x.append(model.addVar(0.0, float('inf'), 1.0, 'C', "x3"))

# Add constraints.
model.addConstr(1.0 * x[0] + 1.0 * x[1] + 2.0 * x[2] + 3.0 * x[3] >= 1, "c0")
model.addConstr(1.0 * x[0]              - 1.0 * x[2] + 6.0 * x[3] == 1, "c1")

# Step 3. Solve the problem and populate optimization result.
model.optimize()

if model.status == MDO.OPTIMAL:
    print(f"Optimal objective value is: {model.objval}")
    print("Decision variables: ")
    for v in x:
        print(f"x[{v.VarName}] = {v.X}")
else:
    print("No feasible solution.")
