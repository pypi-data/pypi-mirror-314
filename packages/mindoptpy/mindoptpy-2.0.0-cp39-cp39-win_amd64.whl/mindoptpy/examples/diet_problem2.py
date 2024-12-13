from mindoptpy import *


req = \
    {
        # requirement: ( lower bound,   upper bound)
        "Cal": (2000, MDO.INFINITY),
        "Carbo": (350, 375),
        "Protein": (55, MDO.INFINITY),
        "VitA": (100, MDO.INFINITY),
        "VitC": (100, MDO.INFINITY),
        "Calc": (100, MDO.INFINITY),
        "Iron": (100, MDO.INFINITY),
        "Volume": (-MDO.INFINITY, 75),

    }

food = \
    {
        # food            : ( lower bound,  upper bound, cost)
        "Cheeseburger": (0, MDO.INFINITY, 1.84),
        "HamSandwich": (0, MDO.INFINITY, 2.19),
        "Hamburger": (0, MDO.INFINITY, 1.84),
        "FishSandwich": (0, MDO.INFINITY, 1.44),
        "ChickenSandwich": (0, MDO.INFINITY, 2.29),
        "Fries": (0, MDO.INFINITY, 0.77),
        "SausageBiscuit": (0, MDO.INFINITY, 1.29),
        "LowfatMilk": (0, MDO.INFINITY, 0.60),
        "OrangeJuice": (0, MDO.INFINITY, 0.72)
    }

req_value = \
    {
        # (requirement, food              ) : value
        ("Cal", "Cheeseburger"): 510,
        ("Cal", "HamSandwich"): 370,
        ("Cal", "Hamburger"): 500,
        ("Cal", "FishSandwich"): 370,
        ("Cal", "ChickenSandwich"): 400,
        ("Cal", "Fries"): 220,
        ("Cal", "SausageBiscuit"): 345,
        ("Cal", "LowfatMilk"): 110,
        ("Cal", "OrangeJuice"): 80,

        ("Carbo", "Cheeseburger"): 34,
        ("Carbo", "HamSandwich"): 35,
        ("Carbo", "Hamburger"): 42,
        ("Carbo", "FishSandwich"): 38,
        ("Carbo", "ChickenSandwich"): 42,
        ("Carbo", "Fries"): 26,
        ("Carbo", "SausageBiscuit"): 27,
        ("Carbo", "LowfatMilk"): 12,
        ("Carbo", "OrangeJuice"): 20,

        ("Protein", "Cheeseburger"): 28,
        ("Protein", "HamSandwich"): 24,
        ("Protein", "Hamburger"): 25,
        ("Protein", "FishSandwich"): 14,
        ("Protein", "ChickenSandwich"): 31,
        ("Protein", "Fries"): 3,
        ("Protein", "SausageBiscuit"): 15,
        ("Protein", "LowfatMilk"): 9,
        ("Protein", "OrangeJuice"): 1,

        ("VitA", "Cheeseburger"): 15,
        ("VitA", "HamSandwich"): 15,
        ("VitA", "Hamburger"): 6,
        ("VitA", "FishSandwich"): 2,
        ("VitA", "ChickenSandwich"): 8,
        ("VitA", "Fries"): 0,
        ("VitA", "SausageBiscuit"): 4,
        ("VitA", "LowfatMilk"): 10,
        ("VitA", "OrangeJuice"): 2,

        ("VitC", "Cheeseburger"): 6,
        ("VitC", "HamSandwich"): 10,
        ("VitC", "Hamburger"): 2,
        ("VitC", "FishSandwich"): 0,
        ("VitC", "ChickenSandwich"): 15,
        ("VitC", "Fries"): 15,
        ("VitC", "SausageBiscuit"): 0,
        ("VitC", "OrangeJuice"): 4,
        ("VitC", "LowfatMilk"): 120,

        ("Calc", "Cheeseburger"): 30,
        ("Calc", "HamSandwich"): 20,
        ("Calc", "Hamburger"): 25,
        ("Calc", "FishSandwich"): 15,
        ("Calc", "ChickenSandwich"): 15,
        ("Calc", "Fries"): 0,
        ("Calc", "SausageBiscuit"): 20,
        ("Calc", "LowfatMilk"): 30,
        ("Calc", "OrangeJuice"): 2,

        ("Iron", "Cheeseburger"): 20,
        ("Iron", "HamSandwich"): 20,
        ("Iron", "Hamburger"): 20,
        ("Iron", "FishSandwich"): 10,
        ("Iron", "ChickenSandwich"): 8,
        ("Iron", "Fries"): 2,
        ("Iron", "SausageBiscuit"): 15,
        ("Iron", "LowfatMilk"): 0,
        ("Iron", "OrangeJuice"): 2,

        ("Volume", "Cheeseburger"): 4,
        ("Volume", "HamSandwich"): 7.5,
        ("Volume", "Hamburger"): 3.5,
        ("Volume", "FishSandwich"): 5,
        ("Volume", "ChickenSandwich"): 7.3,
        ("Volume", "Fries"): 2.6,
        ("Volume", "SausageBiscuit"): 4.1,
        ("Volume", "LowfatMilk"): 8,
        ("Volume", "OrangeJuice"): 12
    }
# Create a model
m = Model()

# Add Variables
variable = {}
for food_name, food_data in food.items():
    variable[food_name] = m.addVar(
        lb=food_data[0], ub=food_data[1], vtype=MDO.CONTINUOUS, name=food_name
    )

# Add Constraints
# Ensure that the intake of each nutrient is above the given lower bound and below the given upper bound
cons = {}
for req_name, req_data in req.items():
    cons[req_name] = m.addRange(
        quicksum(
            variable[food_name] * req_value[(req_name, food_name)]
            for food_name in food.keys()
        ),
        req_data[0],
        req_data[1],
    )

# Add Objective Function
objective = quicksum(variable[i] * food[i][2] for i in food.keys())
m.setObjective(objective, MDO.MINIMIZE)
m.optimize()
print(f"Optimal objective value is: {m.objval}")

for i in variable:
    print("Amount of " + i + " intake :" + str(variable[i].X))
print("Total meal cost : " + str(objective.getValue()))
for req_name, req_data in req.items():
    print(
        "Final intake amount of "
        + req_name
        + ": "
        + str(
            quicksum(
                variable[food_name] * req_value[(req_name, food_name)]
                for food_name in food.keys()
            ).getValue()
        )
    )
