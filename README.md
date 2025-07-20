This is my attempt at an incredibly linear throttle map. While the formula is generic, assuming you update the dyno numbers, in its current form the program only outputs a map for a stock NC Miata.
My goal was to be able to hold a given torque across the rev range with a singular
pedal angle. In addition, I wanted a linear ratio between the cross sectional
area of the intake and the accelerator pedal.

## Requirements

- python
- uv (can install via pipx)

## Usage

`uv run python calc.py`

The tool outputs a number of tables to the terminal. If you're going to flash a Miata ECU, you really only care about the `TP` table. As this is the mapping of the pedal position to desired throttle position.

It also outputs a number of html files. These are graphs meant to demonstrate much of the information. For me, the important ones are `throttle-graph.html` (the TP table in graph form) and `torque-graph.html` (estimated torque per pedal position and RPM). For reference, the same graphs for my estimation of a cable throttle (pedal position == throttle position) are included in this repo.

In the future, I intend to make it simpler to change the logic function of the pedal and to adjust the dyno numbers to your own car.

## Assumptions

I made a few assumptions that may need tweaking once on the car:

1. The cross sectional area of the intake with the throttle at a certain percentage follows the function labeled `calculate_cross_sectional_area`. Basically assume the throttle blade takes up the area of `cos(TP*pi/200)` (where `TP` is throttle position from 0-100).
2. The cross sectional area directly correlates with torque production across all RPMs. This is likely not true if the throttle body is not a restriction at redline. Likely, at lower RPMs the intake manifold reaches atmospheric pressure long before 100% throttle opening.
3. The stock NC Miata follows [this blue torque curve](https://forum.miata.net/vb/showthread.php?t=466026)