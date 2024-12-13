from mindoptpy import *


# Number of required workers for each day
day_name, workers_per_day = multidict(
    {
        "Monday": 3,
        "Tuesday": 1,
        "Wednesday": 4,
        "Thursday": 2,
        "Friday": 1,
        "Saturday": 3,
        "Sunday": 3,
    }
)

workers, pay = multidict(
    {
        "Xiaoming": 13,
        "Huahua": 10,
        "HongHong": 11,
        "Dahua": 8,
        "Lihua": 9,
        "Niuniu": 14,
        "Gouzi": 14,
    }
)

availability = tuplelist(
    [
        ("Xiaoming", "Tuesday"),
        ("Xiaoming", "Wednesday"),
        ("Xiaoming", "Friday"),
        ("Xiaoming", "Sunday"),
        ("Huahua", "Monday"),
        ("Huahua", "Tuesday"),
        ("Huahua", "Friday"),
        ("Huahua", "Saturday"),
        ("HongHong", "Wednesday"),
        ("HongHong", "Thursday"),
        ("HongHong", "Friday"),
        ("HongHong", "Sunday"),
        ("Dahua", "Tuesday"),
        ("Dahua", "Wednesday"),
        ("Dahua", "Friday"),
        ("Dahua", "Saturday"),
        ("Lihua", "Monday"),
        ("Lihua", "Tuesday"),
        ("Lihua", "Wednesday"),
        ("Lihua", "Thursday"),
        ("Lihua", "Friday"),
        ("Lihua", "Sunday"),
        ("Niuniu", "Monday"),
        ("Niuniu", "Tuesday"),
        ("Niuniu", "Wednesday"),
        ("Niuniu", "Saturday"),
        ("Gouzi", "Monday"),
        ("Gouzi", "Tuesday"),
        ("Gouzi", "Wednesday"),
        ("Gouzi", "Friday"),
        ("Gouzi", "Saturday"),
        ("Gouzi", "Sunday"),
    ]
)

m = Model("WorkForce")

# Add Variables
# x[(worker, day)] represents whether this worker is scheduled for this day.
# Using worker-day pair to initialize variables ensure that each person works only at the time they are available
x = m.addVars(availability, vtype=MDO.BINARY, name="schedule")


# Add Constraints
# Constraint : ensure that each day has enough workforce
c1 = m.addConstrs((x.sum("*", day) == workers_per_day[day] for day in day_name))

# Add Objective Function
objective = quicksum(
    pay[worker_day[0]] * x[(worker_day[0], worker_day[1])]
    for worker_day in availability
)
m.setObjective(objective, MDO.MINIMIZE)

# Start Optimizing
m.optimize()
print(f"Optimal objective value is: {m.objval}")

# Print Result
for worker, day in availability:
    if x[(worker, day)].X:
        print(worker + " should work at " + day)

print("The total cost is " + str(objective.getValue()))
