"""
/**
 *  Description
 *  -----------
 *
 *  Linear optimization.
 *   - Compute an IIS on an infeasible problem.
 * 
 *  Formulation
 *  -----------
 *
 *  Minimize
 *  Obj:
 *  Subject To
 *  c0:  -0.500000000 x0 + x1 >= 0.500000000
 *  c1:  2 x0 - x1 >= 3
 *  c2:  3 x0 + x1 <= 6
 *  c3:  3 x3 - x4 <= 2 <- conflit with variable bounds below!
 *  c4:  x0 + x4 <= 10
 *  c5:  x0 + 2 x1 + x3 <= 14
 *  c6:  x1 + x3 >= 1
 *  Bounds
 *   5 <= x3
 *   0 <= x4 <= 2
 *  End
 */
"""
from mindoptpy import *

# Create an empty model for optimization.
model = Model("IIS_LP")

# Add Variables.
x = []
x.append(model.addVar(0.0, float('inf'), vtype = 'C', name = "x0"))
x.append(model.addVar(0.0, float('inf'), vtype = 'C', name = "x1"))
x.append(model.addVar(0.0, float('inf'), vtype = 'C', name = "x2"))
x.append(model.addVar(5.0, float('inf'), vtype = 'C', name = "x3"))
x.append(model.addVar(0.0, 2.0,          vtype = 'C', name = "x4"))

# Add Constraints.
constr = []
constr.append(model.addConstr(-0.5 * x[0]       + x[1]                    >= 0.5,  "c0"))
constr.append(model.addConstr( 2.0 * x[0]       - x[1]                    >= 3.0,  "c1"))
constr.append(model.addConstr( 3.0 * x[0]       + x[1]                    <= 6.0,  "c2"))
constr.append(model.addConstr(                          3.0 * x[3] - x[4] <= 2.0,  "c3"))
constr.append(model.addConstr(       x[0]                          + x[4] <= 10.0, "c4"))
constr.append(model.addConstr(       x[0] + 2.0 * x[1]      + x[3]        <= 14.0, "c5"))
constr.append(model.addConstr(       x[1] +                   x[3]        >= 1.0,  "c6"))

# Optimize the input problem.
model.optimize()

# Run IIS.
if model.status == MDO.INFEASIBLE or model.status == MDO.INF_OR_UBD:
    print("Optimizer terminated with an primal infeasible status.")
    print("Start to compute an Irreducible Inconsistent Subsystem (IIS).")
    # Compute an IIS and write it to file (in ILP format).
    model.computeIIS()
    print("Writing IIS into file (ILP format).")
    model.write("./test1.ilp")
    print("Populating all bounds participate in the computed IIS.")
    for c in constr:
        status = c.IISConstr
        name = c.ConstrName
        if status == 2:
            print(f"The upper bound of inequality constraint [{name}] participates in the IIS.")
        elif status == 3:
            print(f"The lower bound of inequality constraint [{name}] participates in the IIS.")
        elif status == 5:
            print(f"[{name}] is an equality constraint, and both its lower bound and upper bound participate in the IIS.")
    for v in x:
        status = v.IISVar
        name = v.VarName
        if status == 2:
            print(f"The upper bound of variable [{name}] participates in the IIS.")
        elif status == 3:
            print(f"The lower bound of variable [{name}] participates in the IIS.")
        elif status == 5:
            print(f"[{name}] is a fixed variable, and both its lower bound and upper bound participate in the IIS.")
