"""
/**
 *  Description
 *  -----------
 *
 *  Quadratic optimization (row-wise input).
 *
 *  Formulation
 *  -----------
 *
 *  Minimize
 *    obj: 1 x0 + 1 x1 + 1 x2 + 1 x3
 *         + 1/2 [ x0^2 + x1^2 + x2^2 + x3^2 + x0 x1]
 *  Subject To
 *   c1 : 1 x0 + 1 x1 + 2 x2 + 3 x3 >= 1
 *   c2 : 1 x0 - 1 x2 + 6 x3 = 1
 *  Bounds
 *    0 <= x0 <= 10
 *    0 <= x1
 *    0 <= x2
 *    0 <= x3
 *  End
 */
"""
from mindoptpy import *


# Step 1. Create a model.
model = Model("QP_01")

# Step 2. Input model.
# Add variables.
x = []
x.append(model.addVar(0.0,         10.0, 0.0, 'C', "x0"))
x.append(model.addVar(0.0, float('inf'), 0.0, 'C', "x1"))
x.append(model.addVar(0.0, float('inf'), 0.0, 'C', "x2"))
x.append(model.addVar(0.0, float('inf'), 0.0, 'C', "x3"))

# Add constraints.
# Note that the nonzero elements are inputted in a row-wise order here.
model.addConstr(1.0 * x[0] + 1.0 * x[1] + 2.0 * x[2] + 3.0 * x[3] >= 1, "c0")
model.addConstr(1.0 * x[0]              - 1.0 * x[2] + 6.0 * x[3] == 1, "c1")

# Add objective: 1 x0 + 1 x1 + 1 x2 + 1 x3 + 1/2 [ x0^2 + x1^2 + x2^2 + x3^2 + x0 x1]
obj = QuadExpr()

#option-I
obj.addTerms([1.0, 1.0, 1.0, 1.0], [x[0], x[1], x[2], x[3]])
obj.addTerms([0.5, 0.5, 0.5, 0.5, 0.5], [x[0], x[1], x[2], x[3], x[0]], [x[0], x[1], x[2], x[3], x[1]])

#option II
# obj = 1*x[0] + 1*x[1] + 1*x[2] + 1*x[3] + 0.5 * x[0]*x[0] + 0.5 * x[1]*x[1] + 0.5 * x[2]*x[2] + 0.5 * x[3]*x[3] + 0.5*x[0]*x[1]

# Set objective and change to minimization problem.
model.setObjective(obj, MDO.MINIMIZE)

# Step 3. Solve the problem and populate optimization result.
model.optimize()

if model.status == MDO.OPTIMAL:
    print(f"Optimal objective value is: {model.objval}")
    print("Decision variables:")
    for v in x:
        print(f"x[{v.VarName}] = {v.X}")
else:
    print("No feasible solution.")
