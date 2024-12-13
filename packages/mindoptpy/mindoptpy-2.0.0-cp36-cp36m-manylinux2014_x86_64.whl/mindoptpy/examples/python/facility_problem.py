from mindoptpy import *

import math

# 问题背景
# 附近开了商场，商场的位置已经确定。但是供应链的仓库的位置尚未决定。
# 当前已经有了仓库的备选地点的清单。
# 本例子的目标是为了找到建立最小成本的仓库方案。

# 有两个商场，位置分别是(0, 1.7)和(1.4, 2.9)， 所需要的货物重量为100单位和200单位
market_info = tupledict([((0, 1.7), 100), ((1.4, 2.9), 200)])
market_keys = list(market_info.keys())
market_num = len(market_info)
# 有8个仓库， 分别记录了它们的仓库位置和建造成本
facilities_info = tupledict(
    [
        ((0, 1), 3),
        ((0, 2), 1),
        ((1, 0), 1.5),
        ((1, 1), 1.3),
        ((1, 2), 1.8),
        ((2, 0), 1.6),
        ((2, 1), 1.1),
        ((2, 2), 1.9),
    ]
)
facilities_keys = list(facilities_info.keys())
facilities_num = len(facilities_info)
transport_fee_per_m = 1.23

# 初始化模型
m = Model("Facilities")

# 初始化变量
# x是一个variable列表，里面的值的类型为Binary类型，代表是否在该地建仓库
x = m.addVars(len(facilities_info), vtype=MDO.BINARY)

# y数组代表从j仓库运向i商场的货物量，值的类型为CONTINUOUS类型，下限为0代表不能从j仓库运送小于0单位的货物到i商场
provide_quantity = [(i, j) for j in range(facilities_num) for i in range(market_num)]
y = m.addVars(provide_quantity, lb=0, vtype=MDO.CONTINUOUS)

# 初始化约束
# 约束1 已经决定建造的仓库必须满足所有商场的货物需求
m.addConstrs(
    (
        quicksum(y[i, j] for j in range(facilities_num))
        == market_info[market_keys[i]]
        for i in range(market_num)
    ),
    name="is_satisfy",
)
# 约束2 如果不建仓库，则此仓库位置运送给所有商场的货物为0
m.addConstrs(
    (
        y[i, j] / market_info[market_keys[i]] <= x[j]
        for i in range(market_num)
        for j in range(facilities_num)
    ),
    name="is_built",
)


# 初始化目标函数
# 目标函数： 最小化运输费用和建造仓库的费用的总和
# 假设从a地运往b地的运输费用只和距离有关，和货物重量无关
def transportation_fee(pos1, pos2):
    x1 = pos1[0] - pos2[0]
    x2 = pos1[1] - pos2[1]
    return math.sqrt(x1 * x1 + x2 * x2) * transport_fee_per_m


objective1 = quicksum(
    x[j] * facilities_info[facilities_keys[j]] for j in range(facilities_num)
)

objective2 = quicksum(
    y[(i, j)] * transportation_fee(market_keys[i], facilities_keys[j])
    for j in range(facilities_num)
    for i in range(market_num)
)

m.setObjective(objective1+objective2, MDO.MINIMIZE)

m.optimize()
m.write("test_fac.mps")
# 打印出来最佳建仓库的地址和最佳运货方案
print(f"Optimal objective value is: {m.objval}")

for i in x:
    if x[i].X:
        print(
            "A warehouse should build at No."
            + str(i + 1)
            + " location at "
            + str(facilities_keys[i])
        )
        for j in range(market_num):
            print(
                "This warehouse transport "
                + str(y[(j, i)].X)
                + " units of goods to "
                + str(j)
                + "supermarkets"
            )
