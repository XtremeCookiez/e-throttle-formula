import math
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from prettytable import PrettyTable
from mpl_toolkits.mplot3d import Axes3D

# https://forum.miata.net/vb/showthread.php?t=466026
torque_curve = {
    500: 67, # guess
    1000: 80, # guess
    1500: 95, # guess
    2000: 110, # guess
    2500: 120, # guess
    3000: 130,
    3500: 134,
    4000: 134,
    4500: 134,
    5000: 136,
    5500: 133,
    6000: 131,
    6500: 129,
    7000: 116,
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


def app_to_tp(app: float) -> float:
    # app in percentage
    # convert from 0-100 to a fraction, then multiply by 90 degrees (in radians)
    # return 100 * math.sin(app * math.pi / 200) # Wrong, got mixed up
    # return 100 * (1 - math.cos(app * math.pi / 200))
    return (200 / math.pi) * math.acos(1 - (app / 100))

def rpm_app_to_tp(rpm:int, app:float):
    """
    This function contains all your desired logic to calculate
    the desired tp from app and rpm.

    Must return a float between 0 and 100.
    """

    tp = app_to_tp(app)

    cs = calculate_cross_sectional_area(tp)
    needed_cs = cs / torque_percentage[rpm]
    needed_cs_column.append(round(needed_cs, 1))

    tp = calculate_tp_from_cross_section(needed_cs)
    # tp /= torque_percentage[rpm]
    if tp > 100:
        tp = 100

def calculate_cross_sectional_area(tp: float):
    return 100 * (1 - math.cos(tp * math.pi / 200))

def calculate_tp_from_cross_section(cs:float):
    if cs > 100:
        cs = 100
    return (200 / math.pi) * math.acos(1 - (cs / 100))

def plot_app_to_tp_3d(
    apps,
    rpms,
    app_to_tp_table,
    filename,
    title="Throttle Position vs APP and RPM",
    z_axis="TP",
):
    # Convert the table to a 2D NumPy array
    Z = np.array(
        app_to_tp_table
    ).T  # Transpose so that rows = len(apps), cols = len(rpms)
    X, Y = np.meshgrid(rpms, apps)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    surf = ax.plot_surface(X, Y, Z, cmap="viridis", edgecolor="k")

    ax.set_xlabel("RPM")
    ax.set_ylabel("APP (%)")
    ax.set_zlabel(z_axis)
    ax.set_title(title)

    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    plt.tight_layout()

    plt.savefig(f"{filename}.png", dpi=300)
    plt.close(fig)


def plot_app_to_tp_3d_plotly(
    apps,
    rpms,
    app_to_tp_table,
    filename,
    title="Throttle Position vs APP and RPM",
    z_axis="TP",
):
    # Convert the table to a 2D NumPy array
    Z = np.array(app_to_tp_table).T  # Transpose to shape (len(apps), len(rpms))
    X, Y = np.meshgrid(rpms, apps)

    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale="Viridis")])

    fig.update_layout(
        title=title,
        scene=dict(xaxis_title="RPM", yaxis_title="APP (%)", zaxis_title=z_axis),
        autosize=True,
        margin=dict(l=0, r=0, t=50, b=0),
    )

    # Save interactive HTML
    fig.write_html(f"{filename}.html", include_plotlyjs="cdn")
    print(f"Saved interactive plot to {filename}.html")


app_to_tp_table: list[list[float]] = []
app_to_cross_sectional: list[list[float]] = []
app_to_torque: list[list[float]] = []
app_to_needed_cs = []

for rpm in rpms:
    tp_column = list()
    cs_column = list()
    torque_column = list()
    needed_cs_column = list()
    for app in apps:
        tp = app_to_tp(app)

        cs = calculate_cross_sectional_area(tp)
        needed_cs = cs / torque_percentage[rpm]
        needed_cs_column.append(round(needed_cs, 1))
        if needed_cs > 100:
            needed_cs = 100
        tp = calculate_tp_from_cross_section(needed_cs)
        # tp /= torque_percentage[rpm]
        if tp > 100:
            tp = 100

        tp_column.append(round(tp, 1))
        cs = calculate_cross_sectional_area(tp)
        cs_column.append(round(cs, 1))
        torque_column.append(round(cs * torque_percentage[rpm], 1))

    app_to_tp_table.append(tp_column)
    app_to_cross_sectional.append(cs_column)
    app_to_torque.append(torque_column)
    app_to_needed_cs.append(needed_cs_column)

print("Torque")
printing = PrettyTable()

field_names = ["APP"]
for i in rpms:
    field_names.append(str(i))

# printing.field_names = field_names
printing.add_column("APP", [str(app) for app in apps])
for c in range(len(app_to_torque)):
    printing.add_column(str(rpms[c]), app_to_torque[c])

print(printing)

print("Cross Sectional Area")
printing = PrettyTable()

field_names = ["APP"]
for i in rpms:
    field_names.append(str(i))

# printing.field_names = field_names
printing.add_column("APP", [str(app) for app in apps])
for c in range(len(app_to_cross_sectional)):
    printing.add_column(str(rpms[c]), app_to_cross_sectional[c])

print(printing)

print("Needed CS Area")
printing = PrettyTable()

field_names = ["APP"]
for i in rpms:
    field_names.append(str(i))

# printing.field_names = field_names
printing.add_column("APP", [str(app) for app in apps])
for c in range(len(app_to_needed_cs)):
    printing.add_column(str(rpms[c]), app_to_needed_cs[c])

print(printing)

print("TP")
printing = PrettyTable()

field_names = ["APP"]
for i in rpms:
    field_names.append(str(i))

# printing.field_names = field_names
printing.add_column("APP", [str(app) for app in apps])
for c in range(len(app_to_tp_table)):
    printing.add_column(str(rpms[c]), app_to_tp_table[c])

print(printing)


plot_app_to_tp_3d_plotly(apps, rpms, app_to_tp_table, f"throttle-graph")
plot_app_to_tp_3d_plotly(
    apps,
    rpms,
    app_to_cross_sectional,
    f"cross-sectional-graph",
    title="Cross Sectional Area",
    z_axis="Cross Section",
)

plot_app_to_tp_3d_plotly(
    apps,
    rpms,
    app_to_torque,
    f"torque-graph",
    title="Torque",
    z_axis="Torque",
)
