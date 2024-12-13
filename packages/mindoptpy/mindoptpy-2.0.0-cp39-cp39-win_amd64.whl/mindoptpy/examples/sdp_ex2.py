"""
/**
 *  Description
 *  -----------
 *
 *  Semidefinite optimization (row-wise input).
 *
 *  Formulation
 *  -----------
 *
 *  Maximize
 *  obj: 
 *   tr(C0 X0)   + tr(C1 X1)    + 0 x0 + 0 x1
 *  Subject To
 *   c0 : tr(A00 X0)                + 1 x0        = 1
 *   c1 :              tr(A11 X1)          + 1 x1 = 2
 *  Bounds
 *    0 <= x0
 *    0 <= x1
 *    X0,X1 are p.s.d.
 *
 *  Matrix
 *    C0 =  [ 2 1 ]   A00 = [ 3 1 ]
 *          [ 1 2 ]         [ 1 3 ]
 *
 *    C1 = [ 3 0 1 ]  A11 = [ 3 0 1 ]
 *         [ 0 2 0 ]        [ 0 4 0 ]
 *         [ 1 0 3 ]        [ 1 0 5 ]
 *  End
 */
 """
import numpy as np
from mindoptpy import *


# Step 1. Create a model.
model = Model()

# Step 2. Input model.
# Add nonnegative scalar variables.
x0 = model.addVar(lb=0.0, name="x0")
x1 = model.addVar(lb=0.0, name="x1")

# Add PSD matrix variables.
X0 = model.addPsdVar(dim = 2, name = "X0")
X1 = model.addPsdVar(dim = 3, name = "X1")

# Set objective
C0 = np.array([[2, 1], [1, 2]])
C1 = np.array([[3, 0, 1], [0, 2, 0], [1, 0, 3]])
objective = C0 * X0 + C1 * X1
model.setObjective(objective, MDO.MAXIMIZE)

# Input the first constraint.
A00 = np.array([[3, 1], [1, 3]])
model.addConstr(A00 * X0 + x0 == 1, "c0")

# Input the second constraint.
A11 = np.array([[3, 0, 1], [0, 4, 0], [1, 0, 5]])
model.addConstr(A11 * X1 + x1 == 2, "c1")

# Step 3. Solve the problem and display the result.
model.optimize()

if model.status == MDO.OPTIMAL:
    # Display objective.
    print(f"Optimal objective value is: {str(objective.getValue())}")

    # Display the solution.
    print("x0 = " + " {0:7.6f}".format(x0.X))
    print("x1 = " + " {0:7.6f}".format(x1.X))
    print("X0 = ")
    print(X0.PsdX)
    print("X1 = ")
    print(X1.PsdX)
else:
    print("No feasible solution.")
