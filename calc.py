import math
from prettytable import PrettyTable

# rough estimate from chatgpt
torque_curve = {
    500: 67,
    1000: 80,
    1500: 95,
    2000: 110,
    2500: 120,
    3000: 128,
    3500: 134,
    4000: 138,
    4500: 140,  # peak torque
    5000: 139,
    5500: 135,
    6000: 130,
    6500: 122,
    7000: 112,
}
max_torque = max(torque_curve.values())
torque_percentage = {rpm: torque / max_torque for rpm, torque in torque_curve.items()}


apps = [
    0,
    2.299999952316284,
    5,
    7.5,
    10,
    15,
    20,
    25,
    30,
    35,
    40,
    45,
    50,
    60,
    70,
    80,
    90,
    100,
]

rpms = [500, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 6000, 7000]


def linear_app_to_tp(app: float) -> float:
    # app in percentage
    # convert from 0-100 to a fraction, then multiply by 90 degrees (in radians)
    # return 100 * math.sin(app * math.pi / 200) # Wrong, got mixed up
    return 100 * (1 - math.cos(app * math.pi / 200))


app_to_tp_table: list[list[float]] = []

for rpm in rpms:
    column = list()
    for app in apps:
        tp = linear_app_to_tp(app)
        # if app < 55:
        tp /= torque_percentage[rpm]
        if tp > 100:
            tp = 100
        column.append(round(tp, 1))
    app_to_tp_table.append(column)

printing = PrettyTable()

field_names = ["APP"]
for i in rpms:
    field_names.append(str(i))

# printing.field_names = field_names
printing.add_column("APP", [str(app) for app in apps])
for c in range(len(app_to_tp_table)):
    printing.add_column(str(rpms[c]), app_to_tp_table[c])

print(printing)
