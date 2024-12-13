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
 *    tr(C X)
 *  Subject To
 *    c0 : tr(A X) = 1
 *  Bounds
 *    X is p.s.d.
 *
 *  Matrix
 *    C = [ -3  0  1 ]  A = [ 3 0 1 ]
 *        [  0 -2  0 ]      [ 0 4 0 ]
 *        [  1  0 -3 ]      [ 1 0 5 ]
 *  End
 */
 """
import numpy as np
from mindoptpy import *


# Step 1. Create a model.
model = Model()

# Step 2. Input model.
# Add a PSD matrix variable.
X = model.addPsdVar(dim=3, name="X")

# Set objective.
C = np.array([[-3, 0, 1], [0, -2, 0], [1, 0, -3]])
objective = C * X
model.setObjective(objective, MDO.MAXIMIZE)

# Input the constraint.
A = np.array([[3, 0, 1], [0, 4, 0], [1, 0, 5]])
model.addConstr(A * X == 1, "c0")

# Step 3. Solve the problem and display the result.
model.optimize()

if model.status == MDO.OPTIMAL or model.status == MDO.SUB_OPTIMAL:
    # Display objective.
    print(f"Optimal objective value is: {str(objective.getValue())}")

    # Display the solution.
    print("X = ")
    print(X.PsdX)
else:
    print("No feasible solution.")
